import { useState } from "react"
import {
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
import { Badge } from "@/components/ui/badge"
import { Card } from "@/components/ui/card"
import { CompareReveal } from "@/components/site/CompareReveal"
import { Reveal } from "@/components/site/Reveal"

const INSTALL = "npx skills add codeswithroh/tastemaker"
const REPO = "https://github.com/codeswithroh/tastemaker"

function InstallRow({ large = false }: { large?: boolean }) {
  const [copied, setCopied] = useState(false)
  return (
    <div
      className={`flex w-full max-w-[540px] items-center gap-2 rounded-full py-2 pr-2 pl-5 text-white shadow-[0_30px_90px_rgba(12,20,20,0.3)] ${
        large ? "border border-white/10 bg-dark-soft" : "bg-dark"
      }`}
    >
      <code className="min-w-0 flex-1 overflow-x-auto font-mono text-[0.8rem] whitespace-nowrap [scrollbar-width:none]">
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
            /* clipboard blocked; the command stays selectable either way */
          }
        }}
        aria-label="Copy install command"
        className="inline-flex min-h-9 flex-none cursor-pointer items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3.5 font-mono text-[0.68rem] font-extrabold transition-colors hover:bg-white/20 focus-visible:ring-2 focus-visible:ring-teal-bright focus-visible:outline-none"
      >
        {copied ? <Check size={13} /> : <Copy size={13} />}
        {copied ? "Copied" : "Copy"}
      </button>
    </div>
  )
}

function Eyebrow({ children }: { children: React.ReactNode }) {
  return (
    <p className="mb-4 inline-block w-max rounded-full border border-orange/30 bg-cream px-3 py-1.5 font-mono text-[0.68rem] font-extrabold tracking-[0.08em] text-[#a94314] uppercase">
      {children}
    </p>
  )
}

const CHECKS = [
  {
    icon: ScanSearch,
    title: "Reference intelligence",
    body: "Builds a board of direct competitors, adjacent products, and cultural references before picking a single color.",
    wide: true,
  },
  {
    icon: Palette,
    title: "Contrast-checked palette",
    body: "Every pairing runs through real WCAG math before it ships.",
  },
  {
    icon: ImageIcon,
    title: "Real assets, not placeholders",
    body: "Real photography, real icons, real screenshots. No gray boxes.",
  },
  {
    icon: PlayCircle,
    title: "Motion by default",
    body: "Scroll-driven reveals ship in the same pass, not a later polish step.",
  },
  {
    icon: Lock,
    title: "A style that persists",
    body: "Once a project's palette and type are locked, every later screen reuses them instead of drifting.",
    wide: true,
  },
  {
    icon: Sparkles,
    title: "Four visual registers",
    body: "Brutalist, glassmorphic, minimalist, calm. A project commits to one instead of defaulting to the template.",
  },
]

const MODES = [
  {
    file: "brutalist.jpg",
    name: "Brutalist",
    note: "Heavy type, hard edges, no apology.",
    alt: "Brutalist mode: a finance dashboard with heavy black type and a yellow highlight block.",
  },
  {
    file: "glassmorphic.jpg",
    name: "Glassmorphic",
    note: "Layered translucency, soft depth.",
    alt: "Glassmorphic mode: a design-review tool with frosted panels over a warm gradient.",
  },
  {
    file: "minimalist.jpg",
    name: "Minimalist",
    note: "Restraint as the whole style.",
    alt: "Minimalist mode: a restrained product screen with generous whitespace.",
  },
  {
    file: "soft-calm.jpg",
    name: "Soft / Calm",
    note: "Low contrast, unhurried pacing.",
    alt: "Soft calm mode: a gentle, low-contrast interface with rounded shapes.",
  },
]

const CONTRAST = [
  { label: "text / background", value: "16.15" },
  { label: "label / primary", value: "4.63" },
  { label: "accent / dark surface", value: "6.60" },
]

