# Kapitel 18 — Genre-Kochbuch

Pro Genre eine kurze Strudel-Vorlage mit den typischen Defaults: Tempo, Drum-Bank, Bass-Charakter, Effekt-Reihen- folge. Zum Anhören und als Startpunkt.

Jedes Genre hat seine Konventionen — wer dazwischen springt sollte die Defaults kennen, dann kann man sie bewusst brechen.

### Berlin Techno (130 BPM, dunkel, repetitiv)

```strudel
setcps(0.55)

stack(
  s("bd*4").gain(0.95),                                  // tighter Kick
  s("~ ~ rim ~").gain(0.4),                              // sparse Perc
  s("hh*16").gain(0.3),
  note("c2*8").scale("C:phrygian")                       // dunkler Mood
    .s("sawtooth")
    .lpf(sine.range(200, 800).slow(16))                  // SLOWER Filter-Sweep
    .lpq(8)
    .gain(0.7)
)
```

```
Notes:
  - 909-Kick, dunkel, kein Sub-Boom (.lpf darüber wenn nötig)
  - Filter-Sweeps SEHR langsam (slow(16) = 32 s bei cps=0.5)
  - Skala: phrygian / aeolian — dunkle Modi
  - Reverb sparsam, kurzer Plate auf Snare/Clap
  - Layout: 4-on-floor + Acid-Bass + sparse Perc
```

### Detroit Techno (124-128 BPM, mehr Soul, melodischer)

```strudel
setcps(0.53)

stack(
  s("bd*4"),
  s("~ cp ~ cp"),
  s("hh*16").gain(0.4).pan(perlin.range(0.3, 0.7)),      // lebendige Hihat
  note("c3 eb3 g3 c4").scale("C:dorian")                 // hellerer Mood
    .s("sawtooth").lpf(1500)
    .attack(0.05).release(0.4),
  note("c2 ~ c2 ~").s("sine").gain(0.7)                  // Sub-Bass
)
```

```
Notes:
  - 909er-Drums mit Swing
  - Skala: dorian / mixolydian — heller, soulful
  - Pads + Strings gehören dazu
  - Mittlere Halls auf melodische Layer
```

### House (124-128 BPM, sample-basiert, groovy)

```strudel
setcps(0.53)

stack(
  s("bd*4"),
  s("~ cp ~ cp").room(0.3),
  s("hh*16").gain(0.4),
  s("[~ ~ ~ oh]/2").gain(0.5).cut(1),                    // klassisches OH-Pattern
  note("c2 c2 g1 c2").scale("C:minor")
    .s("sawtooth").lpf(800).gain(0.7),
  note("[c4, eb4, g4]")                                  // Stab-Akkorde
    .s("sawtooth").attack(0.001).release(0.15)
    .lpenv(8).lpa(0).lpd(0.1)
    .gain(0.5)
)
```

```
Notes:
  - 909-Kick + Clap auf 2 und 4
  - Stab-Chords (kurzer Attack, Filter-Pluck)
  - Shaker mit Swing
  - Plate-Reverb auf Vocals/Stabs
```

### Drum & Bass (174 BPM, Amen-Break-Stil, Reese-Bass)

```strudel
setcps(0.725)   // ~174 BPM bei 4 Steps/Cycle

stack(
  // Halftime-Drums (klingt wie 87 BPM)
  s("bd ~ ~ ~ ~ ~ sd ~ ~ ~ bd ~ sd ~ ~ ~"),
  s("hh*16").gain(0.4),
  // Reese-Bass (zwei detunete Saws)
  note("c2*4").scale("C:minor")
    .s("sawtooth").detune(0.15)
    .lpf(sine.range(300, 1000).slow(2))
    .lpq(5)
    .gain(0.7),
  // Stabs
  note("<eb5 g5 c5 bb4>").s("sine")
    .attack(0.001).release(0.3)
    .gain(0.4)
)
```

```
Notes:
  - Tempo: 174 BPM (cps ~0.725 bei 4er-Cycle)
  - Kick und Snare auf 1 und Step 7 (im 16tel-Raster)
  - Reese: zwei Sägezähne ca. 15 cents detunet, breiter Filter
  - Plate-Reverb auf Snare, sehr sparsam
  - Multiband-Compression auf den Bass (in Strudel begrenzt
    simulierbar)
```

### Dubstep (140 BPM half-time, Wobble-Bass)

```strudel
setcps(0.583)   // ~140 BPM, aber half-time klingt wie 70

stack(
  s("bd ~ ~ ~ ~ ~ ~ ~ ~ ~ sd ~ ~ ~ ~ ~"),                // half-time: nur 1 und 11
  s("hh*16").gain(0.3),
  note("c1*16").scale("C:minor")                         // tiefer Sub
    .s("sawtooth")
    .lpf(square.range(200, 1500).fast(2))                // WOBBLE per square-LFO
    .lpq(10)
    .distort(0.2)
    .gain(0.7),
  s("crash").gain(0.3).slow(8)                           // Crash auf 1
)
```

