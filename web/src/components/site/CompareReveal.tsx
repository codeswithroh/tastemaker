import { useEffect, useRef, useState } from "react"

/**
 * The proof visual: two real captures of the same prompt (before.html /
 * after.html from the repo) with a wipe that sweeps continuously, so the
 * comparison reads without a click. Draggable/hoverable too — the loop
 * pauses the moment the user takes over.
 */
export function CompareReveal() {
  const wrapRef = useRef<HTMLDivElement>(null)
  const [wipe, setWipe] = useState(50)
  const [manual, setManual] = useState(false)
  const rafRef = useRef<number | undefined>(undefined)

  useEffect(() => {
    if (manual) return
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setWipe(50)
      return
    }
    let start: number | null = null
    const loop = (t: number) => {
      if (start === null) start = t
      const elapsed = (t - start) / 1000
      // 7.6s round trip, eased, held between 18% and 82% so neither side
      // is ever fully hidden.
      const phase = (Math.sin((elapsed / 3.8) * Math.PI) + 1) / 2
      setWipe(18 + phase * 64)
      rafRef.current = requestAnimationFrame(loop)
    }
    rafRef.current = requestAnimationFrame(loop)
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current)
    }
  }, [manual])

  const setFromPointer = (clientX: number) => {
    const el = wrapRef.current
    if (!el) return
    const r = el.getBoundingClientRect()
    const pct = ((clientX - r.left) / r.width) * 100
    setWipe(Math.max(0, Math.min(100, pct)))
  }

  return (
    <figure className="m-0">
      <div
        ref={wrapRef}
        role="img"
        aria-label="The same landing-page prompt built twice: once with no design skill, once with tastemaker installed. The divider sweeps between them."
        className="relative aspect-[1200/660] overflow-hidden rounded-[28px] border border-border bg-dark shadow-[0_30px_90px_rgba(12,20,20,0.3)] select-none"
        onPointerDown={(e) => {
          setManual(true)
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
          />
        </div>
        <div
          className="absolute inset-0"
          style={{ clipPath: `inset(0 ${100 - wipe}% 0 0)` }}
        >
          <img
            src="/assets/proof/before-fold.png"
            alt=""
            width={1200}
            height={660}
            className="h-full w-full object-cover object-top"
          />
        </div>

        <div
          className="absolute top-0 bottom-0 z-20 w-0.5 bg-white shadow-[0_0_0_1px_rgba(23,21,20,0.25)]"
          style={{ left: `${wipe}%`, transform: "translateX(-1px)" }}
        >
          <span className="absolute top-1/2 left-1/2 grid h-9 w-9 -translate-x-1/2 -translate-y-1/2 place-items-center rounded-full bg-white shadow-[0_20px_60px_rgba(23,21,20,0.1)]">
            <svg width="16" height="10" viewBox="0 0 16 10" aria-hidden="true">
              <path d="M5 1 1 5l4 4M11 1l4 4-4 4" fill="none" stroke="#171514" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </span>
        </div>

        <span className="absolute bottom-4 left-4 z-10 rounded-full bg-dark/80 px-3 py-1.5 font-mono text-[0.68rem] font-bold text-[#e5f6f6] backdrop-blur-sm">
          no skill
        </span>
        <span className="absolute right-4 bottom-4 z-10 rounded-full bg-dark/80 px-3 py-1.5 font-mono text-[0.68rem] font-bold text-[#e5f6f6] backdrop-blur-sm">
          tastemaker
        </span>
      </div>
    </figure>
  )
}
