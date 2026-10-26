"""Render figures to PNG for a quick visual check (light and dark backgrounds).

Usage, from the repository root (needs `pip install cairosvg`):

    python3 tools/figures/render.py docs/assets/figures /tmp/figure-previews s_plane_map pendulum

Previews are for checking layout only; they aren't part of the site.
"""
import sys, cairosvg
from pathlib import Path
src = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
for name in sys.argv[3:]:
    for suf, bg in (("", "white"), ("_dark", "#1e2129")):
        cairosvg.svg2png(url=str(src / f"{name}{suf}.svg"), write_to=str(out / f"{name}{suf}.png"),
                         output_width=1000, background_color=bg)
print("rendered", len(sys.argv) - 3)
