# Lehrbuch — Strudel

Ein Strudel-Lehrbuch in Strudel. Jede Datei ist lauffähiger Code,
der dich durch ein Thema führt. Du arbeitest dich von oben nach
unten durch, drückst Strg+Enter, hörst was passiert, änderst eine
Zahl, hörst nochmal.

## Wie das gemeint ist

[strudel.cc](https://strudel.cc) im Browser öffnen, Inhalt eines
Kapitels in den Editor pasten. **Strg+Enter** spielt den untersten
nicht-kommentierten Block. **Strg+.** stoppt. **Strg+/** kommentiert
die aktuelle Zeile aus.

Jedes Kapitel hat:

1. Beispielcode mit Kommentaren als Lehrtext
2. Mini-Aufgaben (`▶ AUFGABE`) zum Selber-Probieren
3. Ein FINALE-Block am Ende, der alles zusammenführt
4. Hier und da `💡 PRAXIS`-Boxen mit Sound-Design- oder
   Workflow-Tipps aus Foren-Konsens

## Reihenfolge

| Kap | Datei | Worum es geht |
|---|---|---|
| 00 | `00_lies_mich_zuerst.strudel` | Bedienung |
| 01 | `01_hello_sound.strudel` | Eine Note. Ein Sample. |
| 02 | `02_mininotation.strudel` | Klammern, Sterne, Tilden |
| 03 | `03_polyrhythmik.strudel` | `stack`, mehrere Spuren |
| 04 | `04_euklidisch.strudel` | Tresillo, Bossa, Aksak: `(N,M)` |
| 05 | `05_skalen_und_melodie.strudel` | `note()`, `scale` |
| 06 | `06_akkorde_und_voicings.strudel` | Akkorde |
| 07 | `07_effekte.strudel` | Filter, Hall, Delay, Distortion |
| 08 | `08_signale_und_modulation.strudel` | `sine`, `perlin`, LFO |
| 09 | `09_time_modifier.strudel` | `fast`, `slow`, `every`, `mask` |
| 10 | `10_samples_eigene.strudel` | Eigene WAVs laden, slicen |
| 11 | `11_song_struktur.strudel` | `arrange`, Sektionen |
| 12 | `12_mini_track_in_50_zeilen.strudel` | Alles zusammen, ein Track |
| 13 | `13_synthese_tief.strudel` | Sound-Design aus Bordmitteln |
| 14 | `14_midi_und_io.strudel` | Hardware-Knobs rein, Synths raus |
| 15 | `15_performance_hygiene.strudel` | Live-Set-Tipps |
| 16 | `16_eigene_helper.strudel` | `register()`, Achsen-Konzept |
| 17 | `17_hap_internals.strudel` | Pattern-Theorie |
| 18 | `18_genre_kochbuch.strudel` | Vorlagen pro Genre |
| 19 | `19_valenz_und_arousal.strudel` | Stimmungs-Achsen (Russell-Modell) |
| 20 | `20_cheatsheet.strudel` | Spickzettel |

## Voraussetzungen

- Browser (Chrome empfohlen, Firefox funktioniert)
- Kopfhörer oder Boxen
- Etwas Geduld beim ersten Sample-Trigger (Lade-Latenz)

Keine Installation. Keine Anmeldung.

## Pfade durch das Buch

- **Erstmals**: Kapitel 00 bis 12 nacheinander.
- **Mini-Notation schon drauf**: 07 (Effekte) und 08 (Modulation)
  sind oft nützlich.
- **Performance-Vorbereitung**: 14 (MIDI), 15 (Hygiene), 16 (Helper).
- **Genre-Defaults nachschlagen**: 18 (Kochbuch).
- **Pattern-Theorie verstehen**: 17 (Hap-Internals).

## Lehrphilosophie

Klang vor Theorie. Du hörst zuerst, dann kommt die Erklärung.
Vollständigkeit ist nicht das Ziel — eher: drei Beispiele die
hörbar anders klingen, statt 20 Varianten desselben.

Edge-Cases stehen in den Tiefen-Kapiteln (13-17). Wer da
einsteigt bevor 01-12 klar ist, verliert den Faden.

## Wenn was nicht klingt

- **Stille direkt nach Strg+Enter**: Sample wird geladen, zweiter
  Hit hilft.
- **Editor zeigt rote Zeile**: Syntaxfehler, meist fehlende
  Klammer oder Anführungszeichen.
- **Pattern läuft aber kein Ton**: Browser-/System-Lautstärke,
  Strudel-Master-Volume rechts unten.
- **Gar nichts**: Browser-Tab refreshen.

## Quellen

- Felix Roos und das Strudel-Team
- Dan Gorelick + Viola He (Workshop)
- Switch Angel (`prebake.strudel`, Achsen-Pattern)
- Toussaint (2005) zu euklidischen Rhythmen
- Russell (1980) zu Valenz-Arousal-Modell
- Sound-Design-Faustregeln aus Sound on Sound, KVR Audio,
  r/edmproduction, Reid "Synth Secrets"
- Weitere in `wissen/strudel/quellen.md`

## Hinweis zur Stabilität

Strudel ist in aktiver Entwicklung (Stand 2026-05). Vor allem
`register()`-Verhalten, MIDI-Setup, MQTT können sich ändern.
Bei Problemen: [strudel.cc/learn](https://strudel.cc/learn)
prüfen. Die Grundlagen (01-12) sind stabil.
