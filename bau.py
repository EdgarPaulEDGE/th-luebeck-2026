"""Baut index.html für den Vortrag an der TH Lübeck, Projektwoche 2026 (10.11.2026, 13 Uhr).

Aufruf:  python3 bau.py
Folien, Texte und Sprechernotizen werden hier gepflegt, nie direkt in index.html.
Stamm: EDGE x Deutsche Bank (Raumschwarz, Galaxie, Avenir Next, Schimmer), Grundstil in stamm.html.
Dramaturgie: Das Deck beginnt nachts in TH-Rot vor dem Seminargebäude und endet im Morgengrauen
im EDGE-Blau vor demselben Gebäude. Die Farbe erzählt den Weg vom Hörsaal zum eigenen Unternehmen.
"""
import json
import shutil
from pathlib import Path

ORDNER = Path(__file__).parent
# Duplikat auf dem Schreibtisch, nach jedem Bau aktuell (Edgars Regel: alles auch direkt unter ~/Desktop/<Auftrag>/)
SCHREIBTISCH = Path.home() / "Desktop" / "TH Lübeck Projektwoche 2026"

# ----------------------------------------------------------------------------
# Inhalte
# ----------------------------------------------------------------------------

TITEL = "Ehemalige Studierende. Heute Unternehmer."
DATUM = "10. November 2026"
KONTAKT = "emre@edge-digital.com · edgar@edge-digital.com"
# Adresse der Karte zum Mitnehmen. Solange None, bleibt der QR-Code auf der letzten Folie weg.
KARTE_URL = None

# Originaler Chatverlauf vom 28.12.2020 (Screenshot aus der Präsi 2025), wörtlich mit Tippfehlern
CHAT = [("Ab nächstes Jahr setzen wir uns mal hin und bereden", "12:31"),
        ("Ich könnte mir sogar vorstellen social media mangament Firma zu gründen", "12:31"),
        ("Lübeck ohne <span class='zensur'>scheiß</span> social media kommt hier bei den Betrieben erst neu an", "12:32"),
        ("Weil wirklich ich weiß es aus so persönlichen Quellen Also die meisten selbständigen sind ü50 in Lübeck und haben von social media kein plan", "12:33"),
        ("Die wissen gar nicht was das alles bringt", "12:33"),
        ("Die posten immernoch lame auf Facebook", "12:33"),
        ("Kriegen 3 likes", "12:33")]

# (name, kennung eines Trägerlogos)
PREISE = [("Existenzgründerpreis", "lnpreis"), ("Gründerpreis der Sparkasse zu Lübeck", "sparkasse"), ("Social Hackathon", "socialhackathon"), ("Überflieger Wettbewerb", "startupsh")]

# Team: (name, rolle, bilddatei)
SERVICE_KOPF = ("Eddie", "Head of AI-Services", "eddie.png")
SERVICE = [("Chakira", "AI Content Creatorin", "chakira.png"), ("Sohal", "AI Network Expertin", "sohal.png"), ("Jorge", "Data Scientist", "jorge.png")]
SOFTWARE_KOPF = ("Dom", "Head of AI-Software", "dom.png")
SOFTWARE = [("Mats", "Frontend Entwickler", "mats.png"), ("Saroj", "Backend Entwickler", "saroj.png"), ("Nadira", "AI und Software Engineer", "nadira.png")]

# Icons im Lucide-Stil (24er Raster, nur Konturen)
ICON = {
    "job": '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    "master": '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>',
    "gruenden": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "frage": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "buch": '<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>',
    "taeglich": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    "name": '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8" cy="12" r="2.2"/><path d="M5 17c.6-1.6 1.7-2.4 3-2.4s2.4.8 3 2.4M14 10h5M14 14h4"/>',
    "adresse": '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "telefon": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.9.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "passwort": '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    "gesundheit": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>',
    "firma": '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4M10 18h4"/>',
    "quelle": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "zahl": '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "sprache": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "zeitung": '<path d="M4 22h16a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2H8a2 2 0 0 0-2 2v16a2 2 0 0 1-2 2Zm0 0a2 2 0 0 1-2-2v-9c0-1.1.9-2 2-2h2"/><path d="M18 14h-8M15 18h-5"/><path d="M10 6h8v4h-8V6Z"/>',
    "anker": '<path d="M12 22V8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/><circle cx="12" cy="5" r="3"/>',
    "ehrlich": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
}

NACH_DEM_STUDIUM = [("job", "Job"), ("master", "Master"), ("gruenden", "Gründen"), ("frage", "Keine Ahnung")]
KI_NUTZUNG = [("chat", "Schon mal ausprobiert"), ("buch", "Fürs Studium"), ("taeglich", "Jeden Tag")]
NIE_IN_DIE_KI = [("name", "Namen"), ("adresse", "Adressen"), ("telefon", "Telefonnummern"), ("passwort", "Passwörter"),
                 ("gesundheit", "Gesundheitsdaten"), ("firma", "Firmeninterna")]
FAKTENCHECK = [("quelle", "Jede Quelle selbst öffnen"), ("zahl", "Jede Zahl gegenprüfen"), ("ehrlich", "„Sag mir, wenn du es nicht weißt.“")]

# Was KI heute kann: Lautstärke der echten KI-Stimme (assets/audio/ki-stimme.mp3) in 40 Abschnitten,
# 0 bis 1, berechnet mit ffmpeg als Effektivwert je Abschnitt. Ändert sich die Aufnahme, neu messen.
WELLE = [1.0, 0.62, 0.29, 0.74, 0.38, 0.53, 0.45, 0.08, 0.08, 0.08, 0.08, 0.19, 0.36, 0.49, 0.47, 0.46, 0.17, 0.26, 0.42, 0.27, 0.26, 0.26, 0.24, 0.51, 0.11, 0.08, 0.08, 0.08, 0.39, 0.33, 0.5, 0.51, 0.49, 0.35, 0.47, 0.4, 0.51, 0.52, 0.18, 0.2]
# Diesen Text tippt die Kachel „Schreiben“ live, Zeichen für Zeichen
KI_TIPPTEXT = "Sehr geehrte Frau Professorin,\nmein Laptop und ich haben uns gestern getrennt. Es ging nicht von mir aus."

# Kompass: Rolle, Aufgabe, Kontext, Förmchen. Dieselben Begriffe wie in den CBL-Vorträgen.
KOMPASS = [("Rolle", "Wer soll die KI sein?"), ("Aufgabe", "Was genau soll passieren?"),
           ("Kontext", "Was weißt nur du?"), ("„Förmchen“", "In welcher Form?")]





FOTOS_STUDIUM = 24

# Turm: was unter einer „fertigen“ KI-App noch alles liegt (von unten nach oben)
TURM = ["Wartung", "Backups", "Sicherheit", "Hosting", "Datenschutz", "Datenbank", "Login"]

# Logos auf dem Logo-Bogen der Präsi vom November 2025 (Folie 6 der alten PowerPoint). Alles andere kam seitdem dazu.
LOGOS_2025 = ["sparkasse", "wfluebeck", "wfl", "hansebelt", "exrohr", "wks", "swm", "it4b", "kish", "diakonie", "elvis", "ihk",
              "k2konzept", "ln", "mediamagneten", "epunkt", "collins", "ltm", "inlingua", "baumstark", "digitalesmv"]
# Von Edgar genannt (06.10.2026): seit letztem November dazugekommen, groß zeigen
LOGOS_NEU_GROSS = ["staatskanzlei", "hansestadt", "norva24", "vs", "ksk"]
NICHT_AUF_DIE_WAND = {"thluebeck", "lnpreis", "socialhackathon", "startupsh"}
# Lage von Handy und Server im Bild handy-cloud.jpg, in Prozent der Bildbreite
HANDY_X, SERVER_X = 18, 83

# Microsoft Research, „Working with AI“ (Tomlinson u. a., arXiv 2507.07935v6, Dez. 2025), Tabellen S3 und S4.
# 200.000 Copilot-Gespräche, USA. Score = KI-Anwendbarkeit, ausdrücklich kein Maß für Jobverlust.
BERUFE_RATEN = [("code", "Programmierer"), ("sprache", "Dolmetscher"), ("zeitung", "Journalisten"), ("anker", "Brückenwärter")]
BERUFE = [("Dolmetscher", 0.492, "Platz 1"), ("Historiker", 0.462, "Platz 2"), ("Journalisten", 0.383, "Platz 11"),
          ("Data Scientists", 0.357, "Platz 19"), ("Brückenwärter", 0.0, "ganz unten")]

# Anthropic, „Scenarios for our Economic Future“ (Sept. 2026): US-Wirtschaftsleistung 2030 gegenüber ohne KI. Szenarien, keine Vorhersage.
# (Bedingung, Zuwachs gegenüber 2030 ohne KI in %, so viele Jahre normales Wachstum bei rund 2 % pro Jahr)
ZUKUENFTE = [("KI so viel verändert wie damals das Internet", 1.6, "<small>knapp</small> 1 Jahr"),
             ("KI die Hälfte der Büroarbeit erledigt", 8.3, "4 Jahre"),
             ("KI fast jede Büroarbeit besser kann als wir", 32.4, "14 Jahre")]


# ----------------------------------------------------------------------------
# Bausteine
# ----------------------------------------------------------------------------

def icon(k, klasse=""):
    return f'<svg class="icon {klasse}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[k]}</svg>'


def notizen(text):
    """Sprechernotizen (Taste S). Regie in normalem Deutsch: was gesagt, geklickt und gezeigt wird."""
    return f'<aside class="notes">{text}</aside>'


def ring(n):
    """Nummer im drehenden Verlaufsring, nie mit führender Null."""
    return f'<span class="ring"><b>{n}</b></span>'


def kopf_kreis(name, rolle, bild, klasse, gross=False):
    return f'''<figure class="person {klasse}{" gross" if gross else ""}">
  <div class="rund"><img src="assets/team/{bild}" alt="{name}" width="720" height="720"></div>
  <figcaption><b>{name}</b><span>{rolle}</span></figcaption>
</figure>'''


def team_seite(klasse, titel, kopf, leute):
    reihe = "".join(kopf_kreis(n, r, b, klasse) for n, r, b in leute)
    return f'''<div class="seite {klasse}">
  <p class="seiten-titel">{titel}</p>
  {kopf_kreis(*kopf, klasse, gross=True)}
  <div class="reihe">{reihe}</div>
</div>'''


def kunst_kante(stopps):
    """Die EDGE: eine leuchtende Kante am Rand eines dunklen Körpers (aus dem Stamm, ohne SVG-Filter)."""
    farben = ", ".join(f"{f} {18 + o * 64:.0f}%" for o, f in stopps)
    verlauf = f"linear-gradient(to bottom, transparent 3%, {farben}, transparent 97%)"
    mitte = "1640px 540px"
    schein = f"radial-gradient(circle at {mitte}, transparent 0, transparent 637px, rgba(0,0,0,.95) 639px, #000 641px, rgba(0,0,0,.62) 645px, rgba(0,0,0,.34) 664px, rgba(0,0,0,.16) 710px, rgba(0,0,0,.06) 790px, transparent 900px)"
    koerper = f"radial-gradient(circle at {mitte}, #030309 0, #030309 637px, transparent 640px)"
    return f'''<div class="kunst kante" aria-hidden="true">
  <div style="position:absolute;inset:0;background:{koerper};"></div>
  <div style="position:absolute;inset:0;background:{verlauf};-webkit-mask-image:{schein};mask-image:{schein};"></div>
</div>'''


def chat():
    blasen = "".join(f'<div class="blase" style="--i:{i};"><span>{t}</span><i>{z}<svg viewBox="0 0 16 11" aria-hidden="true"><path d="M1 6l3 3 6-7M6 9l1 1 7-8" fill="none" stroke="#53BDEB" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></i></div>'
                     for i, (t, z) in enumerate(CHAT))
    return f'<div class="chat"><div class="chat-datum">28. Dez. 2020</div>{blasen}</div>'


def fotowand():
    return '<div class="fotowand">' + "".join(f'<img src="assets/alt/studium-{i}.jpg" alt="" loading="lazy">' for i in range(1, FOTOS_STUDIUM + 1)) + "</div>"


def prompt_box(text, klein=False):
    return f'<div class="prompt{" klein" if klein else ""}"><span class="prompt-label">Prompt</span><p>{text}</p></div>'


def antwort_box(text, quelle="Antwort von Claude, gekürzt"):
    return f'<div class="antwort"><span class="prompt-label">{quelle}</span><p>{text}</p></div>'


# ----------------------------------------------------------------------------
# Zusatzstil: TH-Rot, Kapitelmarker, Chat, Fotowand, Prompts
# ----------------------------------------------------------------------------