```
Notes:
  - Tempo: 140 BPM, aber Drums spielen half-time (klingt 70)
  - Wobble = LFO auf Filter, Square für aggressives Pumpen
  - Tief, sub-fokussiert
  - Snare oft mit Gate-Reverb
```

### Trap (140 BPM, 808-Bass, schnelle Hihat-Rolls)

```strudel
setcps(0.583)

stack(
  // Tighter Kick auf 1, snappy Snare auf 3
  s("bd ~ ~ ~ sd ~ ~ ~ ~ ~ bd ~ sd ~ ~ ~"),
  // 808-Bass (sub mit Pitch-Slide)
  note("c1 ~ ~ ~ eb1 ~ ~ ~ g1 ~ ~ ~ c1 ~ ~ ~")
    .s("sine")
    .attack(0.01).release(0.5)
    .penv(6).pattack(0).pdecay(0.05)                     // Pitch-Slide am Anfang
    .distort(0.05)                                       // leichte Saturation
    .gain(0.85),
  // Hihat-Rolls (fast(2) auf bestimmten Cycles)
  s("hh*16").gain(0.4)
    .every(4, x => x.fast(2))                            // alle 4 Cycles Roll
)
```

```
Notes:
  - 808 = Sub mit langem Tail + leichte Tube-Saturation
  - Snare-Crack bei 5 kHz
  - Hi-Hat Rolls (1/16 bis 1/64) sind Genre-Signature
  - Reverb sparsam, kurzer Hall auf Vocals
```

### Synthwave (110-120 BPM, Vintage-Charakter)

```strudel
setcps(0.5)

stack(
  s("bd*4").bank("LinnDrum"),                            // Linn-Style
  s("~ sd ~ sd").bank("LinnDrum")
    .room(0.6).roomsize(3),                              // Gated-Reverb-Snare-Imitation
  s("hh*16").gain(0.4),
  // Big Brass / FM-Lead
  note("c3 ~ eb3 g3").s("sawtooth")
    .attack(0.01).release(0.3)
    .lpf(2000).lpq(2)
    .delay(0.4).delaytime(0.375).delayfeedback(0.4)      // Slap-back-Delay
    .gain(0.5),
  // Detune-Pad
  note("[c3, eb3, g3, c4]").s("sawtooth").detune(0.1)
    .attack(1).release(2)
    .lpf(sine.range(800, 2000).slow(4))                  // langsamer LFO
    .gain(0.35)
)
```

```
Notes:
  - LinnDrum oder Roland-CR-78
  - Gated Reverb auf Snare (in Strudel begrenzt — room+Cut)
  - Saw-Bass mono, oft mit FM für DX7-Charakter
  - Slow LFO auf Pad-Filter (0.1-0.3 Hz)
```

### Lo-Fi Hip-Hop (70-90 BPM, Vinyl-Crackle, Jazz-Chords)

```strudel
setcps(0.4)

stack(
  // Boom-Bap-Drums
  s("bd ~ ~ ~ ~ ~ sd ~ ~ ~ bd ~ sd ~ ~ ~").gain(0.85)
    .crush(6),                                           // Lo-Fi-Crusher
  s("hh*8").gain(0.3),
  // Jazz-Chord (Maj7)
  note("[c4, e4, g4, b4]").s("piano")
    .attack(0.001).release(1)
    .lpf(2500)                                            // dumpfer
    .gain(0.5)
    .room(0.3),
  // Sample-Bass aus Vinyl
  note("c2 ~ ~ a1 ~ ~ f1 ~").s("sine")
    .attack(0.01).release(0.3)
    .gain(0.7),
  // Vinyl-Crackle simulieren
  s("noise*16").gain(0.05).hpf(3000)                     // sehr leises Crackeln
)
```

```
Notes:
  - Tempo: 70-90 BPM, oft 85
  - crush(4-6) und coarse(2-3) für Lo-Fi-Charakter
  - Jazz-Akkorde: Maj7, m7, m9
  - Vinyl-Crackle als Layer (gefiltertes Noise)
  - Sample-Bass aus Vinyl-Loops (oder hier als sine simuliert)
```

### Ambient (variable BPM, oft kein Beat)

```strudel
setcps(0.25)   // sehr langsam

stack(
  // Long Pad (Maj7-Voicing)
  note("[c3, e3, g3, b3]").s("sawtooth").detune(0.1)
    .attack(4).release(8)
    .lpf(sine.range(800, 2000).slow(16))                 // SEHR langsame Bewegung
    .gain(0.35)
    .room(0.7),
  // Drone-Layer
  note("c2").s("sine").gain(0.5)
    .vibrato(5).vibratodepth(0.05),
  // Sparse "Glocken"
  note("<g4 ~ ~ c5 ~ ~ ~ eb5>").s("sine")
    .attack(0.001).release(2)
    .gain(0.3)
    .delay(0.5).delaytime(0.5).delayfeedback(0.7)
    .room(0.8)
    .slow(2)
)
```

