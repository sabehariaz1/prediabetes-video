"""Makes vo/<scene>_<line>.wav with the Kokoro neural voice (Apache-2.0, no account needed)."""
import os
import sys
import urllib.request

import numpy as np
import soundfile as sf

from story import SCENES, VOICE, LANG, SPEED, spoken

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


def trim(y, sr, pad=0.04, thr=0.01):
    idx = np.where(np.abs(y) > thr)[0]
    if len(idx) == 0:
        return y
    a = max(0, idx[0] - int(pad * sr))
    b = min(len(y), idx[-1] + int(pad * 2 * sr))
    y = y[a:b].astype(np.float32).copy()
    n = int(0.005 * sr)
    if len(y) > 2 * n:
        y[:n] *= np.linspace(0, 1, n)
        y[-n:] *= np.linspace(1, 0, n)
    return y


fetch(MODEL)
fetch(VOICES)
from kokoro_onnx import Kokoro

kokoro = Kokoro(MODEL, VOICES)
os.makedirs("vo", exist_ok=True)
count = 0
for sid, lines in SCENES:
    for i, line in enumerate(lines):
        text = spoken(line)
        samples, sr = kokoro.create(text, voice=VOICE, speed=SPEED, lang=LANG)
        sf.write(os.path.join("vo", f"{sid}_{i}.wav"), trim(samples, sr), sr, subtype="PCM_16")
        count += 1
        print(f"{sid}_{i}: {text[:60]}", flush=True)
print("voice clips made:", count)
