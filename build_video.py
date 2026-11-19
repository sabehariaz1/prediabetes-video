#!/usr/bin/env python3
"""
Prediabetes explainer video builder.

Pipeline (runs on GitHub Actions or locally):
  1. Voiceover  - natural neural voice (edge-tts) per scene, OR your own recordings
                  placed in video-src/voiceover/<scene-id>.mp3|wav|m4a
  2. Music      - original, royalty-free soft uplifting track synthesised in code
  3. Visuals    - supersampled (anti-aliased) animation drawn with Pillow, 1920x1080 @ 30 fps
  4. Mix + mux  - music ducks under the voice, loudness normalised, H.264 + AAC MP4

Environment options (all optional):
  TTS_VOICE   comma list of voices to try   (default en-US-AvaNeural,en-US-AndrewNeural,en-GB-SoniaNeural)
  TTS_RATE    speaking rate                 (default -6%)
  PREVIEW=1   fast low-res preview render
  DRY_RUN=1   no internet needed: placeholder silence instead of TTS (for testing only)
  OUT_FILE    output path                   (default ../prediabetes-explainer.mp4)
"""
import asyncio
import glob
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("OUT_FILE", HERE.parent / "prediabetes-explainer.mp4"))
WORK = HERE / "build"
WORK.mkdir(exist_ok=True)

PREVIEW = os.environ.get("PREVIEW") == "1"
DRY_RUN = os.environ.get("DRY_RUN") == "1"
W, H = (960, 540) if PREVIEW else (1920, 1080)
FPS = 15 if PREVIEW else 30
SS = 2                      # supersampling factor (anti-aliasing)
K = W * SS / 1920.0         # design-units (1920x1080) -> canvas pixels
SR = 44100

VOICES = os.environ.get("TTS_VOICE", "en-US-AvaNeural,en-US-AndrewNeural,en-GB-SoniaNeural").split(",")
RATE = os.environ.get("TTS_RATE", "-6%")

# ---------------------------------------------------------------- colours
BGC = (11, 34, 58)
WHITE = (255, 255, 255)
INK = (8, 22, 42)
TEAL = (46, 196, 182)
AMBER = (255, 183, 3)
CORAL = (239, 71, 111)
GREEN = (6, 214, 160)
MUTED = (150, 175, 200)


def mix(col, a=1.0, bg=BGC):
    a = max(0.0, min(1.0, a))
    return tuple(int(bg[i] + (col[i] - bg[i]) * a) for i in range(3))


def clamp01(x):
    return max(0.0, min(1.0, x))


def seg(t, a, b):
    return clamp01((t - a) / (b - a)) if b > a else 1.0


def ease_out(x):
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp01(x)
    return x * x * x * (x * (x * 6 - 15) + 10)


# ---------------------------------------------------------------- fonts
def _find_font(bold):
    names = ["OpenSans-Bold.ttf", "OpenSans-Semibold.ttf"] if bold else ["OpenSans-Regular.ttf"]
    names += ["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]
    for n in names:
        for root in ("/usr/share/fonts", "/usr/local/share/fonts", str(Path.home() / ".fonts")):
            hits = glob.glob(f"{root}/**/{n}", recursive=True)
            if hits:
                return hits[0]
    return None


_FONT_PATH = {False: _find_font(False), True: _find_font(True)}
_FONT_CACHE = {}


def font(size, bold=False):
    key = (round(size * K), bold)
    if key not in _FONT_CACHE:
        p = _FONT_PATH[bold]
        _FONT_CACHE[key] = ImageFont.truetype(p, key[0]) if p else ImageFont.load_default()
    return _FONT_CACHE[key]


def tw(s, size, bold=False):
    return font(size, bold).getlength(s) / K


def px(v):
    return v * K


# ---------------------------------------------------------------- drawing helpers
def rr(d, x, y, w, h, r, fill, corners=None):
    if w < 1 or h < 1:
        return
    r = min(r, w / 2, h / 2)
    d.rounded_rectangle([px(x), px(y), px(x + w), px(y + h)], radius=px(r), fill=fill,
                        corners=corners)


def circle(d, cx, cy, r, fill=None, outline=None, width=0):
    if r <= 0:
        return
    d.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], fill=fill, outline=outline,
              width=max(0, int(px(width))))


