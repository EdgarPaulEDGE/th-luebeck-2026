/** Fotografiert ausgewählte Folien im Handy-Hochformat (430 x 932 (Handy hochkant)). Aufruf: node werkzeuge/pruefe-1610.mjs adresse ordner 1,3,12 */
import puppeteer from "puppeteer";
import { mkdirSync } from "node:fs";
const [adresse, ordner, liste] = process.argv.slice(2);
mkdirSync(ordner, { recursive: true });
const browser = await puppeteer.launch();
const seite = await browser.newPage();
await seite.evaluateOnNewDocument(() => Object.defineProperty(navigator, "webdriver", { get: () => false }));
await seite.setViewport({ width: 430, height: 932, deviceScaleFactor: 2 });
await seite.goto(`${adresse}/?nofrag`, { waitUntil: "networkidle0" });
await seite.evaluate(() => Reveal.configure({ transition: "none", backgroundTransition: "none" }));
await new Promise((r) => setTimeout(r, 1500));
for (const n of liste.split(",").map(Number)) {
  await seite.evaluate((h) => Reveal.slide(h, 0), n - 1);
  await new Promise((r) => setTimeout(r, 500));
  await seite.screenshot({ path: `${ordner}/hoch-${n}.png` });
}
await browser.close();
