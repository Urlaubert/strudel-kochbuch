"""Walk through all 21 chapter pages on the live site in iPhone viewport.
Report which ones load the iframe, dump errors, take screenshots."""

from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://urlaubert.github.io/strudel-kochbuch"
OUT = Path(__file__).parent / "_diag" / "all"
OUT.mkdir(parents=True, exist_ok=True)

CHAPTERS = [
    "00_lies_mich_zuerst",
    "01_hello_sound",
    "02_mininotation",
    "03_polyrhythmik",
    "04_euklidisch",
    "05_skalen_und_melodie",
    "06_akkorde_und_voicings",
    "07_effekte",
    "08_signale_und_modulation",
    "09_time_modifier",
    "10_samples_eigene",
    "11_song_struktur",
    "12_mini_track_in_50_zeilen",
    "13_synthese_tief",
    "14_midi_und_io",
    "15_performance_hygiene",
    "16_eigene_helper",
    "17_hap_internals",
    "18_genre_kochbuch",
    "19_valenz_und_arousal",
    "20_cheatsheet",
]


def safe(s: object) -> str:
    return str(s).encode("ascii", errors="replace").decode("ascii")


def check_pages(label: str, browser, context_kwargs: dict, viewport_w_target: int) -> list[str]:
    ctx = browser.new_context(**context_kwargs)
    page = ctx.new_page()

    rows = []
    for stem in CHAPTERS:
        url = f"{BASE}/{stem}.html"
        errors: list[str] = []
        handler = lambda exc: errors.append(safe(exc))
        page.on("pageerror", handler)
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(1500)
        except Exception as e:
            rows.append(f"{stem}: GOTO ERROR {safe(e)[:80]}")
            page.remove_listener("pageerror", handler)
            continue

        info = page.evaluate(
            """() => {
                const iframe = document.querySelector('#strudel');
                return {
                    has_iframe: !!iframe,
                    iframe_w: iframe ? iframe.getBoundingClientRect().width : 0,
                    iframe_h: iframe ? iframe.getBoundingClientRect().height : 0,
                    src_len: iframe ? (iframe.getAttribute('src') || '').length : 0,
                    viewport_w: window.innerWidth,
                    has_script_tag: !!document.getElementById('strudel-code'),
                    code_text_len: document.getElementById('strudel-code') ? document.getElementById('strudel-code').textContent.length : 0,
                };
            }"""
        )
        page.screenshot(path=str(OUT / f"{label}_{stem}.png"), full_page=False)
        err_str = "; ".join(errors[:2]) if errors else "ok"
        rows.append(
            f"{stem}: iframe={info['has_iframe']} "
            f"{int(info['iframe_w'])}x{int(info['iframe_h'])} "
            f"src_len={info['src_len']} code_len={info['code_text_len']} | {err_str}"
        )
        page.remove_listener("pageerror", handler)

    ctx.close()
    return rows


def run() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()

        print(f"=== iPhone 13 viewport ===")
        iphone_rows = check_pages("iphone", browser, p.devices["iPhone 13"], 390)
        for r in iphone_rows:
            print(r)

        print()
        print(f"=== Desktop 1280x800 viewport ===")
        desktop_rows = check_pages(
            "desktop", browser, {"viewport": {"width": 1280, "height": 800}}, 1280
        )
        for r in desktop_rows:
            print(r)

        browser.close()
        print(f"\nScreenshots in {OUT}")


if __name__ == "__main__":
    run()
