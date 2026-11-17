"""
Narration, cue times and timeline. ONE source of truth for the voice, the audio mix and the video.
Total length is fixed at exactly 120.0 seconds.
Each line is (start_time_seconds, spoken_text) or (start_time_seconds, (spoken_text, caption_text)).
A line may run until 0.1 s before the next line; make_voice.py speeds a clip up if it would not fit.
"""
import os
import wave

VOICE = "af_heart"     # warm American woman. Others: af_bella, af_nicole, af_sky, bf_emma (British), am_michael
LANG = "en-us"         # use "en-gb" together with a bf_ or bm_ voice
SPEED = 1.05           # base speaking speed
MAX_SPEED = 1.3        # a line is never sped up beyond this
TOTAL = 120.0
LEAD = 0.12            # pictures start slightly before the voice
RATE_EST = 2.7         # words per second, used only when there is no voice clip yet

SCENES = [
    ("s01", 0.0, 9.7, [
        (0.3, "Around one in eight adults worldwide has prediabetes, and many don't know it."),
        (5.5, "Let's see what raises your risk."),
    ]),
    ("s02", 9.7, 21.1, [
        (10.1, 'Prediabetes means blood sugar that is higher than normal, but not yet diabetes.'),
        (15.2, ('An A one C blood test shows where you stand.', 'An A1C blood test shows where you stand.')),
    ]),
    ("s03", 21.1, 31.5, [
        (21.5, 'Normally, insulin works like a key, letting sugar into your cells for energy.'),
        (26.6, 'When cells stop listening, sugar stays in your blood.'),
    ]),
    ("s04", 31.5, 46.2, [
        (31.9, "Some risks can't be changed."),
        (34.0, ('Your age, especially after forty five.', 'Your age, especially after 45.')),
        (36.5, 'A parent or sibling with type 2 diabetes.'),
        (39.8, 'And background: Middle Eastern, South Asian, African, and Hispanic groups face higher rates.'),
    ]),
    ("s05", 46.2, 61.7, [
        (46.6, 'These you can change.'),
        (48.3, 'Extra weight, especially around the belly.'),
        (50.9, 'Too little activity.'),
        (52.3, 'An unhealthy diet, high in sugar and processed food.'),
        (55.9, 'Smoking.'),
        (57.0, 'And poor sleep.'),
    ]),
    ("s06", 61.7, 79.4, [
        (62.0, 'Health conditions matter too: high blood pressure.'),
        (64.9, 'Unhealthy cholesterol or blood fats.'),
        (67.1, 'A hormone condition in women, called PCOS.'),
        (70.0, 'High blood sugar during pregnancy.'),
        (72.1, 'And heart disease or stroke.'),
        (74.3, 'Risks add up, but high risk is only a warning.'),
    ]),
    ("s07", 79.4, 96.5, [
        (79.7, 'Only a blood test can tell for sure.'),
        (83.0, ('Your doctor may use an A one C test, a fasting blood sugar test, or a glucose tolerance test.', 'Your doctor may use an A1C test, a fasting blood sugar test, or a glucose tolerance test.')),
        (90.3, 'Ask how often you should be screened.'),
    ]),
    ("s08", 96.5, 109.4, [
        (96.9, 'The good news: you can lower your risk.'),
        (100.1, ('Lifestyle changes cut the risk of type 2 diabetes by fifty eight percent.', 'Lifestyle changes cut the risk of type 2 diabetes by 58%.')),
        (105.2, 'Lose weight, move more, eat whole foods.'),
    ]),
    ("s09", 109.4, 120.0, [
        (109.8, 'So take action today.'),
        (111.6, 'Learn your risk, talk to your doctor, and take small steps.'),
        (115.9, 'This video is for education only, not medical advice.'),
    ]),
]


def clip_path(sid, i):
    return os.path.join("vo", f"{sid}_{i}.wav")


def _clip_len(path):
    if os.path.exists(path):
        try:
            with wave.open(path) as w:
                return w.getnframes() / float(w.getframerate())
        except Exception:
            pass
    return None


def build():
    """Returns (scenes, TOTAL). Every start time is absolute, in seconds from the beginning."""
    out = []
    for sid, start, end, lines in SCENES:
        items = []
        for i, (t0, text) in enumerate(lines):
            spoken, shown = text if isinstance(text, tuple) else (text, text)
            nxt = lines[i + 1][0] if i + 1 < len(lines) else end - 0.5
            win = max(0.5, nxt - 0.1 - t0)
            actual = _clip_len(clip_path(sid, i))
            est = max(0.9, len(spoken.split()) / RATE_EST + 0.15)
            items.append(dict(text=shown, spoken=spoken, start=t0, win=win,
                              dur=min(actual if actual else est, win), path=clip_path(sid, i)))
        out.append(dict(id=sid, start=start, end=end, lines=items))
    return out, TOTAL


if __name__ == "__main__":
    scenes, total = build()
    print(f"total {total:.1f}s")
    for s in scenes:
        print(s["id"], f'{s["start"]:.1f} -> {s["end"]:.1f}')
        for i, ln in enumerate(s["lines"]):
            print(f'   [{ln["start"]:6.1f}] window {ln["win"]:4.1f}s  {ln["spoken"]}')
