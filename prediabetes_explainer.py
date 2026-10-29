"""
Prediabetes risk explainer (Manim). About 3 minutes at 1080p.

Optional files next to this script (the video still renders without them):
  s01.wav ... s10.wav   narration clips, one per scene (made with make_narration.sh)
  music.mp3             background music (trimmed and faded automatically)
  images/<name>.png     your own pictures; they replace the drawn icons
                        names: family age ethnicity weight inactivity diet smoking sleep
                               bp cholesterol pcos gestational heart a1c fasting ogtt
                               scale activity apple
Scene lengths follow the narration clips, so voice and animation stay in sync.
"""
import os
import wave

import numpy as np
from manim import *

# ---------------------------------------------------------------- theme
BG = "#EBF3FC"
NAVY = "#1B3B6F"
RED = "#FF4B5C"
GREEN = "#2EC4B6"
YELLOW = "#FF9F1C"
BLUE = "#3A86FF"
WHITE = "#FFFFFF"
SOFT = "#C9DCF2"
GREY = "#5B6F8A"
DECOR = "#D5E3F5"

# (scene key, minimum seconds if there is no narration file)
SCENES = [
    ("s01", 15), ("s02", 20), ("s03", 20), ("s04", 20), ("s05", 22),
    ("s06", 22), ("s07", 16), ("s08", 18), ("s09", 22), ("s10", 18),
]


def audio_len(key):
    path = f"{key}.wav"
    if not os.path.exists(path):
        return 0.0
    try:
        with wave.open(path) as w:
            return w.getnframes() / float(w.getframerate())
    except Exception:
        return 0.0


# ---------------------------------------------------------------- helpers
def txt(s, size=24, color=NAVY, bold=False, maxw=None):
    m = Text(s, font_size=size, color=color, weight=BOLD if bold else NORMAL)
    if maxw and m.width > maxw:
        m.scale_to_fit_width(maxw)
    return m


def dirv(deg):
    a = deg * DEGREES
    return np.array([np.cos(a), np.sin(a), 0.0])


def pic(name, fallback):
    """Use images/<name>.png if you supplied one, otherwise the drawn icon."""
    for ext in (".png", ".jpg", ".jpeg"):
        p = os.path.join("images", name + ext)
        if os.path.exists(p):
            try:
                return ImageMobject(p)
            except Exception:
                break
    return fallback()


def make_decor():
    items = [
        Circle(radius=1.7, stroke_color=DECOR, stroke_width=22).move_to([-6.9, 3.4, 0]),
        Circle(radius=2.1, stroke_color=DECOR, stroke_width=22).move_to([7.2, -3.6, 0]),
        Circle(radius=0.9, stroke_color=DECOR, stroke_width=14).move_to([6.6, 3.0, 0]),
    ]
    for x, y in [(-6.2, -2.6), (5.9, 1.6), (-5.4, 0.8), (2.2, 3.5)]:
        items.append(VGroup(Line([x - 0.18, y, 0], [x + 0.18, y, 0], color=DECOR, stroke_width=8),
                            Line([x, y - 0.18, 0], [x, y + 0.18, 0], color=DECOR, stroke_width=8)))
    return VGroup(*items)


def person(color=NAVY, h=1.0):
    head = Circle(radius=0.2 * h, fill_color=color, fill_opacity=1, stroke_width=0)
    body = RoundedRectangle(corner_radius=0.22 * h, width=0.62 * h, height=0.78 * h,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    body.next_to(head, DOWN, buff=0.07 * h)
    return VGroup(head, body)


def heart(color=RED, scale=0.045):
    h = ParametricFunction(
        lambda t: np.array([16 * np.sin(t) ** 3,
                            13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t), 0]),
        t_range=[0, TAU], fill_color=color, fill_opacity=1, stroke_width=0)
    return h.scale(scale)


def check_icon(color=GREEN, r=0.26):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_width=0)
    tick = VMobject(stroke_color=WHITE, stroke_width=5).set_points_as_corners(
        [[-0.12, 0.0, 0], [-0.03, -0.1, 0], [0.14, 0.1, 0]])
    return VGroup(c, tick)


