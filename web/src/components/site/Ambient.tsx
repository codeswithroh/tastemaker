import { useEffect, useRef } from "react"

/**
 * Drifting gradient-mesh background. Canvas + rAF writing straight to the
 * 2D context — no React state, so it never re-renders anything. Draws one
 * static frame and stops under prefers-reduced-motion.
 *
 * This is the honest substitute for a licensed stock-video background loop:
 * real continuous motion, nothing to source or license.
 */
export function Ambient() {
  const ref = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = ref.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    let w = 0
    let h = 0

    const resize = () => {
      const p = canvas.parentElement
      if (!p) return
      const r = p.getBoundingClientRect()
      w = r.width
      h = r.height
      canvas.width = Math.max(1, Math.floor(w * dpr))
      canvas.height = Math.max(1, Math.floor(h * dpr))
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    }

    // Tuned for the light canvas — the reference sites this palette now
    // matches (Wunderbucket, Kacco) run almost flat backgrounds, so this
    // reads as a faint warmth rather than a visible gradient mesh.
    const blobs = [
      { x: 0.2, y: 0.28, r: 0.52, c: "0,130,134", a: 0.09, sx: 0.00011, sy: 0.00008, p: 0 },
      { x: 0.78, y: 0.38, r: 0.44, c: "190,133,206", a: 0.07, sx: 0.00009, sy: 0.00013, p: 2.1 },
      { x: 0.52, y: 0.78, r: 0.46, c: "230,104,38", a: 0.05, sx: 0.00013, sy: 0.0001, p: 4.2 },
    ]

    const draw = (t: number) => {
      ctx.clearRect(0, 0, w, h)
      for (const b of blobs) {
        const x = (b.x + Math.sin(t * b.sx + b.p) * 0.06) * w
        const y = (b.y + Math.cos(t * b.sy + b.p) * 0.06) * h
        const r = b.r * Math.max(w, h)
        const g = ctx.createRadialGradient(x, y, 0, x, y, r)
        g.addColorStop(0, `rgba(${b.c},${b.a})`)
        g.addColorStop(1, `rgba(${b.c},0)`)
        ctx.fillStyle = g
        ctx.fillRect(0, 0, w, h)
      }
    }

    resize()
    window.addEventListener("resize", resize)

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      draw(0)
      return () => window.removeEventListener("resize", resize)
    }

    let raf = 0
    const loop = (t: number) => {
      draw(t)
      raf = requestAnimationFrame(loop)
    }
    raf = requestAnimationFrame(loop)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener("resize", resize)
    }
  }, [])

  return (
    <canvas
      ref={ref}
      aria-hidden="true"
      className="pointer-events-none absolute inset-0 h-full w-full"
    />
  )
}

/** Fine film grain, drawn once. Kills the flat-gradient look. */
export function Grain() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 z-[1] opacity-[0.035] mix-blend-overlay"
      style={{
        backgroundImage:
          "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)'/%3E%3C/svg%3E\")",
      }}
    />
  )
}
