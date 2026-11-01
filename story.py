"""
One place for the narration and the timeline.
Each line is a string, or a pair (spoken text, caption text).
The video, the voice clips and the audio mix all use this same timeline,
so pictures and sound stay locked together.
"""
import os
import wave

VOICE = "af_heart"     # warm American woman. Others: af_bella, af_nicole, af_sky, bf_emma (British), am_michael
LANG = "en-us"         # use "en-gb" together with a bf_ or bm_ voice
SPEED = 1.0            # 1.05 = a little faster (shorter video), 0.95 = slower

LINE_GAP = 0.28        # silence after each sentence
SCENE_LEAD = 0.45      # title animates in before the first sentence
SCENE_GAP = 0.45       # fade-out time after the last sentence
INTRO_PAD = 0.3
OUTRO_PAD = 1.2
LEAD = 0.12            # pictures start slightly before the voice

SCENES = [
    ("s01", [
        "Imagine a condition that affects more than two in five adults in the United States.",
        "And about eight in ten of them have no idea.",
        "It's called prediabetes, and it often causes no symptoms at all.",
        "So let's find out what raises your risk, and what you can do about it.",
    ]),
    ("s02", [
        "Prediabetes means your blood sugar is higher than normal, but not yet high enough to be called diabetes.",
        ("A common blood test, the A one C, shows where you stand.", "A common blood test, the A1C, shows where you stand."),
        ("Below five point seven percent is normal.", "Below 5.7% is normal."),
        ("Five point seven to six point four percent is prediabetes.", "5.7% to 6.4% is prediabetes."),
        ("And six point five percent or higher is diabetes.", "And 6.5% or higher is diabetes."),
    ]),
    ("s03", [
        "So what is happening inside the body?",
        "Normally, insulin works like a key. It lets sugar move from your blood into your cells for energy.",
        "With insulin resistance, your cells stop responding well.",
        "The sugar stays in your blood, and your blood sugar rises.",
    ]),
    ("s04", [
        "Some risk factors are out of your control.",
        ("Your risk rises with age, especially after forty five.", "Your risk rises with age, especially after 45."),
        "Having a parent or sibling with type 2 diabetes raises it too.",
        "And some ethnic groups, including Black, Hispanic, Asian, Native American, and Pacific Islander communities, have higher rates.",
    ]),
    ("s05", [
        "Other risk factors come from daily life, and these are the ones you can change.",
        "Carrying extra weight, especially around the belly.",
        "Being physically inactive.",
        "Eating lots of sugary drinks and processed foods.",
        "Smoking.",
        "And not getting enough good sleep.",
    ]),
    ("s06", [
        "Certain health conditions also raise your risk.",
        "High blood pressure.",
        "Abnormal cholesterol, like low good cholesterol or high triglycerides.",
        "Polycystic ovary syndrome.",
        "Diabetes during a past pregnancy, called gestational diabetes.",
        "And a history of heart disease or stroke.",
    ]),
    ("s07", [
        "These risk factors add up.",
        "Family history.",
        "Inactivity.",
        "Extra weight.",
        "Unhealthy eating.",
        "The more you have, the higher your chance of developing prediabetes, and later, type 2 diabetes.",
        "But a high risk is a warning, not a diagnosis.",
    ]),
    ("s08", [
        "Let's try a quick self check.",
        ("Are you over forty five?", "Are you over 45?"),
        "Does a parent or sibling have type 2 diabetes?",
        "Are you inactive, or carrying extra weight?",
        "Every yes adds to your risk.",
        "If you said yes more than once, it's worth talking to your doctor.",
    ]),
    ("s09", [
        "The only way to know for sure is a blood test.",
        ("Your doctor can use an A one C test.", "Your doctor can use an A1C test."),
        "A fasting glucose test.",
        "Or a glucose tolerance test.",
        "If you have risk factors, ask how often you should be screened.",
    ]),
    ("s10", [
        "Now, the good news.",
        ("In a large study called the Diabetes Prevention Program, lifestyle changes lowered the risk of type 2 diabetes by fifty eight percent.",
         "In a large study called the Diabetes Prevention Program, lifestyle changes lowered the risk of type 2 diabetes by 58%."),
        ("Losing five to seven percent of your body weight.", "Losing 5 to 7% of your body weight."),
        ("Getting about one hundred fifty minutes of activity a week.", "Getting about 150 minutes of activity a week."),
        "And eating more whole foods.",
    ]),
    ("s11", [
        "So take action today.",
        "Learn your risk factors.",
        "Talk to your doctor about a blood test.",
        "Move more, eat well, and sleep well.",
        "Small steps now can protect your health for years.",
        "This video is for education only, and is not medical advice.",
    ]),
]


def spoken(line):
    return line[0] if isinstance(line, tuple) else line


def shown(line):
    return line[1] if isinstance(line, tuple) else line


def clip_path(sid, i):
    return os.path.join("vo", f"{sid}_{i}.wav")


def clip_len(sid, i, text):
    p = clip_path(sid, i)
    if os.path.exists(p):
        try:
            with wave.open(p) as w:
                return w.getnframes() / float(w.getframerate())
        except Exception:
            pass
    return 0.40 * len(text.split()) + 0.5      # estimate when there is no voice clip


def build():
    """Returns (scenes, total_seconds). Every start time is absolute."""
    t = INTRO_PAD
    out = []
    for sid, lines in SCENES:
        scene_start = t
        t += SCENE_LEAD
        items = []
        for i, ln in enumerate(lines):
            d = clip_len(sid, i, spoken(ln))
            items.append(dict(text=shown(ln), spoken=spoken(ln), start=t, dur=d, path=clip_path(sid, i)))
            t += d + (LINE_GAP if i < len(lines) - 1 else 0.0)
        t += SCENE_GAP
        out.append(dict(id=sid, start=scene_start, end=t, lines=items))
    return out, t + OUTRO_PAD


if __name__ == "__main__":
    sc, total = build()
    print(f"total {total:.1f}s ({total/60:.2f} min)")
    for s in sc:
        print(s["id"], f'{s["start"]:.1f} -> {s["end"]:.1f}')
