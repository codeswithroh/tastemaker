import { useState } from "react"
import {
  ArrowRight,
  ArrowUpRight,
  Check,
  Copy,
  Image as ImageIcon,
  Lock,
  Palette,
  PlayCircle,
  ScanSearch,
  Sparkles,
} from "lucide-react"
import { CompareReveal } from "@/components/site/CompareReveal"
import { Ambient, Grain } from "@/components/site/Ambient"
import { Reveal } from "@/components/site/Reveal"

const INSTALL = "npx skills add codeswithroh/tastemaker"
const REPO = "https://github.com/codeswithroh/tastemaker"

function InstallRow() {
  const [copied, setCopied] = useState(false)
  return (
    <div className="flex w-full max-w-[560px] items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] py-2 pr-2 pl-5 backdrop-blur-xl">
      <code className="min-w-0 flex-1 overflow-x-auto font-mono text-[0.82rem] whitespace-nowrap text-foreground [scrollbar-width:none]">
        {INSTALL}
      </code>
      <button
        type="button"
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(INSTALL)
            setCopied(true)
            window.setTimeout(() => setCopied(false), 1600)
          } catch {
            /* clipboard blocked; the command stays selectable */
          }
        }}
        aria-label="Copy install command"
        className="inline-flex min-h-9 flex-none cursor-pointer items-center gap-2 rounded-full bg-teal-bright px-4 font-mono text-[0.68rem] font-extrabold text-dark transition hover:brightness-110 focus-visible:ring-2 focus-visible:ring-teal-bright focus-visible:ring-offset-2 focus-visible:ring-offset-background focus-visible:outline-none"
      >
        {copied ? <Check size={13} /> : <Copy size={13} />}
        {copied ? "Copied" : "Copy"}
      </button>
    </div>
  )
}

function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="mb-6 inline-flex w-max items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3.5 py-1.5 font-mono text-[0.66rem] font-bold tracking-[0.14em] text-muted-dark uppercase backdrop-blur-xl">
      <span className="inline-block h-1.5 w-1.5 rounded-full bg-teal-bright" />
      {children}
    </p>
  )
}

function SectionHead({
  eyebrow,
  title,
  lede,
  center = false,
}: {
  eyebrow: string
  title: React.ReactNode
  lede?: string
  center?: boolean
}) {
  return (
    <div className={center ? "flex flex-col items-center text-center" : ""}>
      <Eyebrow>{eyebrow}</Eyebrow>
      <h2 className="max-w-[min(20ch,100%)] font-display text-[clamp(2rem,4.2vw,3.4rem)] leading-[1.06] font-extrabold tracking-[-0.02em] text-foreground">
        {title}
      </h2>
      {lede && (
        <p className="mt-5 max-w-[min(54ch,100%)] text-[clamp(0.98rem,1.2vw,1.1rem)] leading-relaxed text-muted-dark">
          {lede}
        </p>
      )}
    </div>
  )
}

const CHECKS = [
  { icon: ScanSearch, title: "Reference intelligence", body: "Builds a board of competitors, adjacent products, and cultural references before picking a single color." },
  { icon: Palette, title: "Contrast-checked palette", body: "Every pairing runs through real WCAG math before it ships." },
  { icon: ImageIcon, title: "Real assets", body: "Real photography, real icons, real screenshots. No gray boxes." },
  { icon: PlayCircle, title: "Motion by default", body: "Scroll-driven reveals ship in the same pass, not a later polish step." },
  { icon: Lock, title: "A style that persists", body: "Once a palette and type are locked, every later screen reuses them instead of drifting." },
  { icon: Sparkles, title: "Four visual registers", body: "Brutalist, glassmorphic, minimalist, calm. One committed direction, not the default." },
]

const MODES = [
  { file: "brutalist.jpg", name: "Brutalist", note: "Heavy type, hard edges.", alt: "Brutalist mode: a finance dashboard with heavy black type and a yellow highlight block." },
  { file: "glassmorphic.jpg", name: "Glassmorphic", note: "Layered translucency.", alt: "Glassmorphic mode: a design-review tool with frosted panels over a warm gradient." },
  { file: "minimalist.jpg", name: "Minimalist", note: "Restraint as the style.", alt: "Minimalist mode: a restrained product screen with generous whitespace." },
  { file: "soft-calm.jpg", name: "Soft / Calm", note: "Low contrast, unhurried.", alt: "Soft calm mode: a gentle, low-contrast interface with rounded shapes." },
]