def T(d, s, x, y, size, col=WHITE, bold=False, a=1.0, anchor="l"):
    if a <= 0.02:
        return
    d.text((px(x), px(y)), s, font=font(size, bold), fill=mix(col, a),
           anchor={"l": "ls", "c": "ms", "r": "rs"}[anchor])


def wrap(s, size, bold, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if tw(trial, size, bold) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def ring(d, cx, cy, R, lw, frac, col, a=1.0):
    ro = R + lw / 2
    box = [px(cx - ro), px(cy - ro), px(cx + ro), px(cy + ro)]
    d.arc(box, 0, 360, fill=mix(WHITE, 0.09), width=int(px(lw)))
    if frac < 0.004:
        return
    end = -90 + 360 * min(frac, 1.0)
    gl = lw + 30
    gro = R + gl / 2
    d.arc([px(cx - gro), px(cy - gro), px(cx + gro), px(cy + gro)], -90, end,
          fill=mix(col, 0.17 * a), width=int(px(gl)))
    d.arc(box, -90, end, fill=mix(col, a), width=int(px(lw)))
    circle(d, cx, cy - R, lw / 2, fill=mix(col, a))
    ang = math.radians(end)
    circle(d, cx + R * math.cos(ang), cy + R * math.sin(ang), lw / 2, fill=mix(col, a))


def check(d, cx, cy, s, p, col, width=12):
    pts = [(cx - 0.45 * s, cy + 0.02 * s), (cx - 0.1 * s, cy + 0.38 * s), (cx + 0.5 * s, cy - 0.36 * s)]
    p0, p1 = clamp01(p * 2), clamp01(p * 2 - 1)
    path = [pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * p0, pts[0][1] + (pts[1][1] - pts[0][1]) * p0)]
    if p1 > 0:
        path.append((pts[1][0] + (pts[2][0] - pts[1][0]) * p1, pts[1][1] + (pts[2][1] - pts[1][1]) * p1))
    d.line([(px(x), px(y)) for x, y in path], fill=col, width=int(px(width)), joint="curve")
    for x, y in (path[0], path[-1]):
        circle(d, x, y, width / 2, fill=col)


def person(d, cx, cy, col, q=False):
    circle(d, cx, cy - 78, 32, fill=col)
    rr(d, cx - 46, cy - 36, 92, 128, 46, col, corners=(True, True, False, False))
    if q:
        T(d, "?", cx, cy - 64, 44, INK, True, 1, "c")


# ---------------------------------------------------------------- background
def make_background():
    w, h = 960, 540
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u, v = xx / w, yy / h
    g = (u * 0.55 + v * 0.45)[..., None]
    c0 = np.array([7, 18, 40], np.float32)
    c1 = np.array([12, 58, 80], np.float32)
    img = c0 + (c1 - c0) * g

    def glow(cx, cy, rad, col, amt):
        dd = np.sqrt(((u - cx) * 1.78) ** 2 + (v - cy) ** 2) / rad
        return np.clip(1 - dd, 0, 1)[..., None] ** 2 * np.array(col, np.float32) * amt

    img += glow(0.85, 0.15, 0.55, (46, 196, 182), 0.20)
    img += glow(0.10, 0.95, 0.60, (90, 80, 200), 0.18)
    vig = 1 - 0.35 * (((u - 0.5) ** 2 + (v - 0.5) ** 2) * 2.2)[..., None]
    img *= vig
    img += np.random.default_rng(1).normal(0, 0.8, img.shape)  # dither (kills banding)
    small = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    return small.resize((W * SS, H * SS), Image.BICUBIC)


PARTICLES = [(((i * 211) % 1900) + 10, ((i * 137) % 1000) + 40, 3 + (i % 4) * 2, 8 + (i % 5) * 5) for i in range(22)]


def draw_particles(d, T_):
    for i, (x0, y0, r, sp) in enumerate(PARTICLES):
        x = (x0 + T_ * sp) % 1960 - 20
        y = y0 + math.sin(T_ * 0.5 + i) * 18
        circle(d, x, y, r, fill=mix(TEAL if i % 3 else WHITE, 0.14))


