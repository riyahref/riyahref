import os, sys, textwrap
from xml.sax.saxutils import escape as esc

DEBUG = len(sys.argv) > 1 and sys.argv[1] == "debug"
OUT = "/home/claude/riyahref/assets" if not DEBUG else "/home/claude/riyahref/debug"
os.makedirs(OUT, exist_ok=True)

# Catppuccin Mocha
BASE, MANTLE, SURF0, SURF1 = "#1e1e2e", "#181825", "#313244", "#45475a"
TEXT, SUB, OVER = "#cdd6f4", "#bac2de", "#6c7086"
MAUVE, PINK, RED, PEACH, YELLOW = "#cba6f7", "#f5c2e7", "#f38ba8", "#fab387", "#f9e2af"
GREEN, TEAL, BLUE, LAV = "#a6e3a1", "#94e2d5", "#89b4fa", "#b4befe"
FONT = "'JetBrains Mono','Fira Code',Consolas,'SF Mono','Courier New',monospace"
W = 880


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}">\n<defs>{defs}</defs>\n{body}\n</svg>\n')


def typed(uid, x, y, segs, size, cw, s, per, cycle, cursor=None):
    """Typewriter reveal of coloured segments. segs=[(text,color,bold?)]. Returns (defs, body)."""
    n = sum(len(t[0]) for t in segs)
    spans = "".join(
        f'<tspan fill="{c}"{" font-weight=\"700\"" if (len(t) > 2 and t[2]) else ""}>{esc(txt)}</tspan>'
        for t in segs for txt, c in [(t[0], t[1])]
    )
    text = (f'<text x="{x}" y="{y}" font-size="{size}" xml:space="preserve" style="white-space:pre" '
            f'clip-path="url(#{uid})">{spans}</text>')
    ch, cy = size * 1.5, y - size
    if DEBUG:
        defs = f'<clipPath id="{uid}"><rect x="{x-2}" y="{cy}" width="900" height="{ch}"/></clipPath>'
        return defs, text
    times = [0] + [s + per * k / n for k in range(1, n + 1)] + [0.94, 1]
    widths = [0] + [(k * cw if k < n else 900) for k in range(1, n + 1)] + [0, 0]
    kt = ";".join(f"{t:.4f}" for t in times)
    vals = ";".join(f"{v:.1f}" for v in widths)
    defs = (f'<clipPath id="{uid}"><rect x="{x-2}" y="{cy}" width="0" height="{ch}">'
            f'<animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
    body = text
    if cursor:
        xs = ";".join(f"{x + k * cw:.1f}" for k in range(0, n + 1))
        xs = ";".join([f"{x:.1f}"] + [f"{x + k * cw:.1f}" for k in range(1, n + 1)] + [f"{x:.1f}", f"{x:.1f}"])
        body += (f'<rect y="{cy+2}" width="{cw*0.8:.1f}" height="{size*1.25:.1f}" fill="{cursor}">'
                 f'<animate attributeName="x" dur="{cycle}s" repeatCount="indefinite" calcMode="discrete" '
                 f'keyTimes="{kt}" values="{xs}"/>'
                 f'<animate attributeName="opacity" dur="0.9s" repeatCount="indefinite" calcMode="discrete" '
                 f'keyTimes="0;0.5;1" values="1;0;1"/></rect>')
    return defs, body


def glow_stroke(color_a, color_b, dur=6, begin=0):
    if DEBUG:
        return ""
    return (f'<animate attributeName="stroke" values="{color_a};{color_b};{color_a}" dur="{dur}s" '
            f'begin="{begin}s" repeatCount="indefinite"/>')


# ------------------------------------------------------------------ HEADER
def header():
    H, cycle = 350, 14
    defs, body = "", ""
    body += f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BASE}" stroke="{MAUVE}" stroke-width="1.5">{glow_stroke(MAUVE, BLUE, 6)}</rect>'
    body += f'<path d="M1 15 a14 14 0 0 1 14 -14 h{W-30} a14 14 0 0 1 14 14 v21 h-{W-2} z" fill="{MANTLE}"/>'
    for i, c in enumerate([RED, YELLOW, GREEN]):
        body += f'<circle cx="{26+i*20}" cy="19" r="6" fill="{c}"/>'
    body += f'<text x="{W/2}" y="23" text-anchor="middle" font-size="12" fill="{OVER}">riya@portfolio: ~/readme</text>'
    # tabs
    body += f'<rect x="1" y="36" width="{W-2}" height="30" fill="{MANTLE}"/>'
    body += f'<rect x="1" y="36" width="130" height="30" fill="{BASE}"/><rect x="1" y="36" width="130" height="2" fill="{MAUVE}"/>'
    body += f'<text x="16" y="56" font-size="12.5" fill="{TEXT}"><tspan fill="{BLUE}">TS</tspan>  about.ts</text>'
    body += f'<text x="150" y="56" font-size="12.5" fill="{OVER}">README.md</text>'
    body += f'<text x="262" y="56" font-size="12.5" fill="{OVER}">projects.json</text>'
    # editor
    lines = [
        [("// hey, i'm Riya Panjwani", OVER)],
        [("const ", MAUVE), ("riya", TEXT), (" = {", SUB)],
        [("  role", BLUE), (": ", SUB), ('"AI/ML + Full-Stack Engineer"', GREEN), (",", SUB)],
        [("  stack", BLUE), (": [", SUB), ('"Python"', GREEN), (", ", SUB), ('"TypeScript"', GREEN), (", ", SUB),
         ('"React"', GREEN), (", ", SUB), ('"Node.js"', GREEN), ("],", SUB)],
        [("  building", BLUE), (": ", SUB), ('"AI that actually ships"', GREEN), (",", SUB)],
        [("  learning", BLUE), (": [", SUB), ('"MLOps"', GREEN), (", ", SUB), ('"System Design"', GREEN), ("],", SUB)],
        [("  openToWork", BLUE), (": ", SUB), ("true", PEACH), (",", SUB)],
        [("};", SUB)],
        [("$ ", GREEN), ("npm run ship-it", TEXT)],
    ]
    y0, lh = 98, 26
    for i, segs in enumerate(lines):
        y = y0 + i * lh
        body += f'<text x="40" y="{y}" font-size="13" text-anchor="end" fill="{SURF1}">{i+1}</text>'
        d, b = typed(f"hc{i}", 60, y, segs, 14, 8.4, 0.03 + i * 0.05, 0.045, cycle,
                     cursor=MAUVE if i == len(lines) - 1 else None)
        defs += d; body += b
    # terminal panel
    px, py, pw, ph = 548, 80, 316, 232
    body += f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{MANTLE}" stroke="{SURF0}"/>'
    body += f'<text x="{px+14}" y="{py+22}" font-size="11" fill="{OVER}" letter-spacing="1.5">TERMINAL</text>'
    body += f'<line x1="{px}" y1="{py+32}" x2="{px+pw}" y2="{py+32}" stroke="{SURF0}"/>'
    term = [
        [("$ ", GREEN), ("whoami", TEXT)],
        [("riya-panjwani", MAUVE)],
        [("$ ", GREEN), ("cat status.log", TEXT)],
        [("[ok] ", GREEN), ("mern.stack ......... ", SUB), ("loaded", TEAL)],
        [("[ok] ", GREEN), ("ml.models .......... ", SUB), ("training", PEACH)],
        [("[..] ", YELLOW), ("coffee ............ ", SUB), ("brewing", YELLOW)],
        [("[ok] ", GREEN), ("curiosity ......... ", SUB), ("100%", PINK)],
    ]
    for j, segs in enumerate(term):
        y = py + 58 + j * 25
        d, b = typed(f"ht{j}", px + 14, y, segs, 12.5, 7.5, 0.48 + j * 0.06, 0.05, cycle)
        defs += d; body += b
    # status bar
    body += f'<path d="M1 {H-24} h{W-2} v10 a14 14 0 0 1 -14 14 h-{W-30} a14 14 0 0 1 -14 -14 z" fill="{MAUVE}"/>'
    body += f'<text x="16" y="{H-8}" font-size="11.5" font-weight="700" fill="{BASE}">main*   0 errors   0 warnings</text>'
    body += f'<text x="{W-16}" y="{H-8}" font-size="11.5" font-weight="700" text-anchor="end" fill="{BASE}">TypeScript   UTF-8   Ln 9, Col 1</text>'
    return svg(W, H, body, defs)


