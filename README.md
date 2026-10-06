# TH Lübeck Projektwoche 2026

Vortrag von Emre und Eddie, **10.11.2026, 13 Uhr**, 2 bis 3 Stunden. Titel laut Anmeldung: „Ehemalige Studierende. Heute Unternehmer.“ (Reality Check plus KI-Skills). Ansprechpartner TH: Nils Balke.

## Starten

- Doppelklick auf `Präsentation starten.command` (Server plus Chrome im Vollbild, beenden mit cmd+Q).
- Sprechernotizen mit der Regie pro Folie: im Vortrag Taste **S**.
- Rückfall ohne Technik: `TH Lübeck Projektwoche 2026.pdf`.
- `karte.html`: alle Prompts zum Kopieren, fürs Handy. Für einen QR-Code auf der letzten Folie braucht sie eine öffentliche Adresse, dann `KARTE_URL` in `bau.py` setzen.

## Ändern

Folien, Texte und Notizen stehen in `bau.py`, der Grundstil in `stamm.html` (Stamm: EDGE x Deutsche Bank). Nie `index.html` direkt ändern, danach immer:

```bash
python3 bau.py
```

Der Bau kopiert die fertige Präsi automatisch nach `~/Desktop/TH Lübeck Projektwoche 2026/`.

Prüfen: `node werkzeuge/pruefe-folien.mjs http://localhost:8794 _quelle/pruefung` (misst Überlauf, legt PNGs ab). PDF neu: `sh werkzeuge/export-pdf.sh` (legt es auch auf den Schreibtisch). Animierte Folien live fotografieren: `node werkzeuge/zeitreihe.mjs http://localhost:8794 <folienindex> <ordner> 1500,6000`.

## Dramaturgie

Das Deck beginnt nachts in TH-Rot vor dem Seminargebäude und endet im Morgengrauen im EDGE-Blau vor demselben Gebäude. Folien bleiben bewusst textarm, die Live-Prompts stehen in den Notizen (Kompass-Folie) und auf `karte.html`. Bewegte Kniffe: Chat vom 28.12.2020 läuft ein, EPG-Gag in drei Klicks, Polaroids fallen ein, Umzugs-Raster, Foto-Orbit um „Du“, krumme Route bis heute, Turm unter dem Prompt. Das KI-Kapitel startet mit einem Hotel-Lobby-Video (Higgsfield Genjutsu: Emre und Eddie im COLORS-Auftritt von Quavo und Takeoff, 19 s mit Ton, auf Klick „Alles KI.“; Rohdaten und Skripte in `_quelle/genjutsu/`, nur live zeigen). „Was KI heute kann“ zeigt nur echtes Material: das Foto vom Seminargebäude blendet ins KI-Bild über, das Maskottchen läuft als Video, ein Text tippt sich live, die KI-Stimme spielt beim nächsten Klick und färbt ihre Wellenform mit. Fotos kommen aus der Fotobibliothek `~/Desktop/EDGE/Fotobibliothek/`.

## Bilder

`assets/illu/` entstehen mit Higgsfield (`gpt_image_2_5`, 4K), Vorlage für das Gebäude war ein echtes Foto von Wikimedia Commons (`_quelle/th/`). Rohdateien in `_quelle/higgsfield/`. Das Maskottchen-Video ist mit Kling 3.0 aus einem Standbild entstanden, verkleinert liegt es in `assets/video/`. Die KI-Stimme (`assets/audio/ki-stimme.mp3`) ist ElevenLabs, Stimme Clemens. Fotos aus der Präsi 2025 liegen in `assets/alt/`, die Originale in `_quelle/alt-praesi-2025/`.
