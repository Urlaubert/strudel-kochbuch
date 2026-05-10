# Kapitel 08 — Signale und Modulation

Bis jetzt waren alle Werte STATISCH oder PATTERN-DISKRET. "lpf(800)" — immer 800. "lpf('200 800 2000')" — zwischen drei festen Werten gesprungen.

Jetzt: kontinuierliche Signale. Sinuswellen, Sägezähne, Perlin-Noise. Das sind Werte die SCHWANKEN über die Zeit. Damit baust du Filter-Sweeps, Auto-Pan, organische Variation, Riser, Fader.

### Das einfachste Signal — sine

sine ist ein Sinus-Signal. Werte zwischen 0 und 1, ein vollständiger Schwingungs-Zyklus pro Cycle.

```strudel
note("c4*16").s("sawtooth").lpf(sine.range(200, 4000))
```

Cutoff geht von 200 zu 4000 Hz und wieder runter — wie eine Welle. Klassischer Filter-Sweep, automatisch.

```strudel
note("c4*16").s("sawtooth").lpf(sine.range(200, 4000).slow(4))
```

.slow(4) — ein Sinus dauert 4 Cycles. Langsamer Sweep.

```strudel
note("c4*16").s("sawtooth").lpf(sine.range(200, 4000).fast(2))
```

.fast(2) — zwei Sinus-Wellen pro Cycle. Wackeliger.

💡 PRAXIS — LFO-Bereiche und ihre Wirkung Aus der Psychoakustik: LFO-Raten werden in fünf Wirkbereichen gehört. Jeder hat seinen Zweck. Bei cps=0.5 (2 s/Cycle):

```
  slow(8)+ → 0.06 Hz   "Drift, lebt"        (Analog-Emulation)
  slow(2-4) → 0.2-0.5 Hz "Atem, Schwebung"  (Pad-Filter, Wow)
  slow(1)  → 0.5 Hz    "erkennbare Welle"  (klassisches Vibrato)
  fast(2-3) → 1-3 Hz   "klar als Rhythmus" (Tremolo, Wobble)
  fast(8+) → 4-8 Hz    "Vibrato"           (Voice-/String-Vibrato)
  fast(15+) → 7-15 Hz  "nervös"            (Chiptune)
  fast(30+) → 15-30 Hz "Rauheit"           (Ringmod-Charakter)
  audio rate           → Klangfarbe         (FM-Synthese)
```

Default für "lebendig ohne aufdringlich": slow(2)-slow(8). Sehr häufig genau richtig. fast(2) klingt schon synthwave-ig.

### Andere Signal-Formen

```
sine       /‾‾\        /‾‾\        /‾‾\        weich, rund
          /    \      /    \      /    \
        _/      \____/      \____/      \____
```

```
saw          /|         /|         /|          Riser, springt
           _/ |       _/ |       _/ |
         _/   |     _/   |     _/   |
        /     |____/     |____/     |____
```

```
tri        /\          /\          /\          spitzer als sine
          /  \        /  \        /  \
        _/    \______/    \______/    \____
```

square   ‾‾‾‾|____|‾‾‾‾|____|‾‾‾‾|____         binär, an/aus

perlin   _/‾‾\__/‾‾\___/‾\___/‾‾\_/‾\___       organisch zufällig

```strudel
note("c4*16").s("sawtooth").lpf(saw.range(200, 4000))
```

Sägezahn — startet bei 200, steigt linear bis 4000, springt zurück. Klassischer Riser.

```strudel
note("c4*16").s("sawtooth").lpf(tri.range(200, 4000))
```

Dreieck — wie sine, aber spitzer.

```strudel
note("c4*16").s("sawtooth").lpf(square.range(200, 4000))
```

Rechteck — springt zwischen Min und Max. Klingt rhythmisch wie an/aus.

```strudel
note("c4*16").s("sawtooth").lpf(perlin.range(200, 4000))
```

Perlin-Noise — organisch zufällig. Keine zwei Cycles gleich, aber nie wild. Das natürlichste Signal.

### .range(min, max) — Mapping

Default-Bereich der Signale ist 0-1. Mit .range zappen wir den auf einen sinnvollen Bereich für den Parameter.