```
Notes:
  - Sub-Fokus oder gar kein tiefer Anker
  - Lange Pads (4-15 s decay)
  - Sehr viel Hall, oft Convolution oder Shimmer
  - Sehr langsame, organische Modulation
  - Field-Recordings als zusätzlicher Layer (siehe Kap 10)
```

### Drone (extrem langsam, kein Beat, Texturen)

```strudel
setcps(0.15)

stack(
  // Sub-Drone
  note("c2").s("sawtooth").detune(0.05)
    .attack(8).release(20)
    .lpf(400)
    .gain(0.6),
  // Mittel-Drone
  note("g3").s("sawtooth").detune(0.08)
    .attack(6).release(15)
    .lpf(sine.range(800, 1500).slow(32))
    .gain(0.4),
  // Gewebe oben
  note("c5").s("sine")
    .attack(4).release(10)
    .delay(0.4).delaytime(0.75).delayfeedback(0.6)
    .room(0.85)
    .gain(0.3)
)
```

```
Notes:
  - Tempo egal — Drones haben keinen Puls
  - Eine Tonart/Stimmung, sehr lange ausgehalten
  - Mehrere Schichten in verschiedenen Registern
  - Modulation muss SUB-langsam sein (slow(32) und mehr)
```

### Cinematic / Filmscore (variable, hybride Klänge)

```strudel
setcps(0.45)

stack(
  // Sub-Bass (emotionale Mitte)
  note("<c1 c1 ab0 c1>").s("sine")
    .attack(0.5).release(2)
    .gain(0.7),
  // Pad-Stack
  note("[c3, eb3, g3]").scale("<C:minor C:minor Ab:major C:minor>")
    .s("sawtooth").detune(0.15)
    .attack(1).release(3)
    .lpf(2000)
    .gain(0.4)
    .room(0.7),
  // Pulsierender Rhythmus (oft Taikos in Cinematic)
  s("bd ~ bd ~ bd bd ~ bd").gain(0.7)
    .lpf(400),                                            // tieferes Drum-Sound
  // "Whoosh" als Riser
  s("noise").gain(saw.range(0, 0.4).slow(8))
    .lpf(saw.range(500, 8000).slow(8))
    .room(0.6)
)
```

```
Notes:
  - Sub-Bass als emotionaler Anker (Hans Zimmer)
  - Pad-Stacks aus 3-5 Stimmen, leicht detuned
  - Halbtaktige Taiko-artige Drums
  - Riser/Whoosh als Übergänge
  - Convolution-Reverb (in Strudel: room hoch)
```

### Wie das Kochbuch zu lesen ist

Kein Genre ist exklusiv. Du kannst Tempo aus Trap mit Akkorden aus Lo-Fi und Wobble-Bass aus Dubstep mischen — das gibt's eine Wirkung, die jenseits der einzelnen Genres ist.

Pragmatischer Tipp: ein Genre als Skelett wählen, ein Element bewusst aus einem anderen Genre brechen rein. Aphex Twin macht das ständig — Drums aus Dance, Akkorde aus Klassik, Sound-Design aus Frühstücks-Cereals.

### ▶ AUFGABE: Cross-over

Nimm zwei Vorlagen oben. Misch je zwei Layer aus jeder. Was klingt überraschend gut?

```
Beispiele:
  - Trap-808 + Lo-Fi-Akkorde → Cloud-Rap
  - Synthwave-Pad + Techno-Drums → Industrial-Synthwave
  - Drum&Bass-Reese + Ambient-Pad → "liquid DnB"
```

### Mini-Zusammenfassung Kapitel 18

Genre-Defaults sind Konventionen, keine Gesetze. Bewusst im Genre starten gibt dir Kontrast wenn du brichst.

```
  Genre        BPM    Charakteristisch
  ────────────────────────────────────────────────
  Berlin Techno  130   dunkel, sparse, Filter-Sweep
  Detroit Techno 126   Soul, Pads, mixolydian
  House          126   Stabs, Plate-Reverb, Swing
  D&B            174   Halftime-Drums, Reese-Bass
  Dubstep        140   Half-time, Wobble, Sub
  Trap           140   808 + Hi-Hat-Rolls + Pitch-Slide
  Synthwave      115   LinnDrum, Detune-Pad, Slap-Delay
  Lo-Fi Hip-Hop  85    Boom-Bap, Vinyl-Crackle, Maj7
  Ambient        var.  Pads, viel Hall, kein Beat
  Drone          0     ein Ton, ewig
  Cinematic      var.  Sub-Bass, Hybrid-Pads
```

Weiter zu 19_valenz_und_arousal.strudel.