EXTRA_STIL = """
/* ---------- TH Lübeck Projektwoche 2026: Zusatzstil ---------- */
body.standbild .reveal .slides section .fragment { opacity: 1 !important; visibility: inherit !important; transform: none !important; }
:root { --th: #E4003A; --th-hell: #FF5C7A; --th-zart: #FF9FB1; --edge-blau: #7FD4FF; }
/* TH-Phase: Schimmer von TH-Rot ins Helle. Die EDGE-Phase am Ende nutzt f-hblau aus dem Stamm. */
.f-th { --s1: #E4003A; --s2: #FF3D63; --s3: #FF9FB1; }
.st-th { background: radial-gradient(46% 42% at 80% 46%, rgba(228,0,58,.26), transparent 70%), radial-gradient(30% 26% at 12% 86%, rgba(255,92,122,.12), transparent 70%); }
.st-neutral { background: radial-gradient(38% 30% at 78% 24%, rgba(228,0,58,.10), transparent 70%), radial-gradient(34% 28% at 16% 80%, rgba(255,92,122,.07), transparent 70%) !important; }
body[data-stimmung="th"] .st-th { opacity: 1; }

/* Vollflächige Bilder und Schleier (aus dem Stamm Deutsche Bank) */
.voll { position: absolute; inset: 0; width: 1920px; height: var(--buehne-h); object-fit: cover; display: block; margin: 0 !important; max-width: none !important; max-height: none !important; }
.schleier-links { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(3,3,9,.92) 0%, rgba(3,3,9,.72) 30%, rgba(3,3,9,.18) 52%, rgba(3,3,9,0) 64%); }
.schleier-unten { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(3,3,9,.94) 0%, rgba(3,3,9,.6) 28%, rgba(3,3,9,0) 55%); }
.schleier-unten.stark { background: linear-gradient(0deg, rgba(3,3,9,.97) 0%, rgba(3,3,9,.85) 24%, rgba(3,3,9,.35) 48%, rgba(3,3,9,0) 66%); }
.schleier-ganz { position: absolute; inset: 0; background: rgba(3,3,9,.55); }
.bild-quelle { position: absolute; right: 40px; bottom: 26px; font-size: 16px; color: rgba(244,246,255,.4); letter-spacing: .06em; }
.slide.mittig { justify-content: center; align-items: center; text-align: center; }
.slide.unten { justify-content: flex-end; padding-bottom: 120px; }
.slide.links-mitte { justify-content: center; }
.schatten { text-shadow: 0 6px 40px rgba(3,3,9,.85), 0 2px 10px rgba(3,3,9,.6); }
@keyframes auftauchen { to { opacity: 1; } }
@keyframes hochkommen { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: none; } }



/* Nummern im drehenden Verlaufsring */
.ring { position: relative; display: inline-grid; place-items: center; width: 92px; height: 92px; border-radius: 50%; flex-shrink: 0; isolation: isolate; overflow: hidden; }
.ring::before { content: ""; position: absolute; inset: -40%; background: conic-gradient(from 0deg, #E4003A, #FF9FB1, #7FD4FF, #E4003A); animation: drehen 5s linear infinite; z-index: -2; }
.ring::after { content: ""; position: absolute; inset: 4px; border-radius: 50%; background: #0A0710; z-index: -1; }
.ring b { font-size: 40px; font-weight: 700; color: var(--weiss); }
@keyframes drehen { to { transform: rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .ring::before { animation: none; } }

/* Titel */
.titel-duo { display: flex; align-items: center; gap: 36px; position: relative; }
.titel-duo .th-logo { height: 118px; width: auto; display: block; margin: 0; }
.titel-duo .edge-logo { height: 96px; width: auto; display: block; margin: 0; }
.titel-duo .mal { font-size: 52px; font-weight: 400; color: var(--w-45); line-height: 1; }
.deckblatt { justify-content: space-between; padding-top: 104px; padding-bottom: 92px; }
.deckblatt .hero { font-size: 128px; position: relative; }
.deckblatt .unterzeile { font-size: 46px; font-weight: 600; margin: 26px 0 0; color: var(--w-70); position: relative; letter-spacing: .02em; }
.ecken { position: relative; display: flex; justify-content: space-between; font-size: 24px; font-weight: 600; letter-spacing: .08em; color: var(--w-45); margin-top: 60px; }

/* Große Fragen */
.frage-gross { font-size: 132px; line-height: 1.06; font-weight: 700; letter-spacing: -.025em; text-transform: uppercase; margin: 0; }
.nein { font-size: 420px; line-height: .9; font-weight: 700; letter-spacing: -.04em; margin: 0; }
.vielleicht { position: relative; font-size: 96px; font-weight: 700; letter-spacing: -.02em; margin: 0; }
.weil-liste { list-style: none; margin: 60px 0 0; padding: 0; }
.weil-liste li { font-size: 62px; line-height: 1.2; font-weight: 600; padding: 24px 0 24px 0; border-top: 1px solid var(--hairline); color: var(--weiss); }
.weil-liste li:last-child { border-bottom: 1px solid var(--hairline); }
.weil-liste li span { color: var(--w-45); font-weight: 500; }

/* Wer sind wir: zwei Freisteller */
.duo { display: flex; justify-content: center; gap: 140px; margin-top: auto; margin-bottom: 0; }
.duo figure { margin: 0; display: flex; flex-direction: column; align-items: center; }
.duo .rund { width: 380px; height: 380px; border-width: 6px; --ring: var(--th); }
.duo figcaption { margin-top: 26px; text-align: center; }
.duo figcaption b { display: block; font-size: 46px; font-weight: 700; }
.duo figcaption span { display: block; font-size: 26px; color: var(--w-45); margin-top: 6px; letter-spacing: .04em; }

/* Wer sind wir: Freisteller groß */
.duo-frei { position: absolute; right: 40px; bottom: calc(0px - var(--extra)); height: 980px; width: auto; margin: 0 !important; max-width: none !important; max-height: none !important; filter: drop-shadow(0 0 60px rgba(228,0,58,.25)); }
.namen-duo { display: flex; flex-direction: column; gap: 22px; margin-top: 60px; }
.namen-duo p { margin: 0; display: flex; flex-direction: column; border-left: 4px solid var(--th); padding-left: 24px; }
.namen-duo b { font-size: 44px; font-weight: 700; }
.namen-duo span { font-size: 26px; color: var(--w-45); letter-spacing: .04em; margin-top: 2px; }
body.hochkant .duo-frei { height: 900px; right: -60px; }

/* Agenda */
.agenda { display: flex; flex-direction: column; gap: 34px; margin-top: 70px; }
.agenda-zeile { display: flex; align-items: center; gap: 44px; }
.agenda-zeile b { font-size: 72px; font-weight: 700; text-transform: uppercase; letter-spacing: -.015em; }
.agenda-zeile.pause b { font-size: 40px; color: var(--w-45); font-weight: 600; letter-spacing: .1em; }
.agenda-zeile.pause .strich { width: 92px; display: flex; justify-content: center; }
.agenda-zeile.pause .strich::before { content: ""; width: 2px; height: 46px; background: var(--hairline); }

/* Chat vom 28.12.2020 */
.chat-buehne { display: grid; grid-template-columns: 640px 1fr; gap: 90px; flex: 1; align-items: center; }
.chat { display: flex; flex-direction: column; align-items: flex-end; gap: 12px; padding: 30px 34px; border-radius: 28px; background: #0B141A; border: 1px solid rgba(244,246,255,.08); }
.chat-datum { align-self: center; font-size: 20px; font-weight: 600; color: #D1D7DB; background: #182229; padding: 6px 18px; border-radius: 10px; margin-bottom: 6px; }
.blase { max-width: 88%; background: #005C4B; color: #E9EDEF; border-radius: 16px 4px 16px 16px; padding: 12px 18px 10px; font-size: 27px; line-height: 1.32; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 4px 14px; justify-content: flex-end; opacity: 0; }
.blase span { flex: 1 1 auto; text-align: left; }
/* Kraftausdrücke wie im Fernsehen unkenntlich, das Wort bleibt an seiner Stelle */
.blase .zensur { display: inline-block; filter: blur(7px); background: rgba(233,237,239,.25); border-radius: 6px; padding: 0 4px; user-select: none; }
.blase i { font-style: normal; font-size: 16px; color: rgba(233,237,239,.6); display: flex; align-items: center; gap: 5px; white-space: nowrap; }
.blase svg { width: 17px; height: 12px; }
.reveal section.present .blase { animation: hochkommen .45s calc(.5s + var(--i) * .7s) cubic-bezier(.2,.7,.3,1) forwards; }
body.standbild .blase { opacity: 1; }
.chat-text .label { color: var(--th-hell); }
.chat-text .hero { font-size: 118px; margin-top: 18px; }

/* Erster Name: EPG wird EDGE */
.namen-buehne { display: flex; align-items: center; justify-content: space-between; gap: 60px; flex: 1; }
.namen-buehne .epg { width: 540px; height: auto; margin: 0 0 40px; display: block; background: #fff; padding: 34px 40px; border-radius: 10px; transform: rotate(-3deg); }
.epg-spalte { display: flex; flex-direction: column; align-items: flex-start; }
.lesart { display: flex; align-items: baseline; gap: 26px; padding: 16px 0; border-top: 1px solid var(--hairline); width: 760px; }
.lesart span { width: 150px; flex-shrink: 0; font-size: 22px; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: var(--w-45); }
.lesart b { font-size: 50px; font-weight: 600; letter-spacing: -.01em; white-space: nowrap; }
.lesart i { font-style: normal; font-weight: 700; color: var(--th-hell); }
.namen-buehne .pfeil { font-size: 110px; color: var(--th); line-height: 1; }
.namen-buehne .edge { width: 520px; height: auto; margin: 0; display: block; }
.namen-buehne .wurde { display: flex; align-items: center; gap: 50px; }

/* Fotowand Studium: 8 x 3, randlos */
.fotowand { position: absolute; left: 0; top: 0; width: 1920px; height: var(--buehne-h); display: grid; grid-template-columns: repeat(8, 1fr); grid-template-rows: repeat(3, 1fr); gap: 6px; }
.fotowand img { width: 100%; height: 100%; object-fit: cover; display: block; margin: 0 !important; max-width: none !important; max-height: none !important; filter: saturate(.85); }

/* Master-Urkunde: Polaroid fällt auf Klick über die Fotowand */
.polaroid.master { position: absolute; right: 150px; top: calc(var(--extra) + 120px); width: 640px; margin: 0; z-index: 3; }
.polaroid.master img { height: auto; aspect-ratio: 665 / 640; }
.reveal .slides section .polaroid.master.fragment { transition: opacity .4s ease, transform .6s cubic-bezier(.2,.8,.3,1.2); transform: translateY(-80px) rotate(-12deg); }
.reveal .slides section .polaroid.master.fragment.visible { transform: translateY(0) rotate(-4deg); }
body.standbild .polaroid.master { transform: rotate(-4deg) !important; }

@font-face { font-family: "Caveat"; src: url("assets/fonts/Caveat.ttf") format("truetype"); font-weight: 400 700; }
/* Stapel echter Momente: Beschriftung wie mit Stift auf dem Polaroid-Rand */
.polaroid figcaption { font-family: "Caveat", "Bradley Hand", cursive; font-weight: 600; color: #2A2630; text-align: center; line-height: 1.05; }
.polaroid.stapel figcaption { margin-top: 8px; font-size: 28px; }
.polaroid.stapel { position: absolute; margin: 0; padding: 12px 12px 12px; }
.polaroid.stapel img { height: auto; }

/* Karten drehen auf Klick (Kniff aus dem Charta-Deck) */
.karten { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin-top: auto; margin-bottom: auto; perspective: 2400px; }
.reveal .slides section .fragment.karte { opacity: 1 !important; visibility: inherit !important; }
.karte { height: 470px; }
.karte .innen { position: relative; width: 100%; height: 100%; transform-style: preserve-3d; transition: transform 1s cubic-bezier(.3,.8,.25,1); }
.karte.visible .innen, body.standbild .karte .innen { transform: rotateY(180deg); }
.karte .seite { position: absolute; inset: 0; border-radius: 22px; backface-visibility: hidden; -webkit-backface-visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; padding: 30px; text-align: center; }
.karte .vorn { background: rgba(244,246,255,.06); border: 1.5px solid rgba(244,246,255,.2); }
.karte .vorn span { font-size: 46px; font-weight: 700; color: var(--w-70); white-space: nowrap; }
.karte .hinten { transform: rotateY(180deg); background: linear-gradient(150deg, #FF5C7A, #E4003A 55%, #9A0027); }
.karte .hinten b { font-size: 64px; line-height: 1.1; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: -.01em; }
.polaroid.quelle-foto { position: absolute; right: 70px; top: calc(var(--extra) + 36px); width: 320px; margin: 0; padding: 10px 10px 30px; }
.polaroid.quelle-foto img { height: auto; }
.polaroid.quelle-foto figcaption { margin-top: 6px; font-size: 27px; }
body.hochkant .karten { grid-template-columns: 1fr; }


/* Platzhalter für fehlende Fotos: gestrichelter Rahmen im Polaroid */
.polaroid .platzhalter { aspect-ratio: 4 / 5; display: grid; place-items: center; border: 3px dashed #B9B2C2; background: #E9E5EE; }
.polaroid .platzhalter span { font-family: var(--font); font-size: 26px; font-weight: 600; color: #6B6475; text-align: center; line-height: 1.3; }
.polaroid figcaption { margin-top: 8px; font-size: 30px; }
.platzhalter-foto { position: absolute; right: 200px; top: calc(var(--extra) + 170px); width: 560px; margin: 0; padding: 16px 16px 20px; }
.platzhalter-foto img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; object-position: 50% 45%; }

/* Gründung: vier Polaroids nebeneinander */
.polaroid.gruendung { position: absolute; top: calc(var(--extra) + 330px); width: 380px; margin: 0; padding: 14px 14px 18px; }
.polaroid.gruendung img { height: 480px; width: 100%; object-fit: cover; object-position: 50% 40%; }
.polaroid.gruendung .platzhalter { height: 480px; aspect-ratio: auto; }

/* EPG-Szene: Karte, zwei Freisteller, Buchstaben fliegen auf Klick */
.epg-szene, .dom-szene { position: absolute; left: 0; top: var(--extra); width: 1920px; height: 1080px; pointer-events: none; }
.epg-s1, .epg-s2, .dom-s1 { position: absolute; width: 1px; height: 1px; opacity: 0; }
.epg-karte { position: absolute; left: 1570px; top: 50px; width: 300px; background: #fff; padding: 20px 24px; border-radius: 10px; transform: rotate(-4deg); margin: 0 !important; }
.epg-person, .dom-person { -webkit-mask-image: linear-gradient(180deg, #000 72%, transparent 99%); mask-image: linear-gradient(180deg, #000 72%, transparent 99%); }
.epg-person.emre, .dom-person.p-emre { -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 13%, #000 87%, transparent 100%), linear-gradient(180deg, #000 72%, transparent 99%); -webkit-mask-composite: source-in; mask-image: linear-gradient(90deg, transparent 0, #000 13%, #000 87%, transparent 100%), linear-gradient(180deg, #000 72%, transparent 99%); mask-composite: intersect; }
.epg-person { position: absolute; bottom: -34px; height: 700px; width: auto; margin: 0 !important; max-width: none !important; max-height: none !important; transition: transform 1s cubic-bezier(.5,0,.2,1), opacity .8s; }
.epg-person.emre { left: 560px; }
.epg-person.eddie { left: 1080px; z-index: 1; }
.epg-buchstabe { position: absolute; top: 244px; width: 116px; height: 116px; border-radius: 20px; display: grid; place-items: center; font-size: 84px; font-weight: 700; color: #fff;
  background: linear-gradient(150deg, #FF5C7A, #E4003A); opacity: 0; transform: translate(560px, -120px) scale(.4) rotate(-20deg); transition: transform .9s cubic-bezier(.3,1.4,.4,1), opacity .4s; z-index: 3; }
.epg-schild { position: absolute; padding: 6px 22px 8px; background: #fff; color: #231F28; border-radius: 10px; font-family: "Caveat", cursive; font-weight: 700; font-size: 50px; line-height: 1; white-space: nowrap; transform: translateX(-50%) rotate(-3deg); opacity: 0; transition: opacity .5s; z-index: 3; }
.epg-schild i { font-style: normal; color: #E4003A; }
.s-emre { left: 803px; top: 724px; }
.s-eddie-a, .s-eddie-b { left: 1359px; top: 734px; }
.epg-krone { position: absolute; left: 1299px; top: 352px; width: 120px; height: 80px; opacity: 0; transform: translateY(-260px) rotate(-30deg); transition: transform .8s cubic-bezier(.3,1.5,.4,1), opacity .3s; z-index: 2; }
.epg-blase { position: absolute; left: 560px; top: 394px; padding: 14px 26px 18px; background: #fff; color: #231F28; border-radius: 26px; font-family: "Caveat", cursive; font-weight: 700; font-size: 58px; opacity: 0; transition: opacity .4s .7s; z-index: 3; }
.epg-blase::after { content: ""; position: absolute; left: 30px; bottom: -18px; border: 12px solid transparent; border-top: 16px solid #fff; border-left-width: 4px; }
.epg-label { position: absolute; left: 130px; top: 250px; margin: 0; font-family: "Caveat", cursive; font-weight: 700; font-size: 64px; color: var(--th-hell); opacity: 0; transition: opacity .4s; }
/* Klick 1: Eddies Vorschlag */
.epg-szene:has(.epg-s1.visible) .epg-buchstabe { opacity: 1; }
.epg-szene:has(.epg-s1.visible) .b-e { transform: translate(745px, 0) rotate(-4deg); }
.epg-szene:has(.epg-s1.visible) .b-p { transform: translate(1243px, 0) rotate(3deg); }
.epg-szene:has(.epg-s1.visible) .b-g { transform: translate(1373px, 0) rotate(-2deg); }
.epg-szene:has(.epg-s1.visible) .s-emre, .epg-szene:has(.epg-s1.visible) .s-eddie-a { opacity: 1; }
.slide:has(~ .epg-szene .epg-s1.visible) .l1 { opacity: 1; }
/* Klick 2: was alle gelesen haben */
.epg-szene:has(.epg-s2.visible) .emre, body.standbild .epg-szene .emre { transform: translateX(-420px) rotate(-9deg); }
.epg-szene:has(.epg-s2.visible) .s-emre, .epg-szene:has(.epg-s2.visible) .s-eddie-a { opacity: 0; }
.epg-szene:has(.epg-s2.visible) .s-eddie-b, .epg-szene:has(.epg-s2.visible) .epg-blase { opacity: 1; }
.epg-szene:has(.epg-s2.visible) .b-e, body.standbild .epg-szene .b-e { transform: translate(1170px, 0px) rotate(-6deg); }
.epg-szene:has(.epg-s2.visible) .b-p, body.standbild .epg-szene .b-p { transform: translate(1300px, 0px) rotate(2deg); }
.epg-szene:has(.epg-s2.visible) .b-g, body.standbild .epg-szene .b-g { transform: translate(1430px, 0px) rotate(-3deg); }
.epg-szene:has(.epg-s2.visible) .epg-krone, body.standbild .epg-szene .epg-krone { opacity: 1; transform: rotate(-8deg); }
.slide:has(~ .epg-szene .epg-s2.visible) .l1 { opacity: 0; }
.slide:has(~ .epg-szene .epg-s2.visible) .l2 { opacity: 1; }
/* Standbild (PDF): die Pointe */
body.standbild .epg-buchstabe, body.standbild .epg-krone, body.standbild .s-eddie-b, body.standbild .epg-blase, body.standbild .l2 { opacity: 1 !important; }
body.standbild .l1, body.standbild .s-emre, body.standbild .s-eddie-a { opacity: 0 !important; }

/* Dom-Szene: drei Freisteller, E D G E auf Klick */
.dom-person { position: absolute; bottom: 0; height: 640px; width: auto; margin: 0 !important; max-width: none !important; max-height: none !important; }
.p-emre { left: 360px; z-index: 2; }
.p-dom { left: 655px; z-index: 1; }
.p-eddie { left: 1180px; z-index: 2; }
.dom-b { position: absolute; top: 290px; width: 116px; height: 116px; border-radius: 20px; display: grid; place-items: center; font-size: 84px; font-weight: 700; color: #fff;
  background: linear-gradient(150deg, #FF5C7A, #E4003A); opacity: 0; transform: translateY(-80px) scale(.5); transition: transform .7s cubic-bezier(.3,1.5,.4,1), opacity .3s; z-index: 3; }
.d1 { left: 518px; } .d2 { left: 838px; transition-delay: .15s; } .d3 { left: 968px; transition-delay: .3s; } .d4 { left: 1378px; transition-delay: .45s; }
.n-emre { left: 576px; top: 760px; } .n-dom { left: 960px; top: 760px; } .n-eddie { left: 1436px; top: 760px; }
.dom-szene:has(.dom-s1.visible) .dom-b { opacity: 1; transform: none; }
.dom-szene:has(.dom-s1.visible) .epg-schild { opacity: 1; transition-delay: .6s; }
body.standbild .dom-b, body.standbild .dom-szene .epg-schild { opacity: 1 !important; transform: none; }
body.standbild .dom-szene .epg-schild { transform: translateX(-50%) rotate(-3deg) !important; }

/* Büros: drei Stationen */
.bueros { display: grid; grid-template-columns: repeat(5, 1fr); gap: 34px; margin-top: 60px; padding: 0 10px; }
.polaroid.buero { margin: 0; padding: 14px 14px 18px; }
.polaroid.buero img { width: 100%; height: 480px; object-fit: cover; object-position: 50% 45%; }
.bueros-team { display: grid; grid-template-columns: repeat(3, 1fr); gap: 70px; padding: 0 30px; margin-top: 36px; text-align: center; }
.bueros-team span { font-size: 30px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: var(--w-45); }
.bueros-team span:last-child { color: var(--th-hell); }

.umzug-datum { position: absolute; left: 96px; bottom: 84px; z-index: 5; padding: 8px 24px 10px; background: #fff; color: #231F28; border-radius: 10px; font-family: "Caveat", cursive; font-weight: 700; font-size: 46px; transform: rotate(-3deg); }

/* Persönliche Folien */
.person-folie { justify-content: flex-start; }
.person-folie .headline { font-size: 104px; margin-bottom: 0; }
.person-folie .rolle { font-size: 30px; color: var(--w-45); letter-spacing: .06em; margin: 8px 0 0; font-weight: 600; }
.fotoreihe { display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-top: auto; margin-bottom: auto; padding: 0 10px; }
/* Polaroids: weißer Rand, leicht schräg, fallen beim Folienwechsel nacheinander ein */
.polaroid { margin: 0; background: #F6F3EE; padding: 16px 16px 58px; border-radius: 3px; transform: translateY(var(--y)) rotate(var(--d)); }
.polaroid img { width: 100%; height: 470px; object-fit: cover; object-position: 50% 30%; display: block; margin: 0 !important; max-width: none !important; max-height: none !important; }
.reveal section.present .polaroid { animation: einfallen .7s calc(.15s + var(--i) * .16s) cubic-bezier(.2,.8,.3,1.15) both; }
@keyframes einfallen { from { opacity: 0; transform: translateY(calc(var(--y) - 120px)) rotate(calc(var(--d) * 3)); } to { opacity: 1; transform: translateY(var(--y)) rotate(var(--d)); } }
body.standbild .polaroid { animation: none !important; }

/* Team heute */
.slide.team { flex-direction: row !important; padding: 172px 60px 60px; gap: 0; }
.mitte { width: 420px; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 50px; padding-top: 72px !important; }
.slide.team .person.du .rund { width: 216px; height: 216px; }
.slide.team .person.du figcaption span { white-space: nowrap; font-size: 23px; }
.slide.team .seiten-titel { font-size: 30px; height: 36px; line-height: 36px; margin-bottom: 36px; }
.slide.team .person.gross .rund { width: 262px; height: 262px; border-width: 6px; }
.slide.team .person.gross figcaption { margin-top: 16px; }
.slide.team .person.gross figcaption b { font-size: 42px; }
.slide.team .person.gross figcaption span { font-size: 25px; }
.slide.team .reihe { gap: 22px; margin-top: 56px; }
.slide.team .reihe .rund { width: 184px; height: 184px; }
.slide.team .reihe figcaption b { font-size: 30px; }
.slide.team .reihe figcaption span { font-size: 21px; max-width: 206px; }
.team-titel { position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-size: 56px; font-weight: 700; text-transform: uppercase; letter-spacing: -.01em; margin: 0; }
.du .rund { --ring: var(--th); border-style: dashed; background: rgba(228,0,58,.06); }
.du .rund::before { display: none; }
.du .rund b { position: absolute; inset: 0; display: grid; place-items: center; font-size: 96px; font-weight: 700; color: var(--th-hell); }
.person.du figcaption span { color: var(--w-70); }

/* Seit letztem Jahr */
.drei { display: grid; grid-template-columns: repeat(3, 1fr); gap: 70px; margin-top: auto; margin-bottom: auto; }
.drei > div { display: flex; flex-direction: column; gap: 22px; padding-top: 30px; border-top: 2px solid var(--th); }
.drei h3 { font-size: 54px; font-weight: 700; text-transform: uppercase; letter-spacing: -.01em; line-height: 1.1; }
.drei p { margin: 0; font-size: 36px; line-height: 1.4; color: var(--w-70); }
.drei .logo-reihe { display: flex; flex-wrap: wrap; gap: 26px 34px; align-items: center; margin-top: 10px; }
.drei .logo-reihe img { height: 70px; width: auto; max-width: 210px; object-fit: contain; display: block; margin: 0 !important; opacity: .92; }
.drei .soft-icons { display: flex; gap: 34px; margin-top: 10px; }
.drei .soft-icons .icon { width: 96px; height: 96px; color: var(--th-hell); filter: drop-shadow(0 0 14px rgba(228,0,58,.5)); }
.drei .koepfe { display: flex; margin-top: 10px; }
.drei .koepfe img { width: 128px; height: 128px; border-radius: 50%; object-fit: cover; object-position: center bottom; border: 3px solid #030309; margin: 0 -16px 0 0 !important; background: #14101c; }

/* Logowand (aus dem Stamm) */
.slide.wand { padding: 120px 110px 56px; }
.logos { display: grid; align-items: center; justify-items: center; flex-shrink: 0; }
.logos > div { display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; }
.logos img { display: block; margin: 0; width: auto; height: auto; object-fit: contain; }
.logos.gross { grid-template-columns: repeat(6, 1fr); grid-auto-rows: 120px; column-gap: 40px; }
.logos.gross img { max-width: 240px; max-height: 92px; opacity: .96; }
.logos.klein { display: flex; flex-wrap: wrap; justify-content: center; }
.logos.klein > div { width: calc(100% / var(--spalten, 10)); height: 84px; padding: 0 13px; }
.logos.klein img { max-width: 100%; max-height: 56px; opacity: .84; }
.trenner { border: none; height: 1px; width: 100%; flex-shrink: 0; margin: 20px 0 16px; background: linear-gradient(90deg, transparent, rgba(228,0,58,.8), transparent); }
.preise { margin-top: auto; flex-shrink: 0; display: flex; flex-direction: column; align-items: center; gap: 18px; }
.preis-reihe { display: flex; align-items: center; justify-content: center; gap: 60px; }
.preis { display: flex; align-items: center; gap: 11px; }
.preis b { font-size: 20px; font-weight: 600; color: var(--weiss); white-space: nowrap; }
.preis img { height: 23px; width: auto; max-width: 170px; opacity: .8; object-fit: contain; display: block; margin: 0 0 0 4px !important; }
.preis img[src*="socialhackathon"], .preis img[src*="lnpreis"] { height: 38px; }
.preis img[src*="sparkasse"] { height: 32px; }
.wand-kopf { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 26px; flex-shrink: 0; }
.wand-kopf .vielleicht { font-size: 64px; }

/* Icon-Reihen für Handzeichen und Checklisten */
.icons { display: grid; grid-template-columns: repeat(var(--n, 4), 1fr); gap: 30px; margin-top: auto; margin-bottom: auto; }
.icons > div { display: flex; flex-direction: column; align-items: center; text-align: center; }
.icons .icon { width: 150px; height: 150px; color: var(--th-hell); filter: drop-shadow(0 0 16px rgba(228,0,58,.5)); }
.icons p { margin: 30px 0 0; font-size: 38px; font-weight: 700; letter-spacing: .02em; line-height: 1.25; }
.icons.klein .icon { width: 180px; height: 180px; }
.icons.klein p { font-size: 28px; letter-spacing: .06em; text-transform: uppercase; }
.handzeichen { display: inline-flex; align-items: center; gap: 14px; font-size: 22px; font-weight: 600; letter-spacing: .16em; text-transform: uppercase; color: var(--th-hell); margin: 0 0 18px; }

/* Reality-Check-Thesen */
.these { font-size: 124px; line-height: 1.06; font-weight: 700; letter-spacing: -.025em; text-transform: uppercase; margin: 0; max-width: 1500px; }
.these-beleg { margin-top: 70px; display: flex; align-items: center; gap: 40px; }
.these-beleg .blase { opacity: 1; animation: none !important; font-size: 40px; max-width: none; }
.these-foto.breit { width: 1060px; object-position: 30% 50%; -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 22%); mask-image: linear-gradient(90deg, transparent 0, #000 22%); }
.these-foto { position: absolute; right: 0; top: 0; width: 900px; height: var(--buehne-h); object-fit: cover; margin: 0 !important; max-width: none !important; max-height: none !important;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 36%); mask-image: linear-gradient(90deg, transparent 0, #000 36%); }

/* So arbeiten wir: KI-Video vollflächig, auf Klick die Auflösung */
.sa-video { position: absolute; left: 0; top: 0; width: 1920px; height: var(--buehne-h); object-fit: cover; margin: 0 !important; max-width: none !important; max-height: none !important; background: #F2F2F2; }
.sa-titel { position: absolute; left: 60px; top: 50px; margin: 0; padding: 10px 24px 12px; border-radius: 14px; background: rgba(21,18,28,.86); font-size: 40px; font-weight: 700; letter-spacing: -.01em; text-transform: uppercase; }
.sa-aufloesung { position: absolute; inset: calc(-1 * var(--extra)) 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: rgba(8,6,12,.84); }
.sa-aufloesung .hero { font-size: 190px; }
.sa-aufloesung p { margin: 18px 0 0; font-size: 44px; color: var(--w-70); }
.sa-kennung { position: absolute; right: 150px; bottom: 26px; margin: 0; padding: 6px 14px; border-radius: 8px; background: rgba(21,18,28,.7); font-size: 20px; letter-spacing: .04em; color: rgba(244,246,255,.85); }

/* Was KI heute kann: Bento aus fünf Kacheln mit echtem Material */
.ki-bento { flex: 1; min-height: 0; margin-top: 14px; display: grid; gap: 22px; grid-template-columns: 570px 1fr 500px; grid-template-rows: 1.12fr 1fr;
  grid-template-areas: "bild video avatar" "text stimme avatar"; }
.kachel { position: relative; margin: 0; overflow: hidden; border-radius: 22px; background: #0F0C16; border: 1px solid rgba(244,246,255,.09); }
.k-bild { grid-area: bild; } .k-video { grid-area: video; } .k-avatar { grid-area: avatar; } .k-text { grid-area: text; } .k-stimme { grid-area: stimme; }
.kachel > img, .kachel > video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; margin: 0 !important; max-width: none !important; max-height: none !important; }
.kachel figcaption { position: absolute; left: 24px; bottom: 18px; z-index: 3; font-size: 22px; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; color: #fff; }
.kachel.medien::after { content: ""; position: absolute; inset: auto 0 0 0; height: 38%; z-index: 2; background: linear-gradient(180deg, transparent, rgba(5,4,10,.78)); pointer-events: none; }
/* Bild: das Foto blendet langsam ins KI-Bild über, das Etikett wechselt mit */
.k-bild .nachher { opacity: 0; }
.k-bild .marke { position: absolute; left: 20px; top: 18px; z-index: 3; display: grid; justify-items: center; padding: 7px 16px; border-radius: 999px; background: rgba(5,4,10,.62); font-size: 20px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.k-bild .marke i { grid-area: 1 / 1; font-style: normal; }
.k-bild .m-nach { color: var(--th-hell); opacity: 0; }
.reveal .slides section.present .k-bild .nachher, .reveal .slides section.present .k-bild .m-nach { animation: ki-nacht 10s ease-in-out .8s infinite; }
.reveal .slides section.present .k-bild .m-vor { animation: ki-tag 10s ease-in-out .8s infinite; }
@keyframes ki-nacht { 0%, 22% { opacity: 0; } 34%, 88% { opacity: 1; } 100% { opacity: 0; } }
@keyframes ki-tag { 0%, 22% { opacity: 1; } 34%, 88% { opacity: 0; } 100% { opacity: 1; } }
body.standbild .k-bild .nachher, body.standbild .k-bild .m-nach { animation: none !important; opacity: 1; }
body.standbild .k-bild .m-vor { animation: none !important; opacity: 0; }
.k-avatar > img { object-position: 50% 40%; }
/* Schreiben: Text tippt sich, roter Cursor blinkt */
.k-text { background: #F4F6FF; border: 0; }
.k-text figcaption { color: rgba(15,12,22,.45); }
.tipp { margin: 0; padding: 34px 36px 0; font-size: 31px; line-height: 1.42; font-weight: 500; color: #15121C; white-space: pre-line; }
.tipp .cursor { display: inline-block; width: 3px; height: 1.05em; margin-left: 3px; vertical-align: -.16em; background: var(--th); animation: ki-cursor 1s steps(1) infinite; }
@keyframes ki-cursor { 50% { opacity: 0; } }
/* Stimme: Knopf und die echte Wellenform der Aufnahme, beim Abspielen färbt sie sich durch */
.k-stimme { display: flex; align-items: center; gap: 34px; padding: 0 40px 30px; }
.k-stimme .knopf { flex: none; width: 96px; height: 96px; border-radius: 50%; background: var(--th); position: relative; cursor: pointer; }
.k-stimme .knopf::before { content: ""; position: absolute; left: 38px; top: 29px; border-style: solid; border-width: 19px 0 19px 30px; border-color: transparent transparent transparent #fff; }
.k-stimme.spielt .knopf { animation: ki-puls 1.2s ease-in-out infinite; }
@keyframes ki-puls { 50% { box-shadow: 0 0 0 16px rgba(228,0,58,.18); } }
.welle { flex: 1; height: 170px; display: flex; align-items: center; gap: 5px; }
.welle i { flex: 1; height: calc(var(--h) * 100%); border-radius: 3px; background: rgba(244,246,255,.26); transition: background .15s; }
.welle i.an { background: linear-gradient(180deg, var(--th-hell), var(--th)); }
.k-stimme audio { display: none; }

/* Kurve: Moore gegen KI, in TH-Rot */
.kurve { width: 100%; height: auto; margin-top: 30px; overflow: visible; }
.kurve .jahre text { font-size: 24px; fill: rgba(244,246,255,.45); font-family: var(--font); }
.kurve .kurven-name { font-size: 30px; font-weight: 700; font-family: var(--font); opacity: 0; }
.kurve .kurven-name.ki { fill: var(--th-hell); }
.kurve .kurven-name.moore { fill: rgba(244,246,255,.7); }
.kurve .linie { stroke-dasharray: 1; stroke-dashoffset: 1; }
.reveal section.present .kurve .linie.moore { animation: zeichnen 2.4s .3s ease-out forwards; }
.reveal section.present .kurve .linie.ki { animation: zeichnen 1.6s 1.2s ease-in forwards; }
.reveal section.present .kurve .kurven-name.moore { animation: auftauchen .6s 2.5s forwards; }
.reveal section.present .kurve .kurven-name.ki { animation: auftauchen .6s 2.8s forwards; }
body.standbild .kurve .linie { stroke-dashoffset: 0; }
body.standbild .kurve .kurven-name { opacity: 1; }
@keyframes zeichnen { to { stroke-dashoffset: 0; } }

/* Alles KI: vier Bilder aus diesem Vortrag */
.alles-ki { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px 26px; margin-top: auto; margin-bottom: auto; }
.reveal section.present .alles-ki figure { animation: kachel-ein .5s calc(.2s + var(--i) * .1s) cubic-bezier(.2,.8,.3,1) both; }
body.standbild .alles-ki figure { animation: none !important; }
.alles-ki figure { margin: 0; }
.alles-ki img { width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 8px; display: block; margin: 0 !important; outline: 1.5px solid rgba(228,0,58,.55); outline-offset: 0; }
.alles-ki figcaption { margin-top: 10px; font-size: 22px; color: var(--w-45); letter-spacing: .06em; }

/* Statement */
.zitat { font-size: 104px; line-height: 1.1; font-weight: 700; letter-spacing: -.02em; margin: 0; max-width: 1640px; text-transform: uppercase; }

/* Pizza (aus dem Stamm) */
.pizza { display: grid; grid-template-columns: auto 1px auto; justify-content: center; gap: 90px; flex: 1; align-items: stretch; }
.pizza .trennlinie { background: linear-gradient(180deg, transparent, rgba(244,246,255,.25), transparent); }
.pizza > div:not(.trennlinie) { display: flex; flex-direction: column; align-items: center; text-align: center; }
.pizza .label { margin-bottom: 26px; }
.pizza .label.gut { color: var(--th-hell); }
.pizza .ansage { min-height: 170px; display: flex; align-items: center; justify-content: center; margin: 0; font-weight: 700; }
.pizza .ansage.kurz { font-size: 88px; }
.pizza .ansage.lang { font-size: 34px; line-height: 1.4; white-space: nowrap; font-weight: 600; }
.pizza img { height: 420px; width: auto; display: block; margin: 20px 0 !important; }

/* Kompass */
.kompass { display: flex; flex-direction: column; margin-top: auto; margin-bottom: auto; }
.kompass-zeile { display: grid; grid-template-columns: 560px 1fr; align-items: center; gap: 40px; padding: 40px 0; border-top: 1px solid var(--hairline); }
.kompass-zeile:last-child { border-bottom: 1px solid var(--hairline); }
.kompass-zeile .kopf { font-size: 64px; font-weight: 700; text-transform: uppercase; letter-spacing: .02em; color: var(--th-hell); }
.kompass-zeile b { font-size: 50px; font-weight: 600; }
.kompass-zeile span { font-size: 33px; line-height: 1.35; color: var(--w-70); }

/* Prompt und Antwort */
.demo { display: grid; grid-template-columns: 1fr 1fr; gap: 50px; margin-top: auto; margin-bottom: auto; align-items: start; }
.prompt, .antwort { border-radius: 20px; padding: 34px 40px 36px; }
.prompt { background: rgba(228,0,58,.08); border: 1.5px solid rgba(228,0,58,.55); }
.antwort { background: rgba(244,246,255,.04); border: 1.5px solid rgba(244,246,255,.14); }
.prompt-label { display: block; font-size: 19px; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; color: var(--th-hell); margin-bottom: 18px; }
.antwort .prompt-label { color: var(--w-45); }
.prompt p, .antwort p { margin: 0; font-size: 37px; line-height: 1.45; }
.prompt.klein p { font-size: 34px; }
.prompt p { font-weight: 600; }
.antwort p { color: var(--w-70); }
.antwort p b { color: var(--weiss); }
.antwort .nach { color: var(--th-hell); font-weight: 600; }
.risiken { list-style: none; margin: 0; padding: 0; counter-reset: r; }
.risiken li { position: relative; font-size: 35px; line-height: 1.42; color: var(--w-70); padding: 18px 0 18px 66px; border-top: 1px solid var(--hairline); }
.risiken li:first-child { border-top: none; padding-top: 0; }
.risiken li::before { counter-increment: r; content: counter(r); position: absolute; left: 0; top: 16px; width: 44px; height: 44px; border-radius: 50%; border: 2px solid var(--th); display: grid; place-items: center; font-size: 24px; font-weight: 700; color: var(--weiss); }
.risiken li:first-child::before { top: -2px; }
.demo-kopf { display: flex; align-items: center; gap: 22px; }
.demo-kopf .headline { margin: 0; }

/* Lernseite im Rahmen */
.bauen { display: grid; grid-template-columns: 560px 1fr; gap: 50px; flex: 1; margin-top: 36px; min-height: 0; }
.bauen .prompt { align-self: start; }
.bauen .prompt p { font-size: 29px; }
.fenster { border-radius: 16px; overflow: hidden; border: 1.5px solid rgba(244,246,255,.18); background: #0B0A10; display: flex; flex-direction: column; min-height: 0; }
.fenster-leiste { height: 44px; display: flex; align-items: center; gap: 9px; padding: 0 18px; background: #16131D; flex-shrink: 0; }
.fenster-leiste i { width: 13px; height: 13px; border-radius: 50%; background: rgba(244,246,255,.18); }
.fenster-leiste span { margin-left: 14px; font-size: 16px; color: var(--w-45); letter-spacing: .04em; }
.fenster.gross { flex: 1; margin-top: 30px; }
.fenster iframe { flex: 1; width: 100%; border: 0; display: block; background: #0B0A10; }

/* Trotzdem gemacht */
.trotzdem-foto { object-position: 50% 62%; }

/* Faktencheck */
.faktencheck { display: flex; flex-direction: column; gap: 0; margin-top: 70px; max-width: 1300px; }
.faktencheck > div { display: flex; align-items: center; gap: 40px; padding: 30px 0; border-top: 1px solid var(--hairline); }
.faktencheck > div:last-child { border-bottom: 1px solid var(--hairline); }
.faktencheck .icon { width: 74px; height: 74px; color: var(--th-hell); flex-shrink: 0; }
.faktencheck p { margin: 0; font-size: 50px; font-weight: 700; }

/* Studie */
.studie { display: flex; flex-direction: column; justify-content: center; flex: 1; }
.riesig { font-size: 300px; line-height: .95; font-weight: 700; letter-spacing: -.04em; margin: 16px 0 0; }
.riesig small { font-size: 72px; letter-spacing: -.01em; margin-left: 28px; color: var(--weiss); -webkit-text-fill-color: var(--weiss); }
.nebenzahlen { display: flex; gap: 90px; margin-top: 40px; font-size: 44px; font-weight: 600; color: var(--w-70); }
.nebenzahlen b { color: var(--weiss); }

/* Das Handy ist nur das Fenster */
.fenster-bild { position: absolute; left: 0; top: calc(var(--extra) + 60px); width: 1920px; height: 1080px; object-fit: cover; margin: 0 !important; max-width: none !important; max-height: none !important; }
.fenster-erklaerung { position: absolute; left: 890px; top: calc(var(--extra) + 470px); transform: translateX(-50%); white-space: nowrap; margin: 0; text-align: center; font-size: 34px; line-height: 1.45; font-weight: 600; color: var(--w-90, rgba(244,246,255,.9)); text-shadow: 0 2px 18px rgba(0,0,0,.9); }
.fenster-name { position: absolute; top: calc(var(--extra) + 60px + 1080px * .86); transform: translateX(-50%); font-size: 32px; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; white-space: nowrap; padding: 6px 16px; border-radius: 8px; background: rgba(3,3,9,.78); }

/* Seit letztem November: Wand wächst */
.wachstum-folie { padding-bottom: 70px; }
.wachstum { position: relative; display: flex; flex-direction: column; gap: 34px; margin-top: auto; margin-bottom: auto; }
.wachstum-trigger { position: absolute; width: 1px; height: 1px; opacity: 0; }
.wachstum-gross { display: grid; grid-template-columns: repeat(5, 1fr); gap: 50px; align-items: center; min-height: 130px; }
.wachstum-gross div { display: flex; align-items: center; justify-content: center; height: 130px; }
.wachstum-gross img { max-width: 290px; max-height: 120px; width: auto; height: auto; margin: 0 !important; filter: drop-shadow(0 0 22px rgba(228,0,58,.55)); }
.wachstum-wand { display: grid; grid-template-columns: repeat(11, 1fr); grid-auto-rows: 84px; gap: 8px 26px; align-items: center; }
.wachstum-wand div { display: flex; align-items: center; justify-content: center; height: 84px; }
.wachstum-wand img { max-width: 100%; max-height: 54px; width: auto; height: auto; margin: 0 !important; }
.wachstum .alt { transition: opacity .8s ease; }
.wachstum .neu { opacity: 0; transform: scale(.6); }
.wachstum:has(.wachstum-trigger.visible) .alt { opacity: .28; }
.wachstum:has(.wachstum-trigger.visible) .neu { animation: aufploppen .45s calc(var(--i) * 45ms) cubic-bezier(.2,.9,.3,1.3) forwards; }
@keyframes aufploppen { to { opacity: 1; transform: none; } }
body.standbild .wachstum .neu { opacity: 1; transform: none; animation: none; }
body.standbild .wachstum .alt { opacity: .28; }

/* Eisberg: über Wasser nur der Prompt, auf Klick taucht alles darunter auf.
   Bild und Begriffe teilen sich eine 1920 x 1080 Bühne, damit Wasserlinie (y 258) und Eisblock (Mitte x 1320) zusammenpassen. */
.eisberg-buehne { position: absolute; left: 0; top: 0; width: 1920px; height: var(--buehne-h); background: linear-gradient(180deg, #04030D 0, #04030D 50%, #01040F 50%, #01040F 100%); }
.eis-innen { position: absolute; left: 0; top: var(--extra); width: 1920px; height: 1080px; }
.eis-innen > img { position: absolute; inset: 0; width: 1920px; height: 1080px; margin: 0 !important; max-width: none !important; max-height: none !important; }
.eis-wasser { position: absolute; left: 0; top: 262px; width: 1920px; height: calc(818px + var(--extra)); background: linear-gradient(180deg, rgba(1,4,18,.55) 0, rgba(1,4,18,.97) 70px, #01040F 100%); transition: opacity 1.6s ease; }
.eisberg-trigger { position: absolute; width: 1px; height: 1px; opacity: 0; }
.eis-spitze { position: absolute; left: 1320px; top: 52px; transform: translateX(-50%); padding: 10px 28px; border-radius: 10px; background: linear-gradient(135deg, #E4003A, #FF5C7A); color: #fff; font-size: 32px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; filter: drop-shadow(0 0 26px rgba(228,0,58,.6)); }
.eis-schicht { position: absolute; left: 1320px; top: var(--y); transform: translate(-50%, 18px); padding: 8px 24px; border-radius: 10px; background: rgba(1,4,18,.55); border: 1.5px solid rgba(190,225,255,.35); color: #EAF4FF; font-size: 28px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; white-space: nowrap; opacity: 0; transition: opacity .5s, transform .5s; }
.eis-innen:has(.eisberg-trigger.visible) .eis-wasser { opacity: 0; }
.eis-innen:has(.eisberg-trigger.visible) .eis-schicht { opacity: 1; transform: translate(-50%, 0); transition-delay: calc(.9s + var(--i) * .12s); }
body.standbild .eis-wasser { opacity: 0; }
body.standbild .eis-schicht { opacity: 1; transform: translate(-50%, 0); }
body.hochkant .eisberg-buehne { transform: scale(.5625); transform-origin: top left; top: 1100px; }

/* Route: krumme Linie durch echte Stationen */
.route { width: 100%; height: auto; margin-top: auto; overflow: visible; }
.route .linie, .route .schein { stroke-dasharray: 1; stroke-dashoffset: 1; }
.route .schein { opacity: .25; }
.route .station { opacity: 0; }
.route .station circle { fill: #F4F6FF; }
.route .station text { font-family: var(--font); font-size: 34px; font-weight: 700; fill: #F4F6FF; }
.route .station:last-child circle { fill: #7FD4FF; }
.route .station:last-child text { fill: #7FD4FF; font-size: 44px; }
.reveal section.present .route .linie, .reveal section.present .route .schein { animation: zeichnen 4.2s .4s cubic-bezier(.45,.05,.4,1) forwards; }
.reveal section.present .route .station { animation: auftauchen .4s calc(.6s + var(--i) * .7s) forwards; }
body.standbild .route .linie, body.standbild .route .schein { stroke-dashoffset: 0; }
body.standbild .route .station { opacity: 1; }

/* Zehn-Sekunden-Ring */
.ring-zeit { position: relative; width: 190px; height: 190px; margin: 70px auto 0; }
.ring-zeit svg { width: 100%; height: 100%; transform: rotate(-90deg); overflow: visible; }
.ring-zeit .spur { fill: none; stroke: rgba(244,246,255,.14); stroke-width: 8; }
.ring-zeit .lauf { fill: none; stroke: #7FD4FF; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 534; stroke-dashoffset: 534; filter: drop-shadow(0 0 10px rgba(127,212,255,.6)); }
.ring-zeit .ausloeser { position: absolute; width: 1px; height: 1px; opacity: 0; }
.ring-zeit:has(.ausloeser.visible) .lauf { animation: ring-fuellen 10s linear forwards; }
@keyframes ring-fuellen { to { stroke-dashoffset: 0; } }
body.standbild .ring-zeit .lauf { stroke-dashoffset: 0; animation: none; }

/* These 1: nachgestellter Betriebs-Post plus echte Chatnachrichten */
.nervt { flex-direction: row !important; align-items: center; justify-content: space-between; gap: 60px; }
.post-buehne { position: relative; width: 820px; height: 860px; flex-shrink: 0; }
.post { position: absolute; right: 0; top: 0; width: 700px; background: #FFFFFF; color: #1C1E21; border-radius: 14px; padding: 22px 0 0; transform: rotate(2.5deg); font-family: Helvetica, Arial, sans-serif; }
.post-kopf { display: flex; align-items: center; gap: 14px; padding: 0 22px; }
.post-kopf i { width: 56px; height: 56px; border-radius: 50%; background: #C9A26B; color: #fff; font-style: normal; font-weight: 700; font-size: 28px; display: grid; place-items: center; }
.post-kopf b { display: block; font-size: 24px; }
.post-kopf span { font-size: 18px; color: #65676B; }
.post-text { margin: 16px 22px 14px; font-size: 26px; }
.post img { width: 100%; height: 470px; object-fit: cover; display: block; margin: 0 !important; max-width: none !important; }
.post-fuss { display: flex; justify-content: space-between; padding: 16px 22px 20px; font-size: 21px; color: #65676B; border-top: 1px solid #E4E6EB; }
.post-fuss .daumen { font-weight: 700; color: #1C1E21; }
.nachgestellt { position: absolute; right: 18px; top: -40px; font-size: 18px; letter-spacing: .14em; text-transform: uppercase; color: var(--w-45); font-family: var(--font); transform: rotate(-2.5deg); }
.post-chat { position: absolute; left: -40px; bottom: 30px; display: flex; flex-direction: column; align-items: flex-start; gap: 12px; }
.post-chat .blase { opacity: 1; animation: none !important; font-size: 36px; max-width: none; border-radius: 4px 18px 18px 18px; }
.reveal section.present .post-chat .blase { animation: hochkommen .45s .6s both !important; }
.reveal section.present .post-chat .blase + .blase { animation-delay: 1.3s !important; }
body.standbild .reveal section .post-chat .blase, body.standbild .reveal section.present .post-chat .blase { animation: none !important; opacity: 1; }
body.hochkant .nervt { flex-direction: column !important; }

/* Orbit: echte Fotos kreisen um „Du“ (Idee aus dem Charta-Deck) */
.orbit { position: absolute; left: 0; top: var(--extra); width: 1920px; height: 1080px; pointer-events: none; }
.orbit .o { position: absolute; left: 0; top: 0; width: 230px; height: 230px; border-radius: 50%; object-fit: cover; margin: 0 !important; max-width: none !important; border: 4px solid rgba(244,246,255,.9); will-change: transform; }
.orbit-du { position: absolute; left: 1420px; top: 540px; width: 260px; height: 260px; margin: -130px 0 0 -130px; border-radius: 50%; display: grid; place-items: center;
  background: radial-gradient(circle at 35% 30%, #FF5C7A, #E4003A 60%, #9A0027); font-size: 76px; font-weight: 700; letter-spacing: .02em; text-transform: uppercase; color: #fff; filter: drop-shadow(0 0 40px rgba(228,0,58,.6)); }
body.hochkant .orbit { top: 600px; left: -840px; }

/* Berufe: Balken */
.balken { display: flex; flex-direction: column; gap: 26px; margin-top: auto; margin-bottom: auto; }
.balken-zeile { display: grid; grid-template-columns: 560px 1fr 120px 200px; align-items: center; gap: 30px; }
.balken-zeile .beruf { font-size: 40px; font-weight: 700; }
.balken-zeile .spur { height: 26px; border-radius: 13px; background: rgba(244,246,255,.07); overflow: hidden; }
.balken-zeile .spur i { display: block; height: 100%; border-radius: 13px; background: linear-gradient(90deg, #E4003A, #FF9FB1); }
.balken-zeile b { font-size: 40px; font-weight: 700; text-align: right; }
.balken-zeile .platz { font-size: 26px; color: var(--w-45); font-weight: 600; letter-spacing: .04em; }
.balken-zeile:first-child .beruf, .balken-zeile:first-child b { color: var(--th-hell); }
.quelle-klein { font-size: 22px; color: var(--w-45); letter-spacing: .08em; font-weight: 600; margin: 0; }

/* Geldautomat */
.automat-bild { object-position: 70% 50%; }

/* Drei Zukünfte: Bedingung oben, Ergebnis in Jahren groß */
.fussquelle { position: absolute; right: 130px; bottom: 34px; margin: 0; font-size: 19px; letter-spacing: .02em; color: rgba(244,246,255,.42); }
.unterzeile-klar { font-size: 34px; color: var(--w-70); margin: 10px 0 0; font-weight: 500; }
.szenarien { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 60px; margin-top: auto; margin-bottom: auto; }
.szenario { display: flex; flex-direction: column; padding-top: 28px; border-top: 2px solid var(--hairline); }
.szenario .wenn { margin: 0; font-size: 38px; line-height: 1.3; font-weight: 600; min-height: 150px; }
.szenario .wenn span { color: var(--w-45); }
.szenario .jahre { margin-top: 26px; font-size: 110px; line-height: 1; font-weight: 700; letter-spacing: -.02em; color: rgba(244,246,255,.55); white-space: nowrap; }
.szenario.s1 .jahre { color: var(--th-zart); }
.szenario.s2 .jahre { color: var(--th-hell); }
.szenario.s2 { border-top-color: var(--th); }
.szenario .jahre small { font-size: 50px; font-weight: 600; margin-right: 8px; }
.szenario .prozent { margin-top: 16px; font-size: 26px; color: var(--w-45); letter-spacing: .03em; }
.offen { font-size: 52px; font-weight: 700; margin: 10px 0 0; }

/* Ende */
.ende-foto { position: absolute; right: 0; top: 0; width: 960px; height: var(--buehne-h); object-fit: cover; object-position: 35% 50%; margin: 0 !important; max-width: none !important; max-height: none !important;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 20%); mask-image: linear-gradient(90deg, transparent 0, #000 20%); }
body.hochkant .ende-foto { width: 1080px; height: 900px; top: auto; bottom: 0; -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 40%); mask-image: linear-gradient(180deg, transparent 0, #000 40%); }
.slide.schluss { justify-content: center; }
.slide.schluss .hero { font-size: 112px; max-width: 1100px; }
.slide.schluss .kontakt { position: static; margin-top: 80px; display: flex; align-items: center; gap: 36px; }
.slide.schluss .kontakt img { width: 280px; height: auto; margin: 0; }
.slide.schluss .kontakt p { margin: 0; font-size: 28px; line-height: 1.55; color: var(--w-70); border-left: 1px solid var(--hairline); padding-left: 36px; font-weight: 500; }
.slide.schluss .kontakt p b { color: var(--weiss); }
.qr { position: absolute; right: 130px; top: calc(var(--extra) + 300px); display: flex; flex-direction: column; align-items: center; gap: 20px; }
.qr img { width: 300px; height: 300px; border-radius: 16px; background: #fff; padding: 16px; margin: 0 !important; }
.qr span { font-size: 24px; font-weight: 600; color: var(--w-70); }

/* ---------- Hochkant (Handy) ---------- */
body.hochkant .deckblatt .hero { font-size: 96px; }
body.hochkant .titel-duo .th-logo { height: 100px; }
body.hochkant .titel-duo .edge-logo { height: 80px; }
body.hochkant .ecken { flex-direction: column; gap: 10px; }
body.hochkant .frage-gross { font-size: 96px; }
body.hochkant .nein { font-size: 300px; }
body.hochkant .weil-liste li { font-size: 50px; }
body.hochkant .duo { flex-direction: column; gap: 60px; align-items: center; }
body.hochkant .chat-buehne { grid-template-columns: 1fr; gap: 50px; }
body.hochkant .namen-buehne, body.hochkant .namen-buehne .wurde { flex-direction: column; gap: 50px; }
body.hochkant .fotowand { width: 1080px; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(6, 1fr); }
body.hochkant .fotoreihe { grid-template-columns: 1fr 1fr; }
body.hochkant .polaroid img { height: 420px; }
body.hochkant .slide.team { flex-direction: column !important; align-items: center; padding: 260px 60px 130px; }
body.hochkant .mitte { display: contents; }
body.hochkant .seite { flex: none; width: 100%; margin-top: 70px; }
body.hochkant .drei { grid-template-columns: 1fr; gap: 50px; }
body.hochkant .icons { grid-template-columns: repeat(2, 1fr); gap: 70px 30px; }
body.hochkant .these { font-size: 88px; }
body.hochkant .these-foto { width: 1080px; height: 900px; top: auto; bottom: 0; -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 40%); mask-image: linear-gradient(180deg, transparent 0, #000 40%); }
body.hochkant .ki-bento { grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr 1.3fr; grid-template-areas: "bild video" "text stimme" "avatar avatar"; }
body.hochkant .alles-ki { grid-template-columns: 1fr 1fr; }
body.hochkant .zitat { font-size: 78px; }
body.hochkant .pizza { grid-template-columns: 1fr; gap: 50px; }
body.hochkant .pizza .trennlinie { display: none; }
body.hochkant .pizza img { height: 300px; }
body.hochkant .kompass-zeile { grid-template-columns: 1fr; gap: 12px; }
body.hochkant .demo, body.hochkant .bauen { grid-template-columns: 1fr; }
body.hochkant .fenster { height: 900px; }
body.hochkant .faktencheck p { font-size: 42px; }
body.hochkant .riesig { font-size: 190px; }
body.hochkant .nebenzahlen { flex-direction: column; gap: 16px; }
body.hochkant .slide.schluss .hero { font-size: 84px; }
body.hochkant .qr { position: static; margin-top: 60px; align-items: flex-start; }
body.hochkant .zitat, body.hochkant .headline { white-space: normal !important; }
body.hochkant .fenster-bild { width: 1080px; height: 608px; top: 700px; }
body.hochkant .fenster-name { top: 1330px; font-size: 26px; }
body.hochkant .balken-zeile { grid-template-columns: 1fr 100px; }
body.hochkant .balken-zeile .spur, body.hochkant .balken-zeile .platz { grid-column: 1 / -1; }
/* Handy hochkant: die Bühne ist so hoch wie das Handy (--extra oben und unten), alles Absolute rechnet --extra mit ein */
body.hochkant .kennen-titel { font-size: 84px !important; }
body.hochkant .polaroid.gruendung { width: 460px; top: calc(var(--extra) + 450px); }
body.hochkant .polaroid.gruendung img { height: 500px; }
body.hochkant .polaroid.gruendung:nth-of-type(1) { left: 60px !important; }
body.hochkant .polaroid.gruendung:nth-of-type(2) { left: 560px !important; }
body.hochkant .polaroid.gruendung:nth-of-type(3) { left: 60px !important; top: calc(var(--extra) + 1110px); }
body.hochkant .polaroid.gruendung:nth-of-type(4) { left: 560px !important; top: calc(var(--extra) + 1110px); }
body.hochkant .epg-szene { top: calc(var(--extra) + 735px); transform-origin: 0 0; transform: translateX(-31px) scale(.582); }
body.hochkant .dom-szene { top: calc(var(--extra) + 571px); transform-origin: 0 0; transform: translateX(-260px) scale(.78); }
body.hochkant .epg-label { left: 70px; top: 330px; font-size: 56px; }
body.hochkant .bueros { grid-template-columns: repeat(6, 1fr); gap: 44px 24px; margin-top: 90px; padding: 0; }
body.hochkant .polaroid.buero { grid-column: span 2; }
body.hochkant .polaroid.buero:nth-child(4) { grid-column: 2 / span 2; }
body.hochkant .polaroid.buero:nth-child(5) { grid-column: 4 / span 2; }
body.hochkant .polaroid.buero img { height: 400px; }
body.hochkant .slide.team { display: grid !important; grid-template-columns: 1fr 1fr; grid-template-areas: "emre emre" "service software" "du du"; align-content: center; justify-items: center; gap: 70px 16px; padding: 250px 30px 120px; }
body.hochkant .slide.team .team-titel { top: 170px; font-size: 64px; }
body.hochkant .slide.team .person.gf { grid-area: emre; }
body.hochkant .slide.team .person.du { grid-area: du; }
body.hochkant .slide.team .seite.service { grid-area: service; margin: 0; }
body.hochkant .slide.team .seite.software { grid-area: software; margin: 0; }
body.hochkant .slide.team .person.gross .rund { width: 250px; height: 250px; }
body.hochkant .slide.team .person.gf .rund { width: 290px; height: 290px; }
body.hochkant .slide.team .person.du .rund { width: 220px; height: 220px; }
body.hochkant .slide.team .reihe { gap: 10px; margin-top: 44px; }
body.hochkant .slide.team .reihe .rund { width: 150px; height: 150px; }
body.hochkant .slide.team .reihe figcaption b { font-size: 30px; }
body.hochkant .slide.team .reihe figcaption span { font-size: 21px; max-width: 168px; }
body.hochkant .slide.team .person.du figcaption span { font-size: 30px; }
body.hochkant section:has(> .polaroid.stapel) .slide, body.hochkant section:has(> .orbit) .slide { justify-content: flex-start !important; padding-top: 300px; }
body.hochkant .polaroid.stapel:nth-of-type(1) { left: 50px !important; top: calc(var(--extra) + 600px) !important; width: 640px !important; }
body.hochkant .polaroid.stapel:nth-of-type(2) { left: 700px !important; top: calc(var(--extra) + 640px) !important; width: 340px !important; }
body.hochkant .polaroid.stapel:nth-of-type(3) { left: 40px !important; top: calc(var(--extra) + 1180px) !important; width: 320px !important; }
body.hochkant .polaroid.stapel:nth-of-type(4) { left: 385px !important; top: calc(var(--extra) + 1160px) !important; width: 300px !important; }
body.hochkant .polaroid.stapel:nth-of-type(5) { left: 705px !important; top: calc(var(--extra) + 1200px) !important; width: 340px !important; }
body.hochkant .headline[style*="max-width:1350px"] { max-width: 650px !important; }
body.hochkant .polaroid.quelle-foto { right: 46px; top: calc(var(--extra) + 160px); width: 290px; }
body.hochkant .polaroid.quelle-foto figcaption { font-size: 25px; }
body.hochkant .karte { height: 320px; }
body.hochkant .orbit { top: calc(var(--extra) + 820px); left: -880px; }
body.hochkant img.voll.foto-rechts { top: auto; bottom: 0; width: 1080px; height: 1250px; object-position: 88% 50%; -webkit-mask-image: linear-gradient(180deg, transparent 0, #000 22%); mask-image: linear-gradient(180deg, transparent 0, #000 22%); }
body.hochkant section:has(> img.foto-rechts) .schleier-links { display: none; }
body.hochkant section:has(> img.foto-rechts) .slide { justify-content: flex-start !important; padding-top: 420px; }
body.hochkant .sa-video { top: calc(var(--extra) + 660px); width: 1080px; height: 608px; }
body.hochkant .sa-titel { top: 560px; left: 60px; }
body.hochkant .sa-kennung { top: 1290px; bottom: auto; right: auto; left: 60px; }
body.hochkant .fenster-bild { top: calc(var(--extra) + 700px); }
body.hochkant .fenster-name { top: calc(var(--extra) + 1330px); }
body.hochkant .fenster-erklaerung { left: 540px; top: calc(var(--extra) + 470px); }
body.hochkant .szenarien { grid-template-columns: 1fr; gap: 56px; }
body.hochkant .szenario .wenn { min-height: 0; }
body.hochkant .slide.schluss { justify-content: flex-start !important; padding-top: 360px; }
body.hochkant .ende-foto { height: 1150px; }
"""



