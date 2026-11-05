"use strict";

async function loadBanner() {
  const container = document.querySelector("[data-banner]");
  if (!container) return;

  try {
    const response = await fetch("banner.html", { cache: "no-cache" });
    if (!response.ok) {
      throw new Error(`Mitteilung konnte nicht geladen werden: HTTP ${response.status}`);
    }

    const bannerDocument = new DOMParser().parseFromString(await response.text(), "text/html");
    const message = bannerDocument.getElementById("mitteilung");
    if (!message || !message.textContent.trim()) {
      throw new Error("In banner.html fehlt die Mitteilung mit der ID mitteilung.");
    }

    container.replaceChildren(...message.childNodes);
  } catch (error) {
    console.error("Fehler beim Laden der aktuellen Mitteilung:", error);
    const text = document.createElement("p");
    text.append("Die aktuelle Mitteilung konnte nicht geladen werden. Bitte ");
    const link = document.createElement("a");
    link.href = "banner.html";
    link.textContent = "den Veranstaltungshinweis direkt öffnen";
    text.append(link, ".");
    container.replaceChildren(text);
  }
}

loadBanner();
