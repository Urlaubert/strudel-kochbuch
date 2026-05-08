"""
Build script: convert .strudel files from lehrbuch/ into HTML pages
with embedded Strudel REPL, plus an index page.

Usage:
    python build.py

Output:
    docs/index.html
    docs/01_hello_sound.html
    docs/02_mininotation.html
    ...
"""

from __future__ import annotations

import re
from pathlib import Path

WEB_DIR = Path(__file__).parent
# Repo layout (parent of WEB_DIR is the repo root):
#   strudel-kochbuch/
#     lehrbuch/        source .strudel files
#     kochbuch_web/    this build script
#     docs/            output, GitHub Pages serves /docs
REPO_ROOT = WEB_DIR.parent
LEHRBUCH_DIR = REPO_ROOT / "lehrbuch"
DOCS_DIR = REPO_ROOT / "docs"

CHAPTER_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Strudel Kochbuch</title>
<link rel="stylesheet" href="style.css?v={css_hash}">
</head>
<body class="chapter">
<header>
<a href="index.html" class="back">← Inhalt</a>
<h1>{title}</h1>
{nav}
</header>
<main>
<iframe id="strudel" title="Strudel REPL" allow="autoplay" loading="lazy"></iframe>
</main>
<footer>
<p>Drücke <kbd>Strg+Enter</kbd> (oder <kbd>Cmd+Enter</kbd> auf dem Mac) im Code-Bereich um den untersten nicht-kommentierten Block zu spielen. <kbd>Strg+.</kbd> stoppt.</p>
<p>Auf dem iPad: lange auf den Code tippen → "Auswählen", dann auf das Play-Symbol unten.</p>
</footer>
<script id="strudel-code" type="text/plain">
{code}
</script>
<script>
// Inline UTF-8-safe variant of @strudel/embed.
// The original package uses btoa() which only handles Latin-1 — chokes
// on Umlaute, arrows, emoji, box-drawing chars in the lehrbuch.
(function () {{
  var code = document.getElementById('strudel-code').textContent;
  var bytes = new TextEncoder().encode(code);
  var binary = '';
  for (var i = 0; i < bytes.length; i++) binary += String.fromCharCode(bytes[i]);
  var src = 'https://strudel.cc/#' + encodeURIComponent(btoa(binary));
  document.getElementById('strudel').setAttribute('src', src);
}})();
</script>
</body>
</html>
"""

INDEX_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Strudel Kochbuch</title>
<link rel="stylesheet" href="style.css?v={css_hash}">
</head>
<body class="index">
<header>
<h1>Strudel Kochbuch</h1>
<p class="lead">Ein Strudel-Lehrbuch in Strudel. Jedes Kapitel ist lauffähiger Code mit eingebauter Erklärung. Tippe ein Kapitel an, dann <kbd>Strg+Enter</kbd> oder das Play-Symbol.</p>
</header>
<main>
<ol class="chapters">
{chapter_links}
</ol>
<section class="hints">
<h2>Hinweise</h2>
<ul>
<li>Funktioniert in Chrome und Safari (auch iPad).</li>
<li>Erstes Sample-Trigger kann 1-2 Sekunden Stille sein — Sample wird geladen.</li>
<li>Master-Volume rechts unten im REPL.</li>
<li>Vollständiger Strudel-Editor mit allen Features: <a href="https://strudel.cc">strudel.cc</a></li>
</ul>
</section>
</main>
<footer>
<p>Quelltext: <a href="https://github.com/Urlaubert/strudel-kochbuch">github.com/Urlaubert/strudel-kochbuch</a></p>
</footer>
</body>
</html>
"""

