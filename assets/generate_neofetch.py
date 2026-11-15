#!/usr/bin/env python3
"""Generate assets/neofetch.svg, the animated terminal card on the profile.

Edit INFO (and PALETTE if you want) then run:  python3 assets/generate_neofetch.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

# ── Theme ── cyan → indigo → violet ("data / neural" palette)
PALETTE = {
    "bg": "#0b1020",
    "bar": "#1a2035",
    "cyan": "#22d3ee",
    "indigo": "#6366f1",
    "violet": "#a78bfa",
    "text": "#e2e8f0",
    "muted": "#64748b",
    "prompt": "#4ade80",
}

# ── Info lines ── ("Key", "value"). Add new lines here as you learn new things.
INFO = [
    ("OS", "Arch Linux x86_64 (btw)"),
    ("Field", "Engineering"),
    ("Uptime", "always learning"),
    ("Location", "Tunisia"),
    ("Shell", "bash"),
    ("Editor", "VS Code"),
    ("Languages", "Python, C, JavaScript, PHP"),
    ("Databases", "SQLite"),
    ("Tools", "Git, Node.js, Vite, Proteus"),
    ("Working on", "everything"),
    ("Learning", "everything about everything"),
]

LOGO = [
    "                   -`",
    "                  .o+`",
    "                 `ooo/",
    "                `+oooo:",
    "               `+oooooo:",
    "               -+oooooo+:",
    "             `/:-:++oooo+:",
    "            `/++++/+++++++:",
    "           `/++++++++++++++:",
    "          `/+++ooooooooooooo/`",
    "         ./ooosssso++osssssso+`",
    "        .oossssso-````/ossssss+`",
    "       -osssssso.      :ssssssso.",
    "      :osssssss/        osssso+++.",
    "     /ossssssss/        +ssssooo/-",
    "   `/ossssso+/:-        -:/+osssso+-",
    "  `+sso+:-`                 `.-/+oso:",
    " `++:.                           `-/+/",
    " .`                                 `/",
]

W = 860
LINE = 21.5
LOGO_LINE = 14.5
LOGO_FONT = 11.5
CHAR_W = LOGO_FONT * 0.6  # monospace glyph width
START = 1.4               # seconds before the output starts appearing


def build() -> str:
    p = PALETTE
    rows = 2 + len(INFO) + 2  # title, rule, info, blank, colours
    H = max(400, int(92 + rows * LINE + 40))
    y0 = 62
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="neofetch-style profile card">')
    a(f"""<style>
  .mono{{font-family:'JetBrains Mono','Fira Code','Cascadia Code',Consolas,Menlo,'DejaVu Sans Mono',monospace;font-size:13.5px}}
  .logo{{font-size:{LOGO_FONT}px}}
  .k{{fill:{p['cyan']};font-weight:700}}
  .v{{fill:{p['text']}}}
  .t{{fill:{p['violet']};font-weight:700}}
  .r{{fill:{p['muted']}}}
  .p{{fill:{p['prompt']};font-weight:700}}
  .reveal{{opacity:0;animation:show .35s ease-out forwards}}
  @keyframes show{{from{{opacity:0;transform:translateX(-6px)}}to{{opacity:1;transform:none}}}}
  .typing{{clip-path:inset(0 100% 0 0);animation:type 1s steps(8) .3s forwards}}
  @keyframes type{{to{{clip-path:inset(0 0 0 0)}}}}
  .cursor{{animation:blink 1s step-end infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  .glow{{animation:glow 3s ease-in-out infinite}}
  @keyframes glow{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
</style>""")
    a(f'<defs><linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p["cyan"]}"/><stop offset=".5" stop-color="{p["indigo"]}"/><stop offset="1" stop-color="{p["violet"]}"/></linearGradient>'
      f'<linearGradient id="lg" gradientUnits="userSpaceOnUse" x1="0" y1="{y0+16}" x2="0" y2="{y0+28+len(LOGO)*LOGO_LINE:.0f}"><stop offset="0" stop-color="{p["cyan"]}"/><stop offset="1" stop-color="{p["violet"]}"/></linearGradient></defs>')
    a(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="{p["bg"]}" stroke="url(#bd)" stroke-width="1.5"/>')
    a(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="14" fill="none" stroke="url(#bd)" stroke-width="3" class="glow"/>')
    a(f'<path d="M3 34 H{W-3}" stroke="{p["bar"]}"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        a(f'<circle cx="{24+i*20}" cy="18" r="6" fill="{c}"/>')
    a(f'<text x="{W/2}" y="23" text-anchor="middle" class="mono r" style="font-size:12px">ibrahim@archlinux: ~</text>')

    prompt = ('<tspan class="p">ibrahim@archlinux</tspan><tspan class="v">:</tspan>'
              f'<tspan style="fill:{p["cyan"]}">~</tspan><tspan class="v">$ </tspan>')
    a(f'<text x="24" y="{y0}" class="mono">{prompt}</text>')
    a(f'<text x="194" y="{y0}" class="mono v typing">neofetch</text>')

    for i, line in enumerate(LOGO):
        lead = len(line) - len(line.lstrip(" "))
        a(f'<text xml:space="preserve" x="{24+lead*CHAR_W:.1f}" y="{y0+28+i*LOGO_LINE:.1f}" class="mono logo reveal" '
          f'fill="url(#lg)" style="animation-delay:{START+i*0.04:.2f}s">{escape(line.lstrip(" "))}</text>')

    ix, iy = 330, y0 + 30
    rows_out = [("title", None), ("rule", None)] + [("kv", kv) for kv in INFO] + [("blank", None), ("colors", None)]
    for i, (kind, val) in enumerate(rows_out):
        d = START + 0.3 + i * 0.12
        y = iy + i * LINE
        if kind == "title":
            a(f'<text x="{ix}" y="{y}" class="mono reveal" style="animation-delay:{d:.2f}s"><tspan class="t">ibrahim</tspan><tspan class="v">@</tspan><tspan class="t">github</tspan></text>')
        elif kind == "rule":
            a(f'<rect x="{ix}" y="{y-5}" width="112" height="1.5" fill="{p["muted"]}" class="reveal" style="animation-delay:{d:.2f}s"/>')
        elif kind == "kv":
            k, v = val
            a(f'<text xml:space="preserve" x="{ix}" y="{y}" class="mono reveal" style="animation-delay:{d:.2f}s"><tspan class="k">{escape(k)}</tspan><tspan class="v">: {escape(v)}</tspan></text>')
        elif kind == "colors":
            cols = ["#1e293b", "#f87171", "#4ade80", "#facc15", p["cyan"], p["indigo"], p["violet"], p["text"]]
            for j, c in enumerate(cols):
                a(f'<rect x="{ix+j*30}" y="{y-14}" width="26" height="16" rx="3" fill="{c}" class="reveal" style="animation-delay:{d+j*0.05:.2f}s"/>')

    fy = H - 22
    fd = START + 0.3 + len(rows_out) * 0.12 + 0.4
    a(f'<g class="reveal" style="animation-delay:{fd:.2f}s"><text x="24" y="{fy}" class="mono">{prompt}</text>'
      f'<rect x="194" y="{fy-12}" width="8" height="15" fill="{p["text"]}" class="cursor"/></g>')
    a("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(__file__).with_name("neofetch.svg")
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out}")
