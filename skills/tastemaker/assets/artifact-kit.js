// Tastemaker artifact kit motion helpers. Requires GSAP + ScrollTrigger.
window.TastemakerArtifacts = {
  init(options = {}) {
    if (!window.gsap || !window.ScrollTrigger) return;

    const {
      board = ".tmk-artifact-board",
      modes = ".tmk-mode-runway",
      ledger = ".tmk-ledger-card",
      reduced = "(prefers-reduced-motion: reduce)",
    } = options;

    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia();

    mm.add(`not all and ${reduced}`, () => {
      gsap.utils.toArray(`${board} .tmk-artifact-side-a`).forEach((el) => {
        gsap.to(el, {
          yPercent: -14,
          rotation: 0,
          scrollTrigger: { trigger: el.closest(board), start: "top bottom", end: "bottom top", scrub: true },
        });
      });

      gsap.utils.toArray(`${board} .tmk-artifact-side-b`).forEach((el) => {
        gsap.to(el, {
          yPercent: -8,
          rotation: -8,
          scrollTrigger: { trigger: el.closest(board), start: "top bottom", end: "bottom top", scrub: true },
        });
      });

      gsap.utils.toArray(`${modes} .tmk-mode-card`).forEach((el, index) => {
        gsap.to(el, {
          y: index % 2 === 0 ? -56 : 42,
          rotation: index % 2 === 0 ? -4 : 5,
          scrollTrigger: { trigger: el.closest(modes), start: "top bottom", end: "bottom top", scrub: true },
        });
      });

      gsap.to(ledger, {
        x: (index) => (index % 2 === 0 ? -18 : 18),
        scrollTrigger: { trigger: ledger, start: "top bottom", end: "bottom top", scrub: true },
      });
    });
  },
};
