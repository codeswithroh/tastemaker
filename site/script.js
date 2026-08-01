const setVisible = (selector) => {
  document.querySelectorAll(selector).forEach((el) => {
    el.style.opacity = "1";
    el.style.transform = "none";
    el.style.clipPath = "none";
  });
};

const initCopyButtons = () => {
  document.querySelectorAll("[data-copy]").forEach((copyButton) => {
    copyButton.addEventListener("click", async () => {
      const value = copyButton.dataset.copy;
      const label = copyButton.querySelector("span");

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

        if (label) label.textContent = "Copied";
        window.setTimeout(() => { if (label) label.textContent = "Copy"; }, 1800);
      } catch {
        if (label) label.textContent = "Select";
      }
    });
  });
};

const initMotion = () => {
  const revealSelector = "[data-reveal], [data-reveal-group] > *";
  const heroRestingSelector = [
    ".site-header",
    ".hero-copy .context-line",
    ".hero-copy h1",
    ".hero-lede",
    ".hero-actions",
    ".command-pill",
    ".capability-console",
    ".console-card",
  ].join(", ");

  if (!window.gsap || !window.ScrollTrigger) {
    setVisible(`${heroRestingSelector}, ${revealSelector}`);
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".site-header", { y: -16, opacity: 0, duration: 0.35 })
      .from(".hero-copy .context-line", { y: 12, opacity: 0, duration: 0.32 }, "-=0.06")
      .from(".hero-copy h1", { y: 26, opacity: 0, duration: 0.58 }, "-=0.12")
      .from(".hero-lede, .hero-actions, .command-pill", { y: 16, opacity: 0, stagger: 0.07, duration: 0.38 }, "-=0.28")
      .from(".capability-console", { y: 28, opacity: 0, duration: 0.62 }, "-=0.44")
      .from(".console-card", { y: 14, opacity: 0, stagger: 0.06, duration: 0.32 }, "-=0.26");

    window.setTimeout(() => {
      gsap.set(heroRestingSelector, { opacity: 1, y: 0, clipPath: "none" });
    }, 2600);

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: 0.42,
        ease: "power3.out",
        scrollTrigger: { trigger: element, start: "top 88%", once: true },
      });
    });

    gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
      gsap.from(group.children, {
        y: 18,
        opacity: 0,
        stagger: 0.07,
        duration: 0.42,
        ease: "power3.out",
        scrollTrigger: { trigger: group, start: "top 86%", once: true },
      });
    });

    gsap.to(".scan-card", {
      borderColor: "rgba(190, 133, 206, .72)",
      boxShadow: "0 0 0 1px rgba(190, 133, 206, .26)",
      duration: 1.6,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      stagger: 0.16,
    });

    gsap.to(".shot-card img", {
      yPercent: -5,
      ease: "none",
      scrollTrigger: { trigger: ".shot-card", start: "top bottom", end: "bottom top", scrub: true },
    });

    window.setTimeout(() => {
      setVisible(revealSelector);
    }, 4200);
  });
};

const initCardHover = () => {
  const cards = document.querySelectorAll(".pipeline-card, .mode-card, .reference-card, .scan-card");

  cards.forEach((card) => {
    card.addEventListener("mouseenter", () => card.classList.add("is-hovered"));
    card.addEventListener("mouseleave", () => card.classList.remove("is-hovered"));
    card.addEventListener("focusin", () => card.classList.add("is-hovered"));
    card.addEventListener("focusout", () => card.classList.remove("is-hovered"));
  });
};

const initSite = () => {
  initCopyButtons();
  initMotion();
  initCardHover();
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
