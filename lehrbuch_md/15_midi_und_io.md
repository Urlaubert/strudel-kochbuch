# Kapitel 15 — MIDI und IO

Strudel allein im Browser ist schon viel. Aber: Hardware kann rein (Knobs steuern Parameter, E-Drums triggern Patterns) und Hardware kann gesteuert werden (Strudel als Sequencer für externe Synths wie Vital, Ableton, MPC).

Dieses Kapitel braucht echte Hardware-Anschlüsse — du kannst das Meiste hier nur ausprobieren wenn du was angeschlossen hast.

### Setup-Voraussetzungen

Browser muss MIDI dürfen. Chrome auf Mac/Windows kann das out-of-the-box.

```
Für MIDI-Output an externe Synths/DAWs brauchst du eine
virtuelle MIDI-Bridge:
  - Mac:  IAC Driver (in Audio-MIDI-Setup aktivieren)
  - Win:  loopMIDI (free, von Tobias Erichsen)
  - Linux: aconnect / a2jmidid
```

### MIDI-Eingabe — Hardware-Knobs nach Strudel

```strudel
const cc = await midin('Akai MPK Mini')
```

"await" wartet bis das Gerät verbunden ist. Geräte-Name muss passen — siehe Browser-Console für die verfügbaren.

```strudel
note("c4 e4 g4")
  .lpf(cc(0).range(100, 4000))    // Knob 1 → Filter
  .lpq(cc(1).range(0, 10))        // Knob 2 → Resonanz
  .gain(cc(2).range(0.3, 1))      // Knob 3 → Lautstärke
  .s("sawtooth")
```

cc(N) liefert einen Pattern-Wert der live mit dem Knob mitgeht. Optional zweiter Parameter: cc(0, 2) liest CC 0 auf MIDI-Channel 2.

### MIDI-Notes-Eingabe — live spielen

```strudel
const keys = await midin('Akai MPK Mini')

$: midikeys('keys').s("piano")
```

$: ist Strudels "Sub-Pattern"-Syntax — definiert eine laufende Spur. midikeys() liefert die gedrückten Tasten. Heißt: du spielst MIDI-Notes auf dem Keyboard, sie triggern den Piano-Sample.

Geht auch mit Effekten:

```strudel
$: midikeys('keys').s("sawtooth").lpf(cc(0).range(200, 4000))
```

### Pads als Trigger

Akai MPK Mini hat 8 Pads. Die senden MIDI-Notes, üblicherweise ab Note 36 (C2). Diese kann man auf bestimmte Aktionen mappen.

```strudel
$: midikeys('keys')
  .when((n) => n.note === 36, () => s("bd"))
  .when((n) => n.note === 37, () => s("cp"))
  .when((n) => n.note === 38, () => s("hh"))
```

(Syntax kann je nach Strudel-Version etwas anders sein — Details in den Docs.)

### MIDI-Ausgabe — Strudel steuert externe Synths

```strudel
note("c4 e4 g4 b4").midi('IAC Driver')          // Mac
note("c4 e4 g4 b4").midi('loopMIDI')            // Win
```

Strudel sendet Note-On/Note-Off via MIDI. Der externe Synth (Vital, Ableton, MPC) muss auf demselben Bus hören.

Mit Velocity, Channel, Latenz:

```strudel
note("c4 e4 g4")
  .velocity("0.8 1 0.6")
  .midichannel(2)
  .latencyMs(50)
  .midi('loopMIDI')
```

### CC-Ausgabe — Filter etc. extern steuern

```strudel
midimaps({
  vital: {
    lpf: 74,
    lpq: 71,
    macro1: { ccn: 13, min: 0, max: 1, exp: 0.5 }
  }
})

note("c4 e4 g4")
  .lpf(0.7)
  .midimap('vital')
  .midi('IAC Driver')
```

Strudel sendet auf CC 74 den Wert für lpf, mappt in den Bereich den der Synth versteht. macro1 hat eine eigene Skalierung (0-1 mit Exponenten 0.5).

### E-Drum (Alesis Strata Prime) als Input

E-Drum sendet Notes wie ein Drum-Computer. Du spielst physisch auf den Pads, Strudel bekommt die MIDI-Daten.

```strudel
const drums = await midin('Strata Prime')

$: midikeys('drums')
  .when((n) => n.note === 36, () => s("bd").gain(n.velocity))
  .when((n) => n.note === 38, () => s("sd").gain(n.velocity))
  .when((n) => n.note === 42, () => s("hh").gain(n.velocity))
```

Velocity wird mitgenommen — leise spielen = leise im Pattern.

### Gamepad — der Notnagel ohne MIDI-Hardware

```strudel
const gp = gamepad(0)

stack(
  s("bd*4").mask(gp.tglA),                       // A-Knopf an/aus
  note("c4 e4 g4").lpf(gp.x1.range(200, 5000)),   // linker Stick X = Filter
  s("hh*16").gain(gp.rt.range(0, 1))              // rechter Trigger = Hihat-Volume
)
```

Bluetooth-Gamepad funktioniert. Praktisch wenn du keinen MIDI-Controller dabei hast.

