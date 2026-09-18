#!/usr/bin/env python3
"""PNG-previews van alle mockups, 1600 px breed, in ../preview/.

Draaien:  python brandbook/assets/mockups/_bron/maak_previews.py
Nodig:    Google Chrome of Microsoft Edge (headless). Geen Python-pakketten.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
OUT = os.path.join(SRC, "preview")
WIDTH = 1600
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium",
]


def main():
    browser = next((b for b in BROWSERS if os.path.exists(b)), None)
    if not browser:
        sys.exit("Geen Chrome of Edge gevonden. Pas BROWSERS aan.")
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for svg in sorted(glob.glob(os.path.join(SRC, "*.svg"))):
            name = os.path.splitext(os.path.basename(svg))[0]
            vb = re.search(r'viewBox="([^"]+)"', open(svg, encoding="utf-8").read()).group(1).split()
            w, h = float(vb[2]), float(vb[3])
            height = round(WIDTH * h / w)
            page = os.path.join(tmp, name + ".html")
            with open(page, "w", encoding="utf-8") as f:
                f.write(f"<!doctype html><body style='margin:0'><img src='file:///{svg.replace(os.sep, '/')}' "
                        f"style='display:block;width:{WIDTH}px;height:{height}px'></body>")
            png = os.path.join(OUT, name + ".png")
            subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--allow-file-access-from-files", f"--user-data-dir={os.path.join(tmp, 'profiel')}",
                            "--force-device-scale-factor=1", f"--window-size={WIDTH},{height}",
                            f"--screenshot={png}", "file:///" + page.replace(os.sep, "/")],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   {name + '.png':34s} {WIDTH} x {height}")


if __name__ == "__main__":
    main()
