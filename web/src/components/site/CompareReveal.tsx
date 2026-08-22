import { useEffect, useRef } from "react"

/**
 * Two real captures of the same prompt, with a wipe that sweeps on its own
 * and hands over to drag on pointer down.
 *
 * Perf note: the wipe is driven by writing a CSS custom property straight to
 * the DOM node, NOT by React state. An earlier version called setState on
 * every animation frame, which re-rendered the whole component 60x/second and
 * made the page visibly janky to scroll. Nothing here re-renders after mount.
 */
export function CompareReveal() {
  const wrapRef = useRef<HTMLDivElement>(null)
  const manualRef = useRef(false)

  useEffect(() => {
    const el = wrapRef.current
    if (!el) return

    const set = (pct: number) => {
      el.style.setProperty("--wipe", `${pct}%`)
    }

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      set(50)
      return
    }

    let raf = 0
    let start: number | null = null
    const loop = (t: number) => {
      if (start === null) start = t
      if (!manualRef.current) {
        const elapsed = (t - start) / 1000
        // ~7.6s round trip, eased, held between 18% and 82% so neither side
        // is ever fully hidden at a glance.
        const phase = (Math.sin((elapsed / 3.8) * Math.PI) + 1) / 2
        set(18 + phase * 64)
      }
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)
    return () => cancelAnimationFrame(raf)
  }, [])

  const setFromPointer = (clientX: number) => {
    const el = wrapRef.current
    if (!el) return
    const r = el.getBoundingClientRect()
    const pct = ((clientX - r.left) / r.width) * 100
    el.style.setProperty("--wipe", `${Math.max(0, Math.min(100, pct))}%`)
  }

  return (
    <figure className="m-0">
      <div
        ref={wrapRef}
        role="img"
        aria-label="The same landing-page prompt built twice: once with no design skill, once with tastemaker installed. The divider sweeps between them."
        className="group relative aspect-[1200/660] -rotate-[1.1deg] cursor-ew-resize touch-none overflow-hidden rounded-[22px] border border-border bg-dark shadow-[0_30px_70px_rgba(23,21,20,0.22)] transition-transform duration-500 select-none [--wipe:50%] hover:rotate-0"
        onPointerDown={(e) => {
          manualRef.current = true
          e.currentTarget.setPointerCapture(e.pointerId)
          setFromPointer(e.clientX)
        }}
        onPointerMove={(e) => {
          if (e.currentTarget.hasPointerCapture(e.pointerId)) setFromPointer(e.clientX)
        }}
        onPointerUp={(e) => e.currentTarget.releasePointerCapture(e.pointerId)}
      >
        <div className="absolute inset-0">
          <img
            src="/assets/proof/after-fold.png"
            alt=""
            width={1200}
            height={660}
            className="h-full w-full object-cover object-top"
            draggable={false}
          />
        </div>
        <div
          className="absolute inset-0"
          style={{ clipPath: "inset(0 calc(100% - var(--wipe)) 0 0)" }}
        >
          <img
            src="/assets/proof/before-fold.png"
            alt=""
            width={1200}
            height={660}
            className="h-full w-full object-cover object-top"
            draggable={false}
          />
        </div>

        <div
          className="absolute top-0 bottom-0 z-20 w-0.5 -translate-x-px bg-gold-bright shadow-[0_0_0_1px_rgba(23,21,20,0.25)]"
          style={{ left: "var(--wipe)" }}
        >
          <span className="absolute top-1/2 left-1/2 grid h-9 w-9 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-gold-bright shadow-[0_20px_60px_rgba(23,21,20,0.18)] transition-transform group-hover:scale-110">
            <svg width="16" height="10" viewBox="0 0 16 10" aria-hidden="true">
              <path
                d="M5 1 1 5l4 4M11 1l4 4-4 4"
                fill="none"
                stroke="#171514"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </span>
        </div>

        {/* Hand-lettered tags rather than UI chips, to match the site's
            illustration language instead of reading as product-marketing
            chrome bolted onto a screenshot. */}
        <span
          className="absolute bottom-4 left-4 z-10 -rotate-3 rounded-md bg-[#f4f1eb] px-3 py-1 text-[1.05rem] font-bold text-ink shadow-[0_6px_16px_rgba(23,21,20,0.22)]"
          style={{ fontFamily: "var(--font-hand)" }}
        >
          no skill
        </span>
        <span
          className="absolute right-4 bottom-4 z-10 rotate-2 rounded-md bg-[#f4f1eb] px-3 py-1 text-[1.05rem] font-bold text-gold shadow-[0_6px_16px_rgba(23,21,20,0.22)]"
          style={{ fontFamily: "var(--font-hand)" }}
        >
          tastemaker
        </span>
      </div>
    </figure>
  )
}
