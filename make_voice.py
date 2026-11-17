"""Makes vo/<scene>_<line>.wav with the Kokoro neural voice (Apache-2.0, no account needed).
Every clip is fitted into its time window from story.py, so the voice always matches the pictures."""
import os
import sys
import urllib.request

import numpy as np
import soundfile as sf

from story import build, VOICE, LANG, SPEED, MAX_SPEED

MODEL, VOICES = "kokoro-v1.0.onnx", "voices-v1.0.bin"
BASES = [
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/",
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/",
]


def fetch(name):
    if os.path.exists(name) and os.path.getsize(name) > 1_000_000:
        return
    for base in BASES:
        try:
            print("downloading", base + name, flush=True)
            urllib.request.urlretrieve(base + name, name)
            if os.path.getsize(name) > 1_000_000:
                return
        except Exception as e:
            print("  failed:", e, flush=True)
    sys.exit("Could not download " + name)


def trim(y, sr, pad=0.03, thr=0.01):
    idx = np.where(np.abs(y) > thr)[0]
    if len(idx) == 0:
        return y.astype(np.float32)
    a = max(0, idx[0] - int(pad * sr))
    b = min(len(y), idx[-1] + int(pad * 2 * sr))
    y = y[a:b].astype(np.float32).copy()
    n = int(0.008 * sr)
    if len(y) > 2 * n:
        y[:n] *= np.linspace(0, 1, n)
        y[-n:] *= np.linspace(1, 0, n)
    return y


fetch(MODEL)
fetch(VOICES)
from kokoro_onnx import Kokoro

kokoro = Kokoro(MODEL, VOICES)
os.makedirs("vo", exist_ok=True)
scenes, _ = build()
count, tight = 0, []
for sc in scenes:
    for i, ln in enumerate(sc["lines"]):
        speed = SPEED
        for attempt in range(3):
            samples, sr = kokoro.create(ln["spoken"], voice=VOICE, speed=speed, lang=LANG)
            y = trim(samples, sr)
            dur = len(y) / sr
            if dur <= ln["win"] or speed >= MAX_SPEED:
                break
            speed = min(MAX_SPEED, speed * dur / ln["win"] * 1.03)
        if dur > ln["win"] + 0.05:
            tight.append((sc["id"], i, round(dur, 2), round(ln["win"], 2)))
        sf.write(os.path.join("vo", f'{sc["id"]}_{i}.wav'), y, sr, subtype="PCM_16")
        count += 1
        print(f'{sc["id"]}_{i}: {dur:4.1f}s of {ln["win"]:4.1f}s (speed {speed:.2f})  {ln["spoken"][:55]}', flush=True)
print("voice clips made:", count)
if tight:
    print("WARNING, these lines are longer than their window (they will be cut at the window end):", tight)
