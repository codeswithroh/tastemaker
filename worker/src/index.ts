export interface Env {
  DB: D1Database
  ADMIN_TOKEN: string
  POLAR_WEBHOOK_SECRET: string
  SPONSOR_PRODUCT_ID: string
}

const TOTAL_SLOTS = 5

const ALLOWED_ORIGINS = new Set([
  "https://www.tastemaker-skill.online",
  "https://tastemaker-skill.online",
  "https://tastemaker-skill.pages.dev",
  "https://tastemaker-web.vercel.app",
  "http://localhost:4173",
  "http://localhost:5173",
])

function corsHeaders(origin: string | null) {
  const allow = origin && ALLOWED_ORIGINS.has(origin) ? origin : "https://www.tastemaker-skill.online"
  return {
    "Access-Control-Allow-Origin": allow,
    "Access-Control-Allow-Methods": "GET,PATCH,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
  }
}

function json(data: unknown, init: ResponseInit = {}, origin: string | null = null) {
  return new Response(JSON.stringify(data), {
    ...init,
    headers: { "Content-Type": "application/json", ...corsHeaders(origin), ...(init.headers ?? {}) },
  })
}

function requireAdmin(req: Request, env: Env): Response | null {
  const auth = req.headers.get("Authorization") ?? ""
  if (auth !== `Bearer ${env.ADMIN_TOKEN}`) {
    return json({ error: "unauthorized" }, { status: 401 }, req.headers.get("Origin"))
  }
  return null
}

/** Standard Webhooks verification: HMAC-SHA256 over `${id}.${timestamp}.${body}`,
 * using the raw UTF-8 secret bytes after the `whsec_` prefix (Polar's secrets are
 * NOT base64-encoded, unlike Svix/Clerk — confirmed against their docs). */
async function verifyPolarSignature(req: Request, rawBody: string, secret: string): Promise<boolean> {
  const id = req.headers.get("webhook-id")
  const timestamp = req.headers.get("webhook-timestamp")
  const signatureHeader = req.headers.get("webhook-signature")
  if (!id || !timestamp || !signatureHeader) return false

  const secretBytes = new TextEncoder().encode(secret.replace(/^whsec_/, ""))
  const key = await crypto.subtle.importKey("raw", secretBytes, { name: "HMAC", hash: "SHA-256" }, false, ["sign"])
  const signedContent = `${id}.${timestamp}.${rawBody}`
  const sigBuffer = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(signedContent))
  const expected = btoa(String.fromCharCode(...new Uint8Array(sigBuffer)))

  return signatureHeader
    .split(" ")
    .map((s) => s.split(",")[1])
    .some((sig) => sig === expected)
}

async function handleWebhook(req: Request, env: Env): Promise<Response> {
  const rawBody = await req.text()
  const valid = await verifyPolarSignature(req, rawBody, env.POLAR_WEBHOOK_SECRET)
  if (!valid) return new Response("invalid signature", { status: 401 })

  const event = JSON.parse(rawBody) as { type: string; data: Record<string, any> }
  if (event.type !== "order.created" && event.type !== "subscription.created") {
    return new Response("ignored", { status: 200 })
  }

  const data = event.data
  const productId = data.product_id ?? data.product?.id
  if (productId !== env.SPONSOR_PRODUCT_ID) {
    return new Response("ignored: different product", { status: 200 })
  }

  const fields = data.custom_field_data ?? {}
  const name = fields.company_name?.trim()
  const blurb = fields.blurb?.trim()
  const website_url = fields.website_url?.trim()
  const logo_url = fields.logo_url?.trim()

  if (!name || !blurb || !website_url || !logo_url) {
    return new Response("missing required custom fields", { status: 200 })
  }

  const id = crypto.randomUUID()
  await env.DB.prepare(
    `INSERT INTO sponsors (id, status, name, blurb, website_url, logo_url, customer_email, polar_order_id, polar_subscription_id)
     VALUES (?, 'pending', ?, ?, ?, ?, ?, ?, ?)`,
  )
    .bind(
      id,
      name,
      blurb,
      website_url,
      logo_url,
      data.customer?.email ?? null,
      event.type === "order.created" ? data.id : null,
      event.type === "subscription.created" ? data.id : null,
    )
    .run()

  return new Response("ok", { status: 200 })
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url)
    const origin = req.headers.get("Origin")

    if (req.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(origin) })
    }

    // Public: approved sponsors for the live site.
    if (req.method === "GET" && url.pathname === "/api/sponsors") {
      const { results } = await env.DB.prepare(
        `SELECT id, slot, name, blurb, website_url, logo_url FROM sponsors WHERE status = 'approved' ORDER BY slot ASC`,
      ).all()
      return json({ slots: TOTAL_SLOTS, sponsors: results }, {}, origin)
    }

    // Polar webhook receiver.
    if (req.method === "POST" && url.pathname === "/webhooks/polar") {
      return handleWebhook(req, env)
    }

    // Admin: list pending submissions for review.
    if (req.method === "GET" && url.pathname === "/api/sponsors/pending") {
      const unauthorized = requireAdmin(req, env)
      if (unauthorized) return unauthorized
      const { results } = await env.DB.prepare(
        `SELECT * FROM sponsors WHERE status = 'pending' ORDER BY created_at ASC`,
      ).all()
      return json({ pending: results }, {}, origin)
    }

    // Admin: approve a submission into the next open slot.
    const approveMatch = url.pathname.match(/^\/api\/sponsors\/([^/]+)\/approve$/)
    if (req.method === "PATCH" && approveMatch) {
      const unauthorized = requireAdmin(req, env)
      if (unauthorized) return unauthorized

      const { results: taken } = await env.DB.prepare(
        `SELECT slot FROM sponsors WHERE status = 'approved'`,
      ).all<{ slot: number }>()
      const takenSlots = new Set(taken.map((r) => r.slot))
      let nextSlot: number | null = null
      for (let s = 1; s <= TOTAL_SLOTS; s++) {
        if (!takenSlots.has(s)) {
          nextSlot = s
          break
        }
      }
      if (nextSlot === null) {
        return json({ error: "all slots full" }, { status: 409 }, origin)
      }

      await env.DB.prepare(
        `UPDATE sponsors SET status = 'approved', slot = ?, reviewed_at = datetime('now') WHERE id = ?`,
      )
        .bind(nextSlot, approveMatch[1])
        .run()
      return json({ ok: true, slot: nextSlot }, {}, origin)
    }

    // Admin: reject a submission.
    const rejectMatch = url.pathname.match(/^\/api\/sponsors\/([^/]+)\/reject$/)
    if (req.method === "PATCH" && rejectMatch) {
      const unauthorized = requireAdmin(req, env)
      if (unauthorized) return unauthorized

      await env.DB.prepare(`UPDATE sponsors SET status = 'rejected', reviewed_at = datetime('now') WHERE id = ?`)
        .bind(rejectMatch[1])
        .run()
      return json({ ok: true }, {}, origin)
    }

    return json({ error: "not found" }, { status: 404 }, origin)
  },
}
