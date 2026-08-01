const showAll = () => {
  document.querySelectorAll("[data-reveal], [data-reveal-group] > *, .hero-copy > *, .hero-collage > *").forEach((el) => {
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
      .from(".release-pill", { y: 12, opacity: 0, duration: 0.28 }, "-=0.05")
      .from(".hero h1", { y: 24, opacity: 0, duration: 0.52 }, "-=0.06")
      .from(".hero-lede, .command-bar, .hero-actions", { y: 16, opacity: 0, stagger: 0.07, duration: 0.36 }, "-=0.24")
      .from(".card-main", { y: 26, rotation: -1.5, opacity: 0, duration: 0.62 }, "-=0.34")
      .from(".card-mode, .card-site, .paper-note, .swatch-rail", { y: 20, opacity: 0, stagger: 0.07, duration: 0.42 }, "-=0.28");

    gsap.to(".card-mode", {
      yPercent: -12,
      rotation: -7,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });
    gsap.to(".card-site", {
      yPercent: -16,
      rotation: 0,
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });
    gsap.to(".swatch-rail", {
      yPercent: 12,
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
        y: 22,
        opacity: 0,
        stagger: 0.07,
        duration: 0.42,
        ease: "power3.out",
        scrollTrigger: { trigger: group, start: "top 82%", once: true },
      });
    });

    gsap.to(".escape-frame figure", {
      y: -42,
      rotation: -4,
      scrollTrigger: { trigger: ".escape-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".skill-polaroid", {
      y: -60,
      rotation: -2,
      scrollTrigger: { trigger: ".skills-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    if (window.matchMedia("(min-width: 681px)").matches) {
      ScrollTrigger.create({
        trigger: ".v2-section",
        start: "top top",
        end: "bottom bottom",
        pin: ".v2-layout",
        anticipatePin: 1,
      });

      gsap.to(".change-list article", {
        x: (index) => index % 2 === 0 ? -18 : 18,
        scrollTrigger: { trigger: ".v2-section", start: "top top", end: "bottom bottom", scrub: true },
      });
    }

    gsap.to(".demo-card.large img", {
      yPercent: -8,
      scrollTrigger: { trigger: ".demo-section", start: "top bottom", end: "bottom top", scrub: true },
    });

    gsap.to(".memory-stack span:nth-child(1)", {
      y: -28,
      scrollTrigger: { trigger: ".memory-section", start: "top bottom", end: "bottom top", scrub: true },
    });
    gsap.to(".memory-stack span:nth-child(2)", {
      y: 26,
      scrollTrigger: { trigger: ".memory-section", start: "top bottom", end: "bottom top", scrub: true },
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