function ScanConsole({
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
  const markColor = tone === "fail" ? "text-orange" : "text-teal-bright"
  return (
    <div className="overflow-hidden rounded-[20px] border border-white/15 bg-dark shadow-[0_20px_60px_rgba(23,21,20,0.1)]">
      <div className="border-b border-white/15 px-5 py-3 font-mono text-[0.8rem] text-muted-dark">
        {command}
      </div>
      <ul className="m-0 list-none p-0">
        {rows.map((r) => (
          <li
            key={r.key}
            className="flex flex-wrap items-baseline gap-x-3.5 gap-y-1 border-t border-white/15 px-5 py-3 first:border-t-0"
          >
            <span className={`w-11 flex-none font-mono text-[0.68rem] font-extrabold tracking-wide ${markColor}`}>
              {r.mark}
            </span>
            <span className="flex-none font-mono text-[0.84rem] font-bold text-[#e5f6f6] sm:w-[168px]">
              {r.key}
            </span>
            <span className="font-mono text-[0.84rem] text-muted-dark">{r.note}</span>
          </li>
        ))}
      </ul>
      <div className={`border-t border-white/15 px-5 py-3 font-mono text-[0.74rem] font-semibold ${markColor}`}>
        {footer}
      </div>
    </div>
  )
}

export default function App() {
  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-100 focus:rounded-xl focus:border focus:border-ink focus:bg-cream focus:px-4 focus:py-2.5 focus:font-bold"
      >
        Skip to content
      </a>

      <header className="sticky top-0 z-90 mx-auto flex w-[min(1180px,calc(100%-40px))] items-center justify-between gap-3 py-3.5">
        <div className="flex min-h-[50px] items-center gap-2.5 rounded-full border border-border bg-paper/85 px-4 backdrop-blur-lg">
          <a href="#top" aria-label="Tastemaker home" className="flex items-center gap-2.5 font-display text-base font-black">
            <img src="/assets/mark-tastemaker.svg" alt="" width={30} height={30} />
            <span>tastemaker</span>
          </a>
        </div>
        <nav aria-label="Primary" className="hidden min-h-[50px] items-center gap-5 rounded-full border border-border bg-paper/85 px-5 backdrop-blur-lg lg:flex">
          {[
            ["How it works", "#how"],
            ["Proof", "#proof"],
            ["Modes", "#modes"],
            ["Memory", "#memory"],
          ].map(([label, href]) => (
            <a key={href} href={href} className="text-[0.86rem] whitespace-nowrap text-ink-soft transition-colors hover:text-teal">
              {label}
            </a>
          ))}
        </nav>
        <div className="flex min-h-[50px] items-center gap-2 rounded-full border border-border bg-paper/85 px-1.5 backdrop-blur-lg">
          <a
            href={REPO}
            target="_blank"
            rel="noopener"
            aria-label="Tastemaker on GitHub"
            className="grid h-9 w-9 place-items-center rounded-full border border-border bg-white transition-colors hover:text-teal"
          >
            <img src="/assets/icons/github.svg" alt="" width={16} height={16} />
          </a>
          <a
            href="#install"
            className="inline-flex min-h-9 items-center rounded-full bg-dark px-4 text-[0.88rem] font-extrabold text-white"
          >
            Install
          </a>
        </div>
      </header>

      <main id="main">
        {/* hero */}
        <section id="top" className="relative isolate overflow-hidden py-16 lg:py-24">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 -z-10 opacity-70"
            style={{
              background:
                "radial-gradient(45% 45% at 18% 30%, rgba(0,130,134,0.18), transparent 70%), radial-gradient(40% 40% at 85% 75%, rgba(190,133,206,0.16), transparent 70%)",
            }}
          />
          <div className="mx-auto grid w-[min(1180px,calc(100%-40px))] grid-cols-[minmax(0,1fr)] items-center gap-10 lg:grid-cols-[minmax(0,0.82fr)_minmax(0,1.18fr)] lg:gap-[72px]">
            <div className="min-w-0">
              <Eyebrow>design taste for coding agents</Eyebrow>
              <h1 className="max-w-[17ch] font-display text-[clamp(2.1rem,3.6vw,3.2rem)] leading-[1.14] font-extrabold tracking-[-0.01em]">
                Your agent writes working code. It doesn't write good taste.
              </h1>
              <p className="mt-5 max-w-[42ch] text-[clamp(1rem,1.15vw,1.12rem)] text-ink-soft">
                Tastemaker is a local skill that gives Claude Code, Gemini CLI, and Windsurf a real
                design process: study references, lock a palette that passes contrast, cast real
                assets, and remember what you keep.
              </p>
              <div className="mt-7">
                <InstallRow />
              </div>
              <div className="mt-4 flex flex-wrap gap-3">
                <a
                  href="#proof"
                  className="inline-flex min-h-[46px] items-center justify-center gap-2 rounded-full bg-dark px-5 font-extrabold text-white transition-transform active:scale-[0.97]"
                >
                  See the proof <ArrowUpRight size={14} />
                </a>
                <a
                  href={REPO}
                  target="_blank"
                  rel="noopener"
                  className="inline-flex min-h-[46px] items-center justify-center rounded-full border border-border bg-cream px-5 font-extrabold text-ink transition-transform active:scale-[0.97]"
                >
                  Read the source
                </a>
              </div>
            </div>
            <CompareReveal />
          </div>
        </section>

        {/* proof strip */}
        <section aria-label="Built as a real local skill" className="border-y border-border py-8">
          <div className="mx-auto flex w-[min(1180px,calc(100%-40px))] flex-wrap items-center gap-x-8 gap-y-4">
            <p className="mr-auto font-mono text-[0.82rem] font-extrabold text-ink-soft">
              Not a prompt pack. A real local skill.
            </p>
            <div className="flex flex-wrap gap-6">
              {[
                ["SKILL.md", `${REPO}/blob/main/skills/tastemaker/SKILL.md`],
                ["anti-slop gates", `${REPO}/blob/main/skills/tastemaker/references/anti-slop-checklist.md`],
                ["motion rules", `${REPO}/blob/main/skills/tastemaker/references/animation-guidelines.md`],
                ["taste memory", `${REPO}/blob/main/skills/tastemaker/references/taste-memory.md`],
              ].map(([label, href]) => (
                <a key={label} href={href} target="_blank" rel="noopener" className="font-mono text-[0.82rem] font-semibold text-teal transition-colors hover:text-ink">
                  {label}
                </a>
              ))}
            </div>
          </div>
        </section>

        {/* problem */}
        <section className="py-16 lg:py-24">
          <div className="mx-auto w-[min(900px,calc(100%-40px))]">
            <Reveal>
              <Eyebrow>the problem</Eyebrow>
              <h2 className="max-w-[22ch] font-display text-[clamp(1.7rem,3vw,2.5rem)] leading-[1.14] font-extrabold">
                Every agent defaults to the same page.
              </h2>
              <p className="mt-3.5 max-w-[62ch] text-[clamp(1rem,1.4vw,1.14rem)] text-ink-soft">
                Purple-to-indigo gradient hero. Rounded card, soft shadow. A palette picked because
                it looked fine in the moment, never checked against anything. Ask ten agents for a
                landing page and you'll recognize the ninth one before it finishes rendering.
              </p>
            </Reveal>
            <Reveal delay={80} className="mt-12">
              <ScanConsole
                tone="fail"
                command="$ anti_slop_scan.py generic-agent-output.html"
                rows={[
                  { mark: "HIGH", key: "ai-gradient", note: "indigo-to-purple hero, unrelated to the product underneath it" },
                  { mark: "HIGH", key: "unchecked-contrast", note: "colors picked by eye, never run against a single pairing" },
                  { mark: "MED", key: "no-style-lock", note: "next screen in the same session drifts, nothing persists" },
                ]}
                footer="3 findings. 0 fixed."
              />
            </Reveal>
          </div>
        </section>

        {/* how it works */}
        <section id="how" className="py-16 lg:py-24">
          <div className="mx-auto w-[min(1180px,calc(100%-40px))]">
            <Reveal>
              <Eyebrow>how it works</Eyebrow>
              <h2 className="max-w-[22ch] font-display text-[clamp(1.7rem,3vw,2.5rem)] leading-[1.14] font-extrabold">
                Six checks run before the first component exists.
              </h2>
              <p className="mt-3.5 max-w-[56ch] text-ink-soft">
                Every one of these is real: a script, a Markdown file, or a gate that has to pass.
                Nothing here is decorative.
              </p>
            </Reveal>

            <div className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {CHECKS.map((c, i) => {
                const Icon = c.icon
                return (
                  <Reveal key={c.title} delay={i * 60} className={c.wide ? "lg:col-span-2" : ""}>
                    <Card className="h-full gap-0 rounded-[20px] border-border bg-white p-6 shadow-none transition-colors hover:border-teal/40">
                      <Icon size={24} className="mb-4 text-orchid" strokeWidth={1.6} />
                      <h3 className="mb-2 font-display text-[1.02rem] font-extrabold">{c.title}</h3>
                      <p className="text-[0.9rem] text-ink-soft">{c.body}</p>
                    </Card>
                  </Reveal>
                )
              })}
            </div>

            <Reveal delay={120} className="mt-4">
              <ScanConsole
                tone="pass"
                command="$ tastemaker build --project tastemaker-skill.online"
                rows={[
                  { mark: "PASS", key: "reference-intel", note: "competitor + cultural board built before the first color" },
                  { mark: "PASS", key: "contrast-check", note: "every pairing run through real WCAG math" },
                  { mark: "PASS", key: "real-assets", note: "real icons and real screenshots, no gray boxes" },
                  { mark: "PASS", key: "motion-default", note: "scroll-driven reveals ship in the same pass" },
                  { mark: "PASS", key: "style-lock", note: "palette and type reused on every later screen" },
                  { mark: "PASS", key: "register-variety", note: "one committed visual direction, not the default template" },
                ]}
                footer="6 checks. 6 passed."
              />
            </Reveal>
          </div>
        </section>

        {/* contrast proof */}
        <section id="proof" className="py-16 lg:py-24">
          <div className="mx-auto w-[min(760px,calc(100%-40px))]">
            <Reveal>
              <Eyebrow>proof, not claims</Eyebrow>
              <h2 className="max-w-[22ch] font-display text-[clamp(1.7rem,3vw,2.5rem)] leading-[1.14] font-extrabold">
                Checked with real math, not eyeballed.
              </h2>
              <p className="mt-3.5 max-w-[56ch] text-ink-soft">
                Every pairing on this page runs through{" "}
                <a href={`${REPO}/blob/main/skills/tastemaker/scripts/check_contrast.py`} target="_blank" rel="noopener" className="text-teal underline-offset-4 hover:underline">
                  check_contrast.py
                </a>{" "}
                before it ships. These are this page's actual numbers.
              </p>
            </Reveal>
            <div className="mt-8 flex flex-col gap-2">
              {CONTRAST.map((c, i) => (
                <Reveal key={c.label} delay={i * 70}>
                  <div className="flex flex-wrap items-center gap-4 rounded-[20px] border border-white/15 bg-dark px-5 py-4">
                    <span className="flex-1 font-mono text-[0.92rem] font-semibold text-[#e5f6f6]">{c.label}</span>
                    <span className="font-mono text-[1.3rem] font-extrabold text-orchid tabular-nums">{c.value}</span>
                    <Badge className="rounded-full border border-teal-bright bg-transparent px-3 py-1 font-mono text-[0.68rem] font-extrabold tracking-wider text-teal-bright">
                      PASS
                    </Badge>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        {/* modes */}
        <section id="modes" className="py-16 lg:py-24">
          <div className="mx-auto w-[min(1180px,calc(100%-40px))]">
            <Reveal>
              <Eyebrow>premium modes</Eyebrow>
              <h2 className="max-w-[22ch] font-display text-[clamp(1.7rem,3vw,2.5rem)] leading-[1.14] font-extrabold">
                Different products shouldn't wear the same suit.
              </h2>
              <p className="mt-3.5 max-w-[56ch] text-ink-soft">
                Four sponsor-exclusive visual registers, generated by the same engine, committing to
                a real direction instead of a default.
              </p>
            </Reveal>
            <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {MODES.map((m, i) => (
                <Reveal key={m.name} delay={i * 70}>
                  <Card className="h-full overflow-hidden rounded-[20px] border-border bg-white p-0 shadow-none transition-colors hover:border-teal">
                    <div className="overflow-hidden border-b border-border bg-paper">
                      <img
                        src={`/assets/modes/${m.file}`}
                        alt={m.alt}
                        width={900}
                        height={495}
                        loading="lazy"
                        className="block aspect-[900/495] h-auto w-full object-cover object-top"
                      />
                    </div>
                    <figcaption className="p-4">
                      <strong className="block font-display text-[0.95rem] font-extrabold">{m.name}</strong>
                      <span className="mt-1 block text-[0.78rem] text-soft-muted">{m.note}</span>
                    </figcaption>
                  </Card>
                </Reveal>
              ))}
            </div>
            <Reveal delay={100}>
              <div className="mt-4 flex flex-wrap items-center justify-between gap-5 rounded-[28px] border border-border bg-cream px-6 py-5">
                <p className="max-w-[44ch] font-mono text-[0.84rem] text-ink-soft">
                  Sponsor-exclusive, on top of the free core skill.
                </p>
                <a
                  href="https://buy.polar.sh/polar_cl_tY4OjST0hD2YW36YeNrDJgHs6Ybz9vmsQeHNX0YSbl4"
                  target="_blank"
                  rel="noopener"
                  className="inline-flex min-h-[46px] items-center justify-center rounded-full bg-dark px-5 font-extrabold text-white transition-transform active:scale-[0.97]"
                >
                  Unlock for $8/month
                </a>
              </div>
            </Reveal>
          </div>
        </section>

        {/* memory */}
        <section id="memory" className="py-16 lg:py-24">
          <div className="mx-auto w-[min(1180px,calc(100%-40px))]">
            <Reveal>
              <Eyebrow>what changed</Eyebrow>
              <h2 className="max-w-[22ch] font-display text-[clamp(1.7rem,3vw,2.5rem)] leading-[1.14] font-extrabold">
                The skill remembers your taste.
              </h2>
              <p className="mt-3.5 max-w-[56ch] text-ink-soft">
                Project style choices live in the repo. Personal preferences can live locally. A
                rejected direction becomes a guardrail for next time instead of getting forgotten.
              </p>
            </Reveal>
            <Reveal delay={80}>
              <Card className="mt-8 gap-0 rounded-[20px] border-border bg-white p-6 shadow-none sm:px-7">
                <div className="flex flex-wrap items-baseline justify-between gap-2 pb-1.5">
                  <code className="font-mono text-[0.88rem] font-extrabold text-teal">.tastemaker/</code>
                  <span className="font-mono text-[0.68rem] font-semibold tracking-wide text-soft-muted uppercase">this project</span>
                </div>
                {[
                  ["├──", "style-lock.md", "Palette, type, shape, assets, motion, and do-not rules for this project."],
                  ["└──", "decisions.log", "Append-only keep, reject, and pending-review decisions from every design pass."],
                ].map(([branch, file, desc]) => (
                  <div key={file} className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-border py-2.5">
                    <code className="font-mono text-[0.88rem] font-bold">
                      <span className="font-normal text-soft-muted">{branch}</span> {file}
                    </code>
                    <span className="text-[0.86rem] text-ink-soft">{desc}</span>
                  </div>
                ))}
                <div className="mt-2.5 flex flex-wrap items-baseline justify-between gap-2 border-t border-dashed border-border pt-4 pb-1.5">
                  <code className="font-mono text-[0.88rem] font-extrabold text-teal">~/.tastemaker/</code>
                  <span className="font-mono text-[0.68rem] font-semibold tracking-wide text-soft-muted uppercase">your machine, every project</span>
                </div>
                <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-border py-2.5">
                  <code className="font-mono text-[0.88rem] font-bold">
                    <span className="font-normal text-soft-muted">└──</span> profile.md
                  </code>
                  <span className="text-[0.86rem] text-ink-soft">
                    Reusable preferences, promoted only when you choose or repeat them.
                  </span>
                </div>
              </Card>
            </Reveal>
          </div>
        </section>

        {/* install */}
        <section id="install" className="py-16 lg:py-24">
          <div className="mx-auto w-[min(1180px,calc(100%-40px))]">
            <Reveal>
              <div className="rounded-[28px] bg-dark px-6 py-12 text-[#e5f6f6] sm:px-16 sm:py-16">
                <p className="mb-4 inline-block w-max rounded-full border border-orange/40 bg-dark-soft px-3 py-1.5 font-mono text-[0.68rem] font-extrabold tracking-[0.08em] text-orange uppercase">
                  free and local
                </p>
                <h2 className="max-w-[20ch] font-display text-[clamp(1.8rem,3.4vw,2.7rem)] leading-[1.1] font-extrabold text-white">
                  Install once. Ask normally.
                </h2>
                <p className="mt-3.5 max-w-[52ch] text-[1.02rem] opacity-80">
                  No hosted editor, no account, no separate design handoff. The taste layer lives
                  where the agent already works.
                </p>
                <div className="mt-7">
                  <InstallRow large />
                </div>
                <p className="mt-4 text-[0.84rem] opacity-70">
                  Using Claude Code specifically? The{" "}
                  <a href={`${REPO}#claude-code-plugin-marketplace`} target="_blank" rel="noopener" className="text-teal-bright underline-offset-4 hover:underline">
                    plugin marketplace
                  </a>{" "}
                  and manual install work too.
                </p>
              </div>
            </Reveal>
          </div>
        </section>
      </main>

      <footer className="py-8 pb-12">
        <div className="mx-auto flex w-[min(1180px,calc(100%-40px))] flex-wrap items-center justify-between gap-5">
          <a href="#top" className="flex items-center gap-2.5 font-display text-base font-black">
            <img src="/assets/mark-tastemaker.svg" alt="" width={30} height={30} />
            <span>tastemaker</span>
          </a>
          <div className="font-mono text-[0.68rem] text-soft-muted">
            Built with the workflow it documents.
          </div>
          <div className="flex flex-wrap items-center gap-5 text-[0.82rem] text-soft-muted">
            <a href={REPO} target="_blank" rel="noopener" className="transition-colors hover:text-teal">GitHub</a>
            <a href={`${REPO}/blob/main/README.md`} target="_blank" rel="noopener" className="transition-colors hover:text-teal">Docs</a>
            <a href={`${REPO}/blob/main/LICENSE`} target="_blank" rel="noopener" className="transition-colors hover:text-teal">MIT License</a>
            <a href="https://github.com/sponsors/codeswithroh" target="_blank" rel="noopener" className="text-teal transition-colors hover:text-ink">Sponsor</a>
          </div>
          <a href="https://fazier.com/launches/tastemaker-skill.online" target="_blank" rel="noopener" className="inline-flex flex-none opacity-85 transition-opacity hover:opacity-100">
            <img
              src="https://fazier.com/api/v1//public/badges/launch_badges.svg?badge_type=launched&theme=dark"
              width={120}
              height={26}
              alt="Fazier badge"
              loading="lazy"
              className="block h-[26px] w-auto"
            />
          </a>
        </div>
      </footer>
    </>
  )
}