def wachstum(logos):
    """Folie Seit letztem November: zuerst die Wand von 2025, auf Klick kommen alle Neuen dazu."""
    nach_id = {l["id"]: l for l in logos}
    img = lambda l: f'<img src="assets/logos/ref-{l["id"]}.png" alt="{l["name"]}">'
    alt = [nach_id[i] for i in LOGOS_2025 if i in nach_id]
    gross = [nach_id[i] for i in LOGOS_NEU_GROSS]
    rest = [l for l in logos if l["id"] not in set(LOGOS_2025) | set(LOGOS_NEU_GROSS) | NICHT_AUF_DIE_WAND]
    reihe_gross = "".join(f'<div class="neu" style="--i:{k};">{img(l)}</div>' for k, l in enumerate(gross))
    wand = "".join(f'<div class="alt">{img(l)}</div>' for l in alt)
    wand += "".join(f'<div class="neu" style="--i:{k + 5};">{img(l)}</div>' for k, l in enumerate(rest))
    return f'''<div class="wachstum">
  <span class="wachstum-trigger fragment" aria-hidden="true"></span>
  <div class="wachstum-gross">{reihe_gross}</div>
  <div class="wachstum-wand">{wand}</div>
</div>'''


def eisberg():
    """Prompt über Wasser, darunter der Unterbau, von oben nach unten im Eisblock. Erscheint auf Klick."""
    unter = list(reversed(TURM))
    schichten = "".join(f'<div class="eis-schicht" style="--i:{k};--y:{336 + k * 80}px;">{s}</div>' for k, s in enumerate(unter))
    return f'''<div class="eisberg-buehne"><div class="eis-innen">
  <img src="assets/illu/eisberg.jpg" alt="Ein Eisberg: kleine Spitze über Wasser, riesige Masse darunter">
  <div class="eis-wasser"></div>
  <div class="eis-spitze">Prompt</div>
  <span class="eisberg-trigger fragment" aria-hidden="true"></span>
  {schichten}
</div></div>'''


