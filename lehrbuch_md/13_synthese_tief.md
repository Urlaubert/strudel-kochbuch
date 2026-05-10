# Kapitel 13 — Synthese, tiefer

Strudels eingebaute Synths sind einfach — sine, sawtooth, square, triangle, supersaw. Mit ADSR und Filter-Envelopes kannst du daraus aber sehr viel rausholen.

Hier: wie du aus den Bordmitteln Bass, Lead, Pad, Stab, Pluck, Acid, Sub baust. Plus FM (siehe DX-Helper).

Wichtig: Strudel ist NICHT für Custom-SynthDefs gemacht. Wenn du komplexe Patches willst — vorher in Vital/Reaper rendern und als WAV laden (siehe Kapitel 10).

### Die fünf Grund-Wellenformen

```
  sine       /‾‾\        nur Grundton, keine Obertöne
            /    \       → Sub-Bass, weich
          _/      \_
```

```
  triangle  /\          ungerade Obertöne, schwächer
           /  \         → sanfte Leads
         _/    \_
```

```
  sawtooth   /|         alle Obertöne, harmonisch reich
           _/ |         → Bass, Lead-Synth, Strings
          /   |____
```

```
  square    ‾‾‾‾|____   nur ungerade Obertöne, hohl
                        → Hammond-artig, Bass
```

```
  pulse     ‾‾|________  veränderbare Breite
                        → Vintage-Pads (mit pwm)
```

```strudel
note("c3").s("sine")         // rein, weich, kein Boden
note("c3").s("triangle")     // sanft, mit Obertönen
note("c3").s("sawtooth")     // alle Obertöne, brassig
note("c3").s("square")       // ungerade Obertöne, hohl
note("c3").s("pulse").pwm(0.3)  // Square mit veränderlicher Pulsbreite
```

### Bass-Sound 1 — Sub-Bass

```strudel
note("c2*4").s("sine").attack(0.01).release(0.3).gain(0.9)
```

Sinus tief, kurze Hüllkurve. Klingt wie Sub-Bass im Auto- Subwoofer. Geht in den Bauch, nicht in die Ohren.

### Bass-Sound 2 — Sägezahn-Bass mit Filter

```strudel
note("c2 c2 eb2 g2").s("sawtooth")
  .lpf(600)
  .attack(0.01).release(0.2)
  .gain(0.7)
```

Klassiker. Filter zähmt die Schärfe.

### Bass-Sound 3 — Acid-Bass (TB-303-Style)

```strudel
note("c2*8").s("sawtooth")
  .lpf(150)                              // tiefer Cutoff
  .lpenv(8)                              // Envelope öffnet 8 Oktaven
  .lpa(0).lpd(0.15)                      // schneller Attack, mittlerer Decay
  .lpq(15)                               // hohe Resonanz — pfeift
  .distort(0.2)
  .release(0.1)
  .gain(0.7)
```

Das ist der Roland-TB-303-Sound. Fast jeder elektronische Bass mit Wow-Charakter ist das hier oder Variation.

### Bass-Sound 4 — FM-Bass

```strudel
note("c2*4").s("triangle")
  .fmh(2)         // FM-Carrier-zu-Modulator-Ratio
  .fmi(3)         // FM-Index (wie tief moduliert)
  .lpf(800)
  .attack(0.01).release(0.3)
  .gain(0.7)
```

fmh / fmi sind für die FM-Synthese (siehe weiter unten). Mit tieferem fmh und höherem fmi wird der Bass kratziger.

### Lead-Sound 1 — Pluck

```strudel
note("c4 e4 g4 b4").s("triangle")
  .attack(0.001).decay(0.15).sustain(0).release(0.2)
  .lpf(2500)
  .gain(0.5)
```

Sehr kurzer Decay, kein Sustain — wie gezupft.

### Lead-Sound 2 — Stab (kurz und knallig)

```strudel
note("c4 ~ ~ g4").s("sawtooth")
  .attack(0.001).release(0.1)
  .lpenv(12).lpa(0).lpd(0.1)
  .lpf(400)
  .distort(0.3)
  .postgain(0.6)
  .gain(0.7)
```

Synth-Stab. Filter-Envelope öffnet beim Anschlag, Distortion macht's wuchtig, postgain zieht's auf normale Lautstärke zurück.

### Lead-Sound 3 — Singende Lead

```strudel
note("c5 eb5 g5 c6 g5 eb5").s("supersaw")
  .attack(0.05).release(0.5)
  .lpf(2500).lpq(2)
  .delay(0.4).delaytime(0.375).delayfeedback(0.4)
  .room(0.4)
  .gain(0.5)
```

