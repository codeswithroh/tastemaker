import { useEffect, useState } from "react"
import { Megaphone, Star, X } from "lucide-react"

const TOTAL_SLOTS = 5
const PRICE_PER_MONTH = 29
const API_BASE = "https://tastemaker-sponsors-api.codeswithroh.workers.dev"

let CHECKOUT_URL: string | null = null
export function setSponsorCheckoutUrl(url: string) {
  CHECKOUT_URL = url
}

type ApprovedSponsor = {
  id: string
  slot: number
  name: string
  blurb: string
  website_url: string
  logo_url: string
}

/** Fetched once per page load from the sponsors Worker — approved sponsors
 * only (the Worker never returns pending/rejected rows). Any slot with no
 * matching entry renders as an open, purchasable slot. */
function useApprovedSponsors() {
  const [sponsors, setSponsors] = useState<ApprovedSponsor[]>([])
  useEffect(() => {
    let cancelled = false
    fetch(`${API_BASE}/api/sponsors`)
      .then((r) => (r.ok ? r.json() : { sponsors: [] }))
      .then((data) => {
        if (!cancelled) setSponsors(data.sponsors ?? [])
      })
      .catch(() => {
        /* API unreachable — every slot just falls back to "open" */
      })
    return () => {
      cancelled = true
    }
  }, [])
  return sponsors
}

function OpenSlotCard() {
  return (
    <a
      href={CHECKOUT_URL ?? "#advertise"}
      onClick={(e) => {
        if (CHECKOUT_URL) return
        e.preventDefault()
        window.dispatchEvent(new CustomEvent("open-advertise-modal"))
      }}
      target={CHECKOUT_URL ? "_blank" : undefined}
      rel={CHECKOUT_URL ? "noopener" : undefined}
      className="group flex min-h-[150px] flex-col justify-between rounded-2xl border border-dashed border-border bg-card/60 p-5 transition hover:border-gold/50 hover:bg-card"
    >
      <Megaphone size={18} className="text-muted-dark transition group-hover:text-gold" />
      <div>
        <p className="font-mono text-[0.78rem] font-bold text-foreground">Sponsor slot open</p>
        <p className="mt-1 text-[0.78rem] leading-snug text-muted-dark">
          Reach developers building with AI coding agents.
        </p>
        <p className="mt-3 font-mono text-[0.7rem] font-bold text-gold">${PRICE_PER_MONTH}/mo</p>
      </div>
    </a>
  )
}

function AdvertiseCard({ takenCount }: { takenCount: number }) {
  const left = TOTAL_SLOTS - takenCount
  return (
    <button
      type="button"
      onClick={() => window.dispatchEvent(new CustomEvent("open-advertise-modal"))}
      className="flex min-h-[150px] w-full flex-col items-center justify-center gap-2 rounded-2xl border border-gold/30 bg-dark p-5 text-center transition hover:border-gold/60"
    >
      <Star size={18} className="text-gold-bright" />
      <p className="font-mono text-[0.78rem] font-bold text-[#e5f6f6]">Advertise</p>
      <p className="font-mono text-[0.68rem] text-muted-dark">
        {left}/{TOTAL_SLOTS} spot{left === 1 ? "" : "s"} left
      </p>
    </button>
  )
}

function SponsorTile({ sponsor }: { sponsor: ApprovedSponsor | undefined }) {
  if (!sponsor) return <OpenSlotCard />
  const [logoFailed, setLogoFailed] = useState(false)
  return (
    <a
      href={sponsor.website_url}
      target="_blank"
      rel="noopener sponsored"
      className="flex min-h-[150px] flex-col justify-between rounded-2xl border border-border bg-card p-5 transition hover:-translate-y-0.5 hover:shadow-[0_16px_30px_rgba(23,21,20,0.1)]"
    >
      {!logoFailed && (
        <img
          src={sponsor.logo_url}
          alt=""
          className="h-7 w-7 rounded-md object-contain"
          onError={() => setLogoFailed(true)}
        />
      )}
      <div>
        <p className="font-mono text-[0.78rem] font-bold text-foreground">{sponsor.name}</p>
        <p className="mt-1 text-[0.78rem] leading-snug text-muted-dark">{sponsor.blurb}</p>
      </div>
    </a>
  )
}

/** Desktop-only sticky side rail. Hidden below a very wide viewport (this
 * site's content column is already 1200px — there's no room for real
 * sidebars until well past that), so it never competes with or squeezes
 * the primary reading column on any normal screen. */
