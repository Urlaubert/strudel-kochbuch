# Kapitel 10 — Eigene Samples

Bisher hattest du die eingebauten Drum-Sounds (bd, sd, hh) und Instrumenten-Samples (piano, jazz). Jetzt: deine eigenen WAVs. Aufnehmen, slicen, missbrauchen.

Drei Wege: GitHub-Repo, lokaler Server, Freesound via Shabda.

### Was zur Verfügung steht (bevor du deine eigenen lädst)

Strudel hat eine MENGE eingebauter Samples. Klick im Editor unten den "sounds"-Tab — durchscrollbar.

```
Grobe Kategorien:
  - Drum-Machines: RolandTR808, RolandTR909, LinnDrum, ...
  - Live-Drums: jazz, breaks, breaks165, ...
  - Synths: piano, casio, gtr, ...
  - GM (General MIDI): gm_acoustic_grand_piano, gm_xylophone, ...
  - FX und Misc: fx, misc, crow, alien_f, ...
  - Vocal: voice, alien_b (heißt im Workshop auch "alien boy")
```

```strudel
s("crow")           // Krähe (Klassiker)
s("casio:0")        // Casio-Klang
s("gm_xylophone")   // Xylophon
```

### Drum-Banken wechseln mit .bank()

```strudel
s("bd sd hh cp")                      // Default-Bank
s("bd sd hh cp").bank("RolandTR808")  // 808er-Sound
s("bd sd hh cp").bank("RolandTR909")  // 909er
s("bd sd hh cp").bank("LinnDrum")     // 80er-Linn

s("bd*4 sd").bank("<RolandTR808 RolandTR909 LinnDrum AkaiLinn>")
```

Jeder Cycle eine andere Drum-Maschine. Ist witzig.

### Sample-Varianten mit n() oder :N

```strudel
s("hh:0 hh:1 hh:2 hh:3")
```

Vier verschiedene Hihat-Samples nacheinander.

```strudel
s("hh*8").n("0 1 2 3 0 1 2 3")
```

Identisch — n() trennt Sound und Sample-Nummer.

```strudel
s("hh*8").n(irand(4))
```

Pro Step zufällig 0-3 — Round-Robin gegen Maschinengewehr.

### Eigene Samples — Variante 1: GitHub-Repo

Wenn jemand ein Repo mit strudel.json hat, kannst du es direkt laden:

```strudel
samples('github:tidalcycles/dirt-samples')
```

Lädt Standard-Tidal-Samples (riesig, dauert).

Nach dem Laden:

```strudel
s("incoming bass:5")  // Beispiel-Sounds aus dem Repo
```

### Eigene Samples — Variante 2: Direkt-URLs

```strudel
samples({
  ocean: 'wellen.wav',
  monkey: ['affe1.wav', 'affe2.wav', 'affe3.wav'],
  rain: 'regen.wav'
}, 'https://my-server.com/samples/')
```

monkey hat drei Varianten — anwählbar via monkey:0, :1, :2.

Nach dem Laden:

```strudel
s("ocean*2, monkey:0 ~ monkey:1 ~")
```

### Eigene Samples — Variante 3: Lokaler Server (EMPFOHLEN)

Im Terminal:

```
  cd path/to/your/samples/
  npx @strudel/sampler
```

Server läuft dann auf http://localhost:5432/.

In Strudel:

```strudel
samples('http://localhost:5432/')
```

Strudel liest automatisch was im Ordner liegt. Files in Unterordnern werden zu "ordner_name". Mehrere Files im gleichen Ordner = automatische Varianten (:0, :1, ...).

Beispiel-Struktur:

```
  samples/
  ├── kick/
  │   ├── 01.wav
  │   ├── 02.wav
  │   └── 03.wav
  ├── synth/
  │   ├── pad_warm.wav
  │   └── pad_cold.wav
  └── voice.wav
```

```
In Strudel:
  s("kick*8").n(irand(3))
  s("synth")
  s("voice")
```

### Pitch-Mapping für tonale Samples

Wenn das Sample mehrere Tonhöhen hat, kannst du Strudel sagen welche Datei welcher Ton ist:

```strudel
samples({
  moog: {
    g2: 'moog_g2.wav',
    g3: 'moog_g3.wav',
    g4: 'moog_g4.wav'
  }
}, 'http://localhost:5432/')

note("g2 [c3 eb3] g3").s("moog").clip(1)
```

Strudel nimmt das nächstliegende Sample und pitcht es.

### Freesound via Shabda — Quick-and-dirty

```strudel
samples('shabda:bass:4,hihat:4,waterfall:2')
```

Shabda fragt freesound.org für die Begriffe ab. Du kriegst 4 Bass-Samples, 4 Hihat-Samples, 2 Wasserfall-Samples.

```strudel
n("0 1 2 3").s("waterfall")
```

### Sprache via Shabda Speech

```strudel
samples('shabda/speech:hello,world')
samples('shabda/speech/de-DE/m:hallo')

s("hallo")
```

Spricht "hallo" mit deutscher männlicher Stimme.

### Sample-Manipulation

.begin() / .end() — nur einen Ausschnitt

