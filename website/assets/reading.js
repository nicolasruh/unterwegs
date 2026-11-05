"use strict";

const readingArea = document.getElementById("inhalt");

if (readingArea) {
  let idleTimer;

  function highlightReadingArea() {
    readingArea.classList.add("reading-active");
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      readingArea.classList.remove("reading-active");
    }, 500);
  }

  window.addEventListener("scroll", highlightReadingArea, { passive: true });
  window.addEventListener("pageshow", highlightReadingArea);
  highlightReadingArea();
}
