# Kapitel 03 — Polyrhythmik (mehrere Spuren übereinander)

Bisher hattest du EINE Spur. Selbst wenn da viel los war — es war eine. Jetzt kommen mehrere parallel.

Das Grundwerkzeug heißt stack(). Es ist der Wendepunkt vom "Pattern" zum "Stück".

### stack — gleichzeitig spielen

stack() nimmt beliebig viele Pattern und spielt sie alle zur gleichen Zeit ab.

```strudel
stack(
  s("bd*4"),
  s("hh*8")
)
```

Eine Bass-Drum auf jedem Viertel, plus durchlaufende 8tel-Hihats.

```
  bd:  X . . . X . . . X . . . X . . .
  hh:  X . X . X . X . X . X . X . X .
```

Das ist schon ein Beat.

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*8")
)
```

Plus Backbeat-Claps. Das ist quasi der Standard-Drum-Pattern der Welt. Du wirst ihn überall hören.

### stack mit Lautstärken

Hihats sind oft zu laut. Per Layer abdimmen:

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*8").gain(0.4)
)
```

.gain() wirkt nur auf den Layer, an den es gehängt ist. Andere Layer bleiben unberührt.

### stack mit melodischem Layer

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*8").gain(0.4),
  note("c2 c2 eb2 g2").s("sawtooth").lpf(800).gain(0.6)
)
```

```
Vier Schichten:
  1. Kick — Puls
  2. Snare/Clap — Backbeat
  3. Hihat — Subdivision
  4. Bass-Linie — Melodie
```

Das ist der Aufbau der meisten elektronischen Tracks.

### Polyrhythmik — verschiedene Längen

stack() ist auch dann interessant wenn die Spuren NICHT dieselbe Anzahl von Schritten haben. Das ergibt Polyrhythmen.

```strudel
stack(
  s("bd*3"),    // 3 Bässe pro Cycle
  s("hh*4")     // 4 Hihats pro Cycle
)
```

3 gegen 4. Sie treffen sich nur am Anfang jedes Cycles.

```
  bd:  X . . . X . . . X . . .
  hh:  X . . X . . X . . X . .
       ↑                       ↑
     treffen                  treffen
```

Das fühlt sich verwoben an, nicht ganz greifbar.

```strudel
stack(
  s("bd*5"),    // 5 gegen 6 — typisch westafrikanisch
  s("hh*6")
)
```

### Polyrhythmik mit Kommas im selben String

Du kannst stack() umgehen indem du das Komma in Mini-Notation nutzt — auf oberster Ebene:

```strudel
s("bd*4, hh*16, ~ cp ~ cp")
```

Identisch zu stack() mit drei Spuren. Kürzer für einfache Sachen. Bei komplexeren Sachen wird stack() lesbarer.

### Spuren mit unterschiedlicher Tempo-Wirkung

Eine Spur kann pro Cycle auch LANGSAMER laufen.

```strudel
stack(
  s("bd*4"),
  s("hh*8").gain(0.4),
  note("c2 g1").s("sawtooth").lpf(400).slow(2)
)
```

Der Bass wechselt nur alle 2 Cycles. Drei Spuren, drei Geschwindigkeiten — aber alle synchron im großen Raster.

### ▶ AUFGABE: Drei-Schicht-Beat

```
Bau einen Beat mit:
  - Kick auf jedem Viertel
  - Snare auf 2 und 4
  - Hihat 16tel mit reduziertem Gain
  - (Optional) eine Bass-Note alle 2 Cycles
```

```strudel
stack(
  s("bd*4"),
  s("~ sd ~ sd"),
  s("hh*16").gain(0.3)
)
```

### Variation — verschiedene Hihat-Akzente

Ein 16tel-Hihat-Pattern wird interessanter, wenn manche Schläge betont sind.

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain("0.3 0.3 0.6 0.3 0.3 0.3 0.6 0.3"),
  note("c2*8").s("sawtooth").lpf(600)
)
```

.gain() kann selbst ein Pattern sein. Hier abwechselnd 0.3, 0.3, 0.6 — die 3. von 8 ist lauter, gibt einen kleinen Akzent.

Du kannst quasi jeden Parameter pattern-isieren. Das ist Strudels Superkraft.

### Stack mit Open-Hihat-Variation

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain(0.3),
  s("[~ ~ ~ oh]/2").gain(0.5)
)
```

Open-Hihat (oh) im 4. Step jedes zweiten Cycles. Klassisch.

### Mehrere Bass-Patterns übereinander — Vorsicht

```strudel
stack(
  s("bd*4"),
  note("c2*4").s("sawtooth").lpf(400),
  note("g2 ~ ~ ~").s("triangle").lpf(800)
)
```

Zwei Bass-Linien mit ähnlichem Frequenzbereich konkurrieren um den Platz. Gute Praxis: ein Sub-Bass tief, dazu eine Lead-Linie höher. Hier ist der Triangle-Bass den C-Bass im Weg — du hörst Matschiges.

In Kapitel 07 lernen wir Filter um sowas zu trennen.

💡 PRAXIS — Frequenz-Slots (Sound-Design-Konvention) Im Mix hat jeder Sound seinen Frequenzbereich. Wenn zwei Sounds denselben Slot besetzen, frisst einer den anderen.

```
Standard-Aufteilung (Pop/EDM):
  Sub      20-80 Hz    Sub-Bass, Kick-Tail
  Low      80-250 Hz   Bass-Body, Kick-Body
  Lower-Mid 250-500 Hz Pad-Body — oft "Matsch-Zone"
  Mid      500 Hz-2 kHz Vocals, Lead-Synth, Snare-Body
  Upper    2-5 kHz     Bite, Hihat-Body
  High     5-10 kHz    Hihat, Cymbal
  Air      10-20 kHz   Reverb-Tails
