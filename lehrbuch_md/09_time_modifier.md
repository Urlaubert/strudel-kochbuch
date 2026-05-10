# Kapitel 09 — Time Modifier

Zeit ist in Strudel kein passiver Hintergrund — sie ist ein Parameter wie alles andere. Du kannst sie strecken, stauchen, umdrehen, segmentieren, mit Wahrscheinlichkeit verändern.

Diese Funktionen sind das Werkzeug um aus einem Loop ein LEBENDES Pattern zu machen — Variation ohne dass man jeden Cycle neu schreibt.

### fast / slow — Tempo lokal ändern

```strudel
s("bd hh sd hh")          // 4 Hits pro Cycle
s("bd hh sd hh").fast(2)  // 8 Hits pro Cycle (gleich wie *2 in Mini)
s("bd hh sd hh").slow(2)  // 4 Hits pro 2 Cycles
```

Identisch:

```strudel
s("bd*2 hh*2 sd*2 hh*2")
s("bd hh sd hh").fast(2)
```

### rev — rückwärts spielen

```strudel
note("c4 d4 e4 g4").rev()
```

g, e, d, c — die Tonfolge umgekehrt.

```strudel
s("bd cp sd cp").rev()
```

Auch auf Drums. Letzter Hit wird erster.

### every(n, fn) — alle n Cycles eine Variation

```
  Cycle:   1     2     3     4     5     6     7     8
  Pattern: norm  norm  norm  fast  norm  norm  norm  fast
                               ↑                       ↑
                             every(4, fast(2)) greift hier
```

  Heißt: 75% der Zeit normal, alle 4 Cycles eine Variation.

```strudel
s("bd hh sd hh").every(4, fast(2))
```

Jeden 4. Cycle ist das Pattern doppelt so schnell.

```strudel
s("bd hh sd hh").every(4, rev)
```

Jeden 4. Cycle rückwärts.

```strudel
s("bd hh sd hh").every(8, x => x.fast(2).rev())
```

Jeden 8. Cycle: doppelt so schnell UND rückwärts.

Eine Spur die meistens gleich ist, aber regelmäßig "etwas Anderes" macht. Häufiger Trick.

### sometimes / rarely / often — Wahrscheinlichkeit

```strudel
s("bd*4").sometimes(rev)
```

Mit 50% Wahrscheinlichkeit wird der Cycle gerev't.

```strudel
s("hh*16").rarely(fast(2))
```

Selten (~10%) wird das Pattern doppelt so schnell.

```strudel
s("hh*16").often(jux(rev))
```

Oft (~75%) wird der Stereo-Trick angewendet.

💡 PRAXIS — Anti-Loop: eine Voice generativ, Rest fest Foren-Konsens (sequencer.de, recording.de): wenn ein Loop langweilt, mach NICHT alles variabel. EINE Spur generativ, alles andere bleibt fest. Das gibt Bewegung ohne den Track zu zerschießen.

```strudel
stack(
  s("bd*4"),                           // FEST
  s("~ cp ~ cp"),                      // FEST
  s("hh*16").gain(0.4)                 // EINE Spur generativ:
    .sometimesBy(0.3, x => x.fast(2)), //   30% Roll-Variation
  note("c2 c2 eb2 g2")                 // FEST
    .s("sawtooth").lpf(500)
)
```

30% ist ein guter Default — selten genug dass es überrascht, häufig genug dass jeder 4-Cycle-Loop anders klingt.

### degrade / degradeBy — Hits weg-würfeln

.degradeBy(p) wirft pro Event mit Wahrscheinlichkeit p den Hit komplett weg. .degrade() ist das gleiche mit p=0.5.

Anders als sometimes (wendet eine Funktion an): degradeBy arbeitet pro Hit auf dem Pattern selbst.

```strudel
s("hh*16").degradeBy(0.3)
```

30% der Hihats fallen aus. Pattern wird "luftiger". Klassisches Anti-Maschinen-Idiom.

```strudel
s("hh*16").degrade()
```