# ---------------------------------------------------------------- icons
def icon_family():
    a, b = person(NAVY, 0.9), person(RED, 0.9)
    parents = VGroup(a, b).arrange(RIGHT, buff=0.6)
    kid = person(NAVY, 0.6).next_to(parents, DOWN, buff=0.4)
    kid.set_x(parents.get_center()[0])
    links = VGroup(*[Line(p.get_bottom(), kid.get_top(), color=NAVY, stroke_width=3) for p in (a, b)])
    return VGroup(parents, kid, links)


def icon_age():
    c = Circle(radius=0.75, stroke_color=NAVY, stroke_width=6, fill_color=WHITE, fill_opacity=1)
    return VGroup(c, txt("45+", 40, NAVY, True))


def icon_globe():
    c = Circle(radius=0.75, stroke_color=NAVY, stroke_width=5, fill_color=WHITE, fill_opacity=1)
    e = Ellipse(width=0.8, height=1.5, stroke_color=NAVY, stroke_width=3)
    h = Line(LEFT * 0.75, RIGHT * 0.75, color=NAVY, stroke_width=3)
    v = Line(DOWN * 0.75, UP * 0.75, color=NAVY, stroke_width=3)
    return VGroup(c, e, h, v)


def icon_scale():
    base = RoundedRectangle(corner_radius=0.2, width=1.6, height=1.3, stroke_color=NAVY,
                            stroke_width=5, fill_color=WHITE, fill_opacity=1)
    ctr = base.get_center() + UP * 0.15
    dial = Arc(radius=0.45, start_angle=PI, angle=-PI, arc_center=ctr, color=NAVY, stroke_width=5)
    needle = Line(ctr, ctr + 0.4 * dirv(55), color=RED, stroke_width=5)
    return VGroup(base, dial, needle, Dot(ctr, radius=0.06, color=NAVY))


def icon_sofa():
    kw = dict(stroke_color=NAVY, stroke_width=4, fill_color=SOFT, fill_opacity=1)
    back = RoundedRectangle(corner_radius=0.15, width=1.5, height=0.7, **kw)
    seat = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.4, **kw).next_to(back, DOWN, buff=-0.1)
    arm_l = RoundedRectangle(corner_radius=0.1, width=0.3, height=0.75, **kw).move_to(seat.get_left() + UP * 0.1)
    arm_r = RoundedRectangle(corner_radius=0.1, width=0.3, height=0.75, **kw).move_to(seat.get_right() + UP * 0.1)
    head = Circle(radius=0.16, fill_color=NAVY, fill_opacity=1, stroke_width=0).move_to(back.get_center() + UP * 0.12)
    return VGroup(back, seat, arm_l, arm_r, head)


def icon_soda():
    cup = Polygon([-0.5, 0.7, 0], [0.5, 0.7, 0], [0.38, -0.7, 0], [-0.38, -0.7, 0],
                  stroke_color=NAVY, stroke_width=4, fill_color=RED, fill_opacity=0.9)
    lid = RoundedRectangle(corner_radius=0.05, width=1.2, height=0.16, fill_color=NAVY,
                           fill_opacity=1, stroke_width=0).move_to([0, 0.78, 0])
    straw = Line([0.12, 0.85, 0], [0.3, 1.3, 0], color=NAVY, stroke_width=5)
    cubes = VGroup(*[Square(side_length=0.22, stroke_color=NAVY, stroke_width=2,
                            fill_color=WHITE, fill_opacity=1).rotate(a) for a in (0.2, -0.3)])
    cubes.arrange(RIGHT, buff=0.08).move_to([0, -0.1, 0])
    return VGroup(cup, lid, straw, cubes)


def icon_smoke():
    cig = Rectangle(width=1.7, height=0.22, stroke_color=NAVY, stroke_width=3, fill_color=WHITE, fill_opacity=1)
    filt = Rectangle(width=0.5, height=0.22, stroke_width=0, fill_color=YELLOW,
                     fill_opacity=1).move_to(cig.get_left() + RIGHT * 0.25)
    ember = Rectangle(width=0.08, height=0.22, stroke_width=0, fill_color=RED,
                      fill_opacity=1).move_to(cig.get_right() + LEFT * 0.04)
    smoke = FunctionGraph(lambda x: 0.09 * np.sin(8 * x), x_range=[0, 1.0], color="#8FA3BF", stroke_width=4)
    smoke.rotate(PI / 2).move_to(cig.get_right() + UP * 0.62 + LEFT * 0.1)
    return VGroup(cig, filt, ember, smoke)


