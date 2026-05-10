# Kapitel 06 — Akkorde und Voicings

Mehrere Töne gleichzeitig. Du kannst sie als Stack schreiben, in eckigen Klammern mit Komma, oder mit dem .voicing()-Helper. Hier sind alle drei Wege — und ein paar Tricks, wie du Akkord-Folgen lebendiger machst.

### Klassischer Stack — drei Stimmen, ein Akkord

```strudel
stack(
  note("c4").s("piano"),
  note("e4").s("piano"),
  note("g4").s("piano")
)
```

C-Dur. Klingt wie sich vorgestellt, aber etwas steif — alle drei treffen exakt zusammen.

### Akkord in einem String — Komma in eckigen Klammern

```strudel
note("[c4, e4, g4]").s("piano")
```

Identisch zu oben. Drei Töne in einem Step.

```strudel
note("[c4, e4, g4] [d4, f4, a4] [e4, g4, b4] [c4, e4, g4]").s("piano")
```

Vier Akkorde pro Cycle. Klingt nach Übungs-Klavier.

### Akkord-Pattern mit Variation

```strudel
note("<[c4, e4, g4] [a3, c4, e4] [f3, a3, c4] [g3, b3, d4]>").s("piano")
```

Vier Akkorde, einer pro Cycle (spitze Klammern). C-Dur, A-Moll, F-Dur, G-Dur. Die berühmte 1-6-4-5-Progression. Du hast das in Hunderten Songs gehört.

### Akkorde mit Skalen-Indices

Du kannst Akkorde als Skalen-Indices schreiben:

```strudel
note("[0, 2, 4] [3, 5, 7] [4, 6, 8] [0, 2, 4]").scale("C:minor").s("piano")
```

"Drei Töne im Abstand 0-2-4" ist die Definition eines Skalen-Dreiklangs. Das funktioniert in JEDER Skala — du musst nicht die Töne wissen, nur die Stufen.

### Voicing — der Strudel-Helper

Schreib einfach den Akkord-Namen, Strudel macht die Töne.

```strudel
voicing("<C^7 Am7 Dm7 G7>").s("piano")
```

Vier Jazz-Akkorde durchgespielt. ^7 = Major-Sept, m7 = Minor-Sept, 7 = Dominant-Sept.

HINWEIS: voicing() braucht oft das @tonal-package, das in vielen Strudel-Versionen out-of-the-box geht. Wenn nicht geht — die Stack-Variante oben funktioniert immer.

### Akkord-Folge in Moll — der "düstere Klassiker"

```strudel
note("<[0,2,4] [3,5,7] [-1,1,3] [-3,-1,1]>").scale("C:minor").s("piano").slow(2)
```

1-4-7-5 in Moll. Je nach Skala kannst du die exakten Akkorde aus dem Pattern herausschmecken.

### Voicing-Tricks — wo Akkorde lebendig werden

Trick 1: Stretch — Akkord über mehrere Oktaven

```strudel
note("[c2, g3, e4, c5]").s("piano")
```

Bass tief, Rest hoch. Klingt offener als alles eng zusammen.

Trick 2: Rolle — Akkord-Töne nacheinander statt zusammen

```strudel
note("c2 g3 e4 c5").s("piano")
```

Identische Noten, aber NACHEINANDER. Das ist eine "broken chord" — Arpeggio.

Trick 3: Akkord als Pad — lange Töne mit Filter

```strudel
stack(
  note("[c4, e4, g4]").s("sawtooth").attack(0.5).release(2).lpf(1500).gain(0.5),
  note("[a3, c4, e4]").s("sawtooth").attack(0.5).release(2).lpf(1500).gain(0.5).slow(2)
)
```

Zwei Akkorde, jeweils mit Attack + Release lang gehalten, gefiltert. Das ist ein Pad.

### Arpeggio — Akkord auseinandergezogen

```strudel
note("c4 e4 g4 b4 g4 e4").s("piano").fast(2)
```

C-Maj7-Arpeggio rauf und runter.

```strudel
note("0 2 4 7 4 2").scale("C:dorian").s("piano").fast(2)
```

Indices in C-Dorisch — selbe Idee, aber abstrakt schreibbar.

### Arpeggio über mehrere Akkorde

```strudel
note("0 2 4 7").scale("<C:minor F:minor Ab:major Bb:major>").s("piano").fast(2)
```

Pro Cycle wechselt die Skala, der Arpeggio-Pattern bleibt. Vier verschiedene Akkord-Arpeggios in vier Cycles.

### Akkord-Folge mit Bass

```strudel
stack(
  note("<c2 a1 f1 g1>").s("sawtooth").lpf(400),
  note("<[c4,e4,g4] [a3,c4,e4] [f3,a3,c4] [g3,b3,d4]>")
    .s("triangle").lpf(1200).attack(0.1).release(0.4)
)
```

Bass spielt die Grundtöne. Akkorde drüber als Pad-artige Triade. Das ist die Skelett-Struktur eines Songs.

### FINALE — Akkord-Track mit Drums

```strudel
const skl = "<C:minor F:minor Ab:major Eb:major>"

stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain(0.3),
  note("0").scale(skl).sub(12).s("sawtooth").lpf(400).gain(0.7),
  note("[0, 2, 4]").scale(skl).s("triangle").lpf(1500).attack(0.05).release(0.5).gain(0.5),
  note("0 4 2 7").scale(skl).add(7).s("piano").fast(2).gain(0.4)
)
```

Vier Akkorde wechseln pro Cycle (skl). Bass-Grundton tief. Drei-Stimm-Akkord in der Mitte. Arpeggio oben mit Piano. Das ist ein vollständiger Track-Skelett.

### ▶ AUFGABE: Variiere die Akkord-Folge

```
Tausch in skl die vier Skalen aus. Was klingt:
  "<C:major G:major Am:minor F:major>"   ← I-V-vi-IV (Pop-Standard)
  "<C:minor Bb:major G:minor F:minor>"   ← Düster
  "<E:phrygian E:phrygian F:major E:phrygian>"  ← Spanish
```

Versuch noch mehr eigene. Notation: Tonika:Modus.

### Voicing-Theorie — was klingt warum gut

```
Ein Dreiklang besteht aus Grundton + Terz + Quinte.
  Major: 0, 4 Halbtöne, 7 Halbtöne (große Terz)
  Minor: 0, 3 Halbtöne, 7 Halbtöne (kleine Terz)
  Diminished: 0, 3, 6 (verminderte Quinte — sehr spannend)
  Augmented: 0, 4, 8 (übermäßige Quinte — schwebend)
```

In Strudels .scale()-Notation entsprechen die Indices 0, 2, 4 IMMER einem Dreiklang im Modus der Skala — ob er dur oder moll ist, hängt von der Skala ab.

Heißt: Du musst nicht wissen "ist das jetzt Eb-Dur oder E-Moll" — du wählst eine Skala, schreibst 0,2,4 und der Akkord stimmt für diese Skala.

### Mini-Zusammenfassung Kapitel 06

```
  "[c4, e4, g4]"                 → Akkord in einem Step
  stack(note("c4"), ...)         → drei Stimmen parallel
  note("[0, 2, 4]").scale(...)   → Akkord aus Skalen-Indices
  voicing("<C^7 Am7>")            → Akkord aus Akkord-Namen
  note("c4 e4 g4")                → Arpeggio (auseinander)
```

Akkord-Sequenzen pro Cycle wechseln: <[a,b,c] [d,e,f]> oder Skala wechseln und gleiche Indices behalten.

Weiter zu 07_effekte.strudel.
