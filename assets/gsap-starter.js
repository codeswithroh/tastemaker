/*
  Tastemaker GSAP starter — the default motion system for generated sites.

  Requires GSAP + ScrollTrigger to already be loaded (see
  references/tech-stack-guides.md for the CDN <script> tags or npm install
  per stack). This file just wires up the same [data-reveal] /
  [data-reveal-group] convention used by the plain-CSS fallback
  (assets/reveal.css + reveal.js), so upgrading a project from the
  dependency-free fallback to GSAP doesn't require touching any markup.

  Usage: include after GSAP/ScrollTrigger, then before </body>:
    <script src="gsap-starter.js"></script>
    <script>
      TastemakerMotion.init({
        duration: 0.22,       // seconds — match .tastemaker/style-lock.md's Motion section
        distance: 16,         // px
        ease: "power2.out",
        staggerStep: 0.06,    // seconds between staggered children
      });
    </script>
*/
(function (global) {
  "use strict";

  function init(options) {
    var opts = Object.assign(
      { duration: 0.22, distance: 16, ease: "power2.out", staggerStep: 0.06 },
      options || {}
    );

    if (typeof gsap === "undefined") {
      console.warn("TastemakerMotion.init: GSAP is not loaded. Include gsap.min.js (and ScrollTrigger) before this script.");
      return;
    }
    if (typeof ScrollTrigger === "undefined") {
      console.warn("TastemakerMotion.init: ScrollTrigger is not loaded. Motion will fall back to entrance-only (no scroll-triggering).");
    } else {
      gsap.registerPlugin(ScrollTrigger);
    }

    // gsap.matchMedia is the idiomatic way to branch on prefers-reduced-motion —
    // the "reduce" context runs a near-instant, non-animated version instead of
    // skipping motion setup entirely (so layout/opacity end state is still correct).
    var mm = gsap.matchMedia();

    mm.add(
      {
        motionOK: "(prefers-reduced-motion: no-preference)",
        reduceMotion: "(prefers-reduced-motion: reduce)",
      },
      function (context) {
        var reduce = context.conditions.reduceMotion;
        var duration = reduce ? 0.01 : opts.duration;
        var distance = reduce ? 0 : opts.distance;

        document.querySelectorAll("[data-reveal]").forEach(function (el) {
          var isGroup = el.hasAttribute("data-reveal-group");
          var targets = isGroup ? el.children : el;

          gsap.set(targets, { opacity: 0, y: distance });

          var tween = {
            opacity: 1,
            y: 0,
            duration: duration,
            ease: opts.ease,
          };
          if (isGroup) {
            tween.stagger = reduce ? 0 : opts.staggerStep;
          }

          if (typeof ScrollTrigger !== "undefined") {
            gsap.to(targets, Object.assign({}, tween, {
              scrollTrigger: {
                trigger: el,
                start: "top 85%",
                once: true,
              },
            }));
          } else {
            gsap.to(targets, tween);
          }
        });
      }
    );
  }

  global.TastemakerMotion = { init: init };
})(typeof window !== "undefined" ? window : this);