def icon_moon():
    moon = Circle(radius=0.7, fill_color=NAVY, fill_opacity=1, stroke_width=0)
    cut = Circle(radius=0.6, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(RIGHT * 0.35 + UP * 0.15)
    stars = VGroup(Dot([0.55, 0.6, 0], radius=0.06, color=YELLOW),
                   Dot([0.85, 0.1, 0], radius=0.05, color=YELLOW),
                   Dot([0.35, -0.5, 0], radius=0.04, color=YELLOW))
    return VGroup(moon, cut, stars)


def icon_gauge():
    c = Circle(radius=0.7, stroke_color=NAVY, stroke_width=5, fill_color=WHITE, fill_opacity=1)
    ticks = VGroup(*[Line(0.5 * dirv(a), 0.62 * dirv(a), color=NAVY, stroke_width=3)
                     for a in (200, 160, 120, 80, 40, 0, -40)])
    needle = Line(ORIGIN, 0.45 * dirv(50), color=RED, stroke_width=5)
    return VGroup(c, ticks, needle, Dot(ORIGIN, radius=0.06, color=NAVY))


def icon_chol():
    tube = RoundedRectangle(corner_radius=0.35, width=1.9, height=0.7, stroke_color=NAVY,
                            stroke_width=5, fill_color="#FFE3E6", fill_opacity=1)
    blobs = VGroup(*[Dot([x, y, 0], radius=r, color=YELLOW)
                     for x, y, r in [(-0.5, -0.12, 0.13), (-0.1, -0.17, 0.11), (0.3, -0.1, 0.14), (0.65, -0.15, 0.1)]])
    return VGroup(tube, blobs)


def icon_female():
    c = Circle(radius=0.38, stroke_color=NAVY, stroke_width=6).shift(UP * 0.35)
    stem = Line(UP * -0.03, DOWN * 0.7, color=NAVY, stroke_width=6)
    bar = Line(LEFT * 0.28 + DOWN * 0.4, RIGHT * 0.28 + DOWN * 0.4, color=NAVY, stroke_width=6)
    return VGroup(c, stem, bar)


def icon_bump():
    p = person(NAVY, 1.3)
    bump = Circle(radius=0.24, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
    bump.move_to(p[1].get_center() + RIGHT * 0.3 + DOWN * 0.1)
    return VGroup(p, bump)


def icon_heart_disease():
    h = heart(RED, 0.05)
    pulse = VMobject(stroke_color=WHITE, stroke_width=5).set_points_as_corners(
        [[-0.5, 0, 0], [-0.2, 0, 0], [-0.08, 0.3, 0], [0.08, -0.3, 0], [0.2, 0, 0], [0.5, 0, 0]])
    pulse.move_to(h.get_center())
    return VGroup(h, pulse)


def icon_drop():
    c = Circle(radius=0.42, fill_color=RED, fill_opacity=1, stroke_width=0).shift(DOWN * 0.2)
    t = Triangle(fill_color=RED, fill_opacity=1, stroke_width=0).scale(0.34).move_to([0, 0.4, 0])
    return VGroup(c, t)


def icon_glucometer():
    body = RoundedRectangle(corner_radius=0.2, width=1.0, height=1.7, fill_color=BLUE, fill_opacity=1,
                            stroke_color=NAVY, stroke_width=4)
    screen = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.5, fill_color=NAVY, fill_opacity=1,
                              stroke_width=0).move_to(body.get_top() + DOWN * 0.5)
    num = txt("120", 20, WHITE, True).move_to(screen)
    btns = VGroup(*[Circle(radius=0.1, fill_color=WHITE, fill_opacity=1, stroke_width=0) for _ in range(2)])
    btns.arrange(RIGHT, buff=0.2).move_to(body.get_center() + DOWN * 0.25)
    strip = Rectangle(width=0.18, height=0.45, fill_color=WHITE, fill_opacity=1, stroke_color=NAVY,
                      stroke_width=2).move_to(body.get_bottom() + DOWN * 0.2)
    drop = icon_drop().scale(0.35).move_to(body.get_bottom() + DOWN * 0.7)
    return VGroup(body, screen, num, btns, strip, drop)


def icon_glass():
    g = Polygon([-0.5, 0.7, 0], [0.5, 0.7, 0], [0.36, -0.7, 0], [-0.36, -0.7, 0],
                stroke_color=NAVY, stroke_width=4, fill_color="#BFE3FF", fill_opacity=1)
    s = Polygon([-0.43, 0.1, 0], [0.43, 0.1, 0], [0.36, -0.7, 0], [-0.36, -0.7, 0],
                stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
    return VGroup(g, s)


def icon_run(color=GREEN):
    head = Circle(radius=0.17, fill_color=color, fill_opacity=1, stroke_width=0).move_to([0.1, 0.8, 0])

    def seg(pts):
        return VMobject(stroke_color=color, stroke_width=8).set_points_as_corners(pts)

    torso = seg([[0.05, 0.58, 0], [-0.1, 0.0, 0]])
    arms = seg([[0.55, 0.25, 0], [0.1, 0.45, 0], [-0.35, 0.3, 0]])
    legs = seg([[0.35, -0.7, 0], [0.15, -0.4, 0], [-0.1, 0.0, 0], [-0.45, -0.35, 0], [-0.75, -0.25, 0]])
    return VGroup(head, torso, arms, legs)


def icon_apple():
    a = Circle(radius=0.45, fill_color=RED, fill_opacity=1, stroke_width=0)
    leaf = Ellipse(width=0.32, height=0.16, fill_color=GREEN, fill_opacity=1, stroke_width=0)
    leaf.rotate(0.5).move_to([0.22, 0.55, 0])
    stem = Line([0, 0.4, 0], [0.03, 0.65, 0], color=NAVY, stroke_width=4)
    return VGroup(a, leaf, stem)


def make_card(icon, title, sub, w=2.7, h=4.2, accent=NAVY, tsize=24, ssize=17):
    box = RoundedRectangle(corner_radius=0.25, width=w, height=h, fill_color=WHITE, fill_opacity=1,
                           stroke_color=accent, stroke_width=3)
    icon.scale_to_fit_height(1.4)
    if icon.width > w - 0.8:
        icon.scale_to_fit_width(w - 0.8)
    icon.move_to(box.get_top() + DOWN * 1.1)
    t = txt(title, tsize, NAVY, True, maxw=w - 0.3).next_to(icon, DOWN, buff=0.3)
    s = txt(sub, ssize, GREY, maxw=w - 0.3).next_to(t, DOWN, buff=0.18)
    return Group(box, icon, t, s)


def chip(icon, text, w=6.6):
    box = RoundedRectangle(corner_radius=0.2, width=w, height=1.0, fill_color=WHITE, fill_opacity=1,
                           stroke_color=SOFT, stroke_width=3)
    icon.scale_to_fit_height(0.7).move_to(box.get_left() + RIGHT * 0.6)
    t = txt(text, 24, NAVY, True, maxw=w - 1.6).next_to(icon, RIGHT, buff=0.35)
    return Group(box, icon, t)


# ---------------------------------------------------------------- the video
class PrediabetesExplainer(Scene):
    # ---- timing helpers: every scene lasts exactly self.D seconds
    def p(self, *anims, rt=1.0):
        self.play(*anims, run_time=rt)
        self.el += rt

    def until(self, t):
        if t > self.el:
            self.wait(t - self.el)
            self.el = t

    def begin(self, key):
        self.el = 0.0
        self.D = self.lens[key]
        if audio_len(key) > 0:
            self.add_sound(f"{key}.wav")

    def end(self):
        self.until(self.D)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.decor], run_time=0.5)

    def title_bar(self, text, color=NAVY):
        t = txt(text, 40, color, True, maxw=12.5).to_edge(UP, buff=0.5)
        self.p(FadeIn(t, shift=DOWN * 0.2), rt=0.8)
        return t

    def reveal(self, items, first=1.6, last=1.4, each=0.7):
        step = (self.D - last - first) / len(items)
        for i, it in enumerate(items):
            self.until(first + i * step)
            self.p(FadeIn(it, shift=UP * 0.3), rt=each)

    def add_music(self, total):
        if not os.path.exists("music.mp3"):
            return
        try:
            from pydub import AudioSegment
            seg = AudioSegment.from_file("music.mp3")
            ms = int(total * 1000)
            while len(seg) < ms:
                seg += seg
            seg[:ms].fade_in(1500).fade_out(2500).export("music_trim.wav", format="wav")
            self.add_sound("music_trim.wav", gain=-20)
        except Exception as e:
            print("Music skipped:", e)

    def construct(self):
        self.camera.background_color = BG
        self.decor = make_decor()
        self.add(self.decor)
        self.lens = {}
        for key, minimum in SCENES:
            a = audio_len(key)
            self.lens[key] = max(minimum, a + 0.8) if a else minimum
        self.add_music(sum(self.lens.values()) + 0.5 * len(SCENES))
        for scene in (self.s1, self.s2, self.s3, self.s4, self.s5,
                      self.s6, self.s7, self.s8, self.s9, self.s10):
            scene()

    # ---- 1. hook
    def s1(self):
        self.begin("s01")
        title = txt("Prediabetes: Are You at Risk?", 46, NAVY, True, maxw=12.5).to_edge(UP, buff=0.7)
        self.p(Write(title), rt=1.2)
        people = VGroup(*[person(NAVY, 1.6) for _ in range(5)]).arrange(RIGHT, buff=0.6).shift(UP * 0.3)
        self.p(LaggedStart(*[FadeIn(x, shift=UP * 0.3) for x in people], lag_ratio=0.25), rt=1.6)
        stat = txt("More than 2 in 5 US adults have prediabetes", 38, NAVY, True, maxw=12.5).shift(DOWN * 1.6)
        sub = txt("About 8 in 10 of them don't know it", 30, RED, True)
        sub.next_to(stat, DOWN, buff=0.35)
        src = txt("Source: CDC (US data)", 18, GREY).to_edge(DOWN, buff=0.4)
        self.until(self.D * 0.3)
        self.p(people[3].animate.set_color(RED), people[4].animate.set_color(RED), FadeIn(stat), rt=1.0)
        self.until(self.D * 0.55)
        self.p(FadeIn(sub), FadeIn(src), rt=1.0)
        self.end()

    # ---- 2. what is prediabetes (segmented gauge)
    def s2(self):
        self.begin("s02")
        self.title_bar("What Is Prediabetes?")
        P = np.array([0.0, -0.9, 0.0])
        R = 2.6
        segs = [(GREEN, 150, "Normal", "Below 5.7%"),
                (YELLOW, 90, "Prediabetes", "5.7% - 6.4%"),
                (RED, 30, "Diabetes", "6.5% or higher")]
        arcs = VGroup(*[Arc(radius=R, start_angle=(a + 28) * DEGREES, angle=-56 * DEGREES, arc_center=P,
                            color=c, stroke_width=36) for c, a, _, _ in segs])
        names = VGroup(*[txt(n, 26, NAVY, True).move_to(P + (R + 0.6) * dirv(a)) for _, a, n, _ in segs])
        label = txt("BLOOD SUGAR (A1C)", 34, NAVY, True).move_to(P + DOWN * 0.9)
        needle = Line(P, P + 1.9 * dirv(150), color=NAVY, stroke_width=8)
        pin = Dot(P, radius=0.2, color="#3D5A8F")
        ranges = VGroup()
        for (c, _, _, r), x in zip(segs, (-3.8, 0.0, 3.8)):
            item = VGroup(Dot(radius=0.12, color=c), txt(r, 24, NAVY, True)).arrange(RIGHT, buff=0.2)
            ranges.add(item.move_to([x, -2.75, 0]))
        note = txt("Higher than normal, but not yet diabetes", 24, GREY).to_edge(DOWN, buff=0.35)
        self.until(self.D * 0.10)
        self.p(Create(arcs), FadeIn(names), FadeIn(label), rt=1.5)
        self.p(FadeIn(needle), FadeIn(pin), rt=0.6)
        self.until(self.D * 0.45)
        self.p(FadeIn(ranges[0]), rt=0.6)
        self.until(self.D * 0.62)
        self.p(Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[1]), rt=1.0)
        self.until(self.D * 0.78)
        self.p(Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[2]), rt=1.0)
        self.until(self.D * 0.90)
        self.p(Rotate(needle, angle=60 * DEGREES, about_point=P), FadeIn(note), rt=1.0)
        self.end()

    # ---- 3. insulin resistance
    def s3(self):
        self.begin("s03")
        self.title_bar("What Goes Wrong Inside the Body")

        def panel(x0, head, hc, ok, cap):
            cell = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.9, fill_color=WHITE, fill_opacity=1,
                                    stroke_color=hc, stroke_width=5).move_to([x0, -0.1, 0])
            cl = txt("Cell", 22, NAVY, True).move_to(cell.get_bottom() + UP * 0.3)
            pill = RoundedRectangle(corner_radius=0.18, width=1.2, height=0.4,
                                    fill_color=(BLUE if ok else "#B8C4D6"), fill_opacity=1,
                                    stroke_width=0).move_to([x0 - 1.3, -0.1, 0])
            pl = txt("insulin", 18, WHITE, True).move_to(pill)
            parts = [cell, cl, pill, pl]
            if not ok:
                parts += [Line([x0 - 1.5, 0.1, 0], [x0 - 1.1, -0.3, 0], color=RED, stroke_width=7),
                          Line([x0 - 1.5, -0.3, 0], [x0 - 1.1, 0.1, 0], color=RED, stroke_width=7)]
            hd = txt(head, 30, hc, True, maxw=5.0).move_to([x0 - 0.75, 1.7, 0])
            sg = txt("sugar", 18, GREY).move_to([x0 - 2.8, -0.95, 0])
            dots = VGroup(*[Dot([x0 - 2.8, 0.7 - 0.3 * i, 0], radius=0.11, color=YELLOW) for i in range(5)])
            caption = txt(cap, 22, NAVY, maxw=5.2).move_to([x0 - 0.75, -2.3, 0])
            return VGroup(*parts, hd, sg), dots, caption

        xl, xr = -2.85, 4.35
        st_l, dots_l, cap_l = panel(xl, "Healthy", GREEN, True, "Insulin opens the door.\nSugar enters the cells.")
        st_r, dots_r, cap_r = panel(xr, "Insulin resistance", RED, False,
                                    "Cells stop responding.\nSugar builds up in the blood.")
        self.until(self.D * 0.15)
        self.p(FadeIn(st_l), FadeIn(st_r), FadeIn(dots_l), FadeIn(dots_r), rt=1.0)
        self.until(self.D * 0.45)
        tg_l = [[xl - 0.6, 0.35, 0], [xl, 0.35, 0], [xl + 0.6, 0.35, 0], [xl - 0.3, -0.15, 0], [xl + 0.3, -0.15, 0]]
        tg_r = [[xr - 2.05 + 0.25 * (i % 2), 0.55 - 0.27 * i, 0] for i in range(5)]
        self.p(AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_l, tg_l)], lag_ratio=0.2),
               AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_r, tg_r)], lag_ratio=0.2), rt=2.5)
        self.until(self.D * 0.62)
        self.p(FadeIn(cap_l), rt=0.8)
        self.until(self.D * 0.78)
        self.p(FadeIn(cap_r), rt=0.8)
        self.end()

    # ---- 4. risks you can't change
    def s4(self):
        self.begin("s04")
        self.title_bar("Risks You Can't Change")
        cards = Group(
            make_card(pic("age", icon_age), "Age", "Risk rises with age,\nespecially after 45", w=3.9, tsize=28, ssize=20),
            make_card(pic("family", icon_family), "Family history", "A parent or sibling with\ntype 2 diabetes", w=3.9, tsize=28, ssize=20),
            make_card(pic("ethnicity", icon_globe), "Ethnicity",
                      "Higher rates in some groups:\nBlack, Hispanic, Asian,\nNative American, Pacific Islander",
                      w=3.9, tsize=28, ssize=20),
        ).arrange(RIGHT, buff=0.4).shift(DOWN * 0.4)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        self.reveal(list(cards.submobjects))
        self.end()

    # ---- 5. lifestyle
    def s5(self):
        self.begin("s05")
        self.title_bar("Lifestyle Risks You Can Change", GREEN)
        cards = Group(
            make_card(pic("weight", icon_scale), "Excess weight", "Extra weight,\nespecially at\nthe belly", w=2.4, tsize=22),
            make_card(pic("inactivity", icon_sofa), "Inactivity", "Little regular\nphysical\nactivity", w=2.4, tsize=22),
            make_card(pic("diet", icon_soda), "Sugary diet", "Sugary drinks &\nprocessed\nfoods", w=2.4, tsize=22),
            make_card(pic("smoking", icon_smoke), "Smoking", "Raises type 2\ndiabetes risk", w=2.4, tsize=22),
            make_card(pic("sleep", icon_moon), "Poor sleep", "Too little or\ndisrupted\nsleep", w=2.4, tsize=22),
        ).arrange(RIGHT, buff=0.25).shift(DOWN * 0.4)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        self.reveal(list(cards.submobjects))
        self.end()

    # ---- 6. health conditions
    def s6(self):
        self.begin("s06")
        self.title_bar("Health Conditions That Raise Risk")
        cards = Group(
            make_card(pic("bp", icon_gauge), "High blood\npressure", "Hypertension", w=2.4, tsize=22),
            make_card(pic("cholesterol", icon_chol), "Abnormal\ncholesterol", "Low HDL or high\ntriglycerides", w=2.4, tsize=22),
            make_card(pic("pcos", icon_female), "PCOS", "Polycystic ovary\nsyndrome", w=2.4, tsize=22),
            make_card(pic("gestational", icon_bump), "Gestational\ndiabetes", "Diabetes during\na past pregnancy", w=2.4, tsize=22),
            make_card(pic("heart", icon_heart_disease), "Heart disease\nor stroke", "A history of\neither", w=2.4, tsize=22),
        ).arrange(RIGHT, buff=0.25).shift(DOWN * 0.4)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        self.reveal(list(cards.submobjects))
        self.end()

    # ---- 7. risks add up (risk hub)
    def s7(self):
        self.begin("s07")
        self.title_bar("Risk Factors Add Up")
        C = np.array([0.0, -0.2, 0.0])
        circle = Circle(radius=1.0, fill_color=GREEN, fill_opacity=1, stroke_color=WHITE, stroke_width=6).move_to(C)
        word = txt("RISK", 26, WHITE, True).move_to(C + UP * 0.3)
        level = txt("LOW", 34, WHITE, True).move_to(C + DOWN * 0.25)
        chips = Group(chip(pic("family", icon_family), "Family history", w=4.4),
                      chip(pic("inactivity", icon_sofa), "Inactivity", w=4.4),
                      chip(pic("weight", icon_scale), "Extra weight", w=4.4),
                      chip(pic("diet", icon_soda), "Unhealthy eating", w=4.4))
        for c, pos in zip(chips.submobjects, ([-3.6, 1.2, 0], [3.6, 1.2, 0], [-3.6, -1.6, 0], [3.6, -1.6, 0])):
            c.move_to(pos)
        lines = []
        for c in chips.submobjects:
            d = c.get_center() - C
            u = d / np.linalg.norm(d)
            lines.append(Line(C + u * 1.0, c.get_center(), color=SOFT, stroke_width=5))
        self.p(FadeIn(circle), FadeIn(word), FadeIn(level), rt=1.0)
        changes = [None, ("ELEVATED", YELLOW), None, ("HIGH", RED)]
        for i, frac in enumerate((0.22, 0.38, 0.54, 0.70)):
            self.until(self.D * frac)
            anims = [FadeIn(lines[i]), FadeIn(chips[i], shift=UP * 0.2)]
            if changes[i]:
                new = txt(changes[i][0], 26, WHITE, True, maxw=1.7).move_to(level)
                anims += [circle.animate.set_fill(changes[i][1]), Transform(level, new)]
            self.p(*anims, rt=1.0)
        box = RoundedRectangle(corner_radius=0.2, width=9.0, height=0.8, fill_color=YELLOW, fill_opacity=0.25,
                               stroke_color=YELLOW, stroke_width=3).to_edge(DOWN, buff=0.5)
        msg = txt("High risk = a warning, not a diagnosis", 28, NAVY, True).move_to(box)
        self.until(self.D * 0.82)
        self.p(FadeIn(box, shift=UP * 0.2), FadeIn(msg), rt=0.8)
        self.end()

    # ---- 8. testing
    def s8(self):
        self.begin("s08")
        self.title_bar("How Do You Find Out?")
        cards = Group(
            make_card(pic("a1c", icon_drop), "A1C test", "Average blood sugar\nover 2-3 months", w=3.9, tsize=28, ssize=20),
            make_card(pic("fasting", icon_glucometer), "Fasting glucose", "Blood sugar after\nnot eating overnight", w=3.9, tsize=28, ssize=20),
            make_card(pic("ogtt", icon_glass), "Glucose tolerance", "Blood sugar before and\n2 hours after a sugary drink",
                      w=3.9, tsize=28, ssize=20),
        ).arrange(RIGHT, buff=0.4).shift(DOWN * 0.1)
        if cards.width > 13.2:
            cards.scale_to_fit_width(13.2)
        note = txt("Ask your doctor how often you should be screened", 28, NAVY, True, maxw=12).to_edge(DOWN, buff=0.5)
        self.reveal(list(cards.submobjects), last=3.2)
        self.until(self.D * 0.80)
        self.p(FadeIn(note, shift=UP * 0.2), rt=0.8)
        self.end()

    # ---- 9. the good news
    def s9(self):
        self.begin("s09")
        self.title_bar("The Good News: You Can Lower Your Risk", GREEN)
        tr = ValueTracker(0)
        num = always_redraw(lambda: txt(f"{int(tr.get_value())}%", 120, GREEN, True).move_to(np.array([-3.9, 0.9, 0])))
        cap = txt("lower risk of type 2 diabetes\nwith lifestyle changes", 26, NAVY, True, maxw=5.6).move_to([-3.9, -0.7, 0])
        src = txt("Diabetes Prevention Program (NIH study)", 18, GREY, maxw=5.6).move_to([-3.9, -1.6, 0])
        self.add(num)
        self.until(self.D * 0.25)
        self.p(tr.animate.set_value(58), FadeIn(cap), FadeIn(src), rt=2.5)
        chips = Group(chip(pic("scale", icon_scale), "Lose 5-7% of body weight"),
                      chip(pic("activity", icon_run), "150 minutes of activity a week"),
                      chip(pic("apple", icon_apple), "Eat more whole foods")).arrange(DOWN, buff=0.35).move_to([3.4, -0.2, 0])
        for i, c in enumerate(chips.submobjects):
            self.until(self.D * (0.50 + 0.1 * i))
            self.p(FadeIn(c, shift=LEFT * 0.3), rt=0.7)
        self.end()

    # ---- 10. call to action
    def s10(self):
        self.begin("s10")
        self.title_bar("Take Action Today", GREEN)
        items = ["Learn your risk factors", "Talk to your doctor about a blood test",
                 "Move more, eat well, sleep well", "Small steps today protect your future"]
        rows = VGroup(*[VGroup(check_icon(), txt(s, 34, NAVY, True)).arrange(RIGHT, buff=0.4) for s in items])
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(UP * 0.1)
        if rows.width > 12.5:
            rows.scale_to_fit_width(12.5)
        d1 = txt("Educational information only - not medical advice or a diagnosis.", 20, GREY, maxw=12).to_edge(DOWN, buff=0.85)
        d2 = txt("Sources: CDC, American Diabetes Association, NIH Diabetes Prevention Program", 18, GREY, maxw=12)
        d2.next_to(d1, DOWN, buff=0.2)
        self.reveal(list(rows.submobjects), first=1.4, last=3.2)
        self.until(self.D * 0.80)
        self.p(FadeIn(d1), FadeIn(d2), rt=0.8)
        self.end()
