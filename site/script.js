const showAll = () => {
  document.querySelectorAll("[data-reveal], [data-reveal-group] > *, .site-header, .hero-copy > *, .art-stage > *").forEach((el) => {
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
        window.setTimeout(() => { if (label) label.textContent = "Copy"; }, 1600);
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
      .from(".hero-copy .context-line", { y: 12, opacity: 0, duration: 0.28 }, "-=0.04")
      .from(".hero h1", { y: 26, opacity: 0, duration: 0.54 }, "-=0.08")
      .from(".hero-lede, .hero-actions", { y: 16, opacity: 0, stagger: 0.08, duration: 0.36 }, "-=0.24")
      .from(".hero-art-main", { y: 30, rotation: -2, opacity: 0, duration: 0.64 }, "-=0.34")
      .from(".canvas-ribbon", { y: 20, opacity: 0, stagger: 0.08, duration: 0.46 }, "-=0.4")
      .from(".hero-art-proof, .palette-stack, .studio-note", { y: 18, opacity: 0, stagger: 0.08, duration: 0.4 }, "-=0.22");

    gsap.to(".ribbon-one", {
      yPercent: -8,
      rotation: -12,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });
    gsap.to(".ribbon-two", {
      yPercent: 10,
      rotation: 12,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });
    gsap.to(".hero-art-proof", {
      yPercent: -14,
      rotation: -1,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: 0.38,
        ease: "power3.out",
        scrollTrigger: { trigger: element, start: "top 86%", once: true },
      });
    });

    gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
      gsap.from(group.children, {
        y: 20,
        opacity: 0,
        stagger: 0.08,
        duration: 0.42,
        ease: "power3.out",
        scrollTrigger: { trigger: group, start: "top 82%", once: true },
      });
    });

    const loom = gsap.timeline({
      defaults: { ease: "none" },
      scrollTrigger: {
        trigger: ".motion-section",
        start: "top top",
        end: "bottom bottom",
        scrub: true,
        pin: ".motion-pin",
        anticipatePin: 1,
      },
    });

    loom
      .fromTo(".loom-line", { scaleX: 0 }, { scaleX: 1 }, 0)
      .fromTo(".card-a", { x: -36, opacity: 0 }, { x: 0, opacity: 1 }, 0.02)
      .fromTo(".card-b", { y: -42, opacity: 0 }, { y: 0, opacity: 1 }, 0.18)
      .fromTo(".card-c", { x: -24, y: 32, opacity: 0 }, { x: 0, y: 0, opacity: 1 }, 0.34)
      .fromTo(".loom-output", { x: 64, opacity: 0 }, { x: 0, opacity: 1 }, 0.5)
      .to(".loom-output img", { yPercent: -8 }, 0.62);

    gsap.to(".gallery-piece img", {
      yPercent: -6,
      ease: "none",
      scrollTrigger: { trigger: ".proof-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".memory-card.one", {
      y: -24,
      scrollTrigger: { trigger: ".memory-section", start: "top bottom", end: "bottom top", scrub: true },
    });
    gsap.to(".memory-card.two", {
      y: 28,
      scrollTrigger: { trigger: ".memory-section", start: "top bottom", end: "bottom top", scrub: true },
    });
    gsap.to(".memory-card.three", {
      y: -16,
      scrollTrigger: { trigger: ".memory-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    window.setTimeout(showAll, 3000);
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
