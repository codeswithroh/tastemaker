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

  initModeCarousel();
};

// The mode carousel is the one place on this site that reaches for anime.js
// instead of GSAP — a deliberate, scoped choice (see
// references/animation-guidelines.md's anime.js section in the skill itself):
// the spring-based release feel on hover/press reads as more tactile than an
// eased GSAP tween for something the user's cursor is directly acting on.
// Everything else on this page stays on GSAP.
function initModeCarousel() {
  const track = document.getElementById("modeCarousel");
  if (!track) return;

  const cards = Array.from(track.querySelectorAll(".mode-card"));
  const arrows = document.querySelectorAll(".carousel-arrow");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Safety net, same discipline as the GSAP fallback above: if anime.js
  // failed to load (CDN blocked/slow), the carousel must still be fully
  // usable — native overflow-x scroll-snap and the plain CSS tilt state
  // don't depend on JS at all. Just wire the arrow buttons to a native
  // smooth scroll and stop; never leave a card stuck in a JS-only hidden
  // state if the library that was supposed to reveal it never arrived.
  if (!window.anime) {
    arrows.forEach((arrow) => {
      arrow.addEventListener("click", () => {
        const dir = Number(arrow.dataset.dir);
        track.scrollBy({ left: dir * (cards[0]?.offsetWidth ?? 280) * 1.2, behavior: "smooth" });
      });
    });
    return;
  }

  const scope = anime.createScope({
    mediaQueries: { reduce: "(prefers-reduced-motion: reduce)" },
  }).add((self) => {
    const reduce = self.matches.reduce;

    // Fan-in entrance: cards start flat and slightly small, then settle into
    // their resting --tilt rotation with a stagger, once the carousel first
    // scrolls into view. Runs once; a card that's already been fanned out
    // never resets on re-scroll.
    if (!reduce) {
      cards.forEach((card) => {
        card.style.transform = "rotate(0deg) scale(0.92)";
        card.style.opacity = "0";
      });
    }

    let fanned = false;
    const fanIn = () => {
      if (fanned) return;
      fanned = true;
      if (reduce) {
        cards.forEach((card) => { card.style.opacity = "1"; card.style.transform = ""; });
        return;
      }
      anime.animate(cards, {
        opacity: [0, 1],
        rotate: (el) => [0, el.style.getPropertyValue("--tilt") || "0deg"],
        scale: [0.92, 1],
        duration: 620,
        delay: anime.stagger(90),
        ease: "outQuad",
      });
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => { if (entry.isIntersecting) fanIn(); });
    }, { threshold: 0.3 });
    observer.observe(track);

    // Safety net matching the GSAP one above: force the resting state after
    // a timeout so a stalled tab or slow observer never leaves cards parked
    // invisible.
    window.setTimeout(() => {
      if (!fanned) fanIn();
    }, 3000);

    // Hover/focus: straighten, lift, and scale up with a springy release —
    // this is the one interaction on the page that's genuinely a physical,
    // user-initiated action (a cursor landing on a card), which is exactly
    // the case animation-guidelines.md scopes spring motion to.
    cards.forEach((card) => {
      const tilt = card.style.getPropertyValue("--tilt") || "0deg";
      const settle = () => {
        anime.animate(card, {
          rotate: 0,
          translateY: -14,
          scale: 1.06,
          duration: reduce ? 1 : 260,
          ease: reduce ? "linear" : createSpringEase(),
        });
        card.style.zIndex = "2";
      };
      const release = () => {
        anime.animate(card, {
          rotate: tilt,
          translateY: 0,
          scale: 1,
          duration: reduce ? 1 : 320,
          ease: reduce ? "linear" : createSpringEase(),
        });
        card.style.zIndex = "";
      };
      card.addEventListener("mouseenter", settle);
      card.addEventListener("mouseleave", release);
      card.addEventListener("focusin", settle);
      card.addEventListener("focusout", release);
    });

    // Arrow nav: glide the track by one card-width, eased through anime.js
    // rather than a native instant jump, for the same "cool, considered
    // motion" the carousel's whole point is to demonstrate.
    arrows.forEach((arrow) => {
      arrow.addEventListener("click", () => {
        const dir = Number(arrow.dataset.dir);
        const distance = (cards[0]?.offsetWidth ?? 280) * 1.2;
        const target = Math.max(
          0,
          Math.min(track.scrollWidth - track.clientWidth, track.scrollLeft + dir * distance)
        );
        anime.animate(track, {
          scrollLeft: target,
          duration: reduce ? 1 : 480,
          ease: reduce ? "linear" : "inOutQuad",
        });
      });
    });
  });

  function createSpringEase() {
    return anime.createSpring({ mass: 1, stiffness: 220, damping: 18 });
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initSite, { once: true });
} else {
  initSite();
}