```strudel
s("ocean").begin(0.2).end(0.7)
```

.speed() — Tempo + Pitch

```strudel
s("ocean").speed(0.5)    // halb so schnell, oktave tiefer
s("ocean").speed(2)      // doppelt so schnell, oktave höher
s("ocean").speed(-1)     // rückwärts mit Originalgeschwindigkeit
```

.loop(1) — looped (nicht tempo-synced)

```strudel
s("drone").loop(1)
```

.loopAt(N) — auf N Cycles strecken

```strudel
s("breakbeat").loopAt(2)
```

.fit() — auf Event-Dauer strecken

```strudel
s("breakbeat").fit()
```

### chop — Sample in N gleiche Stücke schneiden

```strudel
s("ocean").chop(8)
```

Sample wird in 8 Teile geschnitten, in einem Cycle nacheinander abgespielt.

```strudel
s("breakbeat").chop(16).fast(2)
```

16 Slices, doppelt so schnell.

### slice — gezielt Slices anwählen

```strudel
s("breakbeat").slice(8, "0 1 2 3 [4 0] 5 6 7")
```

Sample in 8 Slices teilen, dann in dieser Reihenfolge spielen. Klassisches Beat-Repeat / Vocal-Chop-Werkzeug.

```strudel
s("breakbeat").slice(8, "0 [3 5] 2 7 4 1 6 0")
```

Reihenfolge umgemischt — der Beat klingt zerstückelt aber trotzdem rhythmisch.

### striate — progressive Slice-Order über Cycles

```strudel
s("vocal").striate(16)
```

Sample in 16 Stücke, jedes Cycle eine andere Reihenfolge — das Sample "wandert" über mehrere Cycles.

### scrub — Tape-Style-Scrubbing

```strudel
s("drone").scrub("0.1:1 0.5:2 0.9:0.5")
```

Format: position:speed. Springt zu 10% mit Speed 1, dann 50% mit Speed 2, dann 90% mit Speed 0.5.

### cut — Cut-Group

```strudel
s("[oh hh]*4").cut(1)
```

Wenn ein neuer Hit aus Cut-Group 1 kommt, wird der alte abgeschnitten. Klassisch für Open/Closed-Hihat — ohne cut klingen sie übereinander.

### FINALE — Sample-Beat

Voraussetzung: lokaler @strudel/sampler-Server läuft. Wenn nicht, ersetze "kick"/"snare" durch "bd"/"sd".

```strudel
samples('http://localhost:5432/')

stack(
  s("kick*4").n(irand(4)),
  s("~ snare ~ snare").n(irand(4)),
  s("[hh oh]*4").cut(1).gain(0.4),
  note("c2 ~ eb2 g2").s("sawtooth").lpf(600).gain(0.7),
  s("ocean").chop(8).gain(0.3).slow(2)
)
```

Eigene Drums mit Round-Robin, Open/Closed-Hihat-Logik, Bass-Linie, gechoppter Ocean-Sound als Atmosphäre.

### Drum-Break-Slicen — Klassiker

Ein einziger Break-Sample, in 8 oder 16 Slices, kreativ neu zusammengesetzt.

```strudel
s("breakbeat").slice(8, "0 1 [2 3] 4 5 [6 0] 7")
```

Mit ein paar Subdivisions wird's interessanter.

```strudel
s("breakbeat").slice(8, "<0 1 2 3 4 5 6 7>").every(4, rev)
```

Slice pro Cycle ein anderer, alle 4 Cycles rückwärts.

### Granular-Pads aus Drone

```strudel
s("drone").chop(32).fast(8).gain(0.4).room(0.6)
```

Drone-Sample in 32 Slices, 8x so schnell — wird zu körnigem Gewebe. Mit Hall: Pad-Effekt.

### ▶ AUFGABE: Eigenen Sample-Workflow probieren

1. Suche dir 3-4 WAVs (eigene Aufnahmen oder von Freesound). 2. Leg sie in einen Ordner. 3. Starte npx @strudel/sampler im Terminal. 4. samples('http://localhost:5432/') am Top deiner Datei. 5. Bau einen Beat damit. Mindestens einer der Sounds soll    .chop oder .slice verwenden.

### Mini-Zusammenfassung Kapitel 10

```
  samples('github:user/repo')        → GitHub-Repo
  samples({...}, 'https://...')       → URL-basiert
  samples('http://localhost:5432/')   → Lokaler Server
  samples('shabda:term:n')            → Freesound
  .bank("RolandTR808")                → Drum-Bank
  .n(N) oder ":N"                     → Sample-Variante
  .speed(N)                           → Tempo+Pitch
  .begin/end                          → Ausschnitt
  .loop(1) .loopAt(N) .fit            → Looping
  .chop(N)                            → in N Slices
  .slice(N, "...")                    → Slices anwählen
  .striate(N)                         → progressive Slice-Order
  .cut(N)                             → Cut-Group
```

Eigene Samples sind der Schritt von "Live-Coder" zu "Sample-Manipulator". Hier wird Strudel zu mehr als einem Drum-Computer.

Weiter zu 11_song_struktur.strudel.
