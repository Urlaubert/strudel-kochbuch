# Kapitel 11 — Song-Struktur

Vom Loop zum Stück. Eine 4-Cycle-Idee bleibt eine 4-Cycle- Idee — interessant für 30 Sekunden. Ein Track erzählt eine Geschichte über mehrere Minuten: Intro, Verse, Drop, Bridge, Outro.

Strudel hat dafür drei Werkzeuge: Variablen, mask, arrange. Mit diesen drei kannst du fast alles bauen.

### Schritt 1 — Variablen für Sektionen

Pack jede Sektion in eine Variable. Das macht den Code LESBAR.

```strudel
const intro_drums = stack(
  s("bd").euclid(3, 8),
  s("hh*8").gain(0.3)
)

const verse_drums = stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain(0.4)
)

const drop_drums = stack(
  s("bd*4"),
  s("cp*2").late(0.5),
  s("hh*16").gain(0.6),
  s("oh ~ ~ oh ~ ~ oh ~").gain(0.5)
)
```

Probier sie einzeln:

```strudel
intro_drums

verse_drums

drop_drums
```

### Schritt 2 — manuell wechseln (Live-Coding-Stil)

Strudel spielt nur den UNTERSTEN unkommentierten Block. Im Live-Set wechselst du Sektionen, indem du andere auskommentierst.

stack(intro_drums) stack(verse_drums)

```strudel
stack(drop_drums)
```

Strg+/  in der Zeile schaltet // an/aus. Um zwischen Sektionen zu wechseln: aktive auskommentieren, neue aktivieren, Strg+Enter.

### Schritt 3 — arrange für automatische Sequenz

arrange([n, pattern], ...) spielt jedes Pattern für n Cycles, dann das nächste.

```strudel
arrange(
  [4, intro_drums],
  [8, verse_drums],
  [16, drop_drums],
  [4, intro_drums]
)
```

Das ist ein vollständiger 32-Cycle-Track-Verlauf, automatisch.

```
  Cycle:  0    4         12                  28      32
          |----|---------|-------------------|-------|
          intro  verse        drop             intro
```

### cat — pro Cycle ein anderes Pattern

cat(a, b, c) spielt a in Cycle 1, b in Cycle 2, c in Cycle 3, dann von vorn. Anders als arrange — keine Längen, jedes Pattern bekommt genau einen Cycle. Anders als stack — die Pattern laufen NACHEINANDER, nicht gleichzeitig.

```strudel
cat(
  s("bd*4"),
  s("bd cp bd cp"),
  s("bd*8")
)
```

Cycle 1: 4er-Bass. Cycle 2: Bass+Clap-Wechsel. Cycle 3: 8er-Bass.

Praktisch wenn du eine kurze Variations-Sequenz willst ohne arrange's Längen-Notation. Mini-Notation-Variante: "<a b c>" innerhalb eines Patterns macht das Gleiche auf Step-Ebene.

### Multi-Layer-Track-Struktur

```strudel
const drums_intro = s("bd").euclid(3, 8)
const drums_verse = stack(s("bd*4"), s("~ cp ~ cp"))
const drums_drop = stack(s("bd*4"), s("cp*2").late(0.5), s("hh*16").gain(0.5))

const bass_intro = silence
const bass_verse = note("c2 c2 eb2 g2").s("sawtooth").lpf(400)
const bass_drop = note("c2*8").s("sawtooth").lpf(800).lpenv(8).lpa(0).lpd(0.1)

const lead_intro = silence
const lead_verse = silence
const lead_drop = note("c5 eb5 g5 c5").s("triangle").gain(0.5).room(0.4)

arrange(
  [8, stack(drums_intro)],
  [8, stack(drums_verse, bass_verse)],
  [16, stack(drums_drop, bass_drop, lead_drop)],
  [4, stack(drums_intro)]
)
```

36 Cycles vom Intro über Verse bis Drop und zurück. Jede Sektion ist ein eigenes stack() mit den passenden Layern. "silence" ist ein eingebautes leeres Pattern.

### mask — Layer cycle-weise an/aus

arrange tauscht GANZE Patterns aus. mask schaltet einen Layer in einem Pattern ein und aus.

```strudel
const drums = s("bd*4")
const bass = note("c2*8").s("sawtooth").lpf(500)
const lead = note("c5 eb5 g5 c5").s("triangle")

stack(
  drums,
  bass.mask("<0 0 1 1>"),     // erst nach 2 Cycles
  lead.mask("<0 0 0 1>")      // erst im 4. Cycle
)
```

Cycle:    1    2    3    4 drums:    X    X    X    X bass:     -    -    X    X lead:     -    -    -    X          ─────────────────────          dünn  dünn dichter voll

Klassischer 4-Cycle-Build-Up.

### mask mit längeren Patterns

```strudel
stack(
  drums,
  bass.mask("<0 0 0 0 1 1 1 1>"),
  lead.mask("<0 0 0 0 0 0 1 1>")
)
```

8-Cycle-Build: 4 Cycles nur Drums, 2 Cycles + Bass, 2 Cycles alles.

### Übergänge — Crossfade per mask

Eine alte Sektion fadet aus während die neue einkommt.

```
  Cycle:    1    2    3    4
  sek_a:    X    X    X    -
  sek_b:    -    -    X    X
                      ↑
                 Überlappung: beide spielen
```

