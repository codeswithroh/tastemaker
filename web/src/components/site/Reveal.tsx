import { useEffect, useRef, useState, type ReactNode } from "react"

/**
 * Scroll reveal. Content is visible by default and only animates when the
 * observer confirms it can run — a fail-safe learned the hard way on the
 * previous build, where a CSS-hidden default left whole sections permanently
 * invisible if a scroll trigger ever missed.
 */
export function Reveal({
  children,
  delay = 0,
  className = "",
}: {
  children: ReactNode
  delay?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)
  const [shown, setShown] = useState(false)
  const [armed, setArmed] = useState(false)

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setShown(true)
      return
    }
    setArmed(true)
    const el = ref.current
    if (!el) return

    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShown(true)
          io.disconnect()
        }
      },
      { rootMargin: "0px 0px -10% 0px" },
    )
    io.observe(el)

    // Watchdog: never let a missed trigger hide real content.
    const t = window.setTimeout(() => setShown(true), 2500)
    return () => {
      io.disconnect()
      window.clearTimeout(t)
    }
  }, [])

  const hidden = armed && !shown

  return (
    <div
      ref={ref}
      className={className}
      style={{
        opacity: hidden ? 0 : 1,
        transform: hidden ? "translateY(18px)" : "none",
        transition: `opacity 620ms cubic-bezier(.23,1,.32,1) ${delay}ms, transform 620ms cubic-bezier(.23,1,.32,1) ${delay}ms`,
      }}
    >
      {children}
    </div>
  )
}
