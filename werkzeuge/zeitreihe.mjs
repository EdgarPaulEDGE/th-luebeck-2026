/**
 * Fotografiert eine Folie live (mit Animationen) zu mehreren Zeitpunkten.
 * Aufruf: node zeitreihe.mjs adresse folienindex bildordner ms1,ms2,... [klicks_nach_erstem_bild]
 */
import puppeteer from "puppeteer";
const [adresse, folie, ordner, zeiten, klicks = "0"] = process.argv.slice(2);
const browser = await puppeteer.launch({ args: ["--autoplay-policy=no-user-gesture-required"] });
const seite = await browser.newPage();
await seite.setViewport({ width: 1920, height: 1080 });
await seite.goto(`${adresse}/`, { waitUntil: "networkidle0" });
await seite.evaluate(() => document.fonts.ready);
await seite.evaluate((f) => { Reveal.configure({ transition: "none" }); Reveal.slide(+f, 0, -1); }, folie);
let vorher = 0;
for (const [k, ms] of zeiten.split(",").map(Number).entries()) {
  await new Promise((r) => setTimeout(r, ms - vorher));
  vorher = ms;
  await seite.screenshot({ path: `${ordner}/zeit-${k}.png` });
  if (k === 0) for (let i = 0; i < +klicks; i++) await seite.evaluate(() => Reveal.next());
}
await browser.close();
