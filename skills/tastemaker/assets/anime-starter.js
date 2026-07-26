/*
  Tastemaker anime.js starter — scoped alternative to gsap-starter.js.

  GSAP + ScrollTrigger remains the default motion engine for every project
  (see references/animation-guidelines.md). This starter exists for the case
  where anime.js has a real, verified advantage: a page that needs both
  scroll-reveals AND SVG motion-path/shape-morphing for a constructed logo
  mark or hand-built illustration. anime.js ships that SVG toolset in the
  same bundle as its scroll engine, which comes out meaningfully smaller
  (gzipped) than GSAP core + ScrollTrigger + MorphSVGPlugin + DrawSVGPlugin —
  see the measured comparison in animation-guidelines.md. Bundle size alone
  does NOT justify anime.js for simple reveals with no SVG need — that case
  was checked and doesn't hold up over a plain CDN <script> tag.

  Requires anime.js v4 to already be loaded (CDN <script> tag or npm install
  per references/tech-stack-guides.md). Wires up the same [data-reveal] /
  [data-reveal-group] convention gsap-starter.js and the plain-CSS fallback
  use, so a project can swap engines without touching markup.

  Usage: include after anime.js, then before </body>:
    <script src="anime-starter.js"></script>
    <script>
      TastemakerAnimeMotion.init({
        duration: 220,        // ms — note anime.js uses milliseconds, not seconds like GSAP
        distance: 16,          // px
        ease: "outQuad",       // note anime.js ease names differ from GSAP's (e.g. "power2.out")
        staggerStep: 60,       // ms between staggered children
      });
    </script>

  A real difference from GSAP's ScrollTrigger, confirmed by hands-on testing:
  anime.js's ScrollObserver only fires onEnter on a scroll-crossing transition
  — it does not check whether a target is already in view at creation time.
  Left alone, an above-the-fold [data-reveal] element (a hero's own reveal
  group) would sit invisible until the user's first scroll. This starter
  calls the observer's own handleScroll() once right after wiring each one,
  forcing that initial check — the fix, not a workaround to route around.
*/
(function (global) {
  "use strict";

  function init(options) {
    var opts = Object.assign(
      { duration: 220, distance: 16, ease: "outQuad", staggerStep: 60 },
      options || {}
    );

    if (typeof anime === "undefined") {
      console.warn("TastemakerAnimeMotion.init: anime.js is not loaded. Include anime.min.js before this script.");
      return;
    }

    var observers = [];

    // anime.js's createScope({ mediaQueries }) is the direct equivalent of
    // gsap.matchMedia() — the same idiomatic branch on prefers-reduced-motion,
    // just anime.js's own API shape.
    var scope = anime.createScope({
      mediaQueries: {
        reduce: "(prefers-reduced-motion: reduce)",
      },
    }).add(function (self) {
      var reduce = self.matches.reduce;
      var duration = reduce ? 1 : opts.duration;
      var distance = reduce ? 0 : opts.distance;

      document.querySelectorAll("[data-reveal]").forEach(function (el) {
        var isGroup = el.hasAttribute("data-reveal-group");
        var targets = isGroup ? el.children : el;

        var observer = anime.onScroll({ target: el });

        anime.animate(targets, {
          opacity: [0, 1],
          translateY: [distance, 0],
          duration: duration,
          ease: opts.ease,
          delay: isGroup ? anime.stagger(reduce ? 0 : opts.staggerStep) : 0,
          autoplay: observer,
        });

        observers.push(observer);
      });

      observers.forEach(function (o) {
        o.handleScroll();
      });
    });

    return scope;
  }

  global.TastemakerAnimeMotion = { init: init };
})(typeof window !== "undefined" ? window : this);
