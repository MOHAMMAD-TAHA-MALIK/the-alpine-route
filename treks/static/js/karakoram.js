/**
 * Karakoram panorama — progressive enhancement only.
 * Every peak label, leader line and tooltip already works from :hover /
 * :focus-visible in karakoram.css with zero JS. This file adds two things
 * on top, and both fail safe if it never runs:
 *   1. A subtle parallax drift on the background photo while it's on screen.
 *   2. A tap-to-toggle fallback so touch users (no real ":hover") can open
 *      a peak's tooltip without needing a keyboard.
 */
(function () {
  "use strict";

  var frame = document.querySelector(".panorama__frame");
  var photo = document.querySelector(".panorama__photo");
  if (!frame || !photo) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------- parallax ---------------------------- */
  if (!reduceMotion && "IntersectionObserver" in window) {
    var ticking = false;
    var visible = false;

    var applyParallax = function () {
      ticking = false;
      if (!visible) return;
      var rect = frame.getBoundingClientRect();
      var vh = window.innerHeight || document.documentElement.clientHeight;
      // -1 (frame fully below viewport) .. 1 (frame fully above), 0 = centered
      var progress = (rect.top + rect.height / 2 - vh / 2) / vh;
      var offset = Math.max(-24, Math.min(24, progress * -18)); // px, gentle & clamped
      photo.style.setProperty("--kk-parallax", offset.toFixed(1) + "px");
    };

    var onScroll = function () {
      if (!ticking) {
        ticking = true;
        window.requestAnimationFrame(applyParallax);
      }
    };

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          visible = entry.isIntersecting;
        });
        if (visible) {
          window.addEventListener("scroll", onScroll, { passive: true });
          applyParallax();
        } else {
          window.removeEventListener("scroll", onScroll);
        }
      },
      { threshold: 0 }
    );
    io.observe(frame);
  }

  /* ------------------------ tap-to-toggle tooltip ------------------------ */
  var peakButtons = document.querySelectorAll(".peak__btn");

  var closeAll = function (except) {
    peakButtons.forEach(function (btn) {
      if (btn !== except) btn.classList.remove("is-active");
    });
  };

  peakButtons.forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      var willOpen = !btn.classList.contains("is-active");
      closeAll();
      if (willOpen) btn.classList.add("is-active");
      event.stopPropagation();
    });
  });

  document.addEventListener("click", function () {
    closeAll();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeAll();
  });
})();