def draw_title(d, kicker, title, t):
    a = ease_out(seg(t, 0.15, 0.85))
    T(d, kicker, 120, 112, 26, TEAL, True, a)
    T(d, title, 120, 190 + (1 - a) * 24, 66, WHITE, True, a)


# ---------------------------------------------------------------- scenes
def sc_hook(d, t, S):
    draw_title(d, "PREDIABETES RISK CALCULATOR", "Your score is the starting point", t)
    cx, cy, R = 960, 500, 200
    e = ease_io(seg(t, 0.4, 2.2))
    ring(d, cx, cy, R, 30, e, CORAL)
    T(d, "YOUR RISK SCORE", cx, cy - 118, 28, MUTED, True, ease_out(seg(t, 0.3, 1.0)), "c")
    n = int(round(5 * e))
    T(d, f"{n}+" if e >= 0.999 else str(n), cx, cy + 82, 200, WHITE, True, 1, "c")
    if t > 2.3:
        ph = ((t - 2.3) % 1.8) / 1.8
        ro = R + 15 + 15 + 70 * ph
        d.ellipse([px(cx - ro), px(cy - ro), px(cx + ro), px(cy + ro)],
                  outline=mix(CORAL, 0.55 * (1 - ph)), width=int(px(4)))
    a = ease_out(seg(t, 2.4, 3.1))
    rr(d, 960 - 590, 766 + (1 - a) * 20, 1180, 88, 44, mix(CORAL, a))
    T(d, "5 or higher = HIGH RISK of prediabetes", 960, 826 + (1 - a) * 20, 42, WHITE, True, a, "c")


def sc_what(d, t, S):
    draw_title(d, "THE BASICS", "What is prediabetes?", t)
    x0, tot, y, h = 160, 1600, 430, 96
    ws = [0.4, 0.3, 0.3]
    cols = [GREEN, AMBER, CORAL]
    names = ["Normal", "Prediabetes", "Type 2 diabetes"]
    r = ease_io(seg(t, 0.3, 1.6))
    xs, cx_ = [], x0
    for wf in ws:
        xs.append((cx_, wf * (tot - 20)))
        cx_ += wf * (tot - 20) + 10
    for (sx, sw), col, nm in zip(xs, cols, names):
        vis = clamp01((x0 + tot * r - sx) / sw)
        rr(d, sx, y, sw * vis, h, 22, col)
        T(d, nm, sx + sw / 2, y + h + 60, 36, WHITE, True, r, "c")
    T(d, "BLOOD SUGAR LEVEL  →", x0, y - 40, 26, MUTED, True, r)
    m = ease_io(seg(t, 2.6, 4.4))
    mx = (xs[0][0] + xs[0][1] / 2) * (1 - m) + (xs[1][0] + xs[1][1] / 2) * m
    ma = ease_out(seg(t, 2.2, 2.8))
    pulse = 1 + 0.08 * math.sin(t * 5)
    circle(d, mx, y - 70, 30 * pulse, fill=mix(WHITE, 0.15 * ma))
    d.polygon([(px(mx - 18), px(y - 52)), (px(mx + 18), px(y - 52)), (px(mx), px(y - 18))], fill=mix(WHITE, ma))
    circle(d, mx, y - 78, 20, fill=mix(WHITE, ma))
    a = ease_out(seg(t, 4.0, 4.8))
    T(d, "Blood sugar is higher than normal,", 960, 700, 46, WHITE, True, a, "c")
    T(d, "but not yet in the diabetes range.", 960, 760, 46, AMBER, True, a, "c")
    b = ease_out(seg(t, 7.5, 8.3))
    T(d, "Think of it as a warning light, while you can still act.", 960, 835, 34, MUTED, False, b, "c")


def sc_silent(d, t, S):
    draw_title(d, "WHY SCREENING MATTERS", "Prediabetes is usually silent", t)
    base_y = 520
    for i in range(10):
        cx = 960 + (i - 4.5) * 150
        a = ease_out(seg(t, 0.3 + i * 0.1, 0.9 + i * 0.1))
        unaware = i < 8
        flip = ease_out(seg(t, 2.0 + i * 0.25, 2.5 + i * 0.25)) if unaware else 0
        col = tuple(int(TEAL[k] * (1 - flip) + AMBER[k] * flip) for k in range(3))
        person(d, cx, base_y + (1 - a) * 30, mix(col, a), q=flip > 0.6)
    a = ease_out(seg(t, 4.6, 5.4))
    T(d, "About 8 in 10 adults with prediabetes", 960, 745, 50, WHITE, True, a, "c")
    T(d, "don't know they have it", 960, 808, 50, AMBER, True, a, "c")
    T(d, "Source: CDC, National Diabetes Statistics Report", 960, 858, 24, MUTED, False, a * 0.9, "c")


