"""Builds assets/limits.svg: a joke usage panel in the style of OpenTokenUsage.

Edit ROWS and run `python limits.py`. Shares the font embedding with banner.py.
"""
from banner import font_face

# label, percent used, pace marker (percent or None), left note, right note
ROWS = [
    ("Claude Code, weekly", 94, 60, "Resets in 2d 3h", "Runs out tomorrow at this pace"),
    ("Coffee", 68, None, "Refill in 40m", "Top it up below"),
    ("Side projects", 300, None, "No reset scheduled", "Way over the limit"),
    ("Browser tabs", 87, None, "Resets when the browser crashes", "RAM disagrees"),
    ("Will to use the mouse", 3, None, "Resets never", "Keyboard wins"),
]
W, PAD, ROW_H, TOP = 1200, 56, 118, 200
BAR_W = W - 2 * PAD
H = TOP + ROW_H * (len(ROWS) - 1) + 100


def color(p):
    return "#3ba1ff" if p <= 50 else "#4dd0e1" if p <= 80 else "#f26b38" if p < 100 else "#ff5a4f"


def row(i, label, p, pace, left, right):
    y = TOP + i * ROW_H
    c = color(p)
    fill = min(p, 100) / 100 * BAR_W
    tick = (f'<rect x="{PAD + pace / 100 * BAR_W - 1.5:g}" y="{y + 12}" width="3" height="24" rx="1.5" fill="#ededee"/>'
            if pace else "")
    return f'''<text class="l" x="{PAD}" y="{y}">{label}</text>
<text class="v" x="{W - PAD}" y="{y}" text-anchor="end" fill="{c}">{p}%</text>
<rect x="{PAD}" y="{y + 18}" width="{BAR_W}" height="12" rx="6" fill="#1d1d22"/>
<rect class="bar" style="animation-delay:{.15 + i * .12:g}s" x="{PAD}" y="{y + 18}" width="{fill:g}" height="12" rx="6" fill="{c}"/>
{tick}
<text class="n" x="{PAD}" y="{y + 60}">{left}</text>
<text class="n" x="{W - PAD}" y="{y + 60}" text-anchor="end">{right}</text>'''


def build():
    fonts = "\n".join([
        font_face("Archivo", "Archivo:wdth,wght@125,800", "Archivo X", 800),
        font_face("Archivo", "Archivo:wdth,wght@100,600", "Archivo", 600),
        font_face("Archivo", "Archivo:wdth,wght@100,700", "Archivo", 700),
        font_face("JetBrains Mono", "JetBrains+Mono:wght@500", "JB Mono", 500),
    ])
    rows = "\n".join(row(i, *r) for i, r in enumerate(ROWS))
    alt = "; ".join(f"{l}: {p}%, {a.lower()}, {b.lower()}" for l, p, _, a, b in ROWS)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">Today's limits. {alt}.</title>
<style>
{fonts}
.h {{ font-family: "Archivo X", sans-serif; font-weight: 800; font-size: 40px; fill: #ededee; }}
.m {{ font-family: "JB Mono", monospace; font-weight: 500; font-size: 19px; fill: #9d9da7; }}
.l {{ font-family: "Archivo", sans-serif; font-weight: 600; font-size: 26px; fill: #ededee; }}
.v {{ font-family: "Archivo", sans-serif; font-weight: 700; font-size: 26px; }}
.n {{ font-family: "Archivo", sans-serif; font-weight: 600; font-size: 19px; fill: #9d9da7; }}
.bar {{ transform-box: fill-box; transform-origin: left; animation: grow 1.4s cubic-bezier(.2, .8, .2, 1) both; }}
@keyframes grow {{ from {{ transform: scaleX(0); }} }}
@media (prefers-reduced-motion: reduce) {{ .bar {{ animation: none; }} }}
</style>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="#000" stroke="#27272c" stroke-width="1.5"/>
<text class="h" x="{PAD}" y="98">Today's limits</text>
<text class="m" x="{W - PAD}" y="96" text-anchor="end">updated just now</text>
<line x1="{PAD}" y1="128" x2="{W - PAD}" y2="128" stroke="#27272c" stroke-width="1.5"/>
{rows}
</svg>
'''


if __name__ == "__main__":
    open("assets/limits.svg", "w", encoding="utf-8", newline="\n").write(build())
    print("assets/limits.svg written")