# ------------------------------------------------------------------ SECTION TITLES
def section(cmd, note):
    H, cycle = 52, 9
    prompt = [("riya", GREEN, True), ("@github", GREEN, True), (":", TEXT), ("~", BLUE, True), ("$ ", TEXT)]
    plen = sum(len(p[0]) for p in prompt)
    body = f'<text x="8" y="30" font-size="16" xml:space="preserve" style="white-space:pre">' + "".join(
        f'<tspan fill="{p[1]}"{" font-weight=\"700\"" if len(p) > 2 else ""}>{esc(p[0])}</tspan>' for p in prompt) + "</text>"
    d, b = typed("c", 8 + plen * 9.6, 30, [(cmd, TEXT, True)], 16, 9.6, 0.04, 0.16, cycle, cursor=MAUVE)
    body += b
    body += f'<text x="{W-8}" y="30" font-size="13" text-anchor="end" fill="{OVER}">{esc(note)}</text>'
    grad = (f'<linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{MAUVE}"/>'
            f'<stop offset="0.5" stop-color="{BLUE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>')
    body += f'<line x1="8" y1="44" x2="{W-8}" y2="44" stroke="{SURF0}" stroke-width="2"/>'
    anim = "" if DEBUG else f'<animate attributeName="stroke-dashoffset" from="0" to="-120" dur="3s" repeatCount="indefinite"/>'
    body += (f'<line x1="8" y1="44" x2="{W-8}" y2="44" stroke="url(#g)" stroke-width="2" stroke-linecap="round" '
             f'stroke-dasharray="60 60">{anim}</line>')
    return svg(W, H, body, d + grad)


