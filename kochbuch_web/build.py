"""Build HTML pages from Markdown chapters in lehrbuch_md/.

Each ```strudel code fence becomes a small inline Strudel REPL iframe
(loading strudel.cc with the code base64-encoded as URL hash).

Output:
    docs/index.html
    docs/style.css
    docs/strudel-snippet.js
    docs/01_hello_sound.html
    ...
"""

from __future__ import annotations

import base64
import hashlib
import html
import re
from pathlib import Path

import markdown

WEB_DIR = Path(__file__).parent
REPO_ROOT = WEB_DIR.parent
LEHRBUCH_MD = REPO_ROOT / "lehrbuch_md"
DOCS_DIR = REPO_ROOT / "docs"


# Mapping of chapter file stems to (title, tagline). Order = index order.
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
    ("13_praxis_beispiele", "13 — Praxis-Beispiele", "12 fertige Anwendungs-Lessons"),
    ("14_synthese_tief", "14 — Synthese tief", "Sound-Design aus Bordmitteln"),
    ("15_midi_und_io", "15 — MIDI und IO", "Hardware-Knobs, externe Synths"),
    ("16_performance_hygiene", "16 — Performance-Hygiene", "Live-Set-Tipps"),
    ("17_eigene_helper", "17 — Eigene Helper", "register(), Achsen"),
    ("18_hap_internals", "18 — Hap-Internals", "Pattern-Theorie"),
    ("19_genre_kochbuch", "19 — Genre-Kochbuch", "Vorlagen pro Genre"),
    ("20_valenz_und_arousal", "20 — Valenz und Arousal", "Stimmungs-Achsen"),
    ("21_cheatsheet", "21 — Cheatsheet", "Spickzettel"),
]


