# Kapitel 17 — Eigene Helper-Funktionen

Bisher hast du Strudel benutzt wie es kommt. Jetzt baust du dir eigene Vokabeln. Helper-Funktionen die deine Sprache erweitern: ein Aufruf, viele Effekte. "macheBassWarm()" statt 8 Zeilen Filter-Distortion-Reverb-EQ.

Das ist der Schritt vom Nutzer zum Live-Coder mit eigener Handschrift.

### Warum eigene Helper

Drei Gründe:

```
1. WIEDERVERWENDUNG. Wenn du im Set fünf Mal "lpf, lpenv,
   lpa, lpd, distort" auf einen Bass packst, einmal als
   Helper schreiben, fünf Mal aufrufen.
```

2. ABSTRAKTION. "energieShift(beat, 0.7)" sagt mehr als    ".lpf(2000).gain(0.8).room(0.3).delay(0.4)".

```
3. ACHSEN. Eine "Achse" wie "Energie" ist ein Wert (0-1)
   der GLEICHZEITIG mehrere Parameter steuert. Das geht nur
   mit Helpern.
```

### Variante A — freie Funktion (Inline, sicher)

```strudel
function acidBass(pat) {
  return pat
    .s("sawtooth")
    .lpf(150).lpenv(8).lpa(0).lpd(0.15).lpq(15)
    .distort(0.2)
    .release(0.1)
    .gain(0.7)
}
```

Verwendung:

```strudel
acidBass(note("c2*8 eb2*4 g1 c2"))
```

Du übergibst ein NOTE-Pattern, der Helper packt den ganzen Sound-Kram drauf.

### Variante B — register() für chainbare Methoden (Prebake)

Mit register() wird aus dem Helper eine echte chainbare Pattern-Methode: drums.energieShift(E) statt energieShift(drums, E).

ABER: register() funktioniert in inline strudel.cc-Sessions NICHT zuverlässig. Stille Layer ohne Fehlermeldung. register() gehört in den PREBAKE-Bereich der Strudel- Settings — wird einmal beim Laden ausgeführt und ist dann in jeder Session da.

```
In Prebake-Settings:
  register('acidBass', (pat) => pat
    .s("sawtooth")
    .lpf(150).lpenv(8).lpa(0).lpd(0.15).lpq(15)
    .distort(0.2).release(0.1).gain(0.7))
```

Dann in Sessions:   note("c2*8").acidBass()

Faustregel: ENTWICKELN als freie Funktion (testen, debuggen), PRODUKTIV als register im Prebake.

### Achsen-Pattern — Wert + Helper-Funktion

Eine "Achse" ist ein Slider-Wert (0-1) der mehrere Effekte steuert. Switch Angel hat das Pattern etabliert.

1. Der Wert (live regelbar)

```strudel
const ENERGIE = slider(0.3, 0, 1, 0.05)
```

2. Helper: was kommt an Klang dazu?

```strudel
function energieLayer(e) {
  return stack(
    s("hh*16").gain(e.range(0, 0.6)),
    s("[~ ~ ~ oh]/2").gain(e.range(0, 0.5))
  )
}
```

3. Helper: wie färbt es bestehende Klänge ein?

```strudel
function energieShift(pat, e) {
  return pat
    .lpf(e.range(400, 5000))
    .gain(e.range(0.6, 1))
    .room(e.range(0.1, 0.4))
}
```

4. Verwendung

```strudel
const drums_basis = stack(s("bd*4"), s("~ cp ~ cp"))

stack(
  energieShift(drums_basis, ENERGIE),
  energieLayer(ENERGIE)
)
```

Schiebe den ENERGIE-Slider live. Bei 0: nur Bass+Snare, dunkel, leise. Bei 1: vollgepackt, hell, mit Hall. EIN Slider, viele Wirkungen.

### Slider-Smoothing mit Quadratkurve

Filter und Hall hören wir nicht-linear. Slider-Wert direkt auf den Effekt → fühlt sich oben gestaucht an.