# ------------------------------------------------------------------ PROJECT ART (216x168 panels)
def anim(xml):
    return "" if DEBUG else xml


def draw_anim(dur=6):
    return anim(f'<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;0.5;0.9;1" dur="{dur}s" repeatCount="indefinite"/>')


def art_f1():
    s = ""
    for gy in (40, 80, 120):
        s += f'<line x1="12" y1="{gy}" x2="204" y2="{gy}" stroke="{SURF0}"/>'
    fans = ["M12 120 C45 110 60 70 100 72 S160 60 204 24", "M12 120 C45 118 70 95 100 88 S160 80 204 52",
            "M12 120 C45 100 60 50 100 56 S160 30 204 12", "M12 120 C45 120 80 110 110 100 S170 100 204 84"]
    for d in fans:
        s += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-opacity="0.35" stroke-width="1.5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if DEBUG else 1}">{draw_anim(6)}</path>'
    s += f'<path d="M12 120 C45 110 60 70 100 72 S160 60 204 24" fill="none" stroke="{PINK}" stroke-width="3" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if DEBUG else 1}">{draw_anim(6)}</path>'
    s += f'<line x1="100" y1="22" x2="100" y2="140" stroke="{YELLOW}" stroke-dasharray="3 4"/>'
    s += f'<text x="104" y="34" font-size="10" fill="{YELLOW}">PIT</text>'
    s += f'<text x="12" y="18" font-size="10" fill="{OVER}">monte_carlo x 10k</text>'
    s += f'<rect x="12" y="144" width="86" height="16" rx="8" fill="{TEAL}" fill-opacity="0.15"/><text x="55" y="155.5" font-size="10" text-anchor="middle" fill="{TEAL}">P1 prob 38.2%</text>'
    return s