TESTS = [
    ("Fasting glucose", "no food for at least 8 hours",
     ["Below 100 mg/dL", "100–125 mg/dL", "126 mg/dL or higher"],
     ["(below 5.6 mmol/L)", "(5.6–6.9 mmol/L)", "(7.0 mmol/L or higher)"]),
    ("A1C", "average blood sugar over about 3 months",
     ["Below 5.7%", "5.7–6.4%", "6.5% or higher"],
     ["(below 39 mmol/mol)", "(39–47 mmol/mol)", "(48 mmol/mol or higher)"]),
    ("2-hour glucose tolerance test", "after a 75 g glucose drink",
     ["Below 140 mg/dL", "140–199 mg/dL", "200 mg/dL or higher"],
     ["(below 7.8 mmol/L)", "(7.8–11.0 mmol/L)", "(11.1 mmol/L or higher)"]),
]


def sc_tests(d, t, S):
    draw_title(d, "SOURCE: ADA STANDARDS OF CARE IN DIABETES, 2026", "Three blood tests, three ranges", t)
    cols = [GREEN, AMBER, CORAL]
    cats = ["NORMAL", "PREDIABETES", "DIABETES"]
    txtcol = [INK, INK, WHITE]
    gap = 14
    segw = (1600 - 2 * gap) / 3
    for i, (name, sub, vals, mm) in enumerate(TESTS):
        y0 = 262 + i * 212
        st = 0.5 + i * (S["dur"] - 3.0) * 0.31
        a = ease_out(seg(t, st, st + 0.6))
        T(d, name, 160, y0, 38, WHITE, True, a)
        T(d, sub, 160 + tw(name, 38, True) + 24, y0, 26, MUTED, False, a)
        for j in range(3):
            sx = 160 + j * (segw + gap)
            g = ease_io(seg(t, st + 0.2 + j * 0.25, st + 0.9 + j * 0.25))
            rr(d, sx, y0 + 20, segw * g, 54, 14, cols[j])
            if g > 0.98:
                T(d, cats[j], sx + segw / 2, y0 + 56, 26, txtcol[j], True, 1, "c")
            la = ease_out(seg(t, st + 0.7 + j * 0.25, st + 1.3 + j * 0.25))
            T(d, vals[j], sx + segw / 2, y0 + 116, 36, WHITE, True, la, "c")
            T(d, mm[j], sx + segw / 2, y0 + 152, 26, MUTED, False, la, "c")


def sc_calc(d, t, S):
    draw_title(d, "HOW THE CALCULATOR WORKS", "Six questions. One score.", t)
    for i in range(6):
        cx = 960 + (i - 2.5) * 240
        a = ease_out(seg(t, 0.4 + i * 0.12, 1.0 + i * 0.12))
        circle(d, cx, 410, 66, fill=mix(WHITE, 0.07 * a), outline=mix(TEAL, a), width=5)
        p = ease_out(seg(t, 1.2 + i * 0.5, 1.8 + i * 0.5))
        if p > 0:
            check(d, cx, 410, 80, p, mix(TEAL, 1))
        T(d, f"Question {i + 1}", cx, 530, 28, MUTED, True, a, "c")
    a = ease_out(seg(t, 4.6, 5.4))
    rr(d, 960 - 560, 620 + (1 - a) * 24, 1120, 190, 36, mix(WHITE, 0.07 * a))
    T(d, "Score of 5 or higher", 960, 710 + (1 - a) * 24, 62, CORAL, True, a, "c")
    T(d, "means several common risk factors are present", 960, 775 + (1 - a) * 24, 36, WHITE, False, a, "c")