```

Layer-Faustregel: 2-5 Layer pro Patch. Drunter dünn, drüber Brei. Sweet Spot: 3 Layer (Body + Charakter + Air). Wenn du die Aufgabe eines Layers nicht in 3 Worten sagen kannst — raus damit.

### Variablen — Spuren wiederverwenden

stack() hat als Argument JEDES JS-Wert. Du kannst Spuren in Variablen speichern — das wird besonders ab Kapitel 11 (Song-Struktur) wichtig.

```strudel
const drums = stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain(0.3)
)

const bass = note("c2 c2 eb2 g2").s("sawtooth").lpf(700)

stack(drums, bass)
```

Dasselbe Ergebnis wie ein riesiger stack(), aber lesbarer. "drums" und "bass" sind Bausteine.

### FINALE — ein dichter Beat mit Variation

```strudel
const beat = stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain("0.3 0.3 0.5 0.3"),
  s("[~ ~ ~ oh]/2").gain(0.4)
)

const groove = note("c2 c2 eb2 g2 c2 c2 eb2 f2")
  .s("sawtooth")
  .lpf(800)
  .gain(0.7)

stack(beat, groove)
```

### ▶ AUFGABE: Schreib deinen ersten Stack

Mindestens drei Spuren. Mindestens eine Pause-Spur (~). Mindestens eine melodische Spur. Eine Spur mit reduziertem Gain. Keine Regel ist heilig. Probier.

## Akzente und Velocity

Ein durchlaufendes Hihat-Pattern klingt schnell wie ein Maschinengewehr. Echte Drummer setzen Akzente — manche Schlaege sind lauter, manche heller, manche kuerzer. Das macht den Unterschied zwischen "tickt im Hintergrund" und "groovet".

Die naechsten Snippets gehen von einfach zu komplett: erst Gain als Pattern, dann velocity, dann Round-Robin gegen die Maschinengewehr-Symmetrie.

### Gain als Pattern — die einfachste Variante

```strudel
s("hh*16").gain("1 0.4 0.4 0.4   0.4 0.4 0.4 0.4   1 0.4 0.4 0.4   0.4 0.4 0.4 0.4")
```

Akzent auf 1 und 3 (Step 1 und Step 9 im 16tel-Raster). Vier mal lauter — sofort hoerst du den Puls.

.gain() kann ein Pattern sein. Du legst die Velocity- Kurve direkt auf den Schlag.

### velocity statt gain

```strudel
s("hh*16").velocity("0.4 0.4 0.4 0.4   0.4 0.4 0.4 0.4   1 0.4 0.4 0.4   0.4 0.4 0.4 0.4")
```

.velocity() ist semantisch sauberer. Bei Drum-Samples triggert das oft auch Filter und Decay mit — wie bei einem echten Drumset, wo ein lauterer Schlag auch heller klingt. Bei Synths skaliert es zusaetzlich die Hull-Kurve.

### Akzent-Spur per stack

```strudel
stack(
  s("hh*16").gain(0.4),
  s("oh ~ ~ ~ ~ ~ ~ ~ ~ ~ oh ~ ~ ~ ~ ~").gain(0.6).cut(1)
)
```

Closed-Hihat durchgehend leise, Open-Hihat als Akzent. .cut(1) schneidet das Closed ab wenn das Open kommt — klassisches Drumkit-Verhalten (Closed und Open teilen sich in echt dieselbe Hihat).

### Mit Klangfarbe und Round-Robin

```strudel
stack(
  s("hh*16").n(irand(3)).gain(0.4).lpf(7000),
  s("oh ~ ~ ~ ~ ~ ~ ~ ~ ~ oh ~ ~ ~ ~ ~")
    .n(irand(2)).gain(0.65).hpf(300).speed(1.02)
    .attack(0.001).release(0.15).cut(1)
)
```

irand(3) waehlt pro Schlag eine andere Sample-Variante (0, 1 oder 2 — sofern das Pack so viele hat). Damit ist nie zwei mal hintereinander exakt derselbe Klang — das ist der Trick gegen Maschinengewehr.

Akzent-Open: heller (hpf 300), leicht hoeher gepitcht (speed 1.02), knackiger Release. Das ist wie's ein E-Drum mit Velocity-Layern macht.

### Funk-Hihat mit drei Akzent-Ebenen

```strudel
s("hh*16").gain("1 0.3 0.5 0.3   1 0.3 0.5 0.3   1 0.3 0.5 0.3   1 0.3 0.5 0.3")
```

Viertel volle Akzente (1.0), 8tel-Off mittel (0.5), Rest leise (0.3). Drei Velocity-Ebenen statt zwei — das ist der Unterschied zwischen "robotisch zwei-laut" und "menschlich". Klassischer Funk-Groove, klingt nach Bernard Purdie auf Pillen.

### Mini-Zusammenfassung Kapitel 03

```
  stack(...)              → mehrere Pattern zugleich
  "a, b, c"               → Komma im String, gleicher Effekt
  .gain(0.3)              → Lautstärke nur dieser Spur
  .gain("1 0.4 …")        → Velocity-Pattern, Akzente setzen
  .velocity(…)            → wie gain, aber triggert Filter/Decay
  .n(irand(3))            → Round-Robin gegen Maschinengewehr
  .cut(1)                 → Closed/Open-Hihat-Choke
  slow(n)                 → diese Spur n-fach langsamer
  const x = ...           → Spuren als Variablen
```

Polyrhythmik = unterschiedliche Step-Zahlen in den Spuren. Funktioniert "von alleine" — jede Spur teilt den Cycle nach ihrer eigenen Logik auf.

Weiter zu 04_euklidisch.strudel.
