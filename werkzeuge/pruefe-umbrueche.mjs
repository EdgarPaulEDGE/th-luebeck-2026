/** Misst Zeilenumbrüche: Jede Überschrift und große Aussage muss genau so viele Zeilen haben, wie Umbrüche gesetzt sind.
   Aufruf: node werkzeuge/pruefe-umbrueche.mjs adresse [breite hoehe] */
import puppeteer from "puppeteer";
const [adresse, b = "1600", h = "1000"] = process.argv.slice(2);
const browser = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", userDataDir: "/tmp/th-umbruch-profil" });
const seite = await browser.newPage();
await seite.setViewport({ width: +b, height: +h });
await seite.goto(`${adresse}/?nofrag`, { waitUntil: "load" });
await seite.evaluate(() => document.fonts.ready);
await new Promise((r) => setTimeout(r, 1500));
const zahl = await seite.evaluate(() => Reveal.getTotalSlides());
let fehler = 0;
for (let n = 0; n < zahl; n++) {
  await seite.evaluate((i) => Reveal.slide(i, 0), n);
  await new Promise((r) => setTimeout(r, 250));
  const funde = await seite.evaluate(() => {
    const aus = [];
    document.querySelectorAll(".present h1, .present h2, .present .these, .present .zitat, .present .vielleicht, .present .ansage, .present .fenster-erklaerung, .present figcaption, .present .karte .hinten b, .present .agenda-zeile b, .present .weil-liste li").forEach((e) => {
      if (!e.textContent.trim() || !e.getClientRects().length) return;
      const r = document.createRange(); r.selectNodeContents(e);
      const zeilen = [...r.getClientRects()].filter((k) => k.width > 2).map((k) => (k.top + k.bottom) / 2).sort((a, c) => a - c);
      const hoehe = parseFloat(getComputedStyle(e).fontSize) * (document.querySelector(".slides").getBoundingClientRect().width / 1920) * .5;
      const z = zeilen.filter((v, i, l) => i === 0 || v - l[i - 1] > hoehe).length;
      const gesetzt = e.querySelectorAll("br").length + 1;
      const aussen = r.getBoundingClientRect();
      aus.push({ text: e.innerText.replace(/\n/g, " / ").slice(0, 70), z, gesetzt, raus: aussen.right > innerWidth + 1 || aussen.left < -1 });
    });
    return aus;
  });
  for (const f of funde) if (f.z !== f.gesetzt || f.raus) { fehler++; console.log(`Folie ${n + 1}: ${f.z} Zeilen, ${f.gesetzt} gesetzt${f.raus ? ", ragt raus" : ""}: ${f.text}`); }
}
console.log(fehler ? `${fehler} Stellen prüfen` : "Alle Umbrüche wie gesetzt.");
await browser.close();
