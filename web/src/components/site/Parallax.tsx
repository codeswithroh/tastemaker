import { useEffect, useRef, type ReactNode } from "react"

/**
 * Scroll-linked parallax. Writes `transform` straight to the DOM node on
 * scroll — never through React state. A previous component on this site
 * (CompareReveal) drove an animation through setState on every frame and
 * re-rendered ~60x/second, visibly janking the page; this is the fix
 * pattern applied everywhere motion is scroll-driven now.
 *
 * strength: px of vertical drift at the extremes of the element's transit
 * through the viewport. Small values (20-40) read as depth; large ones
 * read as a gimmick.
 */
export function Parallax({
  children,
  strength = 28,
  className = "",
}: {
  children: ReactNode
  strength?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return

    let raf = 0
    const update = () => {
      const rect = el.getBoundingClientRect()
      const vh = window.innerHeight || 1
      // progress: -1 (element far below viewport) .. 0 (centered) .. 1 (far above)
      const center = rect.top + rect.height / 2
      const progress = (vh / 2 - center) / (vh / 2 + rect.height / 2)
      const y = Math.max(-1, Math.min(1, progress)) * strength
      el.style.transform = `translate3d(0, ${y.toFixed(1)}px, 0)`
      raf = 0
    }

    const onScroll = () => {
      if (raf) return
      raf = requestAnimationFrame(update)
    }

    update()
    window.addEventListener("scroll", onScroll, { passive: true })
    window.addEventListener("resize", onScroll)
    return () => {
      window.removeEventListener("scroll", onScroll)
      window.removeEventListener("resize", onScroll)
      if (raf) cancelAnimationFrame(raf)
    }
  }, [strength])

  return (
    <div ref={ref} className={className} style={{ willChange: "transform" }}>
      {children}
    </div>
  )
}

/** Slow, low-amplitude idle bob — pure CSS, for character illustrations. */
export function Float({
  children,
  className = "",
  duration = 5,
  delay = 0,
}: {
  children: ReactNode
  className?: string
  duration?: number
  delay?: number
}) {
  return (
    <div
      className={`motion-safe:[animation:float_ease-in-out_infinite] ${className}`}
      style={{ animationDuration: `${duration}s`, animationDelay: `${delay}s` }}
    >
      {children}
    </div>
  )
}