Switch-Angels Trick: Slider-Wert quadrieren — bei 0.5 kommt 0.25, bei 0.7 kommt 0.49, bei 1.0 bleibt 1.0. Macht die untere Hälfte feiner regelbar.

```strudel
function sq(pat) {
  return pat.fmap((v) => v * v)
}

const E = sq(slider(0.5, 0, 1, 0.01))
```

Verwendung wie oben, aber mit feinerer Auflösung in der kritischen unteren Hälfte:

```strudel
energieShift(drums_basis, E)
```

### Mehrere Achsen — eine Mixer-Bank am Top

```strudel
const E = sq(slider(0.5, 0, 1, 0.01))   // Energie
const W = sq(slider(0.3, 0, 1, 0.01))   // Wärme
const T = sq(slider(0.0, 0, 1, 0.01))   // Tension

function waermeShift(pat, w) {
  return pat
    .lpf(w.range(8000, 1500))    // wärmer = dumpfer (Filz)
    .room(w.range(0.1, 0.5))     // wärmer = halliger
    .gain(w.range(1, 0.85))      // wärmer = leiser
}

function tensionShift(pat, t) {
  return pat
    .gain(t.range(1, 0.7))       // Tension = leiser (Schock-Stille)
    .distort(t.range(0, 0.2))    // angekratzt
    .delay(t.range(0, 0.4))      // Echo wird weiter
}
```

Verwendung: alle drei nacheinander auf eine Spur

```strudel
const grundszene = stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  note("c2*8").s("sawtooth").lpf(800)
)

stack(
  tensionShift(waermeShift(energieShift(grundszene, E), W), T),
  energieLayer(E)
)
```

Drei Slider, drei Achsen, ein Track. Live-Coding-Performance wird zum Slider-Tanz.

### Der "Standard-Drum-Helper"

```strudel
function standardDrums(intensity = 0.5) {
  return stack(
    s("bd*4").gain(intensity.range ? intensity.range(0.7, 1) : 0.9),
    s("~ cp ~ cp").gain(intensity.range ? intensity.range(0, 0.8) : 0.7),
    s("hh*16").gain(intensity.range ? intensity.range(0.2, 0.5) : 0.4)
  )
}
```

Verwendung mit festem Wert:

```strudel
standardDrums(0.7)
```

Oder mit Slider:

```strudel
const I = slider(0.5, 0, 1, 0.05)
```

standardDrums(I)

(Hinweis: Default-Werte und Pattern-Werte gemischt zu handlen ist tricky — dieser Helper braucht Polish. In Produktion würde man getrennt: standardDrumsFixed(0.7) und standardDrumsPattern(I).)

### Der "Charakter-Layer" — eigene Klänge zu einem Wert

```strudel
function affenLayer(presence) {
  return stack(
    s("crow*2").gain(presence.range(0, 0.7)).slow(2),
    note("c5 e5 ~ g5").s("sawtooth").gain(presence.range(0, 0.4)).fast(2)
  )
}

const AFFE = sq(slider(0, 0, 1, 0.05))

stack(
  grundszene,
  affenLayer(AFFE)
)
```

Bei AFFE = 0: nur grundszene. Bei AFFE = 1: voll mit Krähen (für Affen brauchen wir eigene Samples).

### Prebake-Datei aufbauen (für Strudel-Settings)

Wenn deine Helper stabil sind, packst du sie in eine "prebake.strudel"-Datei und kopierst sie in die Strudel- Settings → Prebake. Dann sind sie in JEDER Session global verfügbar.

```strudel
/*
```

=== prebake.strudel === Lade einmal in Strudel Settings → Prebake.

Slider-Smoothing

```strudel
register('sq', (pat) => pat.fmap((v) => v * v))
```

Sound-Presets