```
Verfügbare Werte:
  gp.x1, y1   linker Stick (0-1)
  gp.x2, y2   rechter Stick (0-1)
  gp.x1_2     dasselbe als -1 bis 1 (manche Mappings einfacher)
  gp.a/b/x/y  Buttons (0/1)
  gp.lb/rb    Schultern
  gp.lt/rt    Trigger (analog 0-1)
  gp.tglA/B   Toggle-Variante
  gp.up/down  D-Pad
```

### Maus — der Letzte-Notlösung-Notnagel

```strudel
note("c4*8").s("sawtooth")
  .lpf(mouseX.range(200, 5000))
  .pan(mouseY.range(0, 1))
```

### OSC — Brücke zu SuperCollider

```strudel
note("c4 e4 g4").osc()
```

Strudel sendet via OSC an SuperCollider/SuperDirt. Erfordert SC-Setup mit lokalem OSC-Server (pnpm run osc).

Macht nur Sinn wenn du in SuperCollider eigene SynthDefs hast die du aus Strudel triggern willst. Sonst ist Strudels eingebaute Engine direkt einfacher.

### MQTT — IoT / Sensoren

```strudel
mqtt('mqtt.example.com', '/topic').s('hello')
```

Sendet als JSON. Aktuell nur Senden, kein Empfangen. Für Setups wo Sensoren via MQTT mit Strudel sprechen (Kunst-Installation mit Bewegungsmeldern).

### Hardware-Setup-Empfehlung

Wenn du performen willst:

```
  Pflicht:
    - Laptop mit Chrome
    - Kopfhörer (zum Üben) und/oder Audio-Interface (Live)
```

```
  Sehr empfohlen:
    - MIDI-Controller mit Knobs (Akai MPK Mini = günstig + komplett)
      → 8 Knobs für 8 Achsen, 8 Pads für 8 Trigger,
        25 Tasten für Improvisation
```

```
  Optional:
    - E-Drum (Alesis Strata, Roland) für Live-Beats
    - Gamepad als Backup
    - DAW (Reaper) zum Aufnehmen der Performance
```

### Audio-Routing — Strudel zu Reaper

Browser-Audio in eine DAW kriegen ist OS-abhängig:

```
  Mac:  BlackHole oder Loopback (virtual audio device).
        Strudel-Ausgabe an BlackHole, Reaper liest BlackHole.
```

```
  Win:  VB-CABLE (free) oder Voicemeeter.
        Strudel ausgabe an CABLE, Reaper liest CABLE.
```

  Linux: PipeWire kann das nativ.

### FINALE — Live-Setup mit allem

Voraussetzung: MIDI-Controller mit 4+ Knobs angeschlossen.

```strudel
const cc = await midin('Akai MPK Mini')
```

Knob-Mapping (Achsen)

```strudel
const ENERGY = cc(0).range(0, 1)
const FILTER = cc(1).range(200, 4000)
const REVERB = cc(2).range(0, 0.8)
const TEMPO  = cc(3).range(0.3, 1.0)
```

Tempo-Setting via Knob (statisch beim setcps)

```strudel
setcps(0.5)  // ggf. live anpassen, hier nicht via TEMPO

stack(
  s("bd*4").gain(ENERGY.range(0.4, 1)),
  s("~ cp ~ cp").room(REVERB),
  s("hh*16").gain(ENERGY.range(0.2, 0.6)).pan(perlin.range(0.3, 0.7)),
  note("c2 c2 eb2 g2").scale("C:minor").s("sawtooth")
    .lpf(FILTER)
    .gain(0.7),
  note("[0,2,4]").scale("C:minor")
    .s("triangle")
    .attack(0.5).release(2)
    .lpf(2000)
    .room(REVERB)
    .gain(ENERGY.range(0.2, 0.5))
)
```

```
Vier Knobs steuern den Track:
  Knob 1 (ENERGY) — Drum-Lautstärke + Pad-Lautstärke
  Knob 2 (FILTER) — Bass-Filter-Cutoff
  Knob 3 (REVERB) — Hall-Tiefe für Snares und Pad
  Knob 4 (TEMPO)  — vorgesehen, hier nicht verbunden
```

Code wird einmal evaluiert. Performance = Knobs drehen.

### Mini-Zusammenfassung Kapitel 15

```
Input:
  midin('Gerät')              → CC und Notes lesen
  cc(N)                        → CC-Wert als Pattern
  midikeys()                   → MIDI-Note-Input
  gamepad(0)                   → Gamepad
  mouseX/mouseY                → Maus
```

```
Output:
  .midi('IAC Driver')          → MIDI an externen Synth
  midimaps({...})              → CC-Mapping definieren
  .midimap('preset')           → Mapping anwenden
  .osc()                       → OSC zu SuperCollider
  mqtt(...)                    → MQTT (experimental)
```

```
Performance-Setup:
  8 Knobs auf 8 Achsen mappen, 1 Stunde proben, dann live.
  Code als "Material" — zur Performance werden Knobs gedreht.
```

Weiter zu 16_performance_hygiene.strudel.
