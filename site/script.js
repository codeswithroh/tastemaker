const showAll = () => {
  document
    .querySelectorAll("[data-reveal], [data-reveal-group] > *, .hero-copy > *, .hero-stage > *, .asset-board > *, .system-scene > *, .poster-pill, .print-stack > *, .ledger article, .still-life > *")
    .forEach((el) => {
      el.style.opacity = "1";
      el.style.transform = "none";
    });
};

const initCopyButtons = () => {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const label = button.querySelector("span");

      try {
        await navigator.clipboard.writeText(button.dataset.copy);
        if (label) label.textContent = "Copied";
        window.setTimeout(() => {
          if (label) label.textContent = "Copy";
        }, 1600);
      } catch {
        if (label) label.textContent = "Select";
      }
    });
  });
};

const initMotion = () => {
  if (!window.gsap || !window.ScrollTrigger) {
    showAll();
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".site-header", { y: -14, opacity: 0, duration: 0.32 })
      .from(".micro-label", { y: 12, opacity: 0, duration: 0.28 }, "-=0.04")
      .from(".hero h1", { y: 28, opacity: 0, duration: 0.58 }, "-=0.06")
      .from(".hero-lede, .install-row, .hero-actions", { y: 18, opacity: 0, stagger: 0.07, duration: 0.4 }, "-=0.28")
      .from(".artifact-main", { y: 30, rotation: -1, opacity: 0, duration: 0.64 }, "-=0.34")
      .from(".artifact-proof, .artifact-system, .artifact-note, .palette-strip", { y: 24, opacity: 0, stagger: 0.07, duration: 0.46 }, "-=0.32");

    gsap.to(".artifact-proof", {
      yPercent: -14,
      rotation: 0,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });

    gsap.to(".artifact-system", {
      yPercent: -9,
      rotation: -7,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });

    gsap.to(".palette-strip", {
      yPercent: 18,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: 0.38,
        ease: "power3.out",
        immediateRender: false,
        scrollTrigger: { trigger: element, start: "top 86%", once: true },
      });
    });

    gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
      gsap.from(group.children, {
        y: 22,
        opacity: 0,
        stagger: 0.07,
        duration: 0.42,
        ease: "power3.out",
        immediateRender: false,
        scrollTrigger: { trigger: group, start: "top 82%", once: true },
      });
    });

    gsap.from(".proof-wall a", {
      y: 18,
      opacity: 0,
      stagger: 0.06,
      duration: 0.34,
      ease: "power3.out",
      immediateRender: false,
      scrollTrigger: { trigger: ".proof-wall", start: "top 78%", once: true },
    });

    gsap.from(".asset-board > *", {
      y: 28,
      opacity: 0,
      stagger: 0.08,
      duration: 0.44,
      ease: "power3.out",
      immediateRender: false,
      scrollTrigger: { trigger: ".asset-board", start: "top 78%", once: true },
    });

    gsap.to(".asset-anchor", {
      y: -34,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".asset-mode", {
      y: 28,
      rotation: 8,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".asset-proof", {
      x: -26,
      y: -28,
      rotation: -6,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".asset-process", {
      x: 18,
      y: 24,
      rotation: -1,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".asset-texture", {
      y: -42,
      rotation: 2,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".asset-reject", {
      y: 34,
      rotation: -12,
      scrollTrigger: { trigger: ".asset-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.from(".system-scene > *", {
      y: 24,
      opacity: 0,
      stagger: 0.08,
      duration: 0.44,
      ease: "power3.out",
      immediateRender: false,
      scrollTrigger: { trigger: ".system-scene", start: "top 78%", once: true },
    });

    gsap.to(".command-card", {
      y: -34,
      scrollTrigger: { trigger: ".system-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".file-card", {
      y: 28,
      rotation: 1,
      scrollTrigger: { trigger: ".system-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".poster-pill.pill-one", {
      y: -44,
      rotation: -3,
      scrollTrigger: { trigger: ".poster-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".poster-pill.pill-two", {
      y: 36,
      rotation: 5,
      scrollTrigger: { trigger: ".poster-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.from(".mode-card", {
      y: 42,
      opacity: 0,
      stagger: 0.1,
      duration: 0.58,
      ease: "power3.out",
      immediateRender: false,
      scrollTrigger: { trigger: ".mode-gallery", start: "top 76%", once: true },
    });

    gsap.to(".mode-minimal", {
      y: -60,
      rotation: -7,
      scrollTrigger: { trigger: ".mode-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".mode-soft", {
      y: 46,
      rotation: 7,
      scrollTrigger: { trigger: ".mode-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".mode-glass", {
      x: -34,
      y: -36,
      rotation: -1,
      scrollTrigger: { trigger: ".mode-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".mode-brutal", {
      x: 28,
      y: 42,
      rotation: 2,
      scrollTrigger: { trigger: ".mode-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".mode-gallery", {
      xPercent: -4,
      scrollTrigger: { trigger: ".mode-section", start: "top center", end: "bottom top", scrub: true },
    });

    gsap.to(".print-stack figure", {
      y: -54,
      rotation: 1,
      scrollTrigger: { trigger: ".capability-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".capability-card:nth-child(odd)", {
      y: -20,
      scrollTrigger: { trigger: ".capability-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".capability-card:nth-child(even)", {
      y: 16,
      scrollTrigger: { trigger: ".capability-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    if (window.matchMedia("(min-width: 721px)").matches) {
      ScrollTrigger.create({
        trigger: ".change-section",
        start: "top top",
        end: "bottom bottom",
        pin: ".change-layout",
        anticipatePin: 1,
      });

      gsap.to(".ledger article", {
        x: (index) => (index % 2 === 0 ? -20 : 20),
        scrollTrigger: { trigger: ".change-section", start: "top top", end: "bottom bottom", scrub: true },
      });
    }

    gsap.to(".demo-wide img", {
      yPercent: -8,
      scrollTrigger: { trigger: ".demo-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".demo-card:not(.demo-wide) img", {
      yPercent: -5,
      stagger: 0.05,
      scrollTrigger: { trigger: ".demo-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".still-life img", {
      y: -28,
      rotation: -2,
      scrollTrigger: { trigger: ".install-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".leaf", {
      y: -18,
      stagger: 0.05,
      scrollTrigger: { trigger: ".install-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    window.setTimeout(showAll, 3200);
  });
};

const initSite = () => {
  initCopyButtons();
  initMotion();
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