def art_sentinel():
    ecg = "M10 96 L50 96 L60 96 L68 64 L78 124 L88 44 L98 96 L140 96 L150 96 L158 76 L166 110 L174 96 L206 96"
    s = f'<path d="{ecg}" fill="none" stroke="{SURF1}" stroke-width="2"/>'
    s += f'<path d="{ecg}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if DEBUG else 1}">{draw_anim(3)}</path>'
    s += f'<circle cx="20" cy="26" r="5" fill="{GREEN}">' + anim(f'<animate attributeName="r" values="4;7;4" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0.4;1" dur="1.6s" repeatCount="indefinite"/>') + '</circle>'
    s += f'<text x="34" y="30" font-size="11" fill="{TEXT}">api-gateway  UP</text>'
    s += f'<text x="12" y="52" font-size="10" fill="{OVER}">p95 124ms  uptime 99.9%</text>'
    s += f'<rect x="12" y="140" width="110" height="16" rx="8" fill="{RED}" fill-opacity="0.15"/>'
    s += f'<circle cx="24" cy="148" r="3" fill="{RED}">' + anim(f'<animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>') + '</circle>'
    s += f'<text x="32" y="151.5" font-size="10" fill="{RED}">alerts: 0 firing</text>'
    return s


def art_route():
    s = ""
    for d in ["M0 60 L216 40", "M0 110 L216 130", "M60 0 L80 168", "M150 0 L130 168"]:
        s += f'<path d="{d}" stroke="{SURF0}" stroke-width="6" fill="none"/>'
    p = "M24 130 C60 120 70 60 110 70 S170 40 196 34"
    s += f'<path d="{p}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round" stroke-dasharray="7 7">' + anim('<animate attributeName="stroke-dashoffset" from="0" to="-28" dur="1s" repeatCount="indefinite"/>') + '</path>'
    s += f'<circle cx="82" cy="92" r="6" fill="{PEACH}" fill-opacity="0.9">' + anim(f'<animate attributeName="r" values="4;9;4" dur="2s" repeatCount="indefinite"/><animate attributeName="fill-opacity" values="0.9;0.2;0.9" dur="2s" repeatCount="indefinite"/>') + '</circle>'
    s += f'<circle cx="24" cy="130" r="6" fill="{GREEN}"/><circle cx="196" cy="34" r="6" fill="{RED}"/>'
    s += f'<circle r="5" fill="{PINK}" cx="{24 if DEBUG else 0}" cy="{130 if DEBUG else 0}">' + anim(f'<animateMotion dur="5s" repeatCount="indefinite" path="{p}"/>') + '</circle>'
    s += f'<rect x="12" y="144" width="96" height="16" rx="8" fill="{GREEN}" fill-opacity="0.15"/><text x="60" y="155.5" font-size="10" text-anchor="middle" fill="{GREEN}">safety score 92%</text>'
    s += f'<text x="12" y="18" font-size="10" fill="{OVER}">weather / crowd / light</text>'
    return s


def art_vibe():
    gr = f'<linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="{RED}"/><stop offset="0.5" stop-color="{YELLOW}"/><stop offset="1" stop-color="{GREEN}"/></linearGradient>'
    s = gr
    s += f'<path d="M38 112 A70 70 0 0 1 178 112" fill="none" stroke="{SURF0}" stroke-width="14" stroke-linecap="round"/>'
    s += f'<path d="M38 112 A70 70 0 0 1 178 112" fill="none" stroke="url(#gg)" stroke-width="14" stroke-linecap="round"/>'
    rot = "" if DEBUG else (f'<animateTransform attributeName="transform" type="rotate" dur="6s" repeatCount="indefinite" '
                            f'values="-70 108 112;45 108 112;5 108 112;62 108 112;-70 108 112" keyTimes="0;0.3;0.5;0.8;1"/>')
    s += f'<g transform="rotate(50 108 112)"><line x1="108" y1="112" x2="108" y2="56" stroke="{TEXT}" stroke-width="3" stroke-linecap="round">{rot}</line></g>' if DEBUG else \
        f'<line x1="108" y1="112" x2="108" y2="56" stroke="{TEXT}" stroke-width="3" stroke-linecap="round">{rot}</line>'
    s += f'<circle cx="108" cy="112" r="6" fill="{TEXT}"/>'
    s += f'<text x="108" y="142" font-size="13" font-weight="700" text-anchor="middle" fill="{GREEN}">Positive</text>'
    s += f'<text x="12" y="18" font-size="10" fill="{OVER}">r/subreddit  AFINN-165</text>'
    for i, h in enumerate([10, 18, 26, 14, 22, 30, 16]):
        x = 20 + i * 27
        a = anim(f'<animate attributeName="height" values="{h};{h+12};{h}" dur="{1.5+i*0.2:.1f}s" repeatCount="indefinite"/><animate attributeName="y" values="{162-h};{162-h-12};{162-h}" dur="{1.5+i*0.2:.1f}s" repeatCount="indefinite"/>')
        s += f'<rect x="{x}" y="{162-h}" width="14" height="{h}" rx="3" fill="{MAUVE}" fill-opacity="0.55">{a}</rect>' if False else ""
    return s