Asymmetrische Grenzen sind das Ohr-Goldstück. Wenn alle Sektionen exakt am 4er- oder 8er-Raster wechseln, klingt das gepatched. Eine Spur die einen halben Takt früher startet wirkt komponiert.

```strudel
const sektion_a = stack(s("bd*4"), note("c2*4").s("sawtooth"))
const sektion_b = stack(s("bd cp sd cp"), note("a1*4").s("sawtooth"))

stack(
  sektion_a.mask("<1 1 1 0>"),    // 3 Cycles aktiv, 1 aus
  sektion_b.mask("<0 0 1 1>")     // 2 Cycles aus, 2 aktiv (Überlapp!)
)
```

### Transitions — Sweep / Riser zwischen Sektionen

```strudel
const riser = note("c2*32")
  .s("sawtooth")
  .lpf(saw.range(200, 8000).slow(4))
  .gain(saw.range(0.2, 1).slow(4))
  .room(0.5)

arrange(
  [4, intro_drums],
  [4, stack(intro_drums, riser)],   // Riser über Intro
  [16, drop_drums],
  [4, intro_drums]
)
```

4 Cycles Intro, 4 Cycles Intro + Riser (Build-Up), dann Drop. Der Riser baut Spannung auf bevor der Drop kommt.

### Vollständige Song-Struktur

```strudel
const skl = "C:minor"
```

=== Material ===

```strudel
const drm_kick    = s("bd*4")
const drm_clap    = s("~ cp ~ cp")
const drm_hh      = s("hh*16").gain(0.4)
const drm_oh      = s("[~ ~ ~ oh]/2").gain(0.5)
const bass_simple = note("c2 c2 eb2 g2").scale(skl).s("sawtooth").lpf(500).gain(0.7)
const bass_acid   = note("c2*8").scale(skl).s("sawtooth")
                      .lpf(400).lpenv(8).lpa(0).lpd(0.1).lpq(10).gain(0.7)
const lead_pad    = note("[0,2,4]").scale(skl).s("triangle")
                      .attack(0.5).release(2).lpf(2000).gain(0.4)
const lead_arp    = note("0 4 7 4").scale(skl).add(14).s("piano").gain(0.4)
```

=== Sektionen ===

```strudel
const intro    = stack(drm_kick.gain(0.7), drm_hh, lead_pad)
const verse    = stack(drm_kick, drm_clap, drm_hh, bass_simple)
const prechor  = stack(drm_kick, drm_clap, drm_hh, drm_oh, bass_simple, lead_pad)
const chorus   = stack(drm_kick, drm_clap, drm_hh, drm_oh, bass_acid, lead_pad, lead_arp)
const bridge   = stack(drm_kick.gain(0.6), drm_hh.gain(0.3), bass_simple, lead_pad)
const outro    = stack(drm_kick.gain(0.7), drm_hh, lead_pad)
```

=== Arrangement ===

```strudel
arrange(
  [4, intro],
  [8, verse],
  [4, prechor],
  [16, chorus],
  [8, bridge],
  [16, chorus],
  [4, outro]
)
```

60 Cycles. Bei cps = 0.5 sind das 2 Minuten — ein vollständiger Track.

### FINALE — Live-Performance-Setup

Im Live-Set willst du oft NICHT arrange, sondern manuelles Wechseln. So sieht die Datei dann aus:

(Material und Sektionen wie oben — gekürzt)

stack(intro) stack(verse) stack(prechor)

```strudel
stack(chorus)         // ← aktuell läuft das
```

stack(bridge) stack(outro)

Während der Performance: 1. Fertige Variablen-Bibliothek im oberen Teil der Datei. 2. Unten in der Sektions-Liste die Zeile aktivieren die    spielen soll, alle anderen kommentieren. 3. Strg+Enter — Strudel macht Crossfade.

Praktisch: Variablen vorher debuggt, Sektionen nur wechseln.

### Was Strudel NICHT hat

- Keine Timeline-Editor-View. Alles bleibt Code. - Keine "Markers" oder Section-Names außer Variablen-Namen. - Kein conditional include via Slider — d.h. ein Slider   kann nicht direkt eine Sektion ein- oder ausschalten.   (Workaround: gain(slider().range(0,1)) — Layer wird stumm.)

Das ist Live-Coding-Philosophie. Strudel ist ein Werkzeug um Tracks zu PERFORMEN, nicht zu RENDERN. Final-Mix passiert eher in einer DAW (Reaper, Ableton) mit Strudel-Audio aufgenommen.

### ▶ AUFGABE: Eigene Song-Struktur

Schreib drei eigene Sektionen (intro, verse, drop) mit jeweils unterschiedlichen Drum-Patterns und einem Bass. Pack sie in arrange() mit unterschiedlichen Längen. Lass den Track 30+ Cycles laufen.

### Mini-Zusammenfassung Kapitel 11

```
  const x = ...                    → Variable für Sektion
  stack(...)                       → Layer parallel
  arrange([n, pat], ...)           → automatisches Sequencing
  .mask("<1 0 1 1>")               → Layer cycle-weise an/aus
  silence                          → leeres Pattern
```

```
Drei Live-Strategien:
  1. arrange() — vorgeplanter Verlauf
  2. manuell auskommentieren — frei live
  3. mask + Slider — semi-live
```

Zum Komponieren: zuerst eine Sektion polieren bis sie für 8 Cycles gut klingt. Dann zweite Sektion. Dann Übergang. Bauen geht von INNEN nach AUSSEN.

Weiter zu 12_mini_track_in_50_zeilen.strudel.
