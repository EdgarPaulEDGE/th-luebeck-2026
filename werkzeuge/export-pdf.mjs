// PDF Export: fotografiert jede Folie in doppelter Auflösung (3840 x 2160). Die Bilder setzt export-pdf.sh zum PDF zusammen.
// Warum nicht decktape: der PDF Druckweg zeichnet um Text mit Farbverlauf (.schimmer) einen dünnen Rahmen.
// Aufruf über:  sh werkzeuge/export-pdf.sh
import puppeteer from '/Users/thisisnotedgarsmacbookpro/Desktop/CC/cbl-aufgeweckt/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';
const ziel = process.argv[2];
const b = await puppeteer.launch({ headless: 'new', protocolTimeout: 180000, args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader'] });
const s = await b.newPage(); await s.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
await s.goto('http://localhost:8794/?nofrag&v=' + Date.now(), { waitUntil: 'networkidle0' }); await new Promise(r => setTimeout(r, 2500));
const anz = await s.evaluate(() => Reveal.getTotalSlides());
for (let i = 0; i < anz; i++) { await s.evaluate(n => Reveal.slide(n), i); await new Promise(r => setTimeout(r, 1500)); await s.screenshot({ path: ziel + '/s-' + String(i + 1).padStart(2, '0') + '.png' }); }
console.log('Seiten fotografiert:', anz); await b.close();
