const initSite = () => {
  const copyButton = document.querySelector("[data-copy]");
  if (copyButton) {
    copyButton.addEventListener("click", async () => {
      const value = copyButton.dataset.copy;
      try {
        if (navigator.clipboard?.writeText) {
          await navigator.clipboard.writeText(value);
        } else {
          const fallback = document.createElement("textarea");
          fallback.value = value;
          fallback.setAttribute("readonly", "");
          fallback.style.position = "fixed";
          fallback.style.opacity = "0";
          document.body.appendChild(fallback);
          fallback.select();
          document.execCommand("copy");
          fallback.remove();
        }
        copyButton.querySelector("span").textContent = "Copied";
        window.setTimeout(() => { copyButton.querySelector("span").textContent = "Copy"; }, 1800);
      } catch {
        copyButton.querySelector("span").textContent = "Select command";
      }
    });
  }

  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".site-header", { y: -16, opacity: 0, duration: .35 })
      .from(".hero-copy .kicker", { y: 12, opacity: 0, duration: .35 }, "-=.05")
      .from(".hero-copy h1", { y: 22, opacity: 0, duration: .6 }, "-=.12")
      .from(".hero-copy > p, .hero-copy .button-row", { y: 14, opacity: 0, stagger: .08, duration: .4 }, "-=.3")
      .from(".hero-showcase", { y: 24, opacity: 0, duration: .62 }, "-=.48")
      .from(".hero-showcase .output-preview", { clipPath: "inset(0 100% 0 0)", duration: .72, ease: "power3.inOut" }, "-=.28");

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: .42,
        ease: "power3.out",
        scrollTrigger: { trigger: element, start: "top 88%", once: true },
      });
    });

    const steps = gsap.utils.toArray(".workflow-step");
    steps.forEach((step, index) => {
      ScrollTrigger.create({
        trigger: step,
        start: "top 48%",
        end: "bottom 48%",
        onToggle: ({ isActive }) => {
          if (!isActive) return;
          steps.forEach((item) => item.classList.remove("is-active"));
          step.classList.add("is-active");
          gsap.to(".meter-fill", { scaleX: (index + 1) / steps.length, duration: .28, ease: "power2.out" });
          const count = document.querySelector("[data-step-count]");
          if (count) count.textContent = String(index + 1).padStart(2, "0");
        },
      });
    });

    gsap.to(".compare-link", {
      y: -8,
      scrollTrigger: { trigger: ".compare-stage", start: "top bottom", end: "bottom top", scrub: true },
    });
    gsap.from(".versus-headline span", {
      xPercent: 24,
      scrollTrigger: { trigger: ".versus-headline", start: "top 80%", end: "bottom 38%", scrub: true },
    });
  });
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
