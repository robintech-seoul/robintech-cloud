#!/usr/bin/env python3
"""프로파일 샘플 사이트의 갤러리 썸네일(profile/<slug>/thumb.jpg)을 만듭니다.

사용법: python3 scripts/profile_thumb.py <slug> [<slug> ...]
macOS 의 Google Chrome(헤드리스)과 sips 를 사용합니다. 1440x900 데스크톱 화면을 찍어 가로 1200px JPEG 으로 줄입니다.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def shoot(slug):
    page = ROOT / "profile" / slug / "index.html"
    if not page.exists():
        raise SystemExit(f"{page} 가 없습니다")
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "shot.png"
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--window-size=1440,900", "--virtual-time-budget=6000",
            f"--screenshot={png}", page.as_uri(),
        ], check=True, capture_output=True)
        out = page.parent / "thumb.jpg"
        subprocess.run(["sips", "-Z", "1200", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                        str(png), "--out", str(out)], check=True, capture_output=True)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for s in sys.argv[1:]:
        shoot(s)