const CONTRAST = [
  { label: "text / background", value: "17.36" },
  { label: "muted / background", value: "7.87" },
  { label: "accent / background", value: "11.13" },
]

function Console({
  command,
  rows,
  footer,
  tone,
}: {
  command: string
  rows: { mark: string; key: string; note: string }[]
  footer: string
  tone: "fail" | "pass"
}) {
  const c = tone === "fail" ? "text-orange" : "text-teal-bright"
  return (
    <div className="overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] backdrop-blur-xl">
      <div className="flex items-center gap-2 border-b border-white/10 px-5 py-3.5">
        <span className="h-2.5 w-2.5 rounded-full bg-orange/70" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="ml-2 font-mono text-[0.78rem] text-muted-dark">{command}</span>
      </div>
      <ul className="m-0 list-none p-0">
        {rows.map((r) => (
          <li key={r.key} className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-white/[0.06] px-5 py-3 first:border-t-0">
            <span className={`w-11 flex-none font-mono text-[0.66rem] font-extrabold ${c}`}>{r.mark}</span>
            <span className="flex-none font-mono text-[0.82rem] font-bold text-foreground sm:w-[164px]">{r.key}</span>
            <span className="font-mono text-[0.82rem] text-muted-dark">{r.note}</span>
          </li>
        ))}
      </ul>
      <div className={`border-t border-white/10 px-5 py-3 font-mono text-[0.72rem] font-bold ${c}`}>{footer}</div>
    </div>
  )
}