export function SponsorRail({ side }: { side: "left" | "right" }) {
  const sponsors = useApprovedSponsors()
  const bySlot = new Map(sponsors.map((s) => [s.slot, s]))
  const slotNumbers = side === "left" ? [1, 2] : [3, 4, 5]

  return (
    <aside
      aria-label={`${side === "left" ? "Left" : "Right"} sponsor rail`}
      className="sticky top-24 hidden h-max min-[1680px]:flex min-[1680px]:w-[210px] min-[1680px]:flex-col min-[1680px]:gap-4"
    >
      {slotNumbers.map((n) => (
        <SponsorTile key={n} sponsor={bySlot.get(n)} />
      ))}
      {side === "right" && <AdvertiseCard takenCount={sponsors.length} />}
    </aside>
  )
}

export function AdvertiseModal() {
  const [open, setOpen] = useState(false)
  const sponsors = useApprovedSponsors()
  const left = TOTAL_SLOTS - sponsors.length

  useEffect(() => {
    const handler = () => setOpen(true)
    window.addEventListener("open-advertise-modal", handler)
    return () => window.removeEventListener("open-advertise-modal", handler)
  }, [])

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => e.key === "Escape" && setOpen(false)
    window.addEventListener("keydown", onKey)
    document.body.style.overflow = "hidden"
    return () => {
      window.removeEventListener("keydown", onKey)
      document.body.style.overflow = ""
    }
  }, [open])

  if (!open) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-ink/50 p-4 backdrop-blur-sm"
      onClick={() => setOpen(false)}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="advertise-modal-title"
        onClick={(e) => e.stopPropagation()}
        className="max-h-[90vh] w-full max-w-[440px] overflow-y-auto rounded-[22px] border border-border bg-card p-7 shadow-[0_30px_70px_rgba(23,21,20,0.25)]"
      >
        <div className="flex items-start justify-between">
          <h3 id="advertise-modal-title" className="font-display text-[1.4rem] font-extrabold text-foreground">
            Advertise on Tastemaker
          </h3>
          <button
            type="button"
            onClick={() => setOpen(false)}
            aria-label="Close"
            className="-mt-1 -mr-1 flex h-8 w-8 flex-none items-center justify-center rounded-full text-muted-dark transition hover:bg-ink/[0.06] hover:text-foreground"
          >
            <X size={16} />
          </button>
        </div>
        <p className="mt-2 text-[0.9rem] leading-relaxed text-muted-dark">
          Reach developers building with AI coding agents — the exact people who install and configure dev-tool skills.
        </p>

        <div className="mt-6 grid grid-cols-3 gap-2">
          {[
            ["286★", "on GitHub"],
            ["7 wks", "since launch"],
            [`${left}/${TOTAL_SLOTS}`, "spots left"],
          ].map(([n, label]) => (
            <div key={label} className="rounded-xl border border-border bg-background px-2 py-3 text-center">
              <p className="font-display text-[1.1rem] font-extrabold text-foreground">{n}</p>
              <p className="mt-0.5 font-mono text-[0.62rem] text-muted-dark">{label}</p>
            </div>
          ))}
        </div>

        <div className="mt-6 rounded-2xl border border-gold/30 bg-gold/[0.06] p-4">
          <p className="font-mono text-[0.7rem] font-bold tracking-wide text-muted-dark uppercase">Pricing</p>
          <p className="mt-1 font-display text-[1.5rem] font-extrabold text-foreground">
            ${PRICE_PER_MONTH}<span className="text-[0.9rem] font-semibold text-muted-dark">/month</span>
          </p>
          <p className="mt-1 text-[0.8rem] text-muted-dark">
            {TOTAL_SLOTS} slots total, {left} open. Cancel anytime.
          </p>
        </div>

        <a
          href={CHECKOUT_URL ?? undefined}
          target="_blank"
          rel="noopener"
          aria-disabled={!CHECKOUT_URL}
          className={`mt-6 flex min-h-[48px] w-full items-center justify-center gap-2 rounded-full px-6 font-extrabold transition ${
            CHECKOUT_URL
              ? "cursor-pointer bg-primary text-primary-foreground hover:brightness-110"
              : "cursor-not-allowed bg-muted text-muted-foreground"
          }`}
        >
          {CHECKOUT_URL ? `Get started ($${PRICE_PER_MONTH}/mo)` : "Checkout coming soon"}
        </a>

        <p className="mt-4 text-[0.78rem] text-muted-dark">
          Checkout collects your company name, link, one-line description, and logo — no separate form. Reviewed and live in the sidebar within a day. Billed monthly via Polar, cancel anytime.
        </p>
      </div>
    </div>
  )
}