def sc_dpp(d, t, S):
    draw_title(d, "THE GOOD NEWS", "Lifestyle changes work", t)
    cx, cy, R = 520, 540, 200
    e = ease_io(seg(t, 0.5, 3.0))
    ring(d, cx, cy, R, 34, 0.58 * e, GREEN)
    T(d, f"{int(round(58 * e))}%", cx, cy + 40, 130, WHITE, True, 1, "c")
    T(d, "lower risk", cx, cy + 100, 34, GREEN, True, ease_out(seg(t, 2.6, 3.4)), "c")
    items = [
        ("About 7% weight loss", "Diabetes Prevention Program lifestyle goal", GREEN),
        ("150 minutes of activity a week", "For example, brisk walking", TEAL),
        ("3,234 adults with prediabetes", "Randomised trial, NEJM 2002 (metformin: 31% lower)", AMBER),
    ]
    for i, (a1, a2, col) in enumerate(items):
        a = ease_out(seg(t, 3.0 + i * 0.9, 3.8 + i * 0.9))
        y = 340 + i * 170 + (1 - a) * 30
        rr(d, 900, y, 880, 130, 26, mix(WHITE, 0.07 * a))
        rr(d, 900, y, 12, 130, 6, mix(col, a))
        T(d, a1, 945, y + 58, 38, WHITE, True, a)
        T(d, a2, 945, y + 98, 26, MUTED, False, a)


def sc_steps(d, t, S):
    draw_title(d, "WHAT YOU CAN DO", "Start small, start now", t)
    cards = [
        ("150", "minutes of brisk walking each week", GREEN),
        ("Swap", "sugary drinks and sweets for vegetables, whole grains and lean protein", TEAL),
        ("7–9", "hours of sleep a night, and ways to manage stress", AMBER),
        ("Test", "ask your doctor about an A1C or fasting glucose test", CORAL),
    ]
    cw, gap = 390, 40
    x0 = (1920 - (4 * cw + 3 * gap)) / 2
    for i, (big, txt, col) in enumerate(cards):
        a = ease_out(seg(t, 0.5 + i * 0.55, 1.2 + i * 0.55))
        x, y = x0 + i * (cw + gap), 290 + (1 - a) * 50
        rr(d, x, y, cw, 470, 30, mix(WHITE, 0.07 * a))
        rr(d, x, y, cw, 14, 7, mix(col, a))
        T(d, big, x + cw / 2, y + 170, 100, col, True, a, "c")
        for k, ln in enumerate(wrap(txt, 32, False, cw - 60)):
            T(d, ln, x + cw / 2, y + 250 + k * 46, 32, WHITE, False, a, "c")


REFS = [
    "American Diabetes Association. Diagnosis and Classification of Diabetes: Standards of Care in Diabetes—2026. Diabetes Care 2026;49(Suppl 1).",
    "Knowler WC et al. Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. N Engl J Med 2002;346:393–403.",
    "Bang H et al. Development and validation of a patient self-assessment score for diabetes risk. Ann Intern Med 2009;151:775–783.",
    "Centers for Disease Control and Prevention. National Diabetes Statistics Report, 2024.",
]


def sc_outro(d, t, S):
    a = ease_out(seg(t, 0.3, 1.1))
    T(d, "KEY MESSAGE", 960, 150, 26, TEAL, True, a, "c")
    T(d, "Know your score. Talk to your doctor.", 960, 250, 76, WHITE, True, a, "c")
    b = ease_out(seg(t, 1.2, 2.0))
    T(d, "Score of 5 or higher? Ask about an A1C or fasting glucose test.", 960, 325, 36, AMBER, True, b, "c")
    c_ = ease_out(seg(t, 2.2, 3.0))
    T(d, "REFERENCES", 160, 430, 24, TEAL, True, c_)
    y = 470
    for i, r in enumerate(REFS):
        for k, ln in enumerate(wrap(f"{i + 1}. {r}", 24, False, 1600)):
            T(d, ln, 160, y, 24, WHITE, False, c_ * 0.9)
            y += 34
        y += 8
    T(d, "Educational video for community awareness. Not a diagnosis or medical advice.", 960, 850, 26, MUTED, False, c_, "c")


SCENES = {"hook": sc_hook, "what": sc_what, "silent": sc_silent, "tests": sc_tests,
          "calc": sc_calc, "dpp": sc_dpp, "steps": sc_steps, "outro": sc_outro}


