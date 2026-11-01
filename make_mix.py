"""Builds mix.wav: the voice placed on the exact timeline, plus calm background music that
automatically dips under the voice. Uses music.mp3 if you upload one, otherwise it composes its own."""
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve, resample_poly

from story import build

SR = 44100
scenes, total = build()
N = int((total + 1.0) * SR)


def resample(x, sr):
    if sr == SR:
        return x
    g = int(np.gcd(SR, sr))
    return resample_poly(x, SR // g, sr // g).astype(np.float32)


def movavg(x, seconds):
    w = max(1, int(seconds * SR))
    c = np.cumsum(np.insert(x.astype(np.float64), 0, 0.0))
    y = (c[w:] - c[:-w]) / w
    pad = len(x) - len(y)
    return np.pad(y, (pad // 2, pad - pad // 2), mode="edge")


# ---------------------------------------------------------------- voice
voice = np.zeros(N, np.float32)
placed = 0
for sc in scenes:
    for ln in sc["lines"]:
        if not os.path.exists(ln["path"]):
            continue
        x, sr = sf.read(ln["path"], dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        x = resample(x, sr)
        s = int(ln["start"] * SR)
        e = min(N, s + len(x))
        if s < N:
            voice[s:e] += x[: e - s]
            placed += 1
print("voice clips placed:", placed)
peak = float(np.abs(voice).max())
if peak > 0:
    voice *= 0.85 / peak


# ---------------------------------------------------------------- music
def add(buf, x, t0):
    s = int(t0 * SR)
    if s >= len(buf):
        return
    e = min(len(buf), s + len(x))
    buf[s:e] += x[: e - s]


def pad_note(f, dur):
    t = np.arange(int(dur * SR)) / SR
    x = sum(np.sin(2 * np.pi * f * (1 + d) * t + ph) for d, ph in ((0, 0.0), (0.003, 1.3), (-0.003, 2.1))) / 3.0
    x = x + 0.25 * np.sin(4 * np.pi * f * t)
    env = np.minimum(1.0, t / 0.7) * np.minimum(1.0, np.maximum(0.0, dur - t) / 0.9)
    return (x * env).astype(np.float32)


def pluck(f, dur):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 3.2) * (1 - np.exp(-t * 90))
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6) + 0.12 * np.sin(6 * np.pi * f * t) * np.exp(-t * 9)
    return (x * env).astype(np.float32)


def compose(n):
    out = np.zeros(n, np.float32)
    beat = 60.0 / 72
    bar = beat * 4
    chords = [
        [130.81, 164.81, 196.00, 246.94],   # Cmaj7
        [110.00, 130.81, 164.81, 196.00],   # Am7
        [87.31, 110.00, 130.81, 164.81],    # Fmaj7
        [98.00, 123.47, 146.83, 196.00],    # G
    ]
    pattern = [0, 2, 1, 3, 2, 3, 1, 2]
    for b in range(int(n / SR / bar) + 2):
        ch = chords[b % 4]
        t0 = b * bar
        for f in ch:
            add(out, pad_note(f, bar + 1.0) * 0.11, t0)
        add(out, pad_note(ch[0] / 2, bar + 0.5) * 0.13, t0)
        for s, k in enumerate(pattern):
            if s in (0, 2, 3, 4, 6, 7):
                add(out, pluck(ch[k] * 2, 1.6) * 0.10, t0 + s * beat / 2)
    ir = np.random.default_rng(1).standard_normal(int(1.8 * SR)) * np.exp(-np.arange(int(1.8 * SR)) / SR * 3.0)
    ir = (ir / np.sqrt((ir ** 2).sum())).astype(np.float32)
    wet = fftconvolve(out, ir, mode="full")[:n].astype(np.float32)
    return out * 0.7 + wet * 0.4


def load_user_music():
    if not os.path.exists("music.mp3"):
        return None
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "music.mp3", "-ar", str(SR), "-ac", "1", "music_tmp.wav"], check=True)
        x, _ = sf.read("music_tmp.wav", dtype="float32")
        while len(x) < N:
            x = np.concatenate([x, x])
        print("using your music.mp3")
        return x[:N]
    except Exception as e:
        print("could not read music.mp3:", e)
        return None


music = load_user_music()
if music is None:
    print("composing background music")
    music = compose(N)
music = music / (np.abs(music).max() + 1e-9) * 0.6
idx = np.arange(N)
music *= np.minimum(1.0, idx / (2.0 * SR)) * np.minimum(1.0, (N - 1 - idx) / (3.0 * SR))

# duck the music while the voice is speaking
active = (movavg(np.abs(voice), 0.12) > 0.012).astype(np.float64)
active = movavg(active, 0.5)
gain = (0.55 - 0.40 * active).astype(np.float32)

mix = voice + music * gain
peak = float(np.abs(mix).max())
if peak > 0.95:
    mix *= 0.95 / peak
sf.write("mix.wav", mix, SR, subtype="PCM_16")
print(f"mix.wav written: {N / SR:.1f}s")
