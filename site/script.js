const initSite = () => {
  document.querySelectorAll("[data-copy]").forEach((copyButton) => {
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
  });

  // Safety net: if GSAP never loads (CDN blocked/slow), never leave the page
  // permanently hidden behind a .from()-authored start state that nothing
  // resolved. Every other motion page in this project carries this same
  // fallback (see site/after.html, site/demo.html) — a page whose CDN script
  // fails should degrade to the plain HTML, not a blank hero.
  if (!window.gsap || !window.ScrollTrigger) {
    document.querySelectorAll("[data-reveal]").forEach((el) => { el.style.opacity = "1"; });
    return;
  }
  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const heroTargets = ".site-header, .hero-copy .kicker, .hero-copy h1, .hero-copy > p, .hero-copy .button-row, .hero-showcase, .hero-showcase .output-preview";

    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".site-header", { y: -16, opacity: 0, duration: .35 })
      .from(".hero-copy .kicker", { y: 12, opacity: 0, duration: .35 }, "-=.05")
      .from(".hero-copy h1", { y: 22, opacity: 0, duration: .6 }, "-=.12")
      .from(".hero-copy > p, .hero-copy .button-row", { y: 14, opacity: 0, stagger: .08, duration: .4 }, "-=.3")
      .from(".hero-showcase", { y: 24, opacity: 0, duration: .62 }, "-=.48")
      .from(".hero-showcase .output-preview", { clipPath: "inset(0 100% 0 0)", duration: .72, ease: "power3.inOut" }, "-=.28");

    // Safety net: a backgrounded tab (browsers throttle rAF there), a slow
    // CDN, or any other stall can leave a .from() timeline parked at its
    // start state indefinitely. Force the resting state after a timeout so
    // the hero is never permanently invisible, same pattern as every other
    // motion page here.
    window.setTimeout(() => {
      gsap.set(heroTargets, { opacity: 1, y: 0, clipPath: "inset(0 0% 0 0)" });
    }, 2600);

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: .42,
        ease: "power3.out",
        scrollTrigger: { trigger: element, start: "top 88%", once: true },
      });
    });

    window.setTimeout(() => {
      document.querySelectorAll("[data-reveal]").forEach((el) => {
        if (parseFloat(getComputedStyle(el).opacity) < 0.05) gsap.set(el, { opacity: 1, y: 0 });
      });
    }, 4000);

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

  initModeShowcase();
};

// The mode showcase grid is the one place on this site that reaches for
// anime.js instead of GSAP — a deliberate, scoped choice (see
// references/animation-guidelines.md's anime.js section in the skill
// itself): the spring-based release feel on hover reads as more tactile
// than an eased GSAP tween for something the user's cursor is directly
// acting on. Everything else on this page stays on GSAP. The grid itself
// (data-reveal) still fades in via the same GSAP pass as every other
// section — this only adds the staggered entrance and hover lift on top.
function initModeShowcase() {
  const grid = document.getElementById("modeGrid");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".mode-card"));

  // Safety net, same discipline as the GSAP fallback above: if anime.js
  // failed to load (CDN blocked/slow), the cards are plain, unanimated,
  // fully visible CSS by default — there's nothing else to wire up, and
  // nothing is ever left stuck invisible.
  if (!window.anime) return;

  anime.createScope({
    mediaQueries: { reduce: "(prefers-reduced-motion: reduce)" },
  }).add((self) => {
    const reduce = self.matches.reduce;

    if (!reduce) {
      cards.forEach((card) => { card.style.opacity = "0"; card.style.transform = "translateY(16px) scale(0.97)"; });
    }

    let entered = false;
    const enter = () => {
      if (entered) return;
      entered = true;
      if (reduce) {
        cards.forEach((card) => { card.style.opacity = "1"; card.style.transform = ""; });
        return;
      }
      anime.animate(cards, {
        opacity: [0, 1],
        translateY: [16, 0],
        scale: [0.97, 1],
        duration: 520,
        delay: anime.stagger(90),
        ease: "outQuad",
      });
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => { if (entry.isIntersecting) enter(); });
    }, { threshold: 0.2 });
    observer.observe(grid);

    // Safety net matching the GSAP one above: force the resting state after
    // a timeout so a stalled tab or slow observer never leaves cards parked
    // invisible.
    window.setTimeout(() => { if (!entered) enter(); }, 3000);

    // Hover/focus: a small, springy lift — the one interaction here that's
    // genuinely a physical, user-initiated action (a cursor landing on a
    // card), which is exactly the case animation-guidelines.md scopes
    // spring motion to. No rotation involved; these cards never tilt.
    const spring = reduce ? "linear" : anime.createSpring({ mass: 1, stiffness: 240, damping: 20 });
    cards.forEach((card) => {
      const lift = () => anime.animate(card, { translateY: -6, duration: reduce ? 1 : 220, ease: spring });
      const drop = () => anime.animate(card, { translateY: 0, duration: reduce ? 1 : 260, ease: spring });
      card.addEventListener("mouseenter", lift);
      card.addEventListener("mouseleave", drop);
      card.addEventListener("focusin", lift);
      card.addEventListener("focusout", drop);
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
