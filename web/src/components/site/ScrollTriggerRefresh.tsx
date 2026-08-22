import { useEffect } from "react"
import { ScrollTrigger } from "@/lib/gsap"

/**
 * Re-measures every ScrollTrigger once all images have actually loaded.
 * The illustrations are large, lazy-loaded images — if one finishes
 * loading after ScrollTrigger already measured trigger start/end pixel
 * positions against the pre-load layout, every reveal/parallax point below
 * it drifts. Renders nothing; just watches and refreshes.
 */
export function ScrollTriggerRefresh() {
  useEffect(() => {
    const images = Array.from(document.images)
    const pending = images.filter((img) => !img.complete)
    if (pending.length === 0) return

    // Debounced, not "wait for every image": each lazy-loaded illustration
    // can shift layout the moment it resolves, so refresh shortly after
    // each load rather than only once at the very end of the page.
    let timer = 0
    const onLoad = () => {
      window.clearTimeout(timer)
      timer = window.setTimeout(() => ScrollTrigger.refresh(), 120)
    }
    pending.forEach((img) => {
      img.addEventListener("load", onLoad, { once: true })
      img.addEventListener("error", onLoad, { once: true })
    })
    return () => {
      window.clearTimeout(timer)
      pending.forEach((img) => {
        img.removeEventListener("load", onLoad)
        img.removeEventListener("error", onLoad)
      })
    }
  }, [])

  return null
}