# Unsere Route: Punkte im SVG (1660 x 600), mit Umweg und Schleife. Nur belegte Stationen.
# (name, x, y, versatz der beschriftung nach oben/unten): beschriftet wird dort, wo die Linie gerade nicht verläuft
ROUTE = [("Tag 1, 2019", 60, 520, 58), ("Corona, 2020", 430, 330, -34), ("Werkstudenten", 700, 470, 60), ("Gründung, 2022", 960, 250, -34),
         ("Master fertig, 2024", 1220, 360, 60), ("Heute", 1580, 70, -30)]


def route():
    """Krumme Linie durch unsere echten Stationen, mit einer Schleife zwischen Studium und Chat."""
    d = ("M60,520 C180,520 220,420 300,470 C380,520 420,600 330,560 C250,520 300,360 430,330 "
         "C540,305 600,500 700,470 C800,440 820,250 960,250 C1080,250 1100,400 1220,360 "
         "C1360,310 1430,120 1580,70")
    punkte = "".join(f'<g class="station" style="--i:{k};"><circle cx="{x}" cy="{y}" r="{16 if k == len(ROUTE) - 1 else 11}"/>'
                     f'<text x="{max(x, 150)}" y="{y + dy}" text-anchor="middle">{n}</text></g>'
                     for k, (n, x, y, dy) in enumerate(ROUTE))
    return f'''<svg class="route" viewBox="0 0 1660 600" aria-label="Unser Weg">
  <defs><linearGradient id="vl-route" x1="0" y1="0" x2="1660" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#E4003A"/><stop offset=".6" stop-color="#FF5C7A"/><stop offset="1" stop-color="#7FD4FF"/></linearGradient></defs>
  <path class="schein" pathLength="1" d="{d}" fill="none" stroke="url(#vl-route)" stroke-width="24" stroke-linecap="round"/>
  <path class="linie" pathLength="1" d="{d}" fill="none" stroke="url(#vl-route)" stroke-width="7" stroke-linecap="round"/>
  {punkte}
</svg>'''