```strudel
register('acidBass', (pat) => pat
  .s("sawtooth")
  .lpf(150).lpenv(8).lpa(0).lpd(0.15).lpq(15)
  .distort(0.2).release(0.1).gain(0.7))

register('warmPad', (pat) => pat
  .s("sawtooth")
  .attack(1).release(3)
  .lpf(1500).gain(0.4))
```

Achsen-Helper

```strudel
register('energieShift', (e, pat) => pat
  .lpf(e.range(400, 5000))
  .gain(e.range(0.6, 1))
  .room(e.range(0.1, 0.4)))
```

... weitere Helper

```strudel
*/
```

### Konvention: Achsen-Variablen GROSS, Sounds klein

Etablierte Live-Coder unterscheiden visuell:

const E = sq(slider(0.5))     ← GROSS = Live-Wert const drums = stack(...)       ← klein = Pattern

Im fertigen Code siehst du sofort: was sind Regler, was sind Sounds. Hilfreich beim Live-Performance-Stress.

### FINALE — Performance-Datei mit Achsen

(Voraussetzung: alle Helper in Prebake geladen, oder hier als freie Funktionen oben definiert.)

=== ACHSEN ===

```strudel
const ENRG = sq(slider(0.5, 0, 1, 0.01))
const WARM = sq(slider(0.3, 0, 1, 0.01))
const TENS = sq(slider(0.0, 0, 1, 0.01))
const AFFE_SLIDER = sq(slider(0.0, 0, 1, 0.01))
```

=== SOUNDS ===

```strudel
const drums = stack(s("bd*4"), s("~ cp ~ cp"))
const bass  = note("c2 c2 eb2 g2").s("sawtooth").lpf(500)
const pad   = note("[c4, eb4, g4]").s("sawtooth").attack(1).release(2).lpf(1500).gain(0.3)
```

=== MIX ===

```strudel
stack(
  tensionShift(waermeShift(energieShift(drums, ENRG), WARM), TENS),
  bass.gain(ENRG.range(0.6, 1)),
  pad,
  energieLayer(ENRG),
  affenLayer(AFFE_SLIDER)
)
```

Vier Slider am Top des Editors. Performer dreht Slider live. Code muss nicht mehr verändert werden — der Track ATMET durch die Slider.

### ▶ AUFGABE: Eigene Achse bauen

Definiere eine Achse "Trockenheit" — bei 0 viel Hall und Delay, bei 1 absolut trocken. Sie soll auf die ganze Mischung wirken.

Schritte: 1. const D = sq(slider(0.5, 0, 1, 0.01)) 2. function trockenShift(pat, d) { return pat... } 3. Verwendung: trockenShift(stack(...), D)

### Designprinzipien für Helper-Library

Aus Switch Angels Stil:

1. EIN Helper, EIN Konzept. Nicht 10 Modi in einer Funktion. 2. Defaults die "richtig" klingen — bei Wert 0 transparent. 3. Range-Limits beachten. Nie lpf auf 0 oder gain auf 0    ohne Sicherheitsabstand → sonst Stille/Clipping. 4. Zwei Funktionen pro Achse: xLayer(x) und xShift(pat, x). 5. Composable — Helper können andere Helper nutzen. 6. Test-Snippet pro Helper im Helper-File.

### Mini-Zusammenfassung Kapitel 17

```
  function name(pat) { return pat... }      → freie Funktion
  register('name', (pat) => ...)             → chainbar (nur in Prebake!)
  .fmap(v => transformation(v))               → pro Sample-Wert ändern
  sq(slider(...))                             → Slider-Smoothing
```

```
Achsen-Pattern:
  const X = sq(slider(default, 0, 1, 0.01))
  function xLayer(x) { return stack(...) }
  function xShift(pat, x) { return pat... }
  stack(xShift(scene, X), xLayer(X))
```

Mit eigenen Helpern wird Live-Coding zu KOMPONIEREN — du hast Vokabeln für Stimmungen, nicht nur für Filter.

Weiter zu 18_hap_internals.strudel.