def art_booth():
    s = f'<rect x="22" y="10" width="62" height="148" rx="8" fill="{PINK}" fill-opacity="0.12" stroke="{PINK}" stroke-opacity="0.5"/>'
    for i in range(3):
        y = 18 + i * 46
        s += f'<rect x="30" y="{y}" width="46" height="40" rx="5" fill="{SURF0}"/>'
        s += f'<circle cx="53" cy="{y+16}" r="8" fill="{PINK}"/><path d="M38 {y+38} a15 13 0 0 1 30 0z" fill="{PINK}"/>'
        a = anim(f'<animate attributeName="opacity" values="0;0;0.95;0;0" keyTimes="0;{0.05+i*0.25:.2f};{0.1+i*0.25:.2f};{0.25+i*0.25:.2f};1" dur="4s" repeatCount="indefinite"/>')
        s += f'<rect x="30" y="{y}" width="46" height="40" rx="5" fill="#fff" opacity="0">{a}</rect>'
    s += f'<rect x="104" y="24" width="96" height="104" rx="8" fill="none" stroke="{MAUVE}" stroke-width="2" stroke-dasharray="6 5"/>'
    s += f'<circle cx="152" cy="68" r="26" fill="none" stroke="{PINK}" stroke-width="2.5"/>'
    s += f'<circle cx="143" cy="62" r="2.5" fill="{PINK}"/><circle cx="161" cy="62" r="2.5" fill="{PINK}"/>'
    s += f'<path d="M140 76 q12 12 24 0" fill="none" stroke="{PINK}" stroke-width="2.5" stroke-linecap="round"/>'
    for (cx, cy) in [(130, 50), (174, 50), (126, 74), (178, 74), (152, 96), (140, 92), (164, 92)]:
        s += f'<circle cx="{cx}" cy="{cy}" r="2" fill="{TEAL}">' + anim(f'<animate attributeName="opacity" values="1;0.15;1" dur="{1+(cx%5)*0.3:.1f}s" repeatCount="indefinite"/>') + '</circle>'
    s += f'<text x="152" y="148" font-size="11" text-anchor="middle" fill="{OVER}">say cheese</text>'
    return s


def art_canvas():
    p = "M26 112 C46 36 70 36 82 90 S112 144 132 84 S162 30 190 70"
    s = f'<rect x="10" y="12" width="196" height="108" rx="8" fill="none" stroke="{SURF1}" stroke-dasharray="4 4"/>'
    s += f'<path d="{p}" fill="none" stroke="{YELLOW}" stroke-width="4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="{0 if DEBUG else 1}">{draw_anim(6)}</path>'
    mot = anim('<animateMotion dur="6s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;0.5;1" path="%s"/>' % p)
    s += f'<g transform="translate({26 if DEBUG else 0},{112 if DEBUG else 0})"><circle r="9" fill="none" stroke="{TEAL}" stroke-width="2">' + anim(f'<animate attributeName="r" values="9;5;9" dur="0.8s" repeatCount="indefinite"/>') + f'</circle><circle r="3" fill="{TEAL}"/>{mot}</g>'
    s += f'<rect x="12" y="136" width="108" height="18" rx="9" fill="{TEAL}" fill-opacity="0.15"/><text x="66" y="148.5" font-size="10.5" text-anchor="middle" fill="{TEAL}">pinch = draw</text>'
    s += f'<text x="206" y="148" font-size="10" text-anchor="end" fill="{OVER}">0 mouse, 0 touch</text>'
    return s


