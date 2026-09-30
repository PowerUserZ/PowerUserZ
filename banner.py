"""Builds assets/banner.svg: the PowerUserZ wordmark with a terminal line that types itself.

Edit PHRASES and run `python banner.py`. Fonts are subset from Google Fonts and embedded,
because an SVG shown through <img> can't load external fonts. Stdlib only.
"""
import base64, re, urllib.parse, urllib.request

PHRASES = [
    "building the tools I wish existed",
    "turning AI rate limits into a tray icon",
    "pasting screenshots where they refuse to go",
    "reading faster, one word at a time",
    "keyboard > mouse",
]
PROMPT = [("poweruserz", "#4dd0e1"), (":~$ ", "#9d9da7")]
CHARS = "".join(chr(c) for c in range(32, 127))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"

W, H = 1200, 340
MONO_SIZE = 30
CHAR_W = MONO_SIZE * 0.55         # measured JetBrains Mono advance in the browser
SLOT = 6                          # seconds each phrase owns
LOOP = SLOT * len(PHRASES)


def font_face(family, spec, css_family, weight):
    url = "https://fonts.googleapis.com/css2?family=" + spec + "&text=" + urllib.parse.quote(CHARS)
    css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
    woff2 = urllib.request.urlopen(re.search(r"url\((https:[^)]+)\)", css).group(1)).read()
    b64 = base64.b64encode(woff2).decode()
    return f'@font-face{{font-family:"{css_family}";font-weight:{weight};src:url(data:font/woff2;base64,{b64}) format("woff2")}}'


def pct(x):
    return f"{x:g}%"


def phrase_css(i, text):
    s = 100 * i / len(PHRASES)            # window start, in % of the loop
    w = 100 / len(PHRASES)                # window length
    width = len(text) * CHAR_W
    vis = (f"0%, {pct(max(s - .01, 0))} {{ opacity: 0; }} {pct(s)}, {pct(s + w - .01)} {{ opacity: 1; }} "
           f"{pct(s + w)}, 100% {{ opacity: 0; }}") if i else \
          f"0%, {pct(w - .01)} {{ opacity: 1; }} {pct(w)}, 100% {{ opacity: 0; }}"
    typing = (f"0%, {pct(s)} {{ transform: translateX(0); }} "
              f"{pct(s + w * .4)}, {pct(s + w * .8)} {{ transform: translateX({width:g}px); }} "
              f"{pct(s + w * .92)}, 100% {{ transform: translateX(0); }}")
    return (f"@keyframes v{i} {{ {vis} }}\n@keyframes t{i} {{ {typing} }}\n"
            f".p{i} {{ animation: v{i} {LOOP}s linear infinite; }}\n"
            f".p{i} .cover {{ animation: t{i} {LOOP}s steps({len(text)}) infinite; }}\n")


def build():
    fonts = "\n".join([
        font_face("Archivo", "Archivo:wdth,wght@125,800", "Archivo X", 800),
        font_face("JetBrains Mono", "JetBrains+Mono:wght@500", "JB Mono", 500),
    ])
    prompt_w = sum(len(t) for t, _ in PROMPT) * CHAR_W
    x0 = 64 + prompt_w
    prompt = "".join(f'<tspan fill="{c}">{t.replace(" ", "&#160;")}</tspan>' for t, c in PROMPT)
    phrases = "\n".join(
        f'<g class="p{i}"><text class="m" x="{x0:g}" y="282">{t.replace("&", "&amp;").replace(">", "&gt;")}</text>'
        f'<g class="cover"><rect class="caret" x="{x0:g}" y="256" width="{CHAR_W:g}" height="34"/>'
        f'<rect x="{x0 + CHAR_W:g}" y="250" width="{W:g}" height="50" fill="#000"/></g></g>'
        for i, t in enumerate(PHRASES))
    css = "".join(phrase_css(i, t) for i, t in enumerate(PHRASES))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">PowerUserZ</title>
<style>
{fonts}
.x {{ font-family: "Archivo X", sans-serif; font-weight: 800; fill: #ededee; }}
.m {{ font-family: "JB Mono", monospace; font-weight: 500; font-size: {MONO_SIZE}px; fill: #ededee; }}
.caret {{ fill: #ededee; animation: blink 1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
.key {{ animation: press {SLOT}s infinite; }}
@keyframes press {{ 0%, 2% {{ transform: translateY(0); }} 5% {{ transform: translateY(9px); }} 10%, 100% {{ transform: translateY(0); }} }}
{css}@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} g[class^="p"]:not(.p0) {{ opacity: 0; }} .p0 .cover {{ transform: translateX({len(PHRASES[0]) * CHAR_W:g}px); }} }}
</style>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="#000" stroke="#27272c" stroke-width="1.5"/>
<text class="x" x="64" y="180" font-size="124" letter-spacing="-3.7">PowerUser</text>
<g transform="translate(ZX 76)">
  <rect x="0" y="12" width="120" height="120" rx="22" fill="#2e2e35"/>
  <g class="key">
    <rect x="0" y="0" width="120" height="120" rx="22" fill="#1d1d22" stroke="#2e2e35" stroke-width="2"/>
    <text class="x" x="60" y="92" font-size="86" text-anchor="middle">Z</text>
  </g>
</g>
<text class="m" x="64" y="282">{prompt}</text>
{phrases}
</svg>
'''
    return svg


if __name__ == "__main__":
    import sys
    zx = sys.argv[1] if len(sys.argv) > 1 else "900"
    open("assets/banner.svg", "w", encoding="utf-8", newline="\n").write(build().replace("ZX", zx))
    print("assets/banner.svg written")
