/*
  Tastemaker scroll-reveal starter (vanilla, no dependencies).
  Pairs with reveal.css. Elements with [data-reveal] fade/rise in once they
  enter the viewport; children of [data-reveal-group] additionally stagger.
*/
(function () {
  "use strict";

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var stepVar = getComputedStyle(document.documentElement)
    .getPropertyValue("--reveal-stagger-step")
    .trim();
  var staggerStepMs = parseFloat(stepVar) || 60;

  function revealGroup(el) {
    if (prefersReduced) {
      el.classList.add("is-revealed");
      return;
    }
    Array.prototype.forEach.call(el.children, function (child, i) {
      child.style.transitionDelay = i * staggerStepMs + "ms";
    });
    el.classList.add("is-revealed");
  }

  var targets = document.querySelectorAll("[data-reveal]");
  if (!targets.length) return;

  if (prefersReduced || !("IntersectionObserver" in window)) {
    targets.forEach(function (el) {
      el.classList.add("is-revealed");
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (el.hasAttribute("data-reveal-group")) {
          revealGroup(el);
        } else {
          el.classList.add("is-revealed");
        }
        obs.unobserve(el);
      });
    },
    { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
  );

  targets.forEach(function (el) {
    observer.observe(el);
  });
})();