def balken():
    zeilen = "".join(f'<div class="balken-zeile"><span class="beruf">{n}</span><div class="spur"><i style="width:{w / 0.5 * 100:.0f}%;"></i></div><b>{str(w).replace(".", ",") if w else "0"}</b><span class="platz">{pl}</span></div>' for n, w, pl in BERUFE)
    return f'<div class="balken">{zeilen}</div>'


def zukuenfte():
    """Drei Szenarien: oben die Bedingung, groß das Ergebnis in Jahren normalem Wachstum. Die Prozentzahlen stehen nur in den Notizen."""
    spalten = "".join(f'''<div class="szenario s{i}">
  <p class="wenn"><span>Wenn</span> {satz}</p>
  <b class="jahre">{jahre}</b>
</div>''' for i, (satz, wert, jahre) in enumerate(ZUKUENFTE))
    return f'<div class="szenarien">{spalten}</div>'


ORBIT_SKRIPT = """<script>
/* Orbit: Fotos laufen auf einer Ellipse um die Mitte. Vorne groß und deckend, hinten klein und blass.
   Läuft nur auf der sichtbaren Folie, im Standbild (PDF) steht er bei t=0. */
(function () {
  var t0 = performance.now(), lauf = null;
  function setzen(o, t) {
    var rx = +o.dataset.rx, ry = +o.dataset.ry, tempo = +o.dataset.tempo, mx = +o.dataset.mitteX, my = +o.dataset.mitteY;
    var bilder = o.querySelectorAll('.o'), n = bilder.length;
    bilder.forEach(function (b, i) {
      var w = t * tempo * 2 * Math.PI + i / n * 2 * Math.PI;
      var x = mx + Math.cos(w) * rx, y = my + Math.sin(w) * ry, tiefe = (Math.sin(w) + 1) / 2;
      b.style.transform = 'translate(' + (x - 115) + 'px,' + (y - 115) + 'px) scale(' + (0.7 + tiefe * 0.4) + ')';
      b.style.opacity = 0.5 + tiefe * 0.5;
      b.style.zIndex = Math.round(tiefe * 10) + (tiefe > 0.5 ? 10 : 0);
    });
  }
  function schleife(jetzt) {
    var f = Reveal.getCurrentSlide(), o = f && f.querySelector('.orbit');
    if (!o) { lauf = null; return; }
    setzen(o, document.body.classList.contains('standbild') ? 0 : (jetzt - t0) / 1000);
    lauf = requestAnimationFrame(schleife);
  }
  function start() {
    document.querySelectorAll('.orbit').forEach(function (o) { setzen(o, 0); });
    if (!lauf) lauf = requestAnimationFrame(schleife);
  }
  Reveal.on('ready', start); Reveal.on('slidechanged', start);
})();
</script>
"""


def ki_bento():
    """Fünf Kacheln, jede zeigt echtes Material statt eines Symbols: Bild, Video, Avatar, Text, Stimme."""
    import math
    balken = "".join(f'<i style="--h:{0.16 + 0.84 * math.sqrt(w):.2f};"></i>' for w in WELLE)
    return f'''<div class="ki-bento">
  <figure class="kachel medien k-bild">
    <img src="assets/fotos/ki-foto-vorher.jpg" alt="Foto des Seminargebäudes der TH Lübeck am Tag">
    <img class="nachher" src="assets/illu/titel.jpg" alt="Dasselbe Gebäude als KI-Bild bei Nacht">
    <span class="marke"><i class="m-vor">Foto</i><i class="m-nach">KI-Bild</i></span>
    <figcaption>Bilder</figcaption>
  </figure>
  <figure class="kachel medien k-video">
    <video src="assets/video/ki-maskottchen.mp4" poster="assets/video/ki-maskottchen.jpg" data-autoplay muted loop playsinline></video>
    <figcaption>Videos</figcaption>
  </figure>
  <figure class="kachel medien k-avatar">
    <img src="assets/fotos/ki-avatar.jpg" alt="Eddie neben einem KI-Avatar auf einem großen Bildschirm">
    <figcaption>Avatare</figcaption>
  </figure>
  <figure class="kachel k-text">
    <p class="tipp" data-text="{KI_TIPPTEXT}"><span class="getippt">{KI_TIPPTEXT}</span><span class="cursor"></span></p>
    <figcaption>Schreiben</figcaption>
  </figure>
  <figure class="kachel k-stimme">
    <span class="knopf" aria-hidden="true"></span>
    <div class="welle">{balken}</div>
    <audio src="assets/audio/ki-stimme.mp3" preload="auto"></audio>
    <figcaption>Stimmen</figcaption>
    <span class="fragment ki-ton"></span>
  </figure>
</div>'''


KI_SKRIPT = """<script>
/* Was KI heute kann: Text tippt sich beim Betreten der Folie, die Stimme startet mit dem nächsten Klick
   und färbt die Wellenform im Takt. Im Standbild (PDF) steht der fertige Text, nichts spielt. */
(function () {
  var standbild = document.body.classList.contains('standbild'), tippLauf = null;
  function tippen(f) {
    var p = f && f.querySelector('.tipp');
    clearTimeout(tippLauf);
    if (!p || standbild) return;
    var ziel = p.querySelector('.getippt'), text = p.dataset.text, i = 0;
    ziel.textContent = '';
    (function weiter() {
      ziel.textContent = text.slice(0, i);
      if (i++ < text.length) tippLauf = setTimeout(weiter, text[i - 2] === ',' || text[i - 2] === '.' ? 260 : 34);
    })();
  }
  function stimme(f) { return f && f.querySelector('.k-stimme'); }
  function anzeigen(k) {
    var a = k.querySelector('audio'), balken = k.querySelectorAll('.welle i');
    var anteil = a.duration ? a.currentTime / a.duration : 0, n = Math.round(anteil * balken.length);
    balken.forEach(function (b, i) { b.classList.toggle('an', i < n); });
    if (!a.paused && !a.ended) requestAnimationFrame(function () { anzeigen(k); });
    else k.classList.remove('spielt');
  }
  function spielen(k) {
    var a = k.querySelector('audio');
    a.currentTime = 0; a.play();
    k.classList.add('spielt'); anzeigen(k);
  }
  function stopp(k) { if (!k) return; var a = k.querySelector('audio'); a.pause(); k.classList.remove('spielt'); }
  Reveal.on('fragmentshown', function (e) { if (e.fragment.classList.contains('ki-ton')) spielen(stimme(Reveal.getCurrentSlide())); });
  Reveal.on('fragmenthidden', function (e) { if (e.fragment.classList.contains('ki-ton')) stopp(stimme(Reveal.getCurrentSlide())); });
  Reveal.on('slidechanged', function (e) { stopp(stimme(e.previousSlide)); tippen(e.currentSlide); });
  Reveal.on('ready', function (e) { tippen(e.currentSlide); });
  document.addEventListener('click', function (e) { var k = e.target.closest && e.target.closest('.k-stimme'); if (k) spielen(k); });
})();
</script>
"""


def kurve():
    """Moore's Law (Verdopplung alle 18 Monate) gegen KI (alle 6 Monate) über zehn Jahre, lineare Skala bis 100."""
    import math
    x0, x1, y0, y1 = 90, 1450, 560, 40
    px = lambda t: x0 + (x1 - x0) * t / 10
    py = lambda v: y0 - (y0 - y1) * min(v, 100) / 100
    def linie(halbwert, ende):
        schritte = [ende * i / 200 for i in range(201)]
        return "M" + " L".join(f"{px(t):.1f},{py(2 ** (t / halbwert)):.1f}" for t in schritte)
    ki_ende = 0.5 * math.log2(100)
    achsen = f'<path d="M{x0},{y1 - 10} L{x0},{y0} L{x1 + 20},{y0}" fill="none" stroke="rgba(244,246,255,.35)" stroke-width="2"/>'
    jahre = "".join(f'<text x="{px(t):.0f}" y="{y0 + 44}" text-anchor="middle">{t} J.</text>' for t in range(2, 11, 2))
    return f'''<svg class="kurve" viewBox="0 0 1520 640" aria-label="Moore's Law gegen KI-Wachstum">
  <defs><linearGradient id="vl-ki" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#E4003A"/><stop offset="1" stop-color="#FF9FB1"/></linearGradient></defs>
  {achsen}<g class="jahre">{jahre}</g>
  <path class="linie moore" pathLength="1" d="{linie(1.5, 10)}" fill="none" stroke="rgba(244,246,255,.55)" stroke-width="5" stroke-linecap="round"/>
  <path class="linie ki" pathLength="1" d="{linie(0.5, ki_ende)}" fill="none" stroke="url(#vl-ki)" stroke-width="8" stroke-linecap="round"/>
  <text class="kurven-name ki" x="{px(ki_ende) + 30:.0f}" y="{y1 + 20}">KI: alle 6 Monate doppelt</text>
  <text class="kurven-name moore" x="{x1}" y="{py(3):.0f}" text-anchor="end">Moore's Law: alle 18 Monate doppelt</text>
</svg>'''


