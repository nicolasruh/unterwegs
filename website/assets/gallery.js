"use strict";

const galleryDialog = document.querySelector(".gallery-dialog");
const galleryTitle = document.getElementById("gallery-title");
const galleryPicture = galleryDialog.querySelector(".gallery-picture");
const galleryCount = galleryDialog.querySelector(".gallery-count");
const galleryCredit = galleryDialog.querySelector(".gallery-credit");
const galleryStatus = galleryDialog.querySelector(".gallery-status");
const galleryPlay = galleryDialog.querySelector(".gallery-play");
const galleryPrevious = galleryDialog.querySelector(".gallery-previous");
const galleryNext = galleryDialog.querySelector(".gallery-next");
const galleryDots = galleryDialog.querySelector(".gallery-dots");
const galleryView = galleryDialog.querySelector(".gallery-view");
const galleryFullscreen = galleryDialog.querySelector(".gallery-fullscreen");

let galleryData;
let currentGallery;
let currentYear;
let currentIndex = 0;
let requestId = 0;
let autoplay = false;
let autoplayTimer;
let openingLink;

function positionCredit() {
  const image = galleryPicture.querySelector("img");
  if (!image) return;
  const width = galleryPicture.clientWidth;
  const height = galleryPicture.clientHeight;
  const scale = Math.min(width / image.naturalWidth, height / image.naturalHeight);
  const imageWidth = image.naturalWidth * scale;
  const imageHeight = image.naturalHeight * scale;
  galleryCredit.style.right = `${(width - imageWidth) / 2}px`;
  galleryCredit.style.bottom = `${(height - imageHeight) / 2}px`;
  galleryCredit.style.maxWidth = `${imageWidth}px`;
}

new ResizeObserver(positionCredit).observe(galleryPicture);

function labelControl(button, label) {
  button.setAttribute("aria-label", label);
  button.title = label;
}

function updateFullscreenControl() {
  const active = document.fullscreenElement === galleryView;
  galleryFullscreen.setAttribute("aria-pressed", String(active));
  galleryFullscreen.classList.toggle("is-fullscreen", active);
  labelControl(galleryFullscreen, active ? "Vollbild verlassen" : "Vollbild einschalten");
}

async function exitGalleryFullscreen() {
  if (document.fullscreenElement === galleryView) {
    await document.exitFullscreen();
  }
}

function reportFullscreenError(error) {
  console.error("Fehler beim Umschalten des Galerie-Vollbilds:", error);
  galleryStatus.textContent = "Vollbild konnte nicht umgeschaltet werden. Die Galerie bleibt im Overlay bedienbar.";
}