CSS = """\
:root {
  color-scheme: dark;
  --bg: #1a1a1a;
  --fg: #e8e8e8;
  --muted: #888;
  --accent: #ffcc00;
  --link: #6cf;
  --code-bg: #0a0a0a;
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  line-height: 1.5;
}

body.chapter {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;          /* dynamic viewport — fixes iOS Safari URL-bar */
  overflow: hidden;
}

body.chapter header {
  flex: 0 0 auto;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #333;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

body.chapter header h1 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 500;
  flex: 1;
}

.back {
  color: var(--link);
  text-decoration: none;
  font-size: 0.9rem;
}

.chapter-nav {
  display: flex;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.chapter-nav a {
  color: var(--link);
  text-decoration: none;
  padding: 0.25rem 0.5rem;
  border: 1px solid #333;
  border-radius: 4px;
}

.chapter-nav a:hover {
  border-color: var(--link);
}

.chapter-nav span.disabled {
  color: var(--muted);
  padding: 0.25rem 0.5rem;
  border: 1px solid #222;
  border-radius: 4px;
}

body.chapter main {
  flex: 1 1 auto;
  display: block;
  width: 100%;
  position: relative;
  min-height: 0;           /* lets the iframe shrink within flex parent */
}

#strudel {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
  background: #1a1a1a;
}

body.chapter footer {
  flex: 0 0 auto;
  padding: 0.75rem 1rem;
  border-top: 1px solid #333;
  font-size: 0.85rem;
  color: var(--muted);
}

body.chapter footer p { margin: 0.3rem 0; }

kbd {
  background: var(--code-bg);
  border: 1px solid #333;
  border-radius: 3px;
  padding: 0.1rem 0.4rem;
  font-family: ui-monospace, "JetBrains Mono", "Fira Code", monospace;
  font-size: 0.85em;
}

/* index page */

body.index {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1.25rem;
}

body.index header h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem;
}

.lead {
  color: var(--muted);
  font-size: 1.05rem;
}

ol.chapters {
  list-style: none;
  padding: 0;
  margin: 2rem 0;
  display: grid;
  gap: 0.5rem;
}

ol.chapters li {
  padding: 0;
}

ol.chapters a {
  display: flex;
  align-items: baseline;
  padding: 0.85rem 1rem;
  background: #232323;
  border-radius: 6px;
  text-decoration: none;
  color: var(--fg);
  border: 1px solid transparent;
  transition: border-color 0.15s, background 0.15s;
  gap: 1rem;
}

ol.chapters a:hover {
  border-color: var(--accent);
  background: #2a2a2a;
}

.chap-num {
  color: var(--accent);
  font-family: ui-monospace, "JetBrains Mono", monospace;
  font-weight: 600;
  flex-shrink: 0;
  width: 2.5rem;
}

.chap-title {
  flex: 1;
}

.chap-tagline {
  color: var(--muted);
  font-size: 0.9rem;
  margin-top: 0.15rem;
}

.hints {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid #333;
}

.hints h2 {
  font-size: 1rem;
  margin: 0 0 0.5rem;
  color: var(--muted);
  font-weight: 500;
}

.hints ul {
  margin: 0;
  padding-left: 1.25rem;
  color: var(--muted);
  font-size: 0.9rem;
}

.hints li {
  margin: 0.3rem 0;
}

.hints a {
  color: var(--link);
}

body.index footer {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid #333;
  font-size: 0.85rem;
  color: var(--muted);
}

body.index footer a {
  color: var(--link);
}

/* Mobile / iPad tweaks */
@media (max-width: 700px) {
  body.chapter header {
    padding: 0.5rem 0.75rem;
    gap: 0.5rem;
  }
  body.chapter header h1 {
    font-size: 0.95rem;
    width: 100%;
    order: 3;
  }
  body.chapter footer {
    font-size: 0.75rem;
    padding: 0.5rem 0.75rem;
  }
  body.chapter footer p { margin: 0.15rem 0; }
  .chapter-nav { font-size: 0.85rem; }
}

/* iPhone in portrait: hide footer for max REPL height. */
@media (max-width: 480px) {
  body.chapter footer { display: none; }
}
"""


# Mapping of chapter file stems to human-readable titles + taglines.
# Order matters — defines the index ordering.
CHAPTER_META: list[tuple[str, str, str]] = [
    ("00_lies_mich_zuerst", "00 — Lies mich zuerst", "Bedienung"),
    ("01_hello_sound", "01 — Hello Sound", "Eine Note. Ein Sample."),
    ("02_mininotation", "02 — Mini-Notation", "Klammern, Sterne, Tilden"),
    ("03_polyrhythmik", "03 — Polyrhythmik", "stack, mehrere Spuren"),
    ("04_euklidisch", "04 — Euklidische Rhythmen", "Tresillo, Bossa, Aksak"),
    ("05_skalen_und_melodie", "05 — Skalen und Melodie", "note(), scale"),
    ("06_akkorde_und_voicings", "06 — Akkorde und Voicings", "Akkorde"),
    ("07_effekte", "07 — Effekte", "Filter, Hall, Delay, Distortion"),
    ("08_signale_und_modulation", "08 — Signale und Modulation", "sine, perlin, LFO"),
    ("09_time_modifier", "09 — Time Modifier", "fast, slow, every, mask"),
    ("10_samples_eigene", "10 — Eigene Samples", "WAVs laden, slicen"),
    ("11_song_struktur", "11 — Song-Struktur", "arrange, Sektionen"),
    ("12_mini_track_in_50_zeilen", "12 — Mini-Track", "Alles zusammen"),
    ("13_synthese_tief", "13 — Synthese tief", "Sound-Design aus Bordmitteln"),
    ("14_midi_und_io", "14 — MIDI und IO", "Hardware-Knobs, externe Synths"),
    ("15_performance_hygiene", "15 — Performance-Hygiene", "Live-Set-Tipps"),
    ("16_eigene_helper", "16 — Eigene Helper", "register(), Achsen"),
    ("17_hap_internals", "17 — Hap-Internals", "Pattern-Theorie"),
    ("18_genre_kochbuch", "18 — Genre-Kochbuch", "Vorlagen pro Genre"),
    ("19_valenz_und_arousal", "19 — Valenz und Arousal", "Stimmungs-Achsen"),
    ("20_cheatsheet", "20 — Cheatsheet", "Spickzettel"),
]