# ----------------------------------------------------------------------------
# Folien
# ----------------------------------------------------------------------------

def bau():
    logos = json.loads((ORDNER / "assets/logos/referenzen.json").read_text(encoding="utf8"))
    # Die TH sitzt im Raum und steht schon auf dem Titel. Die Preisträger stehen unten in der Preisreihe.
    raus = {"thluebeck", "lnpreis", "socialhackathon", "startupsh"}
    logos = [l for l in logos if l["id"] not in raus]
    gross = [l for l in logos if l["klasse"] == "g"]
    klein = [l for l in logos if l["klasse"] == "k"]
    logo_img = lambda l: f'<div><img src="assets/logos/ref-{l["id"]}.png" alt="{l["name"]}" width="{l["w"]}" height="{l["h"]}"></div>'
    spalten = 10 if len(klein) <= 40 else (11 if len(klein) <= 44 else 12)
    preis_chips = "".join(f'<span class="preis"><b>{n}</b><img src="assets/logos/ref-{k}.png" alt=""></span>' for n, k in PREISE)

    icons_studium = "".join(f'<div class="fragment">{icon(k)}<p>{t}</p></div>' for k, t in NACH_DEM_STUDIUM)
    icons_ki = "".join(f'<div class="fragment">{icon(k)}<p>{t}</p></div>' for k, t in KI_NUTZUNG)
    icons_nie = "".join(f'<div>{icon(k)}<p>{t}</p></div>' for k, t in NIE_IN_DIE_KI)
    fakten = "".join(f'<div class="fragment">{icon(k)}<p>{t}</p></div>' for k, t in FAKTENCHECK)
    kompass = "".join(f'<div class="kompass-zeile"><span class="kopf">{k}</span><b>{f}</b></div>' for k, f in KOMPASS)
    # Polaroids: (bild, drehung in grad, versatz nach oben in px)
    polaroid = lambda fotos: "".join(f'<figure class="polaroid" style="--d:{d}deg;--y:{y}px;--i:{k};"><img src="assets/alt/{b}.jpg" alt="" loading="lazy"></figure>' for k, (b, d, y) in enumerate(fotos))
    emre_fotos = polaroid([("emre-2", -5, 30), ("emre-1", 3, -10), ("emre-4", -2, 40), ("emre-3", 5, 0)])
    eddie_fotos = polaroid([("eddie-2", 4, 10), ("eddie-1", -4, 40), ("eddie-3", 3, -15), ("eddie-4", -5, 25)])
    icons_berufe = "".join(f'<div class="fragment">{icon(k)}<p>{t}</p></div>' for k, t in BERUFE_RATEN)
    kante_ende = kunst_kante([(0, "#A8E4FF"), (.5, "#7FD4FF"), (1, "#4FC3FF")])
    qr = (f'<div class="qr"><img src="assets/qr-karte.png" alt="QR-Code zur Karte"><span>Alle Prompts zum Mitnehmen</span></div>' if KARTE_URL else "")
    hat_finale = (ORDNER / "assets/illu/finale.jpg").exists()
    hat_pause = (ORDNER / "assets/illu/pause.jpg").exists()
    finale_bild = '<img class="voll" src="assets/illu/finale.jpg" alt="Das Seminargebäude der TH Lübeck im Morgengrauen"><div class="schleier-links"></div>' if hat_finale else kante_ende
    pause_bild = '<img class="voll foto-rechts" src="assets/illu/pause.jpg" alt="Der EDGE-Roboter im Friesennerz bewacht in der Mensa das letzte Fischbrötchen"><div class="schleier-links"></div>' if hat_pause else ""

    folien = f'''
<!-- ============ TITEL ============ -->
<section class="f-th" data-chrome="aus" data-stimmung="th">
  <img class="voll" src="assets/illu/titel.jpg" alt="Das Seminargebäude der TH Lübeck bei Nacht, die Punktfassade leuchtet rot">
  <div class="schleier-links"></div>
  <div class="schleier-unten"></div>
  <div class="slide deckblatt">
    <div class="titel-duo">
      <img class="th-logo" src="assets/th/logo-thl-weiss.svg" alt="Technische Hochschule Lübeck">
      <span class="mal">×</span>
      <img class="edge-logo" src="assets/logos/edge-logo-white.png" alt="EDGE Digital">
    </div>
    <div>
      <h1 class="hero">Ehemalige Studierende.<br>Heute <span class="schimmer">Unternehmer.</span></h1>
      <p class="unterzeile">Der Reality Check</p>
      <div class="ecken"><span>Emre Erdogan &amp; Edgar Paul-Ghazaryan</span><span>Projektwoche · {DATUM}</span></div>
    </div>
  </div>
  {notizen("Ankommen lassen. Noch nichts sagen, bis es ruhig ist. Dann begrüßen Emre und Eddie gemeinsam, Dank an Herrn Balke. Kurz: zweieinhalb Stunden, eine Pause, zwischendurch Handzeichen, sonst müsst ihr nichts tun. Bild: das neue Seminargebäude bei Nacht, mit KI gebaut (wird später aufgelöst).")}
</section>

<!-- ============ WIEDER DA ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide links-mitte">
    <h2 class="hero" style="font-size:124px;">Wir sind<br><span class="schimmer">wieder da.</span></h2>
  </div>
  <figure class="polaroid platzhalter-foto" style="--d:4deg;--y:0px;--i:0;"><img src="assets/fotos/projektwoche-2025.jpg" alt="Emre, Herr Balke und Eddie vor der Tafel mit TH x EDGE"><figcaption>Projektwoche 2025</figcaption></figure>
  {notizen("Rückgriff aufs letzte Jahr: gleiche Projektwoche, gleiche Hochschule. Dank an Herrn Balke für die zweite Einladung. Das Foto ist vom letzten Mal, mit Herrn Balke in der Mitte.")}
</section>

<!-- ============ WESHALB ZUHÖREN ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide mittig">
    <h2 class="frage-gross">Weshalb solltest du<br>uns <span class="schimmer">zuhören?</span></h2>
  </div>
  {notizen("Die Frage vom letzten Jahr, bewusst wieder als Einstieg. Stehen lassen, zwei Sekunden Stille. Dann: Vielleicht weil …")}
</section>

<!-- ============ VIELLEICHT WEIL: FOTOWAND EVENTS ============ -->
<section class="f-th" data-stimmung="neutral" data-chrome="zahl">
  <img class="voll" src="assets/collage/collage.jpg" alt="Collage aus Bühnen, Preisverleihungen und Events">
  <div class="schleier-unten"></div>
  <div class="slide unten">
    <p class="vielleicht schatten">Vielleicht weil …</p>
  </div>
  {notizen("Nicht kommentieren, nur kurz wirken lassen. Bühnen, Preise, Hände schütteln. Ein, zwei Sätze, welche Bühne euch am meisten bedeutet hat. Dann weiter: oder weil …")}
</section>

<!-- ============ ODER WEIL: LOGOWAND ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide wand">
    <div class="wand-kopf"><p class="vielleicht">… oder weil …</p></div>
    <div class="logos gross">{"".join(logo_img(l) for l in gross)}</div>
    <hr class="trenner">
    <div class="logos klein" style="--spalten:{spalten};">{"".join(logo_img(l) for l in klein)}</div>
    <div class="preise"><span class="label">Gewonnen, ausgezeichnet, nominiert</span><div class="preis-reihe">{preis_chips}</div></div>
  </div>
  {notizen("Die Wand wirken lassen. Kein Logo einzeln erklären. Höchstens: Sparkasse, IHK, Staatskanzlei, die Stadt Lübeck. Die Preise unten nur nennen, nicht feiern.")}
</section>

<!-- ============ GANZ BESTIMMT ABER WEIL ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide links-mitte">
    <p class="vielleicht">… ganz bestimmt aber weil …</p>
    <ul class="weil-liste">
      <li class="fragment">wir auf <span>derselben</span> Hochschule waren wie ihr?</li>
      <li class="fragment">wir erfolgreich sind in dem, was wir tun?</li>
      <li class="fragment">wir dich inspirieren können?</li>
    </ul>
  </div>
  {notizen("Drei Klicks, je ein Grund. Jeden kurz anspielen, als wäre er die Antwort. Nach dem dritten: Pause.")}
</section>

<!-- ============ NEIN ============ -->
<section class="f-th" data-stimmung="th" data-chrome="zahl">
  <div class="slide mittig">
    <p class="nein schimmer">Nein.</p>
  </div>
  {notizen("Laut und kurz. Nein. Dann leiser: Wir sagen euch am Ende, weshalb. Oder besser, ihr sagt es uns. Erst mal: wer wir überhaupt sind.")}
</section>

<!-- ============ WER SIND WIR ============ -->
<section class="f-th" data-stimmung="th">
  <img class="duo-frei" src="assets/fotos/duo-frei.png" alt="Emre Erdogan und Edgar Paul-Ghazaryan">
  <div class="slide links-mitte">
    <h2 class="hero" style="font-size:118px;">Wer sind wir<br><span class="schimmer">überhaupt?</span></h2>
    <div class="namen-duo">
      <p><b>Emre Erdogan</b><span>Gründer und Geschäftsführer</span></p>
      <p><b>Edgar Paul-Ghazaryan</b><span>„Eddie“ · COO</span></p>
    </div>
  </div>
  {notizen("Kurze Vorstellung, Länge nach Gefühl. Beide haben hier an der TH BWL studiert, Bachelor und Master, Master fertig Anfang 2024. Persönliches kommt gleich noch, hier nur Name und Rolle. Links Emre, rechts Eddie.")}
</section>

<!-- ============ AGENDA ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Heute</h2>
    <div class="agenda">
      <div class="agenda-zeile">{ring(1)}<b>Unsere Geschichte</b></div>
      <div class="agenda-zeile">{ring(2)}<b>Der Reality Check</b></div>
      <div class="agenda-zeile pause"><span class="strich"></span><b>Pause</b></div>
      <div class="agenda-zeile">{ring(3)}<b>KI-Skills</b></div>
    </div>
  </div>
  {notizen("Der Ablauf in einem Satz pro Punkt. Zweieinhalb Stunden, in der Mitte eine Pause.")}
</section>

<!-- ============ EMRE ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide person-folie">
    <h2 class="headline">Emre <span class="schimmer">Erdogan</span></h2>
    <p class="rolle">Gründer und Geschäftsführer</p>
    <div class="fotoreihe">{emre_fotos}</div>
  </div>
  {notizen("Emre erzählt seine Geschichte. Kindheit, Familie, Abschluss, Trading. Die Fotos sind die Anker, die Länge ist frei.")}
</section>

<!-- ============ EDDIE ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide person-folie">
    <h2 class="headline">Edgar <span class="schimmer">Paul-Ghazaryan</span></h2>
    <p class="rolle">„Eddie“ · COO</p>
    <div class="fotoreihe">{eddie_fotos}</div>
  </div>
  {notizen("Eddie erzählt seine Geschichte. Familie, Bruder, VfB-Trikot, Nachmittag in der Sonne. Gleiche Länge wie bei Emre, damit es ausgewogen bleibt.")}
</section>

<!-- ============ UND DAS STUDIUM ============ -->
<section class="f-th" data-stimmung="neutral" data-chrome="zahl">
  {fotowand()}
  <div class="schleier-unten stark"></div>
  <div class="slide unten">
    <h2 class="hero kennen-titel" style="font-size:120px;">Kennengelernt am <span class="schimmer">ersten Tag.</span></h2>
  </div>
  {notizen("September 2019, erster Tag BWL hier an der TH: Da haben wir uns kennengelernt und ab dann zusammen gelernt. Ab März 2020 Corona, Hochschule zu, Zoom bis nachts. Bachelor 2022, dann beide den Master in BWL, fertig Anfang 2024. Nebenbei Werkstudenten: Emre bei PwC als Berater im Public Sector, Eddie im Online-Marketing einer Akademie für Führungskräftetrainings, dort sogar als Seminartrainer, dazu selbstständig mit Content. Gegründet haben wir dann mitten im Master.")}
</section>

<!-- ============ CHAT 28.12.2020 ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <div class="chat-buehne">
      <div class="chat-text">
        <h2 class="hero">28.12.<br><span class="schimmer">2020</span></h2>
      </div>
      {chat()}
    </div>
  </div>
  {notizen("Dezember 2020, mitten in Corona. Magic Moment eins. Die Nachrichten laufen von allein ein, wie damals. Nicht vorlesen, mitlesen lassen. Beim letzten (Kriegen 3 likes) kommt meist ein Lacher. Dann: Das war die Idee. Ohne Plan, ohne Geld, mitten im Studium. Die Tippfehler sind original.")}
</section>

<!-- ============ GRÜNDUNG ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">Gegründet im <span class="schimmer">Double Coffee</span></h2>
  </div>
  <figure class="polaroid gruendung" style="left:130px;--d:-4deg;--y:0px;--i:0;"><img src="assets/fotos/double-emre.jpg" alt="Emre am Laptop im Café"><figcaption>Double Coffee</figcaption></figure>
  <figure class="polaroid gruendung" style="left:560px;--d:3deg;--y:30px;--i:1;"><img src="assets/fotos/double-eddie.jpg" alt="Eddie am Laptop im Café"><figcaption>Double Coffee</figcaption></figure>
  <figure class="polaroid gruendung" style="left:990px;--d:-2deg;--y:-10px;--i:2;"><img src="assets/fotos/ratzeburg-2022.jpg" alt="Emre unter einer Decke am Schreibtisch in Eddies Zimmer in Ratzeburg"><figcaption>Ratzeburg, bei Eddie</figcaption></figure>
  <figure class="polaroid gruendung" style="left:1420px;--d:5deg;--y:20px;--i:3;"><img src="assets/fotos/umzug-briefkasten.jpg" alt="Zettel EDGE am Briefkasten über dem Schild Erdogan"><figcaption>Unser Briefkasten, 2023</figcaption></figure>
  {notizen("Ende 2022, mitten im Master. Gegründet haben wir nicht im Büro, sondern im Double Coffee und bei Eddie zu Hause in Ratzeburg. Die Idee dahinter: An der Uni haben wir gelernt, dass Dinge empirisch und valide sein müssen. Draußen in der echten Welt lief Marketing aber fast immer aus dem Bauch. Also EDGE: Marketing aus echten Daten, dazu KI. Rechts der Briefkasten: ein Zettel mit Tesafilm über Emres Klingelschild, so sah unser Firmenschild aus. (Platzhalter: das Schwarzweißfoto von Emre aus Ratzeburg einsetzen.)")}
</section>

<!-- ============ ERSTER NAME ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Fast hießen wir <span class="schimmer">anders</span></h2>
    <p class="epg-label l1">Eddies Vorschlag:</p>
    <p class="epg-label l2">Was alle gelesen haben:</p>
  </div>
  <div class="epg-szene">
    <span class="fragment epg-s1" aria-hidden="true"></span>
    <span class="fragment epg-s2" aria-hidden="true"></span>
    <img class="epg-karte" src="assets/alt/epg.jpg" alt="EPG Agency">
    <img class="epg-person emre" src="assets/fotos/emre-frei.png" alt="Emre">
    <img class="epg-person eddie" src="assets/fotos/eddie-frei.png" alt="Eddie">
    <svg class="epg-krone" viewBox="0 0 120 80" aria-hidden="true"><path d="M6 72 L14 18 L38 46 L60 6 L82 46 L106 18 L114 72 Z" fill="#F5C542" stroke="#B8860B" stroke-width="3" stroke-linejoin="round"/><circle cx="60" cy="6" r="6" fill="#E4003A"/><circle cx="14" cy="18" r="5" fill="#E4003A"/><circle cx="106" cy="18" r="5" fill="#E4003A"/></svg>
    <b class="epg-buchstabe b-e">E</b><b class="epg-buchstabe b-p">P</b><b class="epg-buchstabe b-g">G</b>
    <span class="epg-schild s-emre">Erdogan</span>
    <span class="epg-schild s-eddie-a">Paul-Ghazaryan</span>
    <span class="epg-schild s-eddie-b"><i>E</i>dgar <i>P</i>aul-<i>G</i>hazaryan</span>
    <span class="epg-blase">Und ich?</span>
  </div>
  {notizen("Wir haben einen Namen gesucht. Erst nur die Karte zeigen: EPG Agency. Wofür steht EPG? Klick eins: Eddies Vorschlag, ganz ernst gemeint. E für Erdogan, P und G für Paul-Ghazaryan. Beide Gründer in einem Namen, Teamgeist, Symbolik. Klick zwei: Emre hat es dann gemerkt. E, P, G ist einfach Edgar Paul-Ghazaryan. Eddie hatte die Firma nach sich selbst benannt, ohne es zu merken. Emre fliegt raus, Eddie bekommt die Krone. Lacher abwarten, Eddie darf sich verteidigen. Gegründet haben wir dann als EDGE Digital, von cutting edge. EPG gab es nie, ist aber bis heute unser Running Gag.")}
</section>

<!-- ============ DOM ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">Und dann kam <span class="schimmer">Dom.</span></h2>
  </div>
  <div class="dom-szene">
    <span class="fragment dom-s1" aria-hidden="true"></span>
    <img class="dom-person p-emre" src="assets/fotos/emre-frei.png" alt="Emre">
    <img class="dom-person p-dom" src="assets/fotos/dom-frei.png" alt="Dom">
    <img class="dom-person p-eddie" src="assets/fotos/eddie-frei.png" alt="Eddie">
    <b class="dom-b d1">E</b><b class="dom-b d2">D</b><b class="dom-b d3">G</b><b class="dom-b d4">E</b>
    <span class="epg-schild n-emre">Emre</span>
    <span class="epg-schild n-dom"><i>D</i>ominique <i>G</i>regor</span>
    <span class="epg-schild n-eddie">Eddie</span>
  </div>
  {notizen("Juni 2025: Dom kommt dazu, unser erster Partner, ab da sind wir zu dritt. Eigentlich kommt EDGE von cutting edge. Klick: Aber schaut mal, was im Nachhinein passiert ist. E wie Emre, D und G wie Dominique Gregor, so heißt Dom mit Vornamen, E wie Eddie. Der Name hat uns gefunden. Nach der EPG-Geschichte ist das unsere Revanche.")}
</section>

<!-- ============ BÜROS ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Vom Homeoffice in die <span class="schimmer">Marlesgrube</span></h2>
  <div class="bueros">
    <figure class="polaroid buero" style="--d:-3deg;--y:20px;--i:0;"><img src="assets/fotos/ohne-buero-2022.jpg" alt="Laptop mit Videocall, Emre im Hoodie auf dem Bildschirm"><figcaption>Ohne Büro, 2022</figcaption></figure>
    <figure class="polaroid buero" style="--d:2deg;--y:-6px;--i:1;"><img src="assets/fotos/bus-2023.jpg" alt="Nachts im Bus, Arbeit am Laptop"><figcaption>Im Bus, 2023</figcaption></figure>
    <figure class="polaroid buero" style="--d:-2deg;--y:14px;--i:2;"><img src="assets/fotos/erster-raum-2024.jpg" alt="Eddie im leeren ersten Raum mit Bogenfenstern"><figcaption>Übergangsräume, 2024</figcaption></figure>
    <figure class="polaroid buero" style="--d:3deg;--y:-10px;--i:3;"><img src="assets/fotos/fischstrasse-2025.jpg" alt="Emre am Schreibtisch im Loft in der Fischstraße"><figcaption>Fischstraße, 2025</figcaption></figure>
    <figure class="polaroid buero" style="--d:-2deg;--y:8px;--i:4;"><img src="assets/fotos/umzug-sofa-buero.jpg" alt="Das grüne Sofa vor dem neuen Büro"><figcaption>Marlesgrube, 2026</figcaption></figure>
  </div>
  </div>
  {notizen("Ein Bild pro Jahr. 2022 gab es kein Büro, gearbeitet wurde über Videocalls. 2023 haben wir sogar im Bus gearbeitet. 2024 der erste eigene Raum, die Übergangsräume, ein Projekt der Wirtschaftsförderung Lübeck. Juli 2025, inzwischen mit Dom zu dritt: die Fischstraße, unser erstes großes Büro. Und seit dem 1. Oktober 2026 sitzen wir in der Marlesgrube, über der HypoVereinsbank am Pferdemarkt.")}
</section>

<!-- ============ DIE ANFÄNGE: UMZUG ============ -->
<section class="f-th" data-stimmung="neutral" data-chrome="zahl">
  <div class="slide umzug-folie">
    <span class="umzug-datum">27. September 2026</span>
    <div class="bento">
      <figure class="b-sofa" style="--i:0;"><img src="assets/fotos/umzug-team-sofa.jpg" alt="Das ganze Team zu fünft auf dem grünen Sofa vor der HypoVereinsbank"></figure>
      <figure class="b-rathaus" style="--i:1;"><img src="assets/fotos/umzug-im-transporter.jpg" alt="Eddie und Dom mit dem eingepackten Sofa im Transporter"></figure>
      <figure class="b-schild" style="--i:2;"><img src="assets/fotos/umzug-sofa-boden.jpg" alt="Das eingepackte Sofa im alten Büro, daneben liegt jemand auf dem Boden"></figure>
      <figure class="b-tisch" style="--i:3;"><img src="assets/fotos/umzug-treppe.jpg" alt="Ein Kollege trägt eine Teppichrolle durchs Treppenhaus"></figure>
      <figure class="b-regal" style="--i:4;"><img src="assets/fotos/umzug-ankunft.jpg" alt="Der Transporter vor dem neuen Büro, Emre wartet am Fenster"></figure>
    </div>
  </div>
  {notizen("Der Umzugstag, 27. September 2026. Erst das grüne Sofa im alten Büro eingepackt, irgendwann lag jemand einfach daneben auf dem Boden. Dann ab in den Transporter, Eddie und Dom mit Daumen hoch. Vor der Marlesgrube wartet Emre am Fenster, und alles muss durchs Treppenhaus nach oben. Am Ende sitzt das ganze Team auf dem Sofa vor der HypoVereinsbank, über der jetzt unser Büro ist. Seit dem 1. Oktober arbeiten wir dort. Eine Geschichte pro Foto reicht.")}
</section>

<!-- ============ TEAM HEUTE ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide team">
    <h2 class="team-titel">Aus zwei wurde ein <span class="schimmer">Team</span></h2>
    {team_seite("service", "AI-Services", SERVICE_KOPF, SERVICE)}
    <div class="mitte">
      {kopf_kreis("Emre", "Geschäftsführer", "emre.png", "gf", gross=True)}
      <figure class="person du gross"><div class="rund"><b>?</b></div><figcaption><b>Du?</b><span>Praktikum, Werkstudium, Abschlussarbeit</span></figcaption></figure>
    </div>
    {team_seite("software", "AI-Software", SOFTWARE_KOPF, SOFTWARE)}
  </div>
  {notizen("Seit Juni 2025 zu dritt, 2026 ist das Team richtig gewachsen. Das Team heute, zwei Bereiche: Services und Software. Kurz jeden Namen sagen. Der leere Kreis in der Mitte: Wer Lust hat, kommt nach dem Vortrag zu uns.")}
</section>

<!-- ============ KAPITEL: REALITY CHECK ============ -->
<section class="f-th" data-stimmung="th" data-chrome="zahl">
  <img class="voll" src="assets/illu/hoersaal.jpg" alt="Ein dunkler Hörsaal, dessen Stirnwand sich zur Stadt öffnet">
  <div class="schleier-links"></div>
  <div class="slide links-mitte">
    <h2 class="hero">Der Reality <span class="schimmer">Check</span></h2>
  </div>
  {notizen("Kapitelwechsel. Der Hörsaal, der sich zur Stadt öffnet: Irgendwann ist die Wand einfach weg. Jetzt kommt, was wir gern früher gewusst hätten.")}
</section>

<!-- ============ HANDZEICHEN: NACH DEM STUDIUM ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Was kommt nach dem <span class="schimmer">Studium?</span></h2>
    <div class="icons" style="--n:4;">{icons_studium}</div>
  </div>
  {notizen("Vier Klicks, nach jedem Klick Hände zählen lassen. Bei Keine Ahnung gehen meist die meisten Hände hoch, das ist gut so und der Übergang zu den nächsten Folien.")}
</section>

<!-- ============ THESE 2 ============ -->
<section class="f-th" data-stimmung="neutral">
  <figure class="polaroid stapel" style="left:990px;top:calc(var(--extra) + 70px);width:600px;--d:-3deg;--y:0px;--i:0;"><img src="assets/fotos/nachtarbeit.jpg" alt=""><figcaption>irgendwann nachts</figcaption></figure><figure class="polaroid stapel" style="left:1515px;top:calc(var(--extra) + 110px);width:330px;--d:6deg;--y:0px;--i:1;"><img src="assets/fotos/moment-bildschirme.jpg" alt=""><figcaption>Mehr Bildschirme.<br>Weniger Probleme.</figcaption></figure><figure class="polaroid stapel" style="left:950px;top:calc(var(--extra) + 545px);width:300px;--d:-6deg;--y:0px;--i:2;"><img src="assets/fotos/moment-ueberflieger.jpg" alt="Eddie und Emre beim Überflieger-Wettbewerb"><figcaption>Überflieger, Kiel 2023</figcaption></figure><figure class="polaroid stapel" style="left:1275px;top:calc(var(--extra) + 520px);width:265px;--d:3deg;--y:0px;--i:3;"><img src="assets/fotos/moment-gewonnen.jpg" alt="Emre mit der Urkunde vom Social Hackathon"><figcaption>Social Hackathon 2024</figcaption></figure><figure class="polaroid stapel" style="left:1565px;top:calc(var(--extra) + 560px);width:300px;--d:-4deg;--y:0px;--i:4;"><img src="assets/fotos/preis-2025.jpg" alt="Das Team auf der Bühne beim Existenzgründerpreis"><figcaption>Existenzgründerpreis 2025</figcaption></figure>
  <div class="slide links-mitte">
    <h2 class="these" style="max-width:none;white-space:nowrap;">Anfangen<br><span class="schimmer">&gt;</span> Planen</h2>
  </div>
  {notizen("Echte Momente, keine Planung: Nachtschicht mit Decke über den Schultern, mehr Bildschirme, weniger Probleme. Dann die ersten Bühnen: Überflieger-Wettbewerb in Kiel 2023, Social Hackathon 2024 (Urkunde für den besten Prototyp), Existenzgründerpreis der Lübecker Wirtschaft 2025. Nichts davon stand in einem Businessplan, alles kam, weil wir einfach angefangen haben. Eure eigene Geschichte dazu, wann ihr einfach losgelegt habt.")}
</section>

<!-- ============ EMRES WHITEBOARD ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline" style="font-size:70px;max-width:1350px;">Worin Gründer zu früh <span class="schimmer">investieren</span></h2>
    <div class="karten"><div class="karte fragment"><div class="innen"><div class="seite vorn"><span>Logo</span><span>Website</span><span>Visitenkarten</span></div><div class="seite hinten"><b>Keiner sieht dich.</b></div></div></div><div class="karte fragment"><div class="innen"><div class="seite vorn"><span>Büromöbel</span><span>Büro</span><span>Schicke Gegenstände</span></div><div class="seite hinten"><b>Keiner besucht dich.</b></div></div></div><div class="karte fragment"><div class="innen"><div class="seite vorn"><span>Investoren</span><span>Testphasen</span></div><div class="seite hinten"><b>Bubble.</b></div></div></div></div>
  </div>
  <figure class="polaroid quelle-foto" style="--d:5deg;--y:0px;--i:0;"><img src="assets/fotos/tough-talks.jpg" alt="Emre am Whiteboard in den Tough Talks"><figcaption>Das sagte sogar Emre<br>in seinen Tough Talks …</figcaption></figure>
  {notizen("Die drei Punkte stammen aus Emres Whiteboard in den Tough Talks, einem Format unseres YouTube-Kanals (oben rechts). Drei Karten, drei Klicks. Vorne das, worin fast jeder Gründer zuerst Zeit und Geld steckt. Umgedreht die Wahrheit: Logo, Website, Visitenkarten, keiner sieht dich. Büro, Möbel, schicke Sachen, keiner besucht dich. Investoren und ewige Testphasen, du lebst in einer Blase. Emre erzählt dazu, was wir selbst falsch gemacht haben.")}
</section>

<!-- ============ THESE 3 ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide links-mitte">
    <h2 class="these" style="font-size:96px;white-space:nowrap;">Dein Netzwerk<br>sitzt<br><span class="schimmer">neben dir.</span></h2>
  </div>
  <div class="orbit" data-rx="350" data-ry="330" data-tempo="0.025" data-mitte-x="1420" data-mitte-y="540">
    <div class="orbit-du">Du</div>
    <img class="o" src="assets/orbit/team.jpg" alt=""><img class="o" src="assets/orbit/ueberflieger.jpg" alt=""><img class="o" src="assets/orbit/sakkos.jpg" alt=""><img class="o" src="assets/orbit/ihk.jpg" alt=""><img class="o" src="assets/orbit/messe.jpg" alt=""><img class="o" src="assets/orbit/pitch.jpg" alt=""><img class="o" src="assets/orbit/wfl.jpg" alt=""><img class="o" src="assets/orbit/daumen.jpg" alt="">
  </div>
  {notizen("Die Fotos, die da kreisen: unser Team, der Überflieger-Wettbewerb, unser erster Messestand, Empfänge, Pitch-Abende, Netzwerkabende. Fast jeder dieser Kontakte fing mit einem Gespräch an, oft mit Leuten, die neben uns saßen. Wir zwei haben uns hier kennengelernt, am ersten Tag im ersten Semester. Einmal kurz nach links und rechts schauen lassen: Das sind vielleicht eure ersten Mitgründer, Kunden oder Chefs.")}
</section>

<!-- ============ THESE 4 ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="these" style="font-size:96px;">Du musst noch nicht wissen, <span class="schimmer">was du willst.</span></h2>
    {route()}
  </div>
  {notizen("Zurück zu den vielen Händen bei Keine Ahnung. Die Linie zeichnet sich von allein: So sah unser Weg aus. Kein Plan, Umwege, eine Schleife ganz am Anfang. Studium, dann der Chat, der erste Name, der sich als Eddies eigener Name herausstellte, die ersten Räume, EDGE, heute. Niemand von uns hätte im Hörsaal diese Linie vorhersagen können. Wichtig ist nur, dass man losgeht. Und dafür gibt es heute ein Werkzeug, das es so noch nie gab. Nach der Pause.")}
</section>

<!-- ============ PAUSE ============ -->
<section class="f-th" data-stimmung="neutral" data-chrome="zahl">
  {pause_bild}
  <div class="slide links-mitte">
    <h2 class="hero">Pause</h2>
    <p class="unterzeile" style="font-size:46px;font-weight:600;color:var(--w-70);margin:18px 0 0;">15 Minuten</p>
  </div>
  {notizen("Pause ansagen, Uhrzeit für den Wiederbeginn nennen. Der Roboter hat übrigens gerade das letzte Fischbrötchen erwischt, das Blech hinter ihm ist leer. Also: schnell sein. Folie stehen lassen.")}
</section>

<!-- ============ KAPITEL: KI-SKILLS ============ -->
<section class="f-th" data-stimmung="th" data-chrome="zahl">
  <img class="voll foto-rechts" src="assets/illu/robo-hoersaal.jpg" alt="Der EDGE-Roboter im roten Hoodie meldet sich im Hörsaal">
  <div class="schleier-links"></div>
  <div class="slide links-mitte">
    <h2 class="hero" style="font-size:104px;">Dein neuer<br><span class="schimmer">Kommilitone.</span></h2>
  </div>
  {notizen("Der Roboter mit der Fischbrötchen-Kappe ist unser Maskottchen aus den KI-Vorträgen. Heute sitzt er im Hörsaal und meldet sich immer zuerst. Überleitung: Wer von euch nutzt ihn schon?")}
</section>

<!-- ============ HANDZEICHEN: WER NUTZT KI ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Wer nutzt <span class="schimmer">KI?</span></h2>
    <div class="icons" style="--n:3;">{icons_ki}</div>
  </div>
  {notizen("Drei Klicks, drei Handzeichen. Keine Zahlen nennen, keine Bewertung. Nur: Okay, dann holen wir jetzt alle auf denselben Stand.")}
</section>

<!-- ============ SO ARBEITEN WIR ============ -->
<section class="f-th so-arbeiten" data-stimmung="neutral" data-chrome="aus">
  <video class="sa-video" src="assets/video/hotel-lobby.mp4" poster="assets/video/hotel-lobby.jpg" data-autoplay playsinline></video>
  <div class="slide">
    <p class="sa-titel">Wenn der Kunde Ja sagt.</p>
    <div class="sa-aufloesung fragment">
      <h2 class="hero">Alles <span class="schimmer">KI.</span></h2>
      <p>Kein einziges Bild davon ist echt.</p>
    </div>
    <p class="sa-kennung">KI-generiert · Vorlage: Quavo &amp; Takeoff, A COLORS SHOW (2022)</p>
  </div>
  {notizen("Video startet von selbst, 19 Sekunden mit Ton. Kurz wirken lassen. Klick: Auflösung, alles KI. Das ist der Hotel-Lobby-Trend, den viele gerade auf TikTok sehen: Higgsfield hat die Bewegungen von Quavo und Takeoff aus ihrem COLORS-Auftritt von 2022 auf ein ganz normales Foto von uns beiden übertragen. Gedauert hat das ein paar Minuten. Nur live zeigen, nicht posten: die Rechte an Aufnahme und Song liegen bei anderen. Überleitung: Und was kann KI sonst noch?")}
</section>

<!-- ============ WAS KI HEUTE KANN ============ -->
<section class="f-th ki-folie" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">Was KI <span class="schimmer">heute</span> kann</h2>
    {ki_bento()}
  </div>
  {notizen("Alles hier ist echt und von uns gemacht. Oben links: ein normales Foto vom Seminargebäude, daraus hat die KI das Nachtbild vom Anfang gemacht. Daneben unser Maskottchen, aus einem einzigen Bild ist ein Video geworden. Rechts Eddie neben unserem Avatar am EDGE-Stand auf der Standort-Zukunft-Messe im Juni 2026. Unten links schreibt die KI gerade eine Mail. Klick: die Stimme spielt. Kein Mensch hat das eingesprochen. Überleitung: Und seit diesem Jahr kann KI auch selbst arbeiten, dazu gleich ein Beispiel.")}
</section>

<!-- ============ KURVE ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Moore's Law gegen <span class="schimmer">KI</span></h2>
    {kurve()}
  </div>
  {notizen("Computer wurden alle 18 Monate doppelt so leistungsfähig, das war schon schnell. KI verdoppelt sich etwa alle sechs Monate. Die Linie läuft von allein ein.")}
</section>

<!-- ============ DAS HANDY IST NUR DAS FENSTER ============ -->
<section class="f-th" data-stimmung="th">
  <img class="fenster-bild" src="assets/illu/handy-cloud.jpg" alt="Ein altes Tastenhandy, über eine Lichtlinie mit einem Rechenzentrum verbunden">
  <div class="fenster-name" style="left:{HANDY_X}%;">Nokia 6300 · 8 MB</div>
  <div class="fenster-name" style="left:{SERVER_X}%;">Hier rechnet die KI</div>
  <p class="fenster-erklaerung">Ein Entwickler hat Claude<br>auf sein Nokia von 2007 gebracht.<br>Gerechnet wird im Rechenzentrum,<br>das Handy ist nur der Bildschirm.</p>
  <div class="slide">
    <h2 class="headline" style="position:relative;">Claude auf einem Handy von <span class="schimmer">2007</span></h2>
  </div>
  {notizen("Ende September hat ein Entwickler aus der Türkei Claude auf sein altes Nokia 6300 von 2007 gebracht. 8 MB Speicher, das Handy kommt nicht mal mehr ins heutige Internet. Er hat in ein paar Tagen eine kleine App geschrieben, die über einen Zwischenserver mit Claude spricht. Video: über 3 Millionen Aufrufe in wenigen Tagen. Der Trick: Die KI rechnet gar nicht im Handy, sondern im Rechenzentrum. Das Handy ist nur der Bildschirm. Heißt für euch: Ihr braucht kein teures Gerät, um die stärksten Modelle der Welt zu nutzen. Und: So eine scheinbar sinnlose Bastelei bringt plötzlich Millionen Aufrufe, so fangen Dinge an.")}
</section>

<!-- ============ WIR FRAGEN SCHLECHT ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide mittig">
    <p class="zitat">Die KI liefert nicht schlecht.<br><span class="schimmer">Wir fragen schlecht.</span></p>
  </div>
  {notizen("Der wichtigste Satz des Kapitels. Stehen lassen. Dann das Beispiel mit der Pizza.")}
</section>

<!-- ============ PIZZA ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <div class="pizza">
      <div>
        <p class="label">So fragen die meisten</p>
        <p class="ansage kurz">„Pizza.“</p>
        <img src="assets/robo/pizza-schlecht.png" alt="Der Roboter ist enttäuscht">
      </div>
      <div class="trennlinie"></div>
      <div class="fragment">
        <p class="label gut">So bekommst du, was du willst</p>
        <p class="ansage lang">„Eine Pizza Margherita, dünner Boden,<br>extra Basilikum, in 20 Minuten an die Mensa,<br>ich zahle mit Karte.“</p>
        <img src="assets/robo/pizza-gut.png" alt="Der Roboter freut sich">
      </div>
    </div>
  </div>
  {notizen("Wer nur Pizza sagt, bekommt irgendeine. Klick: Wer genau sagt, was er will, bekommt seine. Genau so funktioniert ein Prompt. Und dafür gibt es einen Kompass.")}
</section>

<!-- ============ KOMPASS ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Der <span class="schimmer">Kompass</span></h2>
    <div class="kompass">{kompass}</div>
  </div>
  {notizen("Vier Bausteine, immer dieselben. Danach live in Sekunden zeigen, Prompts stehen auf der Karte zum Mitnehmen. Bewerbung üben: Du bist Personalerin bei einem Lübecker Medizintechnik-Unternehmen. Führ ein Vorstellungsgespräch mit mir, eine Frage nach der anderen. Ich bewerbe mich als Werkstudent im Marketing, 3. Semester BWL. Nach jeder Antwort ehrliches Feedback, höchstens drei Sätze. Zweitens Tutor: Erklär mir Angebot und Nachfrage in drei Sätzen, dann stell mir eine Frage und warte auf meine Antwort. Drittens, als Rückgriff auf unseren Chat von 2020: Du bist eine skeptische Investorin, zerreiß meine Idee, Social-Media-Agentur in Lübeck, nenn die drei größten Risiken. Die KI findet genau die Fragen, die wir damals beantworten mussten. Und wir haben es trotzdem gemacht.")}
</section>

<!-- ============ DEMO: LERNSEITE BAUEN ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">KI baut dir ein <span class="schimmer">Werkzeug</span></h2>
    <div class="fenster gross"><div class="fenster-leiste"><i></i><i></i><i></i><span>lernseite.html · von KI gebaut</span></div><iframe src="demo/lernseite.html" title="Interaktive Lernseite Angebot und Nachfrage" loading="lazy"></iframe></div>
  </div>
  {notizen("Magic Moment. Diese Seite hat eine KI aus einem einzigen Satz gebaut: Bau mir eine interaktive Lernseite zu Angebot und Nachfrage, mit zwei Reglern, einer Kurve, die sich live bewegt, und dem Lübecker Weihnachtsmarkt als Beispiel. Live an den Reglern ziehen: Besucher hoch, Preis steigt. Ihr könnt euch eure eigenen Lernwerkzeuge bauen lassen. Der Bau dauert Minuten, deshalb zeigen wir das fertige Ergebnis.")}
</section>

<!-- ============ EISBERG ============ -->
<section class="f-th" data-stimmung="neutral">
  {eisberg()}
  <div class="slide links-mitte">
    <h2 class="headline">Die KI baut<br>nur die <span class="schimmer">Spitze.</span></h2>
  </div>
  {notizen("Erst sieht man nur die Spitze über Wasser: Prompt. So wird es auf Instagram verkauft, ein Satz, fertige App. Klick: Darunter taucht der Rest auf. Login, Datenbank, Datenschutz, Hosting, Sicherheit, Backups, Wartung. Das macht keine KI für euch fertig, das ist echte Arbeit und echte Verantwortung. Bei uns läuft jede App vor dem Start durch eine Prüfliste. Für alle aus der Informatik: Euer Job verschwindet nicht, er liegt unter Wasser.")}
</section>

<!-- ============ NIE IN DIE KI ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Was nie in die <span class="schimmer">KI</span> gehört</h2>
    <div class="icons klein" style="--n:6;">{icons_nie}</div>
  </div>
  {notizen("Kurz und klar. Firmeninterna heißt auch: Daten aus dem Praktikum oder der Abschlussarbeit im Unternehmen. Und: Die Regeln eurer Prüfungsordnung zu KI gelten immer, im Zweifel fragt eure Dozierenden.")}
</section>

<!-- ============ FAKTENCHECK ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">KI erfindet auch mal <span class="schimmer">Quellen.</span></h2>
    <div class="faktencheck">{fakten}</div>
  </div>
  {notizen("Drei Klicks, drei Gewohnheiten. Der dritte Punkt ist ein echter Satz für den Prompt: Wer der KI erlaubt, nichts zu wissen, bekommt seltener erfundene Antworten.")}
</section>

<!-- ============ ERST SELBST DENKEN ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide links-mitte">
    <h2 class="these">Erst selbst denken,<br><span class="schimmer">dann KI fragen.</span></h2>
    <p class="fussquelle">Quelle: MIT Media Lab, „Your Brain on ChatGPT“, 2025</p>
  </div>
  {notizen("Die Studie vom MIT: Wer seinen Aufsatz von Anfang an mit KI geschrieben hat, konnte danach kaum einen Satz daraus wiedergeben. Wer erst selbst geschrieben und dann KI genutzt hat, schnitt besser ab. Wichtig: kleine Vorabstudie, 54 Personen, noch nicht begutachtet. Also kein Beweis, aber eine gute Regel fürs Studium.")}
</section>

<!-- ============ STUDIE ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <div class="studie">
      <p class="riesig schimmer">+40 %<small>Qualität</small></p>
      <div class="nebenzahlen"><span><b>25 %</b> schneller</span><span><b>12 %</b> mehr geschafft</span></div>
    </div>
    <p class="fussquelle">Quelle: Harvard Business School und Boston Consulting Group, 758 Berater mit und ohne KI, 2023</p>
  </div>
  {notizen("Die bekannte Studie von Harvard und der Boston Consulting Group (2023). Wer KI richtig nutzt, ist besser, schneller und schafft mehr. Genau das haben wir heute geübt.")}
</section>

<!-- ============ HANDZEICHEN: BERUFE ============ -->
<section class="f-th" data-stimmung="neutral">
  <div class="slide">
    <h2 class="headline">Wo hilft KI am <span class="schimmer">meisten?</span></h2>
    <div class="icons" style="--n:4;">{icons_berufe}</div>
  </div>
  {notizen("Vier Klicks, nach jedem Hände zählen. Die meisten tippen auf Programmierer. Auflösung auf der nächsten Folie.")}
</section>

<!-- ============ BERUFE: AUFLÖSUNG ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline">Dolmetscher, nicht <span class="schimmer">Programmierer</span></h2>
    {balken()}
    <p class="fussquelle">Quelle: Microsoft Research, 200.000 Copilot-Gespräche aus den USA, 2025</p>
  </div>
  {notizen("Die Studie hat gemessen, bei welchen Tätigkeiten Menschen sich wirklich von KI helfen lassen. Ganz oben Dolmetscher und Historiker, Programmierer stehen nicht einmal unter den ersten 40. Ganz unten: Brücken- und Schleusenwärter, die haben wir in Lübeck ja genug. Wichtig: Das ist kein Ranking, wer seinen Job verliert. Die Autoren sagen selbst, daraus Jobverlust abzuleiten wäre ein Fehler. Dazu das Beispiel auf der nächsten Folie.")}
</section>

<!-- ============ GELDAUTOMAT ============ -->
<section class="f-th" data-stimmung="neutral">
  <img class="voll automat-bild foto-rechts" src="assets/illu/geldautomat.jpg" alt="Ein leuchtender Geldautomat im Dunkeln">
  <div class="schleier-links"></div>
  <div class="slide links-mitte">
    <h2 class="these" style="max-width:1100px;font-size:104px;">Der Geldautomat hat die Kassierer <span class="schimmer">nicht abgeschafft.</span></h2>
  </div>
  {notizen("Das Beispiel stammt aus derselben Microsoft-Studie. Der Geldautomat hat die Hauptaufgabe der Bankkassierer übernommen, Geld auszahlen. Trotzdem gab es danach mehr Kassierer, weil Banken günstiger neue Filialen eröffnen konnten und die Leute sich um Beratung kümmerten. KI verändert Aufgaben. Was mit den Jobs passiert, entscheiden Menschen und Unternehmen.")}
</section>

<!-- ============ DREI ZUKÜNFTE ============ -->
<section class="f-th" data-stimmung="th">
  <div class="slide">
    <h2 class="headline" style="margin-bottom:0;">Was KI bis 2030 <span class="schimmer">bringen könnte</span></h2>
    {zukuenfte()}
    <p class="offen fragment">Welches Szenario es wird, steht <span class="schimmer">noch nicht fest.</span></p>
    <p class="fussquelle">Quelle: Anthropic, „Scenarios for our Economic Future“, September 2026</p>
  </div>
  {notizen("Erst Handzeichen: Wer glaubt, KI wird wie das Internet? Wer glaubt, KI macht bald die Hälfte der Büroarbeit? Wer glaubt ans Extrem? Erklärung: Anthropic hat ausgerechnet, wie groß die US-Wirtschaft 2030 ohne KI wäre, und das mit drei Szenarien verglichen. Weil Prozente keiner fühlt, steht groß da, wie viele Jahre normales Wachstum das wären, die US-Wirtschaft wächst sonst um etwa 2 Prozent im Jahr. Wie das Internet: plus 1,6 Prozent, also knapp ein Jahr zusätzlich. Hälfte der Büroarbeit: plus 8,3 Prozent, vier Jahre zusätzlich. Extrem: plus 32,4 Prozent, das wären 14 Jahre Wachstum zusätzlich, und das bis 2030. Klick: Welches Szenario es wird, steht noch nicht fest. Das entscheiden auch die, die heute hier sitzen. Quelle: Anthropic, Scenarios for our Economic Future, September 2026, über 10.000 Befragte.")}
</section>

<!-- ============ WESHALB ZUGEHÖRT ============ -->
<section class="f-hblau" data-stimmung="neutral">
  <div class="slide mittig">
    <h2 class="frage-gross">Weshalb hast du uns<br><span class="schimmer">zugehört?</span></h2>
  </div>
  {notizen("Rückgriff auf den Anfang. Ab hier wechselt die Farbe vom TH-Rot ins EDGE-Blau. Frage stellen, Pause lassen.")}
</section>

<!-- ============ DU BESTIMMST DEN GRUND ============ -->
<section class="f-hblau" data-stimmung="hblau" data-chrome="zahl">
  {finale_bild}
  <div class="slide links-mitte">
    <h2 class="hero" style="font-size:132px;">Du bestimmst<br><span class="schimmer">den Grund.</span></h2>
  </div>
  {notizen("Die Schlussbotschaft vom letzten Jahr, bewusst gleich: Ihr habt unsere Geschichten gehört. Die Ereignisse in deinem Leben haben den Sinn, den du ihnen gibst. Also frag dich: Warum warst du heute hier? Das Gebäude vom Anfang, jetzt im Morgengrauen.")}
</section>

<!-- ============ ENDE ============ -->
<section class="f-hblau" data-stimmung="hblau" data-chrome="zahl">
  <img class="ende-foto" src="assets/fotos/duo-event-hoch.jpg" alt="Emre Erdogan und Edgar Paul-Ghazaryan">
  <div class="slide schluss">
    <h2 class="hero">Und jetzt:<br><span class="schimmer">ausprobieren.</span></h2>
    <div class="kontakt"><img src="assets/logos/edge-logo-white.png" alt="EDGE Digital"><p><b>Emre Erdogan &amp; Edgar Paul-Ghazaryan</b><br>{KONTAKT}</p></div>
  </div>
  {qr}
  {notizen("Danke sagen, Fragen aufmachen. Gemeinsames Foto mit Herrn Balke nicht vergessen (für die TH-Website und LinkedIn).")}
</section>
'''
    zusatz_band = """
/* Die Anfänge: Bento-Raster, jedes Foto groß und erkennbar */
.umzug-folie { padding: 60px 70px; }
.bento { flex: 1; display: grid; grid-template-columns: 1fr 1.25fr 1.25fr 1fr; grid-template-rows: 1fr 1fr; gap: 16px; min-height: 0; }
.bento figure { margin: 0; border-radius: 14px; overflow: hidden; min-height: 0; background: #111; }
.bento img { width: 100%; height: 100%; object-fit: cover; display: block; margin: 0 !important; max-width: none !important; max-height: none !important; }
.bento .b-sofa { grid-column: 1; grid-row: 1 / 3; }
.bento .b-sofa img { object-position: 50% 78%; }
.bento .b-rathaus { grid-column: 2 / 4; grid-row: 1; }
.bento .b-rathaus img { object-position: 50% 40%; }
.bento .b-schild { grid-column: 2; grid-row: 2; }
.bento .b-schild img { object-position: 30% 55%; }
.bento .b-tisch { grid-column: 3; grid-row: 2; }
.bento .b-tisch img { object-position: 60% 45%; }
.bento .b-regal { grid-column: 4; grid-row: 1 / 3; }
.bento .b-regal img { object-position: 60% 55%; }
.reveal section.present .bento figure { animation: kachel-ein .6s calc(.1s + var(--i) * .12s) cubic-bezier(.2,.8,.3,1) both; }
@keyframes kachel-ein { from { opacity: 0; transform: scale(.94); } to { opacity: 1; transform: none; } }
body.standbild .bento figure { animation: none !important; }
body.hochkant .bento { grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr); }
body.hochkant .bento .b-sofa { grid-column: 1; grid-row: 1 / 3; }
body.hochkant .bento .b-regal { grid-column: 2; grid-row: 1 / 3; }
body.hochkant .bento .b-rathaus { grid-column: 1 / 3; grid-row: 3; }
body.hochkant .bento .b-schild { grid-column: 1; grid-row: 4; }
body.hochkant .bento .b-tisch { grid-column: 2; grid-row: 4; }

/* Die Anfänge (alt): fünf Fotos als Band, randlos */
.band-anfang { position: absolute; left: 0; top: 0; width: 1920px; height: var(--buehne-h); display: grid; grid-template-columns: 1fr 1fr 1.5fr 1fr 1fr; gap: 6px; }
.band-anfang img { width: 100%; height: 100%; object-fit: cover; display: block; margin: 0 !important; max-width: none !important; max-height: none !important; }
body.hochkant .band-anfang { grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; }
"""
    html = (ORDNER / "stamm.html").read_text(encoding="utf8")
    html = html.replace("</style>", EXTRA_STIL + zusatz_band + "</style>", 1).replace("<!--FOLIEN-->", folien)
    html = html.replace('<div class="stimmung st-hblau"></div>', '<div class="stimmung st-hblau"></div><div class="stimmung st-th"></div>', 1)
    html = html.replace('<script src="kosmos.js"></script>', ORBIT_SKRIPT + KI_SKRIPT + '<script src="kosmos.js"></script>', 1)
    html = html.replace("<title>EDGE Digital | Künstliche Intelligenz. Echte Wirkung.</title>", f"<title>TH Lübeck × EDGE · {TITEL}</title>")
    (ORDNER / "index.html").write_text(html, encoding="utf8")
    print("index.html gebaut:", len(html) // 1024, "KB,", html.count("<section"), "Folien")
    schreibtisch_kopie()


def schreibtisch_kopie():
    """Kopiert die lauffähige Präsi auf den Schreibtisch. _quelle dort bleibt unberührt."""
    SCHREIBTISCH.mkdir(parents=True, exist_ok=True)
    for name in ["index.html", "karte.html", "favicon.svg", "kosmos.js", "Präsentation starten.command", "TH Lübeck Projektwoche 2026.pdf"]:
        if (ORDNER / name).exists():
            shutil.copy2(ORDNER / name, SCHREIBTISCH / name)
    for ordner in ["assets", "demo", "vendor"]:
        shutil.copytree(ORDNER / ordner, SCHREIBTISCH / ordner, dirs_exist_ok=True)
    print("Kopie auf dem Schreibtisch:", SCHREIBTISCH)


if __name__ == "__main__":
    bau()