def utf8_b64(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("ascii")


# Regex to find ```strudel fenced code blocks.
STRUDEL_FENCE_RE = re.compile(
    r"^```strudel\s*\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL
)


def render_strudel_block(code: str, snippet_id: str) -> str:
    """Replace a strudel code fence with a snippet HTML block.

    The block contains the code as a <pre><code> + a button that
    loads a Strudel iframe on demand. Lazy-load saves bandwidth and
    avoids hammering strudel.cc when a page has 30 snippets.
    """
    code = code.rstrip()
    code_html = html.escape(code)
    code_b64 = utf8_b64(code)
    return (
        f'<div class="snippet" id="{snippet_id}" data-code-b64="{code_b64}">'
        f'<pre class="snippet-code"><code>{code_html}</code></pre>'
        f'<button class="snippet-play" type="button">▶ Spielen</button>'
        f'</div>'
    )


def expand_strudel_blocks(md_text: str) -> tuple[str, int]:
    """Replace ```strudel blocks with snippet placeholders.

    We do this BEFORE markdown processing because markdown might munge
    the HTML otherwise. We use unique placeholder strings that survive
    the markdown pipeline, then substitute back.
    """
    placeholders: list[str] = []
    counter = [0]

    def replace(match: re.Match) -> str:
        code = match.group(1)
        sid = f"snip-{counter[0]:03d}"
        counter[0] += 1
        html_block = render_strudel_block(code, sid)
        # Markdown ignores raw HTML blocks IF they're block-level and surrounded
        # by blank lines. Make sure we have those.
        placeholders.append(html_block)
        # Use a unique placeholder that markdown won't touch.
        return f"\n\n<!--SNIPPET-{len(placeholders) - 1}-->\n\n"

    new_text = STRUDEL_FENCE_RE.sub(replace, md_text)
    return new_text, len(placeholders), placeholders


def build_chapter_nav(idx: int, total: int) -> str:
    parts: list[str] = ['<nav class="chapter-nav">']
    if idx > 0:
        prev_stem, prev_title, _ = CHAPTER_META[idx - 1]
        parts.append(
            f'<a href="{prev_stem}.html" title="{html.escape(prev_title)}">← Zurück</a>'
        )
    else:
        parts.append('<span class="disabled">← Zurück</span>')
    if idx < total - 1:
        next_stem, next_title, _ = CHAPTER_META[idx + 1]
        parts.append(
            f'<a href="{next_stem}.html" title="{html.escape(next_title)}">Weiter →</a>'
        )
    else:
        parts.append('<span class="disabled">Weiter →</span>')
    parts.append("</nav>")
    return "".join(parts)


def build_chapter_links() -> str:
    items = []
    for stem, title, tagline in CHAPTER_META:
        m = re.match(r"^(\d+)\s+—\s+(.+)$", title)
        if m:
            num, rest = m.group(1), m.group(2)
        else:
            num, rest = "", title
        items.append(
            f'<li><a href="{stem}.html">'
            f'<span class="chap-num">{num}</span>'
            f'<span class="chap-body">'
            f'<span class="chap-title">{html.escape(rest)}</span>'
            f'<span class="chap-tagline">{html.escape(tagline)}</span>'
            f"</span></a></li>"
        )
    return "\n".join(items)


CHAPTER_TEMPLATE = """<!DOCTYPE html>
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
{nav}
</header>
<main>
<article class="prose">
{body}
</article>
</main>
<footer>
<p>Tipp: <kbd>Strg+Enter</kbd> startet/aktualisiert ein Pattern, <kbd>Strg+.</kbd> stoppt.</p>
</footer>
<script src="strudel-snippet.js?v={js_hash}" defer></script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
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
<p class="lead">Ein Strudel-Lehrbuch in Strudel. Jedes Kapitel hat erklärenden Text und kleine spielbare Code-Beispiele direkt in der Seite. Klick „Spielen" — der Editor öffnet sich mit dem Code, drück <kbd>Strg+Enter</kbd> oder das Play-Symbol.</p>
</header>
<main>
<ol class="chapters">
{chapter_links}
</ol>
<section class="hints">
<h2>Hinweise</h2>
<ul>
<li>Funktioniert in Chrome und Safari (Desktop + iPhone/iPad).</li>
<li>Erstes Sample-Trigger kann 1-2 Sekunden brauchen — Sample wird geladen.</li>
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
  --bg-elev: #232323;
  --bg-code: #0e0e0e;
  --fg: #e8e8e8;
  --muted: #888;
  --accent: #ffcc00;
  --link: #6cf;
  --border: #333;
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.6;
}

a { color: var(--link); }

kbd {
  background: var(--bg-code);
  border: 1px solid var(--border);
  border-radius: 3px;
  padding: 0.1rem 0.4rem;
  font-family: ui-monospace, "JetBrains Mono", "Fira Code", monospace;
  font-size: 0.85em;
}

/* ---------- Chapter page ---------- */

body.chapter header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.65rem 1rem;
  background: rgba(26, 26, 26, 0.92);
  backdrop-filter: blur(6px);
  border-bottom: 1px solid var(--border);
}

.back {
  text-decoration: none;
  font-size: 0.95rem;
}

.chapter-nav { display: flex; gap: 0.5rem; font-size: 0.9rem; }
.chapter-nav a {
  text-decoration: none;
  padding: 0.25rem 0.6rem;
  border: 1px solid var(--border);
  border-radius: 4px;
}
.chapter-nav a:hover { border-color: var(--link); }
.chapter-nav span.disabled {
  color: var(--muted);
  padding: 0.25rem 0.6rem;
  border: 1px solid #2a2a2a;
  border-radius: 4px;
}

.prose {
  max-width: 760px;
  margin: 1.5rem auto 4rem;
  padding: 0 1.25rem;
}

.prose h1 {
  font-size: 2rem;
  margin: 0.5rem 0 1.5rem;
  line-height: 1.2;
}
.prose h2 {
  font-size: 1.4rem;
  margin: 2.5rem 0 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
}
.prose h3 {
  font-size: 1.1rem;
  margin: 1.75rem 0 0.5rem;
  color: var(--fg);
}

.prose p { margin: 0 0 1rem; }
.prose ul, .prose ol { margin: 0 0 1rem 1.5rem; padding: 0; }
.prose li { margin: 0.25rem 0; }

.prose code {
  background: var(--bg-code);
  padding: 0.1em 0.35em;
  border-radius: 3px;
  font-family: ui-monospace, "JetBrains Mono", "Fira Code", monospace;
  font-size: 0.9em;
}

/* ---------- Snippet ---------- */

.snippet {
  margin: 1.25rem 0 1.5rem;
  border: 1px solid var(--border);
  border-radius: 6px;
  overflow: hidden;
  background: var(--bg-elev);
}

.snippet-code {
  margin: 0;
  padding: 0.85rem 1rem;
  background: var(--bg-code);
  font-family: ui-monospace, "JetBrains Mono", "Fira Code", monospace;
  font-size: 0.88rem;
  line-height: 1.5;
  overflow-x: auto;
}
.snippet-code code { background: transparent; padding: 0; }

.snippet-play {
  display: block;
  width: 100%;
  padding: 0.55rem 1rem;
  background: var(--bg-elev);
  color: var(--fg);
  border: 0;
  border-top: 1px solid var(--border);
  cursor: pointer;
  font: inherit;
  font-size: 0.9rem;
  text-align: left;
}
.snippet-play:hover { background: #2a2a2a; color: var(--accent); }

.snippet.playing .snippet-play { display: none; }
.snippet.playing .snippet-code { display: none; }
.snippet iframe {
  display: block;
  width: 100%;
  height: 360px;
  border: 0;
  background: var(--bg-code);
}

/* footer */

body.chapter footer {
  max-width: 760px;
  margin: 2rem auto 1.5rem;
  padding: 1rem 1.25rem 0;
  border-top: 1px solid var(--border);
  font-size: 0.85rem;
  color: var(--muted);
}

/* ---------- Index page ---------- */

body.index {
  max-width: 760px;
  margin: 0 auto;
  padding: 2.5rem 1.25rem 4rem;
}

body.index header h1 {
  font-size: 2.4rem;
  margin: 0 0 0.5rem;
}
.lead {
  color: var(--muted);
  font-size: 1.05rem;
  margin: 0 0 2rem;
}

ol.chapters {
  list-style: none;
  padding: 0;
  margin: 0 0 3rem;
  display: grid;
  gap: 0.5rem;
}
ol.chapters a {
  display: flex;
  align-items: baseline;
  padding: 0.85rem 1rem;
  background: var(--bg-elev);
  border-radius: 6px;
  text-decoration: none;
  color: var(--fg);
  border: 1px solid transparent;
  gap: 1rem;
  transition: border-color 0.15s, background 0.15s;
}
ol.chapters a:hover { border-color: var(--accent); background: #2a2a2a; }
.chap-num {
  color: var(--accent);
  font-family: ui-monospace, monospace;
  font-weight: 600;
  flex-shrink: 0;
  width: 2.5rem;
}
.chap-body { display: flex; flex-direction: column; }
.chap-tagline { color: var(--muted); font-size: 0.9rem; }

.hints {
  border-top: 1px solid var(--border);
  padding-top: 1.5rem;
  margin-top: 2rem;
}
.hints h2 { font-size: 1rem; color: var(--muted); font-weight: 500; margin: 0 0 0.5rem; }
.hints ul { margin: 0; padding-left: 1.25rem; color: var(--muted); font-size: 0.9rem; }
.hints li { margin: 0.3rem 0; }

body.index footer {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  font-size: 0.85rem;
  color: var(--muted);
}

/* ---------- Mobile ---------- */

@media (max-width: 600px) {
  body.chapter header { padding: 0.5rem 0.75rem; }
  .chapter-nav { font-size: 0.85rem; }
  .chapter-nav a, .chapter-nav span.disabled { padding: 0.2rem 0.45rem; }
  .prose { padding: 0 1rem; margin: 1rem auto 3rem; }
  .prose h1 { font-size: 1.7rem; }
  .prose h2 { font-size: 1.25rem; margin-top: 2rem; }
  .prose h3 { font-size: 1.05rem; }
  .snippet-code { font-size: 0.82rem; padding: 0.7rem 0.85rem; }
  .snippet iframe { height: 320px; }
  body.index { padding: 1.5rem 1rem 3rem; }
  body.index header h1 { font-size: 1.8rem; }
}
"""


JS = """\
// Lazy-load Strudel REPL iframes when "Spielen" is clicked.
// Each .snippet has data-code-b64 with UTF-8 base64 of the code.
(function () {
  document.querySelectorAll('.snippet-play').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var snippet = btn.closest('.snippet');
      if (!snippet || snippet.classList.contains('playing')) return;
      var b64 = snippet.getAttribute('data-code-b64');
      if (!b64) return;
      var src = 'https://strudel.cc/#' + encodeURIComponent(b64);
      var iframe = document.createElement('iframe');
      iframe.setAttribute('src', src);
      iframe.setAttribute('title', 'Strudel REPL');
      iframe.setAttribute('allow', 'autoplay');
      iframe.setAttribute('loading', 'lazy');
      snippet.appendChild(iframe);
      snippet.classList.add('playing');
    });
  });
})();
"""


def render_chapter(idx: int, stem: str, title: str) -> str:
    src = LEHRBUCH_MD / f"{stem}.md"
    if not src.exists():
        return ""
    md_text = src.read_text(encoding="utf-8")

    # Replace ```strudel fences with placeholder + render to HTML blocks later.
    md_no_fences, n_snippets, snippet_html = expand_strudel_blocks(md_text)

    # Markdown -> HTML.
    html_body = markdown.markdown(
        md_no_fences,
        extensions=["extra", "sane_lists"],
    )

    # Substitute snippet placeholders back. Markdown wraps HTML comments
    # in <p> sometimes; strip the wrapping.
    for i, block in enumerate(snippet_html):
        # Possible forms: <p><!--SNIPPET-i--></p>  or  <!--SNIPPET-i-->
        for needle in (
            f"<p><!--SNIPPET-{i}--></p>",
            f"<!--SNIPPET-{i}-->",
        ):
            html_body = html_body.replace(needle, block)

    return html_body


def build() -> None:
    DOCS_DIR.mkdir(exist_ok=True)

    css_hash = hashlib.sha1(CSS.encode("utf-8")).hexdigest()[:10]
    js_hash = hashlib.sha1(JS.encode("utf-8")).hexdigest()[:10]

    (DOCS_DIR / "style.css").write_text(CSS, encoding="utf-8")
    print(f"  wrote style.css (hash {css_hash})")
    (DOCS_DIR / "strudel-snippet.js").write_text(JS, encoding="utf-8")
    print(f"  wrote strudel-snippet.js (hash {js_hash})")

    total = len(CHAPTER_META)
    snippet_total = 0
    for idx, (stem, title, _tagline) in enumerate(CHAPTER_META):
        body = render_chapter(idx, stem, title)
        if not body:
            print(f"  ! missing markdown for {stem}")
            continue
        # Count snippets for the report.
        snippet_total += body.count('class="snippet"')
        nav = build_chapter_nav(idx, total)
        page = CHAPTER_TEMPLATE.format(
            title=html.escape(title),
            nav=nav,
            body=body,
            css_hash=css_hash,
            js_hash=js_hash,
        )
        out = DOCS_DIR / f"{stem}.html"
        out.write_text(page, encoding="utf-8")
        print(f"  wrote {stem}.html")

    index = INDEX_TEMPLATE.format(
        chapter_links=build_chapter_links(),
        css_hash=css_hash,
    )
    (DOCS_DIR / "index.html").write_text(index, encoding="utf-8")
    print(f"  wrote index.html")
    print(f"\nDone. {total} chapters, {snippet_total} snippets in {DOCS_DIR}")


if __name__ == "__main__":
    build()
