"""Builds assets/setup.svg: two rows of keycaps with the systems and AI tools I use.

The keys press in a typing rhythm and light up in their brand color. Edit ROWS and run
`python setup.py`. Logos come from simple-icons (CC0).
"""
import re, urllib.request
from banner import font_face

ROWS = [
    ("My home row", [
        ("windows11", "Windows 11", "#2d9cff"),
        ("apple", "macOS", "#ededee"),
        ("ubuntu", "Ubuntu 26.04", "#e95420"),
        ("linux", "WSL2", "#fcc624"),
        ("android", "Android", "#3ddc84"),
    ]),
    ("My pair programmers", [
        ("claude", "Claude Code", "#d97757"),
        ("openai", "Codex", "#ededee"),
        ("cursor", "Cursor", "#ededee"),
        ("opencode", "OpenCode", "#ededee"),
    ]),
]
ORDER = [0, 5, 2, 7, 1, 8, 3, 6, 4]   # which key is pressed 1st, 2nd, ... (reads like typing)
W, PAD, GAP, KW, KH, SKIRT = 1200, 56, 22, 200, 150, 10
LOOP, STEP = 8, 6                      # seconds per loop, % of the loop between presses
ICON = 52


def icon_path(slug):
    svg = urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{slug}.svg").read().decode()
    return re.search(r' d="([^"]+)"', svg).group(1)


def key(n, x, y, slug, label, glow):
    s = ORDER.index(n) * STEP
    d = icon_path(slug)
    logo = f'transform="translate({x + KW / 2 - ICON / 2:g} {y + 30}) scale({ICON / 24:g})"'
    css = (f"@keyframes p{n} {{ 0%, {s}% {{ transform: translateY(0); }} {s + 2}% {{ transform: translateY(7px); }} "
           f"{s + 6}%, 100% {{ transform: translateY(0); }} }}\n"
           f"@keyframes g{n} {{ 0%, {s}% {{ opacity: 0; }} {s + 2}% {{ opacity: 1; }} {s + 16}%, 100% {{ opacity: 0; }} }}\n"
           f".p{n} {{ animation: p{n} {LOOP}s infinite; }} .g{n} {{ animation: g{n} {LOOP}s infinite; }}\n")
    svg = f'''<rect x="{x}" y="{y + SKIRT}" width="{KW}" height="{KH}" rx="18" fill="#2e2e35"/>
<g class="p{n}">
  <rect x="{x}" y="{y}" width="{KW}" height="{KH}" rx="18" fill="#1d1d22" stroke="#2e2e35" stroke-width="2"/>
  <path d="{d}" fill="#c8c8cf" {logo}/>
  <g class="glow g{n}">
    <rect x="{x}" y="{y}" width="{KW}" height="{KH}" rx="18" fill="{glow}" fill-opacity=".12" stroke="{glow}" stroke-width="2"/>
    <path d="{d}" fill="{glow}" {logo}/>
  </g>
  <text class="k" x="{x + KW / 2:g}" y="{y + 124}" text-anchor="middle">{label}</text>
</g>'''
    return svg, css


def build():
    fonts = "\n".join([
        font_face("Archivo", "Archivo:wdth,wght@125,800", "Archivo X", 800),
        font_face("Archivo", "Archivo:wdth,wght@100,600", "Archivo", 600),
    ])
    body, css, n, y = [], [], 0, 100
    for title, keys in ROWS:
        body.append(f'<text class="h" x="{PAD}" y="{y}">{title}</text>')
        for i, k in enumerate(keys):
            svg, c = key(n, PAD + i * (KW + GAP), y + 28, *k)
            body.append(svg); css.append(c); n += 1
        y += 28 + KH + SKIRT + 72
    h = y - 72 + 56 - 0
    alt = " ".join(f"{t}: {', '.join(k[1] for k in keys)}." for t, keys in ROWS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{alt}</title>
<style>
{fonts}
.h {{ font-family: "Archivo X", sans-serif; font-weight: 800; font-size: 30px; fill: #ededee; }}
.k {{ font-family: "Archivo", sans-serif; font-weight: 600; font-size: 19px; fill: #9d9da7; }}
.glow {{ opacity: 0; }}
{"".join(css)}@media (prefers-reduced-motion: reduce) {{ [class^="p"], .glow {{ animation: none !important; }} }}
</style>
<rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="24" fill="#000" stroke="#27272c" stroke-width="1.5"/>
{chr(10).join(body)}
</svg>
'''


if __name__ == "__main__":
    open("assets/setup.svg", "w", encoding="utf-8", newline="\n").write(build())
    print("assets/setup.svg written")