Identisch zu .degradeBy(0.5).

Praktisch um eine Probability-Achse mit einem Slider zu bauen:

```strudel
const E = slider(0.5, 0, 1, 0.05)
s("hh*16").degradeBy(E.fmap(v => 1 - v))
```

E hoch = mehr Hits durchlassen. E niedrig = mehr werden weggewürfelt. Switch-Angel-Standard für Energie-Achsen.

### Klassischer Build-Up

```strudel
s("bd*4, ~ cp ~ cp, hh*16").every(8, x => x.fast(2))
```

Sieben Cycles normal, jeden 8. Cycle einen Roll. Klassischer "Drum-Fill am Ende der Phrase".

### late / early — Timing-Versatz

```strudel
stack(
  s("bd*4"),
  s("hh*8").late(0.125)
)
```

Hihat ist um 1/8 Cycle versetzt. Klingt nach Off-Beat.

```strudel
stack(
  s("bd*4"),
  s("hh*8").early(0.05)
)
```

Hihat kommt 0.05 Cycle FRÜHER. Wirkt aggressiver, "vorne".

### swing — Groove-Versatz

```strudel
s("hh*8")           // strikt gleichmäßig
s("hh*8").swing(4)  // Swing-Feel auf 4tel-Grid
s("hh*8").swingBy(0.6, 4)  // weniger Swing
s("hh*8").swingBy(1, 4)    // sehr starker Swing (Triolen)
```

### compress / zoom — nur ein Teil des Cycles

```strudel
s("bd hh sd hh").compress(0.25, 0.75)
```

Pattern wird in Mitte zusammengedrückt — Stille davor und danach.

```strudel
s("bd hh sd hh").zoom(0, 0.5)
```

Nur erste Hälfte des Patterns, gestreckt auf vollen Cycle.

```strudel
s("bd hh sd hh").zoom(0.5, 1)
```

Nur zweite Hälfte.

### linger — wiederholen

```strudel
note("c4 e4 g4 b4").linger(0.5)
```

Spielt nur die ERSTE HÄLFTE des Patterns, aber zweimal pro Cycle. Ergibt: "c4 e4 c4 e4" pro Cycle.

```strudel
note("c4 e4 g4 b4").linger(0.25)
```

Erste 25%, viermal — also "c4 c4 c4 c4".

### ply — jedes Event vervielfältigen

```strudel
s("bd cp sd").ply(2)
```

"bd bd cp cp sd sd" — jeder Hit verdoppelt.

```strudel
s("bd cp sd").ply("<1 2 3 4>")
```

Pro Cycle anderer Vervielfacher: 1, 2, 3, 4, dann von vorn.

### off — versetztes Echo im Pattern

```strudel
note("c d e g").off(1/8, x => x.add(7))
```

Original-Pattern + dasselbe Pattern 1/8 Cycle später, 7 Halbtöne (Quinte) höher. Ergibt einen Quint-Versatz-Effekt.

### iter — Pattern jeden Cycle weiter rotieren

```strudel
note("0 1 2 3 4 5 6 7").scale("C:major").iter(4)
```

Jeder Cycle startet das Pattern an einer anderen Stelle. Pattern wandert durch sich selbst.

### palindrome

```strudel
s("bd cp sd hh").palindrome()
```

Ein Cycle vorwärts, einer rückwärts, abwechselnd.

### struct — Rhythmus auf Tonfolge anwenden

```strudel
note("c d e g").struct("1 0 1 1 0 1")
```

Tonfolge wird über die struct-Maske gesteuert: 1 = spielen, 0 = Pause. Die Töne kommen reihum auf die 1en.

```
  Position:  1  2  3  4  5  6
  Struct:    1  0  1  1  0  1
  Note:      c  -  d  e  -  g
             ↑     ↑  ↑     ↑
            c      d  e     g  ← jede 1 schluckt eine Note
```

```strudel
note("c d e g").struct("1 0 1 1 0 1 0 1")
```

8 Steps mit 5 Hits — ergibt einen ungleichmäßigen Rhythmus.