# ------------------------------------------------------------------ CARDS
PROJECTS = [
    dict(n=1, file="f1_race_strategy.py", title="F1 Race Strategy AI", tag="Best AI/ML showcase", art=art_f1,
         desc="An AI-powered race strategy decision-support system that uses historical F1 data, tyre degradation modeling, and Monte Carlo simulations to evaluate pit-stop strategies and estimate race outcomes.",
         tech=["Python", "XGBoost", "FastF1", "Streamlit", "Pandas", "NumPy", "Monte Carlo Simulation"], out="project-1-f1.svg"),
    dict(n=2, file="sentinel.ts", title="Sentinel", tag="Best backend / systems project", art=art_sentinel,
         desc="A self-hosted observability platform designed to monitor service uptime and latency, collect application errors, evaluate alert rules, and track incidents through a live dashboard.",
         tech=["TypeScript", "Node.js", "Express", "PostgreSQL", "Service-oriented monorepo", "Queue-based ingestion", "Docker"], out="project-2-sentinel.svg"),
    dict(n=3, file="safe_route.tsx", title="Safety-Aware Route Recommendation", tag="Full-stack, real-time", art=art_route,
         desc="A full-stack routing prototype that ranks routes using safety factors such as weather, crowd density, lighting, and construction conditions, with real-time updates and visual safety indicators.",
         tech=["React", "TypeScript", "Node.js", "Express", "Socket.IO", "Mapbox GL JS", "Zustand", "Tailwind CSS", "Recharts"], out="project-3-route.svg"),
    dict(n=4, file="vibe_check.jsx", title="Subreddit Vibe Check", tag="Data viz + sentiment analysis", art=art_vibe,
         desc="A sentiment-analysis dashboard that analyzes Reddit post titles, classifies community mood, highlights positive and negative posts, and visualizes sentiment distributions with interactive charts.",
         tech=["React 19", "JavaScript", "Vite", "AFINN-165 sentiment analysis", "Recharts", "Serverless API"], out="project-4-vibecheck.svg"),
    dict(n=5, file="VibeBooth.jsx", title="VibeBooth", tag="Computer vision, creative UI", art=art_booth,
         desc="An interactive digital photobooth with camera capture, face detection, aesthetic filters, customizable photo strips, date stamps, and downloadable photo memories.",
         tech=["React 18", "JavaScript", "Vite", "Tailwind CSS", "MediaPipe Face Mesh"], out="project-5-vibebooth.svg"),
    dict(n=6, file="ai_canvas.js", title="AI Canvas", tag="Hands-free gesture drawing", art=art_canvas,
         desc="A browser-based, hands-free drawing application that uses webcam input and hand gesture recognition to draw on a digital canvas, with pinch gestures controlling strokes.",
         tech=["JavaScript", "HTML5 Canvas", "MediaPipe Tasks Vision", "WebRTC camera access", "Real-time gesture recognition"], out="project-6-aicanvas.svg"),
]


