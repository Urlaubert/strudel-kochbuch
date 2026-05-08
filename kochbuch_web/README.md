# Strudel Kochbuch

Ein Strudel-Lehrbuch in Strudel — als Webseite mit eingebettetem REPL.

**Live:** https://urlaubert.github.io/strudel-kochbuch/

Jedes der 21 Kapitel ist eine eigene Seite mit der `<strudel-repl>`-Web-Component.
Du tippst auf ein Kapitel, scrollst durch den Code mit Lehrtext, drückst
Strg+Enter (oder das Play-Symbol auf dem iPad) und hörst was passiert.

## Aufbau

```
lehrbuch/                    Quellen — die .strudel-Dateien
  00_lies_mich_zuerst.strudel
  01_hello_sound.strudel
  ...
  20_cheatsheet.strudel
  README.md

kochbuch_web/                Web-Build
  build.py                   Generator: .strudel → .html
  docs/                      ← GitHub Pages bedient diesen Ordner
    index.html
    style.css
    01_hello_sound.html
    ...
```

## Bauen

```bash
cd kochbuch_web
python build.py
```

Liest die Kapitel aus `../lehrbuch/`, schreibt nach `docs/`. Keine
Abhängigkeiten außer Python 3.9+.

Die fertige Seite nutzt
[`@strudel/embed`](https://www.npmjs.com/package/@strudel/embed) per CDN, also
kein NPM-Build nötig — reines statisches HTML+CSS.

## Bei Strudel-Änderungen aktualisieren

`lehrbuch/*.strudel` bearbeiten, dann:

```bash
cd kochbuch_web
python build.py
git add docs/
git commit -m "Update Kapitel"
git push
```

GitHub Pages aktualisiert sich automatisch innerhalb 1-2 Minuten.

## Quellen und Inspiration

- [Strudel](https://strudel.cc) (Felix Roos & Strudel-Team)
- [Dan Gorelick + Viola He](https://www.youtube.com/) — Workshop-Format
- [Switch Angel](https://github.com/switchangel/strudel-scripts) — `prebake`-Idiomatik, Achsen-Pattern
- Toussaint (2005) — Euklidische Rhythmen
- Russell (1980) — Valenz-Arousal-Modell
- Sound on Sound, KVR Audio, r/edmproduction — Sound-Design-Faustregeln

## Lizenz

CC-BY-SA 4.0. Mach was draus.
