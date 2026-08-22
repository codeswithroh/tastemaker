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
import { RevealGroup } from "@/components/site/RevealGroup"
import { Parallax, Float } from "@/components/site/Parallax"
import { HeroTimeline } from "@/components/site/HeroTimeline"
import { ScrollTriggerRefresh } from "@/components/site/ScrollTriggerRefresh"

const INSTALL = "npx skills add codeswithroh/tastemaker"
const REPO = "https://github.com/codeswithroh/tastemaker"
const ILL = "/assets/illustrations"

function InstallRow({ large = false }: { large?: boolean }) {
  const [copied, setCopied] = useState(false)
  return (
    <div
      className={`flex w-full max-w-[560px] items-center gap-2 rounded-full border border-ink/10 py-2 pr-2 pl-5 backdrop-blur-xl ${
        large ? "bg-ink/[0.05]" : "bg-ink/[0.04]"
      }`}
    >
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
    <p className="mb-6 inline-flex w-max items-center gap-2 rounded-full border border-ink/10 bg-ink/[0.04] px-3.5 py-1.5 font-mono text-[0.66rem] font-bold tracking-[0.14em] text-muted-dark uppercase backdrop-blur-xl">
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

/** A section's illustration, with scroll parallax. No card, no border, no
 * shadow — it sits directly on the page background so it blends into the
 * site rather than reading as a separate framed asset. */
function Illustration({
  src,
  alt,
  strength = 26,
  maxW = 640,
  float = false,
}: {
  src: string
  alt: string
  strength?: number
  maxW?: number
  float?: boolean
}) {
  const img = (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      className="mx-auto block w-full h-auto select-none"
      style={{ maxWidth: maxW }}
      draggable={false}
    />
  )
  return (
    <Parallax strength={strength} className="mx-auto">
      {float ? <Float duration={6}>{img}</Float> : img}
    </Parallax>
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
  const c = tone === "fail" ? "text-orange" : "text-gold-bright"
  return (
    <div className="overflow-hidden rounded-2xl border border-white/10 bg-dark shadow-[0_20px_50px_rgba(23,21,20,0.14)]">
      <div className="flex items-center gap-2 border-b border-white/10 px-5 py-3.5">
        <span className="h-2.5 w-2.5 rounded-full bg-orange/70" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
        <span className="ml-2 font-mono text-[0.78rem] text-muted-dark">{command}</span>
      </div>
      <ul className="m-0 list-none p-0">
        {rows.map((r) => (
          <li key={r.key} className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-white/[0.08] px-5 py-3 first:border-t-0">
            <span className={`w-11 flex-none font-mono text-[0.66rem] font-extrabold ${c}`}>{r.mark}</span>
            <span className="flex-none font-mono text-[0.82rem] font-bold text-[#e5f6f6] sm:w-[164px]">{r.key}</span>
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
      <ScrollTriggerRefresh />
      <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-100 focus:rounded-xl focus:bg-teal-bright focus:px-4 focus:py-2.5 focus:font-bold focus:text-dark">
        Skip to content
      </a>

      <header data-hero="nav" className="sticky top-0 z-90 border-b border-ink/[0.08] bg-background/70 backdrop-blur-xl">
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
            <a href={REPO} target="_blank" rel="noopener" aria-label="Tastemaker on GitHub" className="grid h-9 w-9 place-items-center rounded-full border border-ink/10 bg-ink/[0.04] transition hover:bg-ink/10">
              <img src="/assets/icons/github.svg" alt="" width={15} height={15} className="opacity-80" />
            </a>
            <a href="https://x.com/tastemaker_ui" target="_blank" rel="noopener" aria-label="Tastemaker on X" className="grid h-9 w-9 place-items-center rounded-full border border-ink/10 bg-ink/[0.04] transition hover:bg-ink/10">
              <img src="/assets/icons/x-twitter.svg" alt="" width={13} height={13} className="opacity-80" />
            </a>
            <a href="#install" className="inline-flex min-h-9 items-center rounded-full bg-primary px-4 text-[0.86rem] font-extrabold text-primary-foreground transition hover:brightness-110">
              Install
            </a>
          </div>
        </div>
      </header>

      <main id="main">
        {/* hero — the transformation illustration is the whole pitch */}
        <section id="top" className="relative isolate overflow-hidden">
          <HeroTimeline />
          <Ambient />
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-40 bg-gradient-to-b from-transparent to-background" />
          <div className="relative mx-auto flex w-[min(1200px,calc(100%-40px))] flex-col items-center pt-20 pb-4 text-center lg:pt-28">
            <h1 data-hero="headline" className="max-w-[min(20ch,100%)] font-display text-[clamp(2.4rem,5.2vw,4.2rem)] leading-[1.04] font-extrabold tracking-[-0.03em]">
              Your agent writes working code.{" "}
              <span className="text-gold" style={{ fontFamily: "var(--font-hand)", fontSize: "1.15em" }}>It doesn't write taste.</span>
            </h1>
            <p data-hero="stagger" className="mt-6 max-w-[min(46ch,100%)] text-[clamp(1rem,1.25vw,1.15rem)] leading-relaxed text-muted-dark">
              A local skill that gives Claude Code, Gemini CLI, and Windsurf a real design
              process: study references, lock a palette that passes contrast, cast real assets,
              and remember what you keep.
            </p>
            <div data-hero="stagger" className="mt-8 flex w-full min-w-0 justify-center"><InstallRow /></div>
            <div data-hero="stagger" className="mt-5 flex flex-wrap items-center justify-center gap-5">
              <a href="#proof" className="group inline-flex min-h-[48px] items-center gap-2 rounded-full bg-primary px-6 font-extrabold text-primary-foreground transition hover:brightness-110">
                See the proof
                <ArrowRight size={16} className="transition-transform group-hover:translate-x-0.5" />
              </a>
              <a href={REPO} target="_blank" rel="noopener" className="inline-flex items-center gap-1.5 text-[0.92rem] font-semibold text-muted-dark transition-colors hover:text-foreground">
                Read the source <ArrowUpRight size={15} />
              </a>
            </div>
          </div>
          <div data-hero="visual" className="relative mx-auto mt-6 w-[min(1200px,calc(100%-24px))] lg:mt-2">
            <Illustration
              src={`${ILL}/hero-transformation.webp`}
              alt="A mentor character shows one robot a beautiful, styled landing page while a confused robot beside her holds a stack of identical generic wireframes — the moment an agent gains design taste."
              maxW={1200}
              strength={22}
            />
          </div>
        </section>

        {/* proof strip */}
        <section aria-label="Built as a real local skill" className="border-y border-ink/[0.08]">
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
                <a key={l} href={h} target="_blank" rel="noopener" className="font-mono text-[0.8rem] font-semibold text-gold transition-opacity hover:opacity-70">{l}</a>
              ))}
            </div>
          </div>
        </section>

        {/* problem — the assembly line of identical robots IS the argument */}
        <section className="py-24 lg:py-32">
          <div className="mx-auto grid w-[min(1200px,calc(100%-40px))] items-center gap-14 lg:grid-cols-[minmax(0,1fr)_minmax(0,0.95fr)]">
            <Reveal className="min-w-0">
              <SectionHead
                eyebrow="the problem"
                title={<>Every agent defaults to the <span className="text-gold" style={{ fontFamily: "var(--font-hand)", fontSize: "1.15em" }}>same page</span>.</>}
                lede="Purple-to-indigo gradient hero. Rounded card, soft shadow. A palette picked because it looked fine in the moment, never checked against anything. Ask ten agents for a landing page and you'll recognize the ninth one before it finishes rendering."
              />
              <div className="mt-10 max-w-[520px]">
                <Console
                  tone="fail"
                  command="anti_slop_scan.py generic-agent-output.html"
                  rows={[
                    { mark: "HIGH", key: "ai-gradient", note: "indigo-to-purple, unrelated to the product" },
                    { mark: "HIGH", key: "unchecked-contrast", note: "colors picked by eye, never measured" },
                    { mark: "MED", key: "no-style-lock", note: "next screen drifts, nothing persists" },
                  ]}
                  footer="3 findings. 0 fixed."
                />
              </div>
            </Reveal>
            <Reveal delay={100} className="min-w-0">
              <Illustration
                src={`${ILL}/problem-assembly-line.webp`}
                alt="An assembly line of identical small robots stamping out identical generic wireframe pages, with one robot at the end scratching its head in confusion."
                maxW={560}
                strength={34}
              />
            </Reveal>
          </div>
        </section>

        {/* how it works — the illustrated journey through the real workflow */}
        <section id="how" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                center
                eyebrow="how it works"
                title="Six checks run before the first component exists."
                lede="Every one is real: a script, a Markdown file, or a gate that has to pass. Nothing here is decorative."
              />
            </Reveal>

            <Reveal delay={80} className="mt-6">
              <Illustration
                src={`${ILL}/how-it-works-journey.webp`}
                alt="A character walks a dotted path through the design process: studying a reference through a magnifying glass, choosing a palette, picking assets from a box, setting type with a ruler, tuning motion on a dashed path, and stamping final approval — then launching the finished page as a paper airplane."
                maxW={1100}
                strength={20}
              />
            </Reveal>

            <RevealGroup className="mt-14 grid gap-px overflow-hidden rounded-2xl border border-ink/10 bg-ink/[0.06] sm:grid-cols-2 lg:grid-cols-3">
              {CHECKS.map((c) => {
                const Icon = c.icon
                return (
                  <div key={c.title} className="group h-full bg-background p-7 transition-colors hover:bg-ink/[0.03]">
                    <div className="mb-5 grid h-10 w-10 place-items-center rounded-xl border border-ink/10 bg-ink/[0.04] text-gold transition-colors group-hover:border-gold/40">
                      <Icon size={18} strokeWidth={1.8} />
                    </div>
                    <h3 className="mb-2 font-display text-[1.05rem] font-extrabold">{c.title}</h3>
                    <p className="text-[0.9rem] leading-relaxed text-muted-dark">{c.body}</p>
                  </div>
                )
              })}
            </RevealGroup>
          </div>
        </section>

        {/* proof / contrast — the measuring illustration frames the real numbers */}
        <section id="proof" className="relative isolate overflow-hidden py-24 lg:py-32">
          <div aria-hidden="true" className="absolute top-1/2 left-1/2 -z-10 h-[420px] w-[820px] max-w-full -translate-x-1/2 -translate-y-1/2 rounded-full bg-orchid/10 blur-[110px]" />
          <div className="mx-auto w-[min(1000px,calc(100%-40px))]">
            <Reveal className="w-full min-w-0">
              <SectionHead center eyebrow="proof, not claims" title="Checked with real math, not eyeballed." />
            </Reveal>

            <Reveal delay={60} className="mt-2">
              <Illustration
                src={`${ILL}/proof-measuring.webp`}
                alt="One character weighs two colors on a balance scale while another kneels with calipers and a ruler, precisely measuring contrast and spacing instead of guessing."
                maxW={780}
                strength={22}
              />
            </Reveal>

            <Reveal delay={120}>
              <p className="mx-auto mt-4 max-w-[52ch] text-center text-muted-dark">
                Every pairing on this page runs through{" "}
                <a href={`${REPO}/blob/main/skills/tastemaker/scripts/check_contrast.py`} target="_blank" rel="noopener" className="text-gold underline-offset-4 hover:underline">check_contrast.py</a>{" "}
                before it ships. These are this page's actual numbers.
              </p>
            </Reveal>

            <RevealGroup className="mx-auto mt-10 flex max-w-[720px] flex-col gap-3" stagger={0.1}>
              {CONTRAST.map((c) => (
                <div key={c.label} className="flex flex-wrap items-center gap-4 rounded-2xl border border-white/10 bg-dark px-6 py-5 shadow-[0_20px_50px_rgba(23,21,20,0.14)]">
                  <span className="flex-1 font-mono text-[0.9rem] text-muted-dark">{c.label}</span>
                  <span className="font-display text-[1.7rem] font-extrabold text-[#e5f6f6] tabular-nums">{c.value}</span>
                  <span className="rounded-full border border-gold-bright/40 bg-gold-bright/10 px-3 py-1 font-mono text-[0.66rem] font-extrabold tracking-wider text-gold-bright">PASS</span>
                </div>
              ))}
            </RevealGroup>

            <Reveal delay={420} className="mx-auto mt-10 max-w-[720px]">
              <CompareReveal />
            </Reveal>
          </div>
        </section>

        {/* modes — four outfits, four registers, same engine */}
        <section id="modes" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                center
                eyebrow="premium modes"
                title={<>Different products shouldn't wear the <span className="text-gold" style={{ fontFamily: "var(--font-hand)", fontSize: "1.15em" }}>same suit</span>.</>}
                lede="Four sponsor-exclusive visual registers, generated by the same engine, each committing to a real direction instead of a default."
              />
            </Reveal>

            <Reveal delay={80} className="mt-4">
              <Illustration
                src={`${ILL}/modes-outfits.webp`}
                alt="Five characters, each dressed in a completely different outfit — a bold geometric block-color suit, a flowing translucent gown, plain minimal clothing, a soft rounded polka-dot coat, and a tailor cutting fabric swatches — representing four distinct visual registers built from the same engine."
                maxW={1000}
                strength={18}
              />
            </Reveal>

            <RevealGroup className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {MODES.map((m) => (
                <figure key={m.name} className="group m-0 overflow-hidden rounded-2xl border border-ink/10 bg-ink/[0.03] transition-all duration-300 hover:-translate-y-1 hover:border-teal-bright/30">
                  <div className="overflow-hidden border-b border-ink/10">
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
              ))}
            </RevealGroup>
            <Reveal delay={120}>
              <div className="mt-6 flex flex-wrap items-center justify-between gap-6 rounded-2xl border border-ink/10 bg-ink/[0.03] px-7 py-6 backdrop-blur-xl">
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

        {/* memory — walking away from the rejected pile, toward the archive */}
        <section id="memory" className="py-24 lg:py-32">
          <div className="mx-auto w-[min(1200px,calc(100%-40px))]">
            <Reveal>
              <SectionHead
                center
                eyebrow="what changed"
                title="The skill remembers your taste."
                lede="Project style choices live in the repo. Personal preferences live on your machine. A rejected direction becomes a guardrail instead of getting forgotten."
              />
            </Reveal>

            <Reveal delay={80} className="mt-6">
              <Illustration
                src={`${ILL}/memory-archive.webp`}
                alt="A character walks away from a scattered pile of rejected, crossed-out generic designs toward an organized, lamp-lit filing cabinet full of kept references and assets."
                maxW={1000}
                strength={20}
              />
            </Reveal>

            <Reveal delay={140} className="mx-auto mt-8 max-w-[900px]">
              <div className="rounded-2xl border border-ink/10 bg-ink/[0.03] p-7 backdrop-blur-xl sm:p-8">
                <div className="flex flex-wrap items-baseline justify-between gap-2 pb-2">
                  <code className="font-mono text-[0.9rem] font-extrabold text-gold">.tastemaker/</code>
                  <span className="font-mono text-[0.66rem] font-bold tracking-widest text-muted-dark uppercase">this project</span>
                </div>
                {[
                  ["├──", "style-lock.md", "Palette, type, shape, assets, motion, and do-not rules."],
                  ["└──", "decisions.log", "Append-only keep, reject, and pending-review decisions."],
                ].map(([b, f, d]) => (
                  <div key={f} className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-ink/[0.08] py-3">
                    <code className="font-mono text-[0.88rem] font-bold text-foreground">
                      <span className="font-normal text-muted-dark">{b}</span> {f}
                    </code>
                    <span className="text-[0.86rem] text-muted-dark">{d}</span>
                  </div>
                ))}
                <div className="mt-3 flex flex-wrap items-baseline justify-between gap-2 border-t border-dashed border-ink/10 pt-5 pb-2">
                  <code className="font-mono text-[0.9rem] font-extrabold text-gold">~/.tastemaker/</code>
                  <span className="font-mono text-[0.66rem] font-bold tracking-widest text-muted-dark uppercase">every project</span>
                </div>
                <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 border-t border-ink/[0.08] py-3">
                  <code className="font-mono text-[0.88rem] font-bold text-foreground">
                    <span className="font-normal text-muted-dark">└──</span> profile.md
                  </code>
                  <span className="text-[0.86rem] text-muted-dark">Reusable preferences, promoted only when you choose or repeat them.</span>
                </div>
              </div>
            </Reveal>
          </div>
        </section>

        {/* install — the developer works normally, the mascot handles taste */}
        <section id="install" className="relative isolate overflow-hidden py-24 lg:py-32">
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
            </Reveal>

            <Reveal delay={80} className="mt-4 w-full">
              <Illustration
                src={`${ILL}/install-mascot.webp`}
                alt="A developer works normally at their desk, plugged by a single cable into a small caped mascot that quietly handles color, type, and asset choices in the background."
                maxW={900}
                strength={16}
                float
              />
            </Reveal>

            <Reveal delay={140} className="mt-2 flex w-full min-w-0 justify-center">
              <InstallRow large />
            </Reveal>
            <Reveal delay={180}>
              <p className="mt-5 text-[0.85rem] text-muted-dark">
                Using Claude Code? The{" "}
                <a href={`${REPO}#claude-code-plugin-marketplace`} target="_blank" rel="noopener" className="text-gold underline-offset-4 hover:underline">plugin marketplace</a>{" "}
                and manual install work too.
              </p>
            </Reveal>
          </div>
        </section>
      </main>

      <footer className="border-t border-ink/[0.08] py-10">
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
            <a href="https://github.com/sponsors/codeswithroh" target="_blank" rel="noopener" className="text-gold transition-opacity hover:opacity-70">Sponsor</a>
          </div>
          <a href="https://x.com/tastemaker_ui" target="_blank" rel="noopener" aria-label="Tastemaker on X" className="grid h-9 w-9 flex-none place-items-center rounded-full border border-ink/10 bg-ink/[0.04] transition hover:bg-ink/10">
            <img src="/assets/icons/x-twitter.svg" alt="" width={13} height={13} className="opacity-80" />
          </a>
        </div>
      </footer>
    </>
  )
}
