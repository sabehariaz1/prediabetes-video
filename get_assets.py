"""Downloads colorful people / food / place illustrations (Twemoji, CC-BY 4.0) into assets/.
Missing files are fine: the video falls back to the simple drawn icons."""
import os
import urllib.request

BASE = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/svg/"

MANIFEST = {
    # people walking / exercising (skin-tone variants first, plain version as backup)
    "walk1": ["1f6b6-1f3fd", "1f6b6"], "walk2": ["1f6b6-1f3fe", "1f6b6"], "walk3": ["1f6b6-1f3fb", "1f6b6"],
    "walk4": ["1f6b6-200d-2640-fe0f", "1f6b6-1f3fc"], "walk5": ["1f6b6-1f3fd-200d-2640-fe0f", "1f6b6-1f3fe"],
    "run1": ["1f3c3-1f3fd", "1f3c3"], "run2": ["1f3c3-200d-2640-fe0f", "1f3c3"],
    "bike": ["1f6b4-1f3fd", "1f6b4"], "yoga": ["1f9d8-1f3fd", "1f9d8"],
    # doctors, patients, faces
    "doctor_f": ["1f469-1f3fd-200d-2695-fe0f", "1f469-200d-2695-fe0f"],
    "doctor_m": ["1f468-1f3fe-200d-2695-fe0f", "1f468-200d-2695-fe0f"],
    "patient": ["1f469-1f3fd", "1f469"], "elder": ["1f474-1f3fd", "1f474"], "elder_w": ["1f475"],
    "pregnant": ["1f930-1f3fd", "1f930"], "woman": ["1f469-1f3fe", "1f469"],
    "face_smile": ["1f642"], "face_neutral": ["1f610"], "face_worried": ["1f61f"], "face_happy": ["1f60a"],
    "man_a": ["1f468-1f3fb"], "man_b": ["1f468-1f3ff"], "woman_a": ["1f469-1f3fd"], "woman_b": ["1f469-1f3fc"],
    "family": ["1f46a"], "globe": ["1f30d"],
    # places and nature
    "hospital": ["1f3e5"], "tree": ["1f333"], "tulip": ["1f337"], "sunflower": ["1f33b"], "blossom": ["1f33c"],
    "sprout": ["1f331"],
    # healthy food
    "apple": ["1f34e"], "banana": ["1f34c"], "grapes": ["1f347"], "orange": ["1f34a"], "strawberry": ["1f353"],
    "avocado": ["1f951"], "broccoli": ["1f966"], "carrot": ["1f955"], "salad": ["1f957"], "fish": ["1f41f"],
    "egg": ["1f95a"], "water": ["1f4a7"],
    # unhealthy food and habits
    "burger": ["1f354"], "fries": ["1f35f"], "donut": ["1f369"], "cola": ["1f964"], "candy": ["1f36c"],
    "smoke": ["1f6ac"], "couch": ["1f6cb"], "sleep": ["1f634"], "moon": ["1f319"], "plate": ["1f37d"],
    # medical
    "stethoscope": ["1fa7a"], "syringe": ["1f489"], "blood": ["1fa78"], "pill": ["1f48a"], "tube": ["1f9ea"],
    "clipboard": ["1f4cb"], "balance": ["2696"], "heart": ["2764"], "heart_anat": ["1fac0"], "clock": ["23f0"],
    "sparkles": ["2728"], "check": ["2705"],
}


def variants(code):
    out = [code, code.replace("-fe0f", "")]
    if "200d" not in code and not code.endswith("fe0f"):
        out.append(code + "-fe0f")
    return list(dict.fromkeys(out))


def fetch(url, dest):
    with urllib.request.urlopen(url, timeout=25) as r:
        data = r.read()
    if b"<svg" not in data[:400]:
        raise ValueError("not an svg")
    with open(dest, "wb") as f:
        f.write(data)


os.makedirs("assets", exist_ok=True)
ok, missing = 0, []
for name, cands in MANIFEST.items():
    dest = os.path.join("assets", name + ".svg")
    if os.path.exists(dest):
        ok += 1
        continue
    done = False
    for c in cands:
        for v in variants(c):
            try:
                fetch(BASE + v + ".svg", dest)
                done = True
                break
            except Exception:
                continue
        if done:
            break
    if done:
        ok += 1
    else:
        missing.append(name)
print(f"illustrations downloaded: {ok}/{len(MANIFEST)}")
if missing:
    print("missing (simple drawn icons will be used):", ", ".join(missing))