def card(p, i, total=6):
    lw = 580          # left content max x
    x0 = 28
    lines = textwrap.wrap(p["desc"], 68)
    y_title = 104
    y_desc = 132
    y_after = y_desc + len(lines) * 21
    # chips layout
    chips, cx, cy = "", x0, y_after + 30
    pal = [MAUVE, BLUE, TEAL, PINK, PEACH, LAV, GREEN]
    for k, t in enumerate(p["tech"]):
        cwid = len(t) * 7.1 + 22
        if cx + cwid > lw:
            cx, cy = x0, cy + 30
        c = pal[k % len(pal)]
        chips += (f'<rect x="{cx:.1f}" y="{cy}" width="{cwid:.1f}" height="23" rx="11.5" fill="{c}" fill-opacity="0.13" stroke="{c}" stroke-opacity="0.45"/>'
                  f'<text x="{cx+cwid/2:.1f}" y="{cy+15.5}" font-size="11.5" text-anchor="middle" fill="{c}">{esc(t)}</text>')
        cx += cwid + 8
    y_link = cy + 52
    H = max(y_link + 22, 250)

    body = f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{BASE}" stroke="{SURF0}" stroke-width="1.5">{glow_stroke(SURF0, MAUVE if i % 2 == 0 else BLUE, 7, i * 0.9)}</rect>'
    body += f'<path d="M1 15 a14 14 0 0 1 14 -14 h{W-30} a14 14 0 0 1 14 14 v19 h-{W-2} z" fill="{MANTLE}"/>'
    for k, c in enumerate([RED, YELLOW, GREEN]):
        body += f'<circle cx="{24+k*16}" cy="18" r="5" fill="{c}"/>'
    tw = len(p["file"]) * 7.4 + 34
    body += f'<rect x="82" y="2" width="{tw:.1f}" height="32" fill="{BASE}"/><rect x="82" y="2" width="{tw:.1f}" height="2" fill="{MAUVE}"/>'
    body += f'<text x="98" y="23" font-size="12" fill="{TEXT}">{esc(p["file"])}</text>'
    body += f'<text x="{W-20}" y="23" font-size="12" text-anchor="end" fill="{OVER}">{p["n"]:02d} / {total:02d}</text>'
    # badge
    bt = "// " + p["tag"]
    bw = len(bt) * 7.0 + 22
    body += f'<rect x="{x0}" y="52" width="{bw:.1f}" height="22" rx="11" fill="{GREEN}" fill-opacity="0.13" stroke="{GREEN}" stroke-opacity="0.4"/>'
    body += f'<text x="{x0+bw/2:.1f}" y="67" font-size="11.5" text-anchor="middle" fill="{GREEN}">{esc(bt)}</text>'
    body += f'<text x="{x0}" y="{y_title}" font-size="23" font-weight="700" fill="{TEXT}">{esc(p["title"])}</text>'
    for k, ln in enumerate(lines):
        body += f'<text x="{x0}" y="{y_desc + k*21}" font-size="13" fill="{SUB}">{esc(ln)}</text>'
    body += f'<text x="{x0}" y="{y_after + 17}" font-size="11.5" fill="{OVER}">// tech stack</text>'
    body += chips
    arrow = anim('<animateTransform attributeName="transform" type="translate" values="0 0;4 -3;0 0" dur="1.6s" repeatCount="indefinite"/>')
    body += f'<text x="{x0}" y="{y_link}" font-size="13.5" font-weight="700" fill="{BLUE}">view repository</text>'
    body += f'<line x1="{x0}" y1="{y_link+5}" x2="{x0+15*8.1:.1f}" y2="{y_link+5}" stroke="{BLUE}" stroke-opacity="0.5" stroke-dasharray="2 3"/>'
    body += f'<text x="{x0+15*8.1+8:.1f}" y="{y_link}" font-size="14" font-weight="700" fill="{BLUE}">&gt;<tspan>_</tspan>{arrow}</text>' if False else \
            f'<g>{arrow}<text x="{x0+15*8.1+8:.1f}" y="{y_link}" font-size="14" font-weight="700" fill="{BLUE}">-&gt;</text></g>'
    # art panel
    px, py = 636, (H + 34) / 2 - 84
    clip = f'<clipPath id="ac{i}"><rect width="216" height="168" rx="10"/></clipPath>'
    body += (f'<g transform="translate({px},{py:.1f})"><rect width="216" height="168" rx="10" fill="{MANTLE}" stroke="{SURF0}"/>'
             f'<g clip-path="url(#ac{i})">{p["art"]()}</g></g>')
    return svg(W, H, body, clip)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


write("header.svg", header())
write("title-about.svg", section("cat about.md", "// who is this person"))
write("title-stack.svg", section("./stack --list", "// tools of the trade"))
write("title-projects.svg", section("ls ./projects", "// 6 items"))
write("title-stats.svg", section("git log --stat", "// receipts"))
write("title-connect.svg", section("ping riya", "// let's build something"))
for i, p in enumerate(PROJECTS):
    write(p["out"], card(p, i))
print("ok", OUT)
write("title-snake.svg", section("./snake --eat contributions", "// nom nom nom"))