export default function App() {
  return (
    <>
      <Grain />
      <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-100 focus:rounded-xl focus:bg-teal-bright focus:px-4 focus:py-2.5 focus:font-bold focus:text-dark">
        Skip to content
      </a>

      <header className="sticky top-0 z-90 border-b border-white/[0.06] bg-background/70 backdrop-blur-xl">
        <div className="mx-auto flex w-[min(1200px,calc(100%-40px))] items-center justify-between gap-3 py-4">
          <a href="#top" aria-label="Tastemaker home" className="flex items-center gap-2.5 font-display text-[1.05rem] font-black tracking-tight">
            <img src="/assets/mark-tastemaker.svg" alt="" width={28} height={28} />
            <span>tastemaker</span>
          </a>
          <nav aria-label="Primary" className="hidden items-center gap-8 lg:flex">
            {[["How it works", "#how"], ["Proof", "#proof"], ["Modes", "#modes"], ["Memory", "#memory"]].map(([l, h]) => (
              <a key={h} href={h} className="text-[0.86rem] text-muted-dark transition-colors hover:text-foreground">{l}</a>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <a href={REPO} target="_blank" rel="noopener" aria-label="Tastemaker on GitHub" className="grid h-9 w-9 place-items-center rounded-full border border-white/10 bg-white/[0.04] transition hover:bg-white/10">
              <img src="/assets/icons/github.svg" alt="" width={15} height={15} className="opacity-80 invert" />
            </a>
            <a href="#install" className="inline-flex min-h-9 items-center rounded-full bg-foreground px-4 text-[0.86rem] font-extrabold text-dark transition hover:brightness-95">
              Install
            </a>
          </div>
        </div>
      </header>

      <main id="main">
        {/* hero */}
        <section id="top" className="relative isolate overflow-hidden">
          <Ambient />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-background" />
          <div className="relative mx-auto grid w-[min(1200px,calc(100%-40px))] grid-cols-[minmax(0,1fr)] items-center gap-14 py-20 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)] lg:gap-16 lg:py-28">
            <div className="min-w-0">
              <Eyebrow>design taste for coding agents</Eyebrow>
              <h1 className="max-w-[min(16ch,100%)] font-display text-[clamp(2.6rem,5.6vw,4.4rem)] leading-[1.02] font-extrabold tracking-[-0.03em]">
                Your agent writes working code.{" "}
                <span className="text-teal-bright">It doesn't write taste.</span>
              </h1>
              <p className="mt-7 max-w-[min(44ch,100%)] text-[clamp(1rem,1.25vw,1.15rem)] leading-relaxed text-muted-dark">
                A local skill that gives Claude Code, Gemini CLI, and Windsurf a real design
                process: study references, lock a palette that passes contrast, cast real assets,
                and remember what you keep.
              </p>
              <div className="mt-9"><InstallRow /></div>
              <div className="mt-5 flex flex-wrap items-center gap-5">
                <a href="#proof" className="group inline-flex min-h-[48px] items-center gap-2 rounded-full bg-foreground px-6 font-extrabold text-dark transition hover:brightness-95">
                  See the proof
                  <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
                </a>
                <a href={REPO} target="_blank" rel="noopener" className="inline-flex items-center gap-1.5 text-[0.92rem] font-semibold text-muted-dark transition-colors hover:text-foreground">
                  Read the source <ArrowUpRight size={15} />
                </a>
              </div>
            </div>

            <div className="relative min-w-0">
              <div aria-hidden="true" className="absolute inset-0 -z-10 rounded-full bg-teal/20 blur-[80px]" />
              <CompareReveal />
            </div>
          </div>
        </section>

        {/* proof strip */}
        <section aria-label="Built as a real local skill" className="border-y border-white/[0.06]">
          <div className="mx-auto flex w-[min(1200px,calc(100%-40px))] flex-wrap items-center gap-x-10 gap-y-4 py-6">
            <p className="mr-auto font-mono text-[0.8rem] font-bold text-muted-dark">
              Not a prompt pack. A real local skill.
            </p>
            <div className="flex flex-wrap gap-6">
              {[
                ["SKILL.md", `${REPO}/blob/main/skills/tastemaker/SKILL.md`],
                ["anti-slop gates", `${REPO}/blob/main/skills/tastemaker/references/anti-slop-checklist.md`],
                ["motion rules", `${REPO}/blob/main/skills/tastemaker/references/animation-guidelines.md`],
                ["taste memory", `${REPO}/blob/main/skills/tastemaker/references/taste-memory.md`],
              ].map(([l, h]) => (
                <a key={l} href={h} target="_blank" rel="noopener" className="font-mono text-[0.8rem] font-semibold text-teal-bright transition-opacity hover:opacity-70">{l}</a>
              ))}
            </div>
          </div>
        </section>

        {/* problem */}
        <section className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                eyebrow="the problem"
                title={<>Every agent defaults to the <span className="text-orange">same page</span>.</>}
                lede="Purple-to-indigo gradient hero. Rounded card, soft shadow. A palette picked because it looked fine in the moment, never checked against anything. Ask ten agents for a landing page and you'll recognize the ninth one before it finishes rendering."
              />
            </Reveal>
            <Reveal delay={100} className="mt-14 max-w-[900px]">
              <Console
                tone="fail"
                command="anti_slop_scan.py generic-agent-output.html"
                rows={[
                  { mark: "HIGH", key: "ai-gradient", note: "indigo-to-purple hero, unrelated to the product" },
                  { mark: "HIGH", key: "unchecked-contrast", note: "colors picked by eye, never measured" },
                  { mark: "MED", key: "no-style-lock", note: "next screen drifts, nothing persists" },
                ]}
                footer="3 findings. 0 fixed."
              />
            </Reveal>
          </div>
        </section>

        {/* how it works */}
        <section id="how" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                eyebrow="how it works"
                title="Six checks run before the first component exists."
                lede="Every one is real: a script, a Markdown file, or a gate that has to pass. Nothing here is decorative."
              />
            </Reveal>

            <div className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-white/10 bg-white/[0.06] sm:grid-cols-2 lg:grid-cols-3">
              {CHECKS.map((c, i) => {
                const Icon = c.icon
                return (
                  <Reveal key={c.title} delay={i * 60}>
                    <div className="group h-full bg-background p-7 transition-colors hover:bg-white/[0.03]">
                      <div className="mb-5 grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/[0.04] text-teal-bright transition-colors group-hover:border-teal-bright/40">
                        <Icon size={18} strokeWidth={1.8} />
                      </div>
                      <h3 className="mb-2 font-display text-[1.05rem] font-extrabold">{c.title}</h3>
                      <p className="text-[0.9rem] leading-relaxed text-muted-dark">{c.body}</p>
                    </div>
                  </Reveal>
                )
              })}
            </div>

            <Reveal delay={140} className="mt-6 max-w-[900px]">
              <Console
                tone="pass"
                command="tastemaker build --project tastemaker-skill.online"
                rows={[
                  { mark: "PASS", key: "reference-intel", note: "board built before the first color" },
                  { mark: "PASS", key: "contrast-check", note: "every pairing run through real WCAG math" },
                  { mark: "PASS", key: "real-assets", note: "real icons and screenshots, no gray boxes" },
                  { mark: "PASS", key: "motion-default", note: "reveals ship in the same pass" },
                  { mark: "PASS", key: "style-lock", note: "palette reused on every later screen" },
                  { mark: "PASS", key: "register-variety", note: "one committed direction" },
                ]}
                footer="6 checks. 6 passed."
              />
            </Reveal>
          </div>
        </section>

        {/* proof / contrast */}
        <section id="proof" className="relative isolate overflow-hidden py-24 lg:py-32">
          <div aria-hidden="true" className="absolute top-1/2 left-1/2 -z-10 h-[420px] w-[820px] max-w-full -translate-x-1/2 -translate-y-1/2 rounded-full bg-orchid/10 blur-[110px]" />
          <div className="mx-auto w-[min(820px,calc(100%-40px))]">
            <Reveal className="w-full min-w-0">
              <SectionHead center eyebrow="proof, not claims" title="Checked with real math, not eyeballed." />
              <p className="mx-auto mt-5 max-w-[min(52ch,100%)] text-center text-muted-dark">
                Every pairing on this page runs through{" "}
                <a href={`${REPO}/blob/main/skills/tastemaker/scripts/check_contrast.py`} target="_blank" rel="noopener" className="text-teal-bright underline-offset-4 hover:underline">check_contrast.py</a>{" "}
                before it ships. These are this page's actual numbers.
              </p>
            </Reveal>
            <div className="mt-12 flex flex-col gap-3">
              {CONTRAST.map((c, i) => (
                <Reveal key={c.label} delay={i * 80}>
                  <div className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/10 bg-white/[0.03] px-6 py-5 backdrop-blur-xl">
                    <span className="flex-1 font-mono text-[0.9rem] text-muted-dark">{c.label}</span>
                    <span className="font-display text-[1.7rem] font-extrabold text-foreground tabular-nums">{c.value}</span>
                    <span className="rounded-full border border-teal-bright/40 bg-teal-bright/10 px-3 py-1 font-mono text-[0.66rem] font-extrabold tracking-wider text-teal-bright">PASS</span>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* modes */}
        <section id="modes" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                eyebrow="premium modes"
                title={<>Different products shouldn't wear the <span className="text-orchid">same suit</span>.</>}
                lede="Four sponsor-exclusive visual registers, generated by the same engine, each committing to a real direction instead of a default."
              />
            </Reveal>
            <div className="mt-14 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {MODES.map((m, i) => (
                <Reveal key={m.name} delay={i * 80}>
                  <figure className="group m-0 overflow-hidden rounded-2xl border border-white/10 bg-white/[0.03] transition-all duration-300 hover:-translate-y-1 hover:border-teal-bright/30">
                    <div className="overflow-hidden border-b border-white/10">
                      <img
                        src={`/assets/modes/${m.file}`}
                        alt={m.alt}
                        width={900}
                        height={495}
                        loading="lazy"
                        className="block aspect-[900/495] h-auto w-full object-cover object-top transition-transform duration-500 group-hover:scale-[1.04]"
                      />
                    </div>
                    <figcaption className="p-5">
                      <strong className="block font-display text-[0.98rem] font-extrabold">{m.name}</strong>
                      <span className="mt-1 block text-[0.8rem] text-muted-dark">{m.note}</span>
                    </figcaption>
                  </figure>
                </Reveal>
              ))}
            </div>
            <Reveal delay={120}>
              <div className="mt-6 flex flex-wrap items-center justify-between gap-6 rounded-2xl border border-white/10 bg-white/[0.03] px-7 py-6 backdrop-blur-xl">
                <p className="max-w-[min(46ch,100%)] font-mono text-[0.84rem] text-muted-dark">
                  Sponsor-exclusive, on top of the free core skill.
                </p>
                <a href="https://buy.polar.sh/polar_cl_tY4OjST0hD2YW36YeNrDJgHs6Ybz9vmsQeHNX0YSbl4" target="_blank" rel="noopener" className="inline-flex min-h-[46px] items-center rounded-full bg-teal-bright px-6 font-extrabold text-dark transition hover:brightness-110">
                  Unlock for $8/month
                </a>
              </div>
            </Reveal>
          </div>
        </section>

        {/* memory */}
        <section id="memory" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                eyebrow="what changed"
                title="The skill remembers your taste."
                lede="Project style choices live in the repo. Personal preferences live on your machine. A rejected direction becomes a guardrail instead of getting forgotten."
              />
            </Reveal>
            <Reveal delay={100} className="mt-14 max-w-[900px]">
              <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-7 backdrop-blur-xl sm:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-2 pb-2">
                  <code className="font-mono text-[0.9rem] font-extrabold text-teal-bright">.tastemaker/</code>
                  <span className="font-mono text-[0.66rem] font-bold tracking-widest text-muted-dark uppercase">this project</span>
                </div>
                {[
                  ["├──", "style-lock.md", "Palette, type, shape, assets, motion, and do-not rules."],
                  ["└──", "decisions.log", "Append-only keep, reject, and pending-review decisions."],
                ].map(([b, f, d]) => (
                  <div key={f} className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-white/[0.06] py-3">
                    <code className="font-mono text-[0.88rem] font-bold text-foreground">
                      <span className="font-normal text-muted-dark">{b}</span> {f}
                    </code>
                    <span className="text-[0.86rem] text-muted-dark">{d}</span>
                  </div>
                ))}
                <div className="mt-3 flex flex-wrap items-baseline justify-between gap-2 border-t border-dashed border-white/10 pt-5 pb-2">
                  <code className="font-mono text-[0.9rem] font-extrabold text-teal-bright">~/.tastemaker/</code>
                  <span className="font-mono text-[0.66rem] font-bold tracking-widest text-muted-dark uppercase">every project</span>
                </div>
                <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-white/[0.06] py-3">
                  <code className="font-mono text-[0.88rem] font-bold text-foreground">
                    <span className="font-normal text-muted-dark">└──</span> profile.md
                  </code>
                  <span className="text-[0.86rem] text-muted-dark">Reusable preferences, promoted only when you choose or repeat them.</span>
                </div>
              </div>
            </Reveal>
          </div>
        </section>

        {/* install */}
        <section id="install" className="relative isolate overflow-hidden py-24 lg:py-36">
          <div aria-hidden="true" className="absolute top-1/2 left-1/2 -z-10 h-[500px] w-[900px] max-w-full -translate-x-1/2 -translate-y-1/2 rounded-full bg-teal/20 blur-[120px]" />
          <div className="mx-auto flex w-[min(1200px,calc(100%-40px))] flex-col items-center text-center">
            <Reveal className="flex w-full min-w-0 flex-col items-center">
              <Eyebrow>free and local</Eyebrow>
              <h2 className="max-w-[min(18ch,100%)] font-display text-[clamp(2.2rem,5vw,3.8rem)] leading-[1.04] font-extrabold tracking-[-0.02em]">
                Install once. Ask normally.
              </h2>
              <p className="mx-auto mt-6 max-w-[min(46ch,100%)] text-[1.05rem] text-muted-dark">
                No hosted editor, no account, no separate design handoff. The taste layer lives
                where the agent already works.
              </p>
              <div className="mt-10 flex w-full min-w-0 justify-center"><InstallRow /></div>
              <p className="mt-5 text-[0.85rem] text-muted-dark">
                Using Claude Code? The{" "}
                <a href={`${REPO}#claude-code-plugin-marketplace`} target="_blank" rel="noopener" className="text-teal-bright underline-offset-4 hover:underline">plugin marketplace</a>{" "}
                and manual install work too.
              </p>
            </Reveal>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/[0.06] py-10">
        <div className="mx-auto flex w-[min(1200px,calc(100%-40px))] flex-wrap items-center justify-between gap-6">
          <a href="#top" className="flex items-center gap-2.5 font-display text-[1.05rem] font-black">
            <img src="/assets/mark-tastemaker.svg" alt="" width={26} height={26} />
            <span>tastemaker</span>
          </a>
          <div className="font-mono text-[0.68rem] text-muted-dark">Built with the workflow it documents.</div>
          <div className="flex flex-wrap items-center gap-6 text-[0.82rem] text-muted-dark">
            <a href={REPO} target="_blank" rel="noopener" className="transition-colors hover:text-foreground">GitHub</a>
            <a href={`${REPO}/blob/main/README.md`} target="_blank" rel="noopener" className="transition-colors hover:text-foreground">Docs</a>
            <a href={`${REPO}/blob/main/LICENSE`} target="_blank" rel="noopener" className="transition-colors hover:text-foreground">MIT</a>
            <a href="https://github.com/sponsors/codeswithroh" target="_blank" rel="noopener" className="text-teal-bright transition-opacity hover:opacity-70">Sponsor</a>
          </div>
          <a href="https://fazier.com/launches/tastemaker-skill.online" target="_blank" rel="noopener" className="inline-flex flex-none opacity-80 transition-opacity hover:opacity-100">
            <img src="https://fazier.com/api/v1//public/badges/launch_badges.svg?badge_type=launched&theme=dark" width={120} height={26} alt="Fazier badge" loading="lazy" className="block h-[26px] w-auto" />
          </a>
        </div>
      </footer>
    </>
  )
}