```strudel
s("hh*16").gain(sine.range(0.3, 0.8).slow(2))
```

Hihats werden lauter und leiser, im Wellenrhythmus.

```strudel
s("hh*16").pan(perlin.range(0.2, 0.8).slow(4))
```

Hihats wandern stereo organisch.

```strudel
s("hh*16").pan(saw.range(0, 1).slow(8))
```

Hihats wandern langsam von links nach rechts und springen alle 8 Cycles zurück. Ein Riser im Stereo-Feld.

### Mehrere Signale auf einer Spur

```strudel
note("c4*8")
  .s("sawtooth")
  .lpf(sine.range(200, 2000).slow(4))           // Filter-Wobble
  .pan(perlin.range(0.3, 0.7).slow(8))           // Pan-Drift
  .gain(saw.range(0.5, 1).slow(2))               // crescendo
```

Drei automatische Bewegungen gleichzeitig. Das klingt lebendig, ohne dass du auch nur einen Knopf drehen müsstest.

### Signale für TONHÖHEN — Vorsicht: kontinuierlich

```strudel
note(sine.range(60, 72))
```

Das ergibt ein GLISSANDO — die Tonhöhe schleift kontinuierlich von MIDI 60 zu 72 hoch und runter. Klingt wie Theremin.

### .segment(N) — kontinuierliches Signal diskretisieren

  ohne segment:        mit segment(8):

```
     ___                  ___
   /     \              ‾|   |‾
  /       \           ‾‾‾     ‾‾‾
                      ___       ___
                      __|       |__
```

```
  gleitend            8 Stufen pro Cycle
  (Theremin)          (Tonleiter)
```

```strudel
note(sine.range(60, 72).segment(8))
```

8 Töne pro Cycle, jeweils ein Wert vom Sinus abgegriffen. Diskrete Tonhöhen statt Glissando.

```strudel
note(sine.range(0, 12).segment(8)).scale("C:dorian")
```

Mit Skala. 8 Indices in C-Dorisch, vom Sinus gezogen.

```strudel
note(perlin.range(0, 14).segment(16)).scale("C:minorPentatonic").s("piano")
```

16 Töne pro Cycle aus C-Moll-Pentatonik, Perlin-organisch gewählt. Klingt wie improvisiertes Klavier.

### Signal mit einem Slider regeln

slider() rendert ein UI-Widget direkt im Editor. Du kannst damit live an Werten drehen während das Pattern läuft.

```strudel
const SPEED = slider(2, 0.25, 8, 0.25)

note("c4*16").s("sawtooth").lpf(sine.range(200, 4000).slow(SPEED))
```

Strg+Enter, dann am erscheinenden Slider live ziehen. SPEED = 0.25: super langsamer Sweep, dauert 4 Cycles. SPEED = 8: zackig.

```strudel
const DEPTH = slider(0.5, 0, 1, 0.05)

note("c4*16").s("sawtooth")
  .lpf(sine.range(200, 4000).slow(2)
    .fmap(v => 1000 + (v - 0.5) * 2000 * DEPTH))
```

Hier steuerst du die TIEFE des Sweeps. DEPTH = 0: kein Sweep. DEPTH = 1: voller Hub.

(Das ist schon fortgeschritten. .fmap() transformiert den Signal-Wert. Mehr dazu in Kapitel 16.)

### Square als Gate

```strudel
s("pad").gain(square.range(0, 1).fast(4))
```

Pad pulsiert vier Mal pro Cycle an/aus.

```strudel
s("pad").gain(square.range(0, 1).fast(8).slow(2))
```

Pulsiert 4x über 2 Cycles — also 4 Mal in 2 Cycles = alle halben Cycle einmal.

### pick — diskrete Auswahl aus einer Signal-Quelle

Manche Parameter sind nicht kontinuierlich. Beispiel: Drum-Sample-Bank, Skala, Hihat-Variante. .pick() nimmt eine Liste und einen Index, gibt das passende Element zurück.

```strudel
const auswahl = sine.range(0, 4).fmap(Math.floor)

note("c4*16").s("sawtooth")
  .lpf(auswahl.pick([400, 800, 1500, 3000]))
```

