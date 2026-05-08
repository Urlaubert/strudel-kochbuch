"""Quick Playwright test: load chapter page in iPhone viewport, screenshot,
dump errors and DOM info for diagnosis."""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = "https://urlaubert.github.io/strudel-kochbuch/01_hello_sound.html"
OUT = Path(__file__).parent / "_diag"
OUT.mkdir(exist_ok=True)


def run() -> None:
    with sync_playwright() as p:
        iphone = p.devices["iPhone 13"]
        browser = p.chromium.launch()
        ctx = browser.new_context(**iphone)
        page = ctx.new_page()

        console: list[str] = []
        page.on(
            "console",
            lambda msg: console.append(f"[{msg.type}] {msg.text}"),
        )
        page.on(
            "pageerror",
            lambda exc: console.append(f"[pageerror] {exc}"),
        )

        page.goto(URL, wait_until="networkidle")
        page.wait_for_timeout(2000)

        page.screenshot(path=str(OUT / "iphone.png"), full_page=False)
        page.screenshot(path=str(OUT / "iphone_full.png"), full_page=True)

        info = page.evaluate(
            """() => {
                const iframe = document.querySelector('#strudel');
                const main = document.querySelector('main');
                return {
                    has_iframe: !!iframe,
                    iframe_rect: iframe ? iframe.getBoundingClientRect() : null,
                    iframe_src_prefix: iframe ? (iframe.getAttribute('src') || '').slice(0, 60) : null,
                    iframe_src_length: iframe ? (iframe.getAttribute('src') || '').length : 0,
                    main_rect: main ? main.getBoundingClientRect() : null,
                    viewport: { w: window.innerWidth, h: window.innerHeight },
                };
            }"""
        )

        # Windows console can't always print emoji/unicode; force-encode.
        def safe(s: object) -> str:
            return str(s).encode("ascii", errors="replace").decode("ascii")

        print("=== console ===")
        for line in console:
            print(safe(line))
        print()
        print("=== dom info ===")
        for k, v in info.items():
            print(f"{k}: {safe(v)}")
        print()
        print(f"screenshots in {OUT}")

        browser.close()


if __name__ == "__main__":
    run()