# ---------------------------------------------------------------- captions
def caption_chunks(text):
    chunks = []
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        if len(s) <= 105:
            chunks.append(s)
        else:
            k = math.ceil(len(s) / 95)
            words = s.split()
            per = math.ceil(len(words) / k)
            chunks += [" ".join(words[i:i + per]) for i in range(0, len(words), per)]
    return chunks


def draw_caption(d, S, t):
    tv = t - S["lead"]
    if tv < 0 or tv > S["vlen"] + 0.2:
        return
    chunks = S["chunks"]
    total = sum(len(c) for c in chunks)
    acc, cur = 0, chunks[-1]
    for c in chunks:
        if tv <= (acc + len(c)) / total * S["vlen"]:
            cur = c
            break
        acc += len(c)
    lines = wrap(cur, 40, False, 1500)
    bh = len(lines) * 54 + 34
    y_top = 1030 - bh
    wmax = max(tw(l, 40) for l in lines) + 80
    rr(d, 960 - wmax / 2, y_top, wmax, bh, 28, mix(INK, 0.78))
    for i, l in enumerate(lines):
        T(d, l, 960, y_top + 56 + i * 54, 40, WHITE, False, 1, "c")


# ---------------------------------------------------------------- audio
async def _tts(text, voice, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=RATE).save(str(path))


def write_wav(path, data, channels=1):
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def get_voice(scene):
    for ext in (".mp3", ".wav", ".m4a"):
        p = HERE / "voiceover" / (scene["id"] + ext)
        if p.exists():
            print(f"  using your recording: {p.name}")
            return p
    out = WORK / f"{scene['id']}.mp3"
    if DRY_RUN:
        secs = len(scene["narration"].split()) * 0.38
        out = WORK / f"{scene['id']}.wav"
        write_wav(out, np.zeros(int(secs * SR)))
        return out
    last = None
    for attempt in range(3):
        for v in VOICES:
            try:
                asyncio.run(_tts(scene["narration"], v.strip(), out))
                if out.exists() and out.stat().st_size > 2000:
                    print(f"  voice {v.strip()} ok")
                    return out
            except Exception as e:  # network hiccup / voice unavailable -> next voice
                last = e
                print(f"  voice {v} failed: {e}")
    sys.exit(f"TTS failed for scene {scene['id']}: {last}\n"
             "Tip: record your own voice into video-src/voiceover/<scene-id>.mp3 and re-run.")


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