Supersaw mit Delay und Hall — der "Trance-Lead".

### Pad-Sound 1 — String-Pad

```strudel
note("[c4, e4, g4, b4]").s("sawtooth")
  .attack(1).release(3)
  .lpf(1500)
  .gain(0.4)
  .room(0.6)
```

Maj7-Pad. Lange Hüllkurve macht aus dem Sägezahn ein Streich- Pad.

### Pad-Sound 2 — Atmosphäre mit Modulation

```strudel
note("[c4, eb4, g4, c5]").s("sawtooth")
  .attack(2).release(4)
  .lpf(sine.range(800, 2000).slow(4))     // Filter atmet
  .pan(perlin.range(0.3, 0.7).slow(8))    // pant stereo
  .room(0.7)
  .gain(0.35)
```

### Pad-Sound 3 — Hauchig durch Vowel-Filter

```strudel
note("[c4, eb4, g4]").s("sawtooth")
  .attack(1).release(2)
  .vowel("<a o u>")          // Vokal wechselt
  .lpf(2000)
  .gain(0.4)
```

Klingt wie ein Chor der "aaa-ooo-uuu" macht.

### FM-Synthese — kurz und schmutzig

```
Strudel hat eine eingebaute FM-Engine. Du brauchst:
  .s("triangle") oder .s("sine")  — Carrier
  .fmh(N)                          — Frequenz-Verhältnis Modulator/Carrier
  .fmi(N)                          — FM-Index (Tiefe)
```

```strudel
note("c4*4").s("sine").fmh(1).fmi(0)    // kein FM
note("c4*4").s("sine").fmh(1).fmi(2)    // leichtes FM
note("c4*4").s("sine").fmh(2).fmi(5)    // glockig (DX7-style)
note("c4*4").s("sine").fmh(3.5).fmi(8)  // metallisch
note("c4*4").s("sine").fmh(11).fmi(3)   // bell-artig
```

```
FM-Faustregeln:
  fmh = ganzzahlig → harmonisch (Bell, E-Piano)
  fmh = nicht ganzzahlig → metallisch
  fmi hoch → mehr Obertöne / mehr Verzerrung
```

Mit Envelope auf fmi (geht direkt):

```strudel
note("c4*4").s("sine").fmh(2).fmi(5).fmattack(0.01).fmdecay(0.3)
```

### Pulsbreiten-Modulation (PWM)

```strudel
note("c4*8").s("pulse").pwm(0.5)        // gleich Square
note("c4*8").s("pulse").pwm(0.1)        // sehr schmal
note("c4*8").s("pulse").pwm(sine.range(0.2, 0.8).slow(2))
```

PWM moduliert mit Sinus — klassischer Vintage-Synth-Pad-Sound.

### Detune und Voicing

```strudel
note("c4*4").s("sawtooth").detune(0.1)   // leichter Pitch-Versatz
note("c4*4").s("sawtooth").detune(0.5)   // mehr — fast Chorus-artig
note("c4*4").s("supersaw").detune(0.3)   // supersaw ist von Natur aus detuned
```

Mehrere Stimmen aufaddieren:

```strudel
stack(
  note("c4*4").s("sawtooth").detune(-0.1),
  note("c4*4").s("sawtooth").detune(0.1),
  note("c4*4").s("sawtooth").detune(0)
)
```

Drei Säge­zähne minimal versetzt — fettere Lead.

### Pitch-Envelope — der Drum-Pitch-Drop

```strudel
s("bd*4")
  .penv(24)             // 24 Halbtöne (zwei Oktaven) Hub
  .pattack(0).pdecay(0.05)
```

Bd kriegt einen "Whump" — Pitch fällt schnell ab. Macht Bass-Drums wuchtiger.

### Noise-Quellen

```strudel
s("noise").gain(0.3)           // weißes Rauschen
s("pink").gain(0.3)            // pink noise (ausgewogen)
s("brown").gain(0.3)           // brown noise (basslastig)
```

Geklautes Snare-Sound durch gefiltertes Rauschen:

```strudel
s("noise*4").attack(0.001).decay(0.15).sustain(0).hpf(800).gain(0.7)
```

Kurzer Anschlag, hochgepasst, kein Sustain. Klingt wie Snare.

### Custom-Sound durch Layering

Wenn ein Synth nicht reicht, stack mehrere übereinander. Jedes Layer hat seinen Zweck im Spektrum:

