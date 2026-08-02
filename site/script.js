const revealSelector = "[data-reveal], [data-reveal-group] > *";

const showAll = () => {
  document.documentElement.classList.remove("reveal-armed");
  document.querySelectorAll(revealSelector).forEach((el) => {
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

// Watchdog: reveal animations are a nice-to-have, never a content gate. If a
// ScrollTrigger fails to fire for any reason (fast scroll, a resize during
// load, a timing edge case), force-reveal anything that's already on
// screen (or close to it) rather than leave it invisible forever.
const startRevealWatchdog = () => {
  const check = () => {
    const cutoff = window.innerHeight * 1.4;
    document.querySelectorAll(revealSelector).forEach((el) => {
      if (getComputedStyle(el).opacity !== "0") return;
      const rect = el.getBoundingClientRect();
      if (rect.top < cutoff) {
        el.style.opacity = "1";
        el.style.transform = "none";
      }
    });
  };
  window.addEventListener("scroll", check, { passive: true });
  window.addEventListener("resize", check);
  check();
  window.setInterval(check, 1200);
};

// Ambient background: a slow, continuously drifting two-blob gradient mesh
// in the brand's teal/orchid, drawn on canvas. This is the honest version of
// "a looped video background" — real generative motion, not a stock clip,
// and it costs nothing to source or license. Draws one still frame and
// exits immediately under reduced motion.
const initHeroCanvas = () => {
  const canvas = document.getElementById("heroCanvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let w = 0;
  let h = 0;
  let dpr = Math.min(window.devicePixelRatio || 1, 2);

  const resize = () => {
    const rect = canvas.parentElement.getBoundingClientRect();
    w = rect.width;
    h = rect.height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const blobs = [
    { baseX: 0.18, baseY: 0.3, r: 0.42, color: "0, 130, 134", speed: 0.00018, phase: 0 },
    { baseX: 0.84, baseY: 0.78, r: 0.38, color: "190, 133, 206", speed: 0.00014, phase: 2 },
  ];

  const draw = (t) => {
    ctx.clearRect(0, 0, w, h);
    blobs.forEach((b) => {
      const x = (b.baseX + Math.sin(t * b.speed + b.phase) * 0.04) * w;
      const y = (b.baseY + Math.cos(t * b.speed * 0.8 + b.phase) * 0.04) * h;
      const r = b.r * Math.max(w, h);
      const grad = ctx.createRadialGradient(x, y, 0, x, y, r);
      grad.addColorStop(0, `rgba(${b.color}, 0.16)`);
      grad.addColorStop(1, `rgba(${b.color}, 0)`);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);
    });
  };

  resize();
  window.addEventListener("resize", resize);

  if (reduceMotion) {
    draw(0);
    return;
  }

  const loop = (t) => {
    draw(t);
    requestAnimationFrame(loop);
  };
  requestAnimationFrame(loop);
};

const initMotion = () => {
  if (!window.gsap || !window.ScrollTrigger) {
    showAll();
    return;
  }

  gsap.registerPlugin(ScrollTrigger);
  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    // Arm the CSS-hidden starting state only now that GSAP is definitely
    // going to animate these elements in.
    document.documentElement.classList.add("reveal-armed");

    gsap.timeline({ defaults: { ease: "power3.out" } })
      .from(".site-header", { y: -14, opacity: 0, duration: 0.32 })
      .from(".hero-copy > *", { y: 20, opacity: 0, stagger: 0.08, duration: 0.42 }, "-=0.1")
      .from(".hero-visual", { y: 24, opacity: 0, duration: 0.5 }, "-=0.28")
      .from(".compare-tag", { opacity: 0, y: 8, stagger: 0.08, duration: 0.3 }, "-=0.15");

    // The continuous wipe loop that stands in for a looped video background:
    // sweeps the before/after divider back and forth so the comparison is
    // visible without a click, built entirely from the two real screenshots.
    gsap.to(".compare-reveal", {
      "--wipe": "82%",
      duration: 3.8,
      ease: "sine.inOut",
      yoyo: true,
      repeat: -1,
      delay: 1,
    });

    gsap.utils.toArray("[data-reveal]").forEach((element) => {
      if (element.closest(".hero")) return;
      gsap.from(element, {
        y: 18,
        opacity: 0,
        duration: 0.42,
        ease: "power3.out",
        immediateRender: false,
        scrollTrigger: { trigger: element, start: "top 90%", once: true },
      });
    });

    gsap.utils.toArray("[data-reveal-group]").forEach((group) => {
      gsap.from(group.children, {
        y: 20,
        opacity: 0,
        stagger: 0.06,
        duration: 0.42,
        ease: "power3.out",
        immediateRender: false,
        scrollTrigger: { trigger: group, start: "top 88%", once: true },
      });
    });

    gsap.from(".proof-wall-links a", {
      y: 14,
      opacity: 0,
      stagger: 0.05,
      duration: 0.32,
      ease: "power3.out",
      immediateRender: false,
      scrollTrigger: { trigger: ".proof-wall", start: "top 88%", once: true },
    });

    startRevealWatchdog();
  });

  mm.add("(prefers-reduced-motion: reduce)", showAll);
};

document.addEventListener("DOMContentLoaded", () => {
  initCopyButtons();
  initHeroCanvas();
  initMotion();
});