### mask — ganze Cycles ein/aus

  mask("<1 1 0 1>")

```
  Cycle:    1   2   3   4   5   6   7   8
  Mask:     1   1   0   1   1   1   0   1
  Output:  XXX XXX  -  XXX XXX XXX  -  XXX
                    ↑               ↑
                  stumm           stumm
```

```strudel
s("bd*4").mask("<1 1 0 1>")
```

Erste 2 Cycles spielt bd, 3. Cycle aus, 4. wieder an. Wichtig für Build-Ups: ein Layer kommt zu bestimmten Cycles dazu/fällt weg.

```strudel
stack(
  s("bd*4"),
  s("~ cp ~ cp").mask("<0 1 1 1>"),
  s("hh*16").gain(0.4).mask("<0 0 1 1>")
)
```

Cycle 1: nur Kick. Cycle 2: + Snare. Cycle 3: + Snare + Hihats. Cycle 4: alles. Klassischer Aufbau einer Phrase.

### chunk — N Cycles, jedes Mal auf einem anderen Step

```strudel
s("bd hh sd hh").chunk(4, fast(2))
```

4 Cycles. Jeden Cycle wird ein anderer Step "doppelt schnell". Ergibt eine wandernde Akzent-Welle.

### fastChunk

```strudel
s("bd cp sd hh").fastChunk(4, fast(2))
```

Wie chunk, aber alles in einem Cycle gestaucht.

### FINALE — Loop mit eingebauter Variation

```strudel
stack(
  s("bd*4")
    .every(8, fast(2)),
  s("~ cp ~ cp")
    .sometimes(rev),
  s("hh*16")
    .gain(0.4)
    .every(4, x => x.fast(2))
    .pan(perlin.range(0.3, 0.7)),
  note("c2 c2 eb2 g2")
    .scale("C:minor")
    .s("sawtooth")
    .lpf(sine.range(400, 2000).slow(8))
    .every(8, rev),
  note("0 4 7 4")
    .scale("C:minor")
    .add(14)
    .s("triangle")
    .gain(0.5)
    .room(0.5)
    .every(8, x => x.fast(2).rev())
)
```

Sechs Spuren. Jede hat ihre eigene Variations-Logik. Bd: alle 8 Cycles ein Roll. Cp: ab und zu rückwärts. Hh: alle 4 Cycles doppelt schnell, dazu Pan-Drift. Bass: alle 8 Cycles rückwärts, dazu langsamer Filter-Sweep. Lead: alle 8 Cycles ein doppelt-schnell-und-rückwärts.

Spielt für 64 Cycles ohne dass es langweilig wird, weil die Variations-Zyklen unterschiedlich sind und sich überlagern.

### ▶ AUFGABE: Variations-Schichtung

```
Nimm einen schlichten Beat: bd*4, hh*8, ~ cp ~ cp.
Pack auf jede Spur eine andere Variations-Logik:
  - bd: every(N, ?)
  - hh: sometimes(?)
  - cp: rarely(?)
```

Welche N und Variationen klingen am besten?

### Mini-Zusammenfassung Kapitel 09

```
  .fast(n) / .slow(n)      → Tempo
  .rev()                   → rückwärts
  .every(n, fn)            → alle n Cycles fn anwenden
  .sometimes(fn)           → 50% pro Event
  .rarely(fn) / .often(fn) → 10% / 75%
  .late(c) / .early(c)     → Timing-Versatz
  .swing(n)                → Groove
  .compress(s, e)          → Pattern in Mitte
  .zoom(s, e)              → Ausschnitt strecken
  .struct("1 0 1")         → Rhythmus-Maske auf Töne
  .mask("<1 0 1 1>")       → Cycle-weise an/aus
  .ply(n)                  → jedes Event n-fach
  .off(t, fn)              → versetzte Kopie
```

Die wichtigsten zwei sind every() und mask(). Mit denen allein machst du Variation ohne Code-Schreiben.

Weiter zu 10_samples_eigene.strudel.