Sinus liefert kontinuierlich 0-4, fmap rundet auf 0/1/2/3, pick wählt einen der vier Cutoff-Werte. Ergibt einen stufigen Filter-Sweep zwischen vier festen Stufen.

Mit Slider: dynamische Auswahl

```strudel
const STUFE = slider(0, 0, 4, 1)

note("c4*8").scale(
  STUFE.pick(["C:major", "D:dorian", "F:lydian", "G:mixolydian", "A:minor"])
)
```

Slider auf 0-4 ziehen — die Skala wechselt diskret zwischen fünf Modi. Anders als .range das interpoliert, springt pick zwischen festen Werten.

pick() ist das Standard-Werkzeug wenn ein kontinuierlicher Wert (Signal, Slider) auf qualitativ unterschiedliche Sounds gemappt werden soll.

### rand und irand — pure Zufallszahlen

Ohne Glättung. Pro Sample/Step ein neuer Würfelwurf.

```strudel
s("hh*16").gain(rand.range(0.2, 0.8))
```

Jeder Hit eine andere Lautstärke, völlig zufällig. Wirkt chaotisch — anders als perlin (das fließt). Manchmal will man genau das.

```strudel
s("hh*8").n(irand(4))
```

.n() wählt eine Sample-Variante. irand(4) gibt eine Zufallszahl 0-3. Heißt: jede Hihat ist eine andere von vier Varianten — Round-Robin-Effekt, kein "Maschinengewehr".

### Maus als Signal — Quick-and-Dirty

```strudel
note("c4*8").s("sawtooth").lpf(mouseX.range(200, 4000)).pan(mouseY.range(0, 1))
```

Strg+Enter. Beweg die Maus. Filter folgt X, Pan folgt Y.

### Phasenversatz — zwei Spuren rotieren gegeneinander

```strudel
stack(
  s("hh*16").pan(sine.range(0, 1)),
  s("oh*8").pan(cosine.range(0, 1))
)
```

sine und cosine sind 90° versetzt. Wenn die eine Spur links ist, ist die andere mittig. Ergibt ein rotierendes Stereo-Bild.

### FINALE — Track mit fünf automatischen Bewegungen

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp").room(perlin.range(0.2, 0.5).slow(8)),
  s("hh*16")
    .gain(sine.range(0.3, 0.7).slow(4))
    .pan(perlin.range(0.3, 0.7).slow(2)),
  note("c2 c2 eb2 g2")
    .s("sawtooth")
    .lpf(sine.range(400, 2000).slow(8))
    .gain(0.7),
  note(perlin.range(0, 14).segment(8))
    .scale("C:minor")
    .add(12)
    .s("triangle")
    .lpf(2000)
    .gain(0.4)
    .room(0.5)
)
```

Bd starr. Cp mit wandernder Reverb-Tiefe. Hihats schwellen und drift en stereo. Bass mit langsamem Filter-Sweep. Lead- Linie aus Perlin-Noise gezogen, in C-Moll, eine Oktave hoch, mit Hall.

Nichts davon hast du explizit "automatisiert" — nur Signale gewählt und auf Parameter gemappt. Das ist Modulation.

### ▶ AUFGABE: Eine Spur, fünf Modulationen

```
Nimm note("c4*16").s("sawtooth"). Pack auf:
  .lpf(sine.range(?, ?).slow(?))
  .pan(perlin.range(?, ?))
  .gain(saw.range(?, ?).slow(?))
  .room(sine.range(?, ?).slow(?))
  .delay(square.range(?, ?))
```

Spiel mit den Werten bis du was hast was atmet.

### Mini-Zusammenfassung Kapitel 08

```
  sine, cosine, saw, tri, square, perlin, rand, irand
  .range(min, max)         → auf sinnvollen Bereich mappen
  .slow(n) / .fast(n)      → Geschwindigkeit
  .segment(n)              → diskrete Werte aus kontinuierlichem Signal
  slider(default, min, max, step)  → Live-Regler
```

```
Faustregeln:
  - Filter, Pan, Gain → kontinuierliche Signale (sine, perlin)
  - Tonhöhen          → mit segment() diskretisieren
  - Riser/Fader       → saw oder tri
  - Organisch         → perlin
  - Pulsieren         → square
```

Weiter zu 09_time_modifier.strudel.