def mavg(x, w):
    pad = np.pad(x, (w // 2, w - w // 2), mode="edge")
    c = np.concatenate([[0.0], np.cumsum(pad, dtype=np.float64)])
    return ((c[w:] - c[:-w]) / w)[:len(x)].astype(np.float32)


def make_music(total):
    n = int((total + 1) * SR)
    bpm = 92
    beat = 60 / bpm
    bar = 4 * beat
    f = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]  # C G Am F
    music = np.zeros(n, np.float32)
    nb = int(total / bar) + 2
    for b in range(nb):
        ch = chords[b % 4]
        s = int(b * bar * SR)
        m = min(n - s, int((bar + 0.9) * SR))
        if m <= 0:
            break
        tt = np.arange(m) / SR
        env = np.clip(tt / 0.7, 0, 1) * np.clip((bar + 0.9 - tt) / 0.9, 0, 1)
        pad = np.zeros(m, np.float32)
        for note in ch[:3]:
            for det in (0.997, 1.0, 1.003):
                pad += np.sin(2 * np.pi * f(note) * det * tt).astype(np.float32) * 0.045
        bass = np.sin(2 * np.pi * f(ch[0] - 24) * tt) * 0.16
        music[s:s + m] += (pad + bass.astype(np.float32)) * env.astype(np.float32)
        pattern = [0, 1, 2, 3, 2, 1, 2, 3]
        build = 0.55 + 0.45 * min(1, (b * bar) / max(total, 1))
        for k, idx in enumerate(pattern):
            ps = s + int(k * beat / 2 * SR)
            pl = min(n - ps, int(1.1 * SR))
            if pl <= 0:
                continue
            pt = np.arange(pl) / SR
            fr = f(ch[idx] + 12)
            pluck = (np.sin(2 * np.pi * fr * pt) + 0.3 * np.sin(2 * np.pi * 2 * fr * pt)) * np.exp(-pt * 5.5)
            pluck *= np.clip(pt / 0.004, 0, 1)
            music[ps:ps + pl] += (pluck * 0.07 * build).astype(np.float32)
    # reverb via synthetic impulse response (FFT convolution)
    rng = np.random.default_rng(7)
    irn = int(1.6 * SR)
    ir = rng.normal(0, 1, irn) * np.exp(-np.arange(irn) / SR / 0.45)
    ir /= np.sqrt((ir ** 2).sum())
    nfft = 1 << int(np.ceil(np.log2(n + irn)))
    wet = np.fft.irfft(np.fft.rfft(music, nfft) * np.fft.rfft(ir, nfft), nfft)[:n].astype(np.float32)
    music = music * 0.7 + wet * 0.45
    music *= np.clip(np.arange(n) / SR / 2.0, 0, 1)
    music *= np.clip((n - np.arange(n)) / SR / 3.0, 0, 1)
    return music / (np.abs(music).max() + 1e-9) * 0.9


def build_audio(scenes, total):
    n = int((total + 1) * SR)
    voice = np.zeros(n, np.float32)
    for S in scenes:
        a = S["audio"]
        rms = np.sqrt(np.mean(a ** 2)) + 1e-9
        a = np.tanh(a * (0.10 / rms) * 1.2) / 1.2
        s = int((S["start"] + S["lead"]) * SR)
        voice[s:s + len(a)] += a[:max(0, n - s)]
    music = make_music(total)
    act = np.clip(mavg(np.abs(voice), int(0.3 * SR)) / 0.03, 0, 1)
    duck = 1 - 0.55 * mavg(act, int(0.5 * SR))
    mixd = voice + music * 0.20 * duck
    path = WORK / "mix.wav"
    write_wav(path, np.repeat(mixd[:, None], 2, axis=1).reshape(-1), channels=2)
    return path


# ---------------------------------------------------------------- main
def main():
    scenes = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
    print("Step 1/3: voiceover")
    t0 = 0.0
    for i, S in enumerate(scenes):
        print(f" scene {S['id']}")
        S["audio"] = decode(get_voice(S))
        S["vlen"] = len(S["audio"]) / SR
        S["lead"] = 0.9 if i == 0 else 0.7
        S["tail"] = 2.8 if i == len(scenes) - 1 else 0.8
        S["dur"] = S["lead"] + S["vlen"] + S["tail"]
        S["start"] = t0
        S["chunks"] = caption_chunks(S["narration"])
        t0 += S["dur"]
    total = t0
    print(f"Total length: {total:.1f}s")

    print("Step 2/3: music + mix")
    wav = build_audio(scenes, total)

    print("Step 3/3: rendering frames")
    bg4 = make_background()
    bg1 = bg4.reduce(SS)
    nframes = int(round(total * FPS))
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", str(wav), "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium" if not PREVIEW else "veryfast", "-crf", "17" if not PREVIEW else "26",
           "-pix_fmt", "yuv420p", "-profile:v", "high",
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
           "-movflags", "+faststart", "-t", f"{total:.3f}", str(OUT)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    si = 0
    for fr in range(nframes):
        Tm = fr / FPS
        while si < len(scenes) - 1 and Tm >= scenes[si]["start"] + scenes[si]["dur"]:
            si += 1
        S = scenes[si]
        t = Tm - S["start"]
        canvas = bg4.copy()
        d = ImageDraw.Draw(canvas)
        draw_particles(d, Tm)
        SCENES[S["id"]](d, t, S)
        draw_caption(d, S, t)
        # progress bar
        rr(d, 0, 1074, 1920 * Tm / total, 6, 0, mix(TEAL, 0.9))
        img = canvas.reduce(SS)
        fade = min(ease_out(t / 0.5), ease_out((S["dur"] - t) / 0.45))
        if fade < 0.999:
            img = Image.blend(bg1, img, fade)
        proc.stdin.write(img.tobytes())
        if fr % 300 == 0:
            print(f"  frame {fr}/{nframes}", flush=True)
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"Done -> {OUT}")


if __name__ == "__main__":
    main()