def sanitize_for_script_tag(code: str) -> str:
    """Code lives inside <script id="strudel-code" type="text/plain">.
    The HTML parser only stops at the literal sequence '</script' (case
    insensitive). The lehrbuch never writes that, but we replace it
    defensively so nobody surprises us later."""
    # Insert zero-width space inside any '</script' so the parser sees a
    # different tag name. The decoded code on the JS side will contain the
    # zero-width char too, but it's invisible and harmless inside comments.
    import re as _re
    return _re.sub(r"</(script)", r"</​\1", code, flags=_re.IGNORECASE)


def build_chapter_nav(idx: int, total: int) -> str:
    """Build prev/next nav for a chapter."""
    parts = ['<nav class="chapter-nav">']
    if idx > 0:
        prev_stem, prev_title, _ = CHAPTER_META[idx - 1]
        parts.append(f'<a href="{prev_stem}.html" title="{prev_title}">← Vorheriges</a>')
    else:
        parts.append('<span class="disabled">← Vorheriges</span>')
    if idx < total - 1:
        next_stem, next_title, _ = CHAPTER_META[idx + 1]
        parts.append(f'<a href="{next_stem}.html" title="{next_title}">Nächstes →</a>')
    else:
        parts.append('<span class="disabled">Nächstes →</span>')
    parts.append('</nav>')
    return "".join(parts)


def build_chapter_links() -> str:
    """Build the index <li> entries."""
    items = []
    for stem, title, tagline in CHAPTER_META:
        # Split title into number and rest for styled rendering.
        m = re.match(r"^(\d+)\s+—\s+(.+)$", title)
        if m:
            num, rest = m.group(1), m.group(2)
        else:
            num, rest = "", title
        items.append(
            f'<li><a href="{stem}.html">'
            f'<span class="chap-num">{num}</span>'
            f'<span class="chap-title">{rest}'
            f'<div class="chap-tagline">{tagline}</div>'
            f'</span></a></li>'
        )
    return "\n".join(items)


def build() -> None:
    import hashlib

    DOCS_DIR.mkdir(exist_ok=True)

    # Hash CSS so HTML can reference it cache-busted.
    css_hash = hashlib.sha1(CSS.encode("utf-8")).hexdigest()[:10]
    (DOCS_DIR / "style.css").write_text(CSS, encoding="utf-8")
    print(f"  wrote {DOCS_DIR / 'style.css'} (hash {css_hash})")

    # Write each chapter HTML.
    total = len(CHAPTER_META)
    for idx, (stem, title, _tagline) in enumerate(CHAPTER_META):
        src = LEHRBUCH_DIR / f"{stem}.strudel"
        if not src.exists():
            print(f"  ! missing: {src}")
            continue
        code = src.read_text(encoding="utf-8")
        code_safe = sanitize_for_script_tag(code)
        html = CHAPTER_HTML_TEMPLATE.format(
            title=title,
            nav=build_chapter_nav(idx, total),
            code=code_safe,
            css_hash=css_hash,
        )
        out = DOCS_DIR / f"{stem}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  wrote {out}")

    # Write index.
    index = INDEX_HTML_TEMPLATE.format(
        chapter_links=build_chapter_links(),
        css_hash=css_hash,
    )
    (DOCS_DIR / "index.html").write_text(index, encoding="utf-8")
    print(f"  wrote {DOCS_DIR / 'index.html'}")

    print(f"\nDone. {total} chapters generated in {DOCS_DIR}")


if __name__ == "__main__":
    build()