```
  Layer        Frequenz-Slot      Quelle
  ──────────────────────────────────────────────
  SUB          20-80 Hz           sine, niedrig
  BODY         80-300 Hz          sawtooth + LPF
  KLICK        300-3 kHz          noise, kurzer Decay
  AIR          >3 kHz             optional, Hihat-artig
```

```strudel
stack(
  note("c2*4").s("sine").attack(0.01).release(0.3),
  note("c2*4").s("sawtooth").lpf(800).gain(0.5),
  note("c2*4").s("noise").attack(0.001).decay(0.05).gain(0.2)
)
```

Sub-Bass + Body + Klick — alle drei zusammen ergeben einen "großen" Bass-Sound.

```
💡 PRAXIS — Layer-Faustregeln (aus Sound-Design-Tradition)
  - 2-5 Layer pro Patch. Drunter dünn, drüber Brei.
  - Sweet Spot: 3 Layer (Body + Charakter + Air)
  - Jeder Layer braucht eine AUFGABE in 3 Worten.
    Wenn du sie nicht nennen kannst — Layer raus.
  - Frequenz-Trennung: jeder Layer eigener Slot.
    Zwei Layer im selben Slot = einer fliegt oder wird
    EQ-mäßig zurechtgeschnitten.
  - Hochpass auf alle Layer AUSSER dem Sub-Layer
    (Default 80-120 Hz HP).
  - Pan-Spread asymmetrisch: Layer A 30% links, Layer B
    25% rechts. Symmetrie klingt steril.
  - Lautstärke-Hierarchie: Hauptlayer 0 dB, Würze-Layer
    -6 bis -12 dB. Wenn alle gleich laut sind, hast du
    keine Würze, sondern noch mal denselben Layer.
```

### FINALE — Synth-Showcase

```strudel
setcps(0.5)

stack(
  s("bd*4").penv(20).pattack(0).pdecay(0.06).gain(0.95),
  s("~ noise ~ noise").attack(0.001).decay(0.15).sustain(0).hpf(800).gain(0.4),
  s("hh*16").gain(0.3),
  // Acid-Bass
  note("c2*8").scale("C:minor").s("sawtooth")
    .lpf(150).lpenv(8).lpa(0).lpd(0.15).lpq(15)
    .distort(0.2).release(0.1).gain(0.65),
  // FM-Lead
  note("<eb5 g5 c6 g5>").s("sine").fmh(2).fmi(4)
    .attack(0.01).release(0.4)
    .delay(0.4).delaytime(0.375).delayfeedback(0.5)
    .room(0.4)
    .gain(0.4),
  // Pad mit PWM
  note("[0,2,4]").scale("C:minor").s("pulse").pwm(sine.range(0.3, 0.7).slow(4))
    .attack(1).release(2).lpf(2000)
    .gain(0.3)
)
```

### Wo Strudel an Grenzen kommt

```
Das hier kannst du NICHT mit Strudels Bordmitteln:
  - Eigene Synth-Algorithmen (Granular, Physical Modeling)
  - Wavetables
  - Mehrere Operatoren in FM (DX7 hatte 6, Strudel 1)
  - Komplexe Modulationsmatrizen
  - Sample-and-Hold-LFOs auf beliebigen Parametern
```

Workaround: Sound in Vital/Reaper bauen und als WAV importieren. Strudel triggert das Sample dann mit .speed() für Pitch.

Das war von den Strudel-Entwicklern absichtlich begrenzt — Live-Coding-Tool, nicht Synth-Lab.

### Mini-Zusammenfassung Kapitel 13

Engines:    sine, triangle, sawtooth, square, pulse, supersaw,              noise, pink, brown FM:         .fmh(N) .fmi(N) .fmattack .fmdecay PWM:        .pwm(0..1) Detune:     .detune(Halbtöne als Bruchzahl) Pitch-Env:  .penv(N) .pattack .pdecay .pcurve ADSR:       .attack .decay .sustain .release Filter-Env: .lpenv .lpa .lpd .lps .lpr (auch hp/bp)

```
Tipp: Wenn ein Sound nicht klingt wie du willst, prüf in
dieser Reihenfolge:
  1. ADSR (oft falsche Hüllkurve)
  2. Filter-Cutoff (zu dumpf oder zu offen)
  3. Distortion / Saturation (Druck)
  4. Layer (Sub-Bass + Body + Klick)
  5. Reverb/Delay als letztes
```

Weiter zu 14_midi_und_io.strudel.
