"""Take preview screenshots of the new layout in iPhone + Desktop viewports."""

from __future__ import annotations

from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent / "_diag" / "preview"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "http://localhost:8765"


def go(page, url, label, full_page=True):
    page.goto(url, wait_until="domcontentloaded")
    page.wait_for_timeout(800)
    page.screenshot(path=str(OUT / f"{label}.png"), full_page=full_page)
    print(f"  {label}.png")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # iPhone
        ctx_iphone = browser.new_context(**p.devices["iPhone 13"])
        page = ctx_iphone.new_page()
        go(page, f"{BASE}/", "iphone_index", full_page=False)
        go(page, f"{BASE}/01_hello_sound.html", "iphone_01_top", full_page=False)
        go(page, f"{BASE}/01_hello_sound.html", "iphone_01_full", full_page=True)
        go(page, f"{BASE}/04_euklidisch.html", "iphone_04_full", full_page=True)
        ctx_iphone.close()

        # Desktop
        ctx_desktop = browser.new_context(viewport={"width": 1280, "height": 900})
        page = ctx_desktop.new_page()
        go(page, f"{BASE}/", "desktop_index", full_page=False)
        go(page, f"{BASE}/01_hello_sound.html", "desktop_01_top", full_page=False)
        go(page, f"{BASE}/01_hello_sound.html", "desktop_01_full", full_page=True)
        go(page, f"{BASE}/07_effekte.html", "desktop_07_full", full_page=True)
        ctx_desktop.close()

        # Click "Spielen" once and screenshot the playing state.
        ctx_iphone = browser.new_context(**p.devices["iPhone 13"])
        page = ctx_iphone.new_page()
        page.goto(f"{BASE}/01_hello_sound.html", wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        page.click(".snippet-play")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / "iphone_01_playing.png"), full_page=False)
        print("  iphone_01_playing.png")
        ctx_iphone.close()

        browser.close()


if __name__ == "__main__":
    main()