async function loadGalleryData() {
  if (galleryData) return galleryData;
  const response = await fetch("assets/bilder/galerien.json", { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Galeriedaten konnten nicht geladen werden: HTTP ${response.status}`);
  }
  const data = await response.json();
  for (const [year, gallery] of Object.entries(data)) {
    if (!/^\d{4}$/.test(year) || !gallery ||
        typeof gallery.place !== "string" || typeof gallery.credit !== "string" ||
        !Array.isArray(gallery.images) || gallery.images.length === 0 ||
        !gallery.images.every(file => typeof file === "string" &&
          /^[^/\\]+\.(jpe?g|png|webp)$/i.test(file))) {
      throw new Error(`Ungültige Galeriedaten für das Jahr ${year}.`);
    }
  }
  galleryData = data;
  return data;
}

function stopAutoplay() {
  autoplay = false;
  clearTimeout(autoplayTimer);
  galleryPlay.querySelector("span").textContent = "▶";
  labelControl(galleryPlay, "Diashow starten");
  galleryPlay.setAttribute("aria-pressed", "false");
  galleryCount.setAttribute("aria-live", "polite");
}

function scheduleNextImage() {
  clearTimeout(autoplayTimer);
  if (autoplay && galleryDialog.open && !document.hidden) {
    autoplayTimer = setTimeout(() => showImage(currentIndex + 1), 5000);
  }
}

function reportGalleryError(error, message) {
  console.error("Fehler in der Bildergalerie:", error);
  stopAutoplay();
  galleryStatus.textContent = message;
  galleryPicture.setAttribute("aria-busy", "false");
}

function showImage(index) {
  clearTimeout(autoplayTimer);
  currentIndex = (index + currentGallery.images.length) % currentGallery.images.length;
  const id = ++requestId;
  const number = currentIndex + 1;
  galleryCount.textContent = `Bild ${number} von ${currentGallery.images.length}`;
  for (const [dotIndex, dot] of [...galleryDots.children].entries()) {
    if (dotIndex === currentIndex) {
      dot.setAttribute("aria-current", "true");
      galleryDots.scrollLeft = dot.offsetLeft - galleryDots.offsetLeft -
        (galleryDots.clientWidth - dot.clientWidth) / 2;
    } else {
      dot.removeAttribute("aria-current");
    }
  }
  galleryStatus.textContent = "Bild wird geladen …";
  galleryPicture.setAttribute("aria-busy", "true");
  galleryPicture.replaceChildren();
  galleryCredit.hidden = true;

  const image = new Image();
  const place = currentGallery.place ? ` (${currentGallery.place})` : "";
  image.alt = `unterWEGs ${currentYear}${place}, Bild ${number}`;
  image.onload = () => {
    if (id !== requestId || !galleryDialog.open) return;
    galleryPicture.replaceChildren(image);
    galleryCredit.hidden = !currentGallery.credit;
    galleryPicture.setAttribute("aria-busy", "false");
    galleryStatus.textContent = "";
    positionCredit();
    scheduleNextImage();
  };
  image.onerror = () => {
    if (id !== requestId || !galleryDialog.open) return;
    reportGalleryError(new Error(`Bild nicht ladbar: ${image.src}`),
      "Dieses Bild konnte nicht geladen werden. Bitte weiterblättern oder die Galerie erneut öffnen.");
  };
  image.src = `assets/bilder/${currentYear}/${encodeURIComponent(currentGallery.images[currentIndex])}`;
}

async function openGallery(link) {
  stopAutoplay();
  currentGallery = null;
  currentYear = link.dataset.year;
  openingLink = link;
  galleryTitle.textContent = link.querySelector("h2").textContent;
  galleryPicture.replaceChildren();
  galleryCredit.hidden = true;
  galleryCount.textContent = "";
  galleryDots.replaceChildren();
  galleryCredit.textContent = "";
  galleryStatus.textContent = "Galerie wird geladen …";
  galleryPlay.disabled = true;
  galleryPrevious.disabled = true;
  galleryNext.disabled = true;
  galleryDialog.showModal();
  document.body.classList.add("gallery-is-open");
  const id = ++requestId;

  try {
    const data = await loadGalleryData();
    if (id !== requestId || !galleryDialog.open) return;
    const gallery = data[currentYear];
    if (!gallery) throw new Error(`Keine Galerie für ${currentYear} gefunden.`);
    currentGallery = gallery;
    galleryTitle.textContent = gallery.place ? `${currentYear} (${gallery.place})` : currentYear;
    galleryCredit.textContent = gallery.credit;
    const dots = gallery.images.map((file, index) => {
      const dot = document.createElement("button");
      dot.type = "button";
      dot.className = "gallery-dot";
      labelControl(dot, `Bild ${index + 1} anzeigen`);
      dot.addEventListener("click", () => {
        stopAutoplay();
        showImage(index);
      });
      return dot;
    });
    galleryDots.replaceChildren(...dots);
    const singleImage = gallery.images.length === 1;
    galleryPlay.disabled = singleImage;
    galleryPrevious.disabled = singleImage;
    galleryNext.disabled = singleImage;
    showImage(0);
  } catch (error) {
    if (id !== requestId || !galleryDialog.open) return;
    reportGalleryError(error, "Die Galerie konnte nicht geladen werden. Bitte schliessen und erneut versuchen.");
  }
}

function moveImage(direction) {
  if (!currentGallery) return;
  stopAutoplay();
  showImage(currentIndex + direction);
}

document.querySelectorAll(".gallery-open").forEach(link => {
  link.setAttribute("aria-haspopup", "dialog");
  link.addEventListener("click", event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    openGallery(link);
  });
});

galleryDialog.querySelector(".gallery-close").addEventListener("click", () => galleryDialog.close());
galleryPrevious.addEventListener("click", () => moveImage(-1));
galleryNext.addEventListener("click", () => moveImage(1));
galleryPlay.addEventListener("click", () => {
  if (autoplay) {
    stopAutoplay();
    return;
  }
  autoplay = true;
  galleryPlay.querySelector("span").textContent = "❚❚";
  labelControl(galleryPlay, "Diashow pausieren");
  galleryPlay.setAttribute("aria-pressed", "true");
  galleryCount.setAttribute("aria-live", "off");
  if (galleryPicture.querySelector("img")) {
    scheduleNextImage();
  } else {
    showImage(currentIndex);
  }
});

galleryDialog.addEventListener("keydown", event => {
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    moveImage(event.key === "ArrowRight" ? 1 : -1);
  }
});

galleryDialog.addEventListener("close", () => {
  ++requestId;
  stopAutoplay();
  currentGallery = null;
  galleryPicture.replaceChildren();
  document.body.classList.remove("gallery-is-open");
  openingLink.focus({ preventScroll: true });
  exitGalleryFullscreen().catch(reportFullscreenError);
});

galleryFullscreen.hidden = !(document.fullscreenEnabled && galleryView.requestFullscreen);
galleryFullscreen.addEventListener("click", async () => {
  galleryFullscreen.disabled = true;
  try {
    if (document.fullscreenElement === galleryView) {
      await exitGalleryFullscreen();
    } else {
      await galleryView.requestFullscreen();
      if (!galleryDialog.open) await exitGalleryFullscreen();
    }
  } catch (error) {
    reportFullscreenError(error);
  } finally {
    galleryFullscreen.disabled = false;
    updateFullscreenControl();
  }
});
document.addEventListener("fullscreenchange", updateFullscreenControl);

document.addEventListener("visibilitychange", () => {
  if (document.hidden) stopAutoplay();
});
