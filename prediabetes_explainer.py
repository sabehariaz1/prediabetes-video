"""
Prediabetes risk explainer, version 4 (exactly 2:00).
Bright scenes with illustrated people; every picture is cued to a narration sentence (timeline in story.py).
Run order on GitHub: get_assets.py -> make_voice.py -> make_mix.py -> manim.
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from manim import *
from icons import *
from scene_kit import *
from story import build, LEAD

# ---- on-screen references (edit here)
SOURCES = ("Sources: American Diabetes Association (ADA), Centers for Disease Control and Prevention (CDC), "
           "NIH Diabetes Prevention Program (DPP), IDF Diabetes Atlas")
PURPOSE = ("Purpose: Created to spread community awareness and educate the public about prediabetes. "
           "For educational purposes only \u2014 not a medical diagnosis.")
CREDIT = "Illustrations: Twemoji (CC BY 4.0)"


def make_caption(text):
    t = txt(textwrap.fill(text, 60), 26, NAVY, False)
    if t.width > 12.4:
        t.scale_to_fit_width(12.4)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.3,
                           fill_color=WHITE, fill_opacity=0.94, stroke_color=SOFT, stroke_width=2)
    return VGroup(box, t).move_to([0, -3.3, 0])


def banner(text, color, x=0.0):
    t = txt(text, 24, WHITE, True)
    b = RoundedRectangle(corner_radius=0.25, width=t.width + 0.9, height=0.55,
                         fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=3)
    t.move_to(b)
    return VGroup(b, t).move_to([x, 2.3, 0])


def test_card(icon, title, sub, normal, pre, w=4.1, h=4.6):
    """A test card with generous padding: name, what it measures, and the normal / prediabetes ranges."""
    pad = 0.45
    box = RoundedRectangle(corner_radius=0.3, width=w, height=h, fill_color=WHITE, fill_opacity=1,
                           stroke_color=SOFT, stroke_width=4)
    icon.scale_to_fit_height(0.95).move_to(box.get_top() + DOWN * 0.8)
    t = txt(title, 24, NAVY, True, maxw=w - 2 * pad).next_to(icon, DOWN, buff=0.22)
    s = txt(sub, 17, GREY, False, maxw=w - 2 * pad).next_to(t, DOWN, buff=0.1)

    def rng(label, value, color, tc):
        chip = pill(label, color, 15, tc=tc, pad=0.5)
        val = txt(value, 22, NAVY, True, maxw=w - 2 * pad)
        return VGroup(chip, val).arrange(DOWN, buff=0.1)

    ranges = VGroup(rng("NORMAL", normal, GREEN, WHITE), rng("PREDIABETES", pre, YELLOW, NAVY))
    ranges.arrange(DOWN, buff=0.24).next_to(s, DOWN, buff=0.3)
    return VGroup(box, icon, t, s, ranges)


class PrediabetesExplainer(Scene):
    # ------------------------------------------------------------ timing helpers
    def now(self):
        return self.renderer.time

    def at(self, t):
        dt = t - self.now()
        if dt > 0.03:
            self.wait(dt)

    def ts(self, i, frac=0.0):
        ln = self.sc["lines"][i]
        return ln["start"] + frac * ln["dur"]

    def mid(self, i, frac):
        self.at(self.ts(i, frac))

    def after(self, i, seconds):
        """Wait until `seconds` after sentence i starts (so a picture lands on the right word)."""
        self.at(self.sc["lines"][i]["start"] + seconds - LEAD)

    def line(self, i, *anims, rt=0.6):
        """Waits for sentence i, shows its caption and plays the animations together with the voice."""
        ln = self.sc["lines"][i]
        self.at(ln["start"] - LEAD)
        new = make_caption(ln["text"])
        extra = [FadeIn(new, shift=UP * 0.1)]
        if self.cap is not None:
            extra.append(FadeOut(self.cap))
        self.cap = new
        self.play(*anims, *extra, run_time=rt)

    def begin(self, sid):
        self.sc = self.S[sid]
        self.cap = None
        self.at(self.sc["start"])

    def title_bar(self, text, color=NAVY, bg=None):
        t = txt(text, 40, color, True, maxw=12.5).to_edge(UP, buff=0.5)
        t.set_stroke(WHITE, 7, background=True)
        anims = ([FadeIn(bg)] if bg is not None else []) + [FadeIn(t, shift=DOWN * 0.2)]
        self.play(*anims, run_time=0.2)
        return t

    def end_scene(self):
        self.at(self.sc["end"] - 0.45)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in self.keep], run_time=0.45)
        self.cap = None

    # ------------------------------------------------------------ main
    def construct(self):
        self.camera.background_color = BG
        self.scenes, self.total = build()
        self.S = {s["id"]: s for s in self.scenes}
        self.cap = None
        decor = make_decor()
        track = Rectangle(width=14.222, height=0.08, fill_color=SOFT, fill_opacity=1,
                          stroke_width=0).move_to([0, -3.96, 0])

        def bar_width():
            return max(0.01, 14.222 * min(1.0, self.now() / self.total))

        bar = always_redraw(lambda: Rectangle(width=bar_width(), height=0.08, fill_color=GREEN, fill_opacity=1,
                                              stroke_width=0).move_to([-7.111 + bar_width() / 2, -3.96, 0]))
        self.keep = [decor, track, bar]
        self.add(decor, track, bar)
        if os.path.exists("mix.wav"):
            self.add_sound("mix.wav")
        for scene in (self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9):
            scene()
        self.at(self.total)

    # ------------------------------------------------------------ 1. hook: a crowd in the park
    def s1(self):
        self.begin("s01")
        self.title_bar("Prediabetes: Are You at Risk?", NAVY, park_bg())
        names = ["walk1", "walk2", "walk3", "walk4", "walk5", "walk1", "walk2", "walk3"]
        xs = np.linspace(-5.2, 5.2, 8)
        y = -1.35
        walkers = []
        for n in names:
            sprite = E(n, 1.5, flip=FLIP_PEOPLE)
            halo = Circle(radius=0.85, fill_color=RED, fill_opacity=0, stroke_color=RED, stroke_width=0).move_to(sprite)
            walkers.append(VGroup(halo, sprite))
        self.add(*walkers)
        starts = [[x - 13, y, 0] for x in xs]
        self.line(0, LaggedStart(*[walk(w, s, [x, y, 0], bobs=8) for w, s, x in zip(walkers, starts, xs)], lag_ratio=0.08), rt=2.6)
        p1 = pill("About 1 in 8 adults worldwide", CORAL, 40).move_to([0, 1.75, 0])
        self.mid(0, 0.5)
        self.play(walkers[3][0].animate.set_fill(RED, opacity=0.4).set_stroke(RED, width=6), FadeIn(p1, scale=0.7), run_time=0.8)
        for k, w in enumerate(walkers):
            float_(w, 0.04, 1.1, phase=k * 0.7)
        p2 = pill("Many don't know they have it", ORNG, 30).move_to([0, 0.8, 0])
        q = VGroup(Circle(radius=0.22, fill_color=YELLOW, fill_opacity=1, stroke_color=WHITE, stroke_width=3), txt("?", 26, WHITE, True))
        q[1].move_to(q[0])
        q.move_to(walkers[3].get_top() + UP * 0.35)
        self.mid(0, 0.75)
        self.play(FadeIn(p2, shift=UP * 0.2), GrowFromCenter(q), run_time=0.7)
        src = txt("Source: IDF Diabetes Atlas, 11th edition (2025)", 16, NAVY, True).move_to([0, -2.55, 0])
        src.set_stroke(WHITE, 6, background=True)
        board = RoundedRectangle(corner_radius=0.2, width=4.8, height=1.4, fill_color="#A9743A", fill_opacity=1,
                                 stroke_color="#6B4423", stroke_width=6)
        board_t = txt("What raises\nyour risk?", 36, WHITE, True).move_to(board)
        post = Rectangle(width=0.3, height=1.2, fill_color="#6B4423", fill_opacity=1, stroke_width=0).next_to(board, DOWN, buff=0)
        sign = VGroup(post, board, board_t).move_to([-3.4, 0.75, 0])
        mena = pill("Middle East & North Africa:\n1 in 6 adults has diabetes", SKYB, 26).move_to([3.3, 0.75, 0])
        self.line(1, FadeOut(p1), FadeOut(p2), FadeOut(q), FadeIn(sign, scale=0.7, shift=UP * 0.3),
                  FadeIn(mena, shift=UP * 0.2), FadeIn(src), rt=0.9)
        self.end_scene()

    # ------------------------------------------------------------ 2. what is prediabetes (gauge + doctor)
    def s2(self):
        self.begin("s02")
        self.title_bar("What Is Prediabetes?", NAVY, sky("#FFF1B8", "#FFD9EC"))
        P = np.array([0.0, -0.55, 0.0])
        R = 2.4
        segs = [(GREEN, 150, "Normal", "Below 5.7%"),
                (YELLOW, 90, "Prediabetes", "5.7% \u2013 6.4%"),
                (RED, 30, "Diabetes", "6.5% or higher")]
        arcs = VGroup(*[Arc(radius=R, start_angle=(a + 28) * DEGREES, angle=-56 * DEGREES, arc_center=P,
                            color=c, stroke_width=44) for c, a, _, _ in segs])
        names = VGroup(*[txt(n, 26, NAVY, True).move_to(P + (R + 0.65) * dirv(a)) for _, a, n, _ in segs])
        label = txt("BLOOD SUGAR (A1C)", 30, NAVY, True).move_to(P + DOWN * 0.85)
        needle = Line(P, P + 1.75 * dirv(150), color=NAVY, stroke_width=9)
        pin = Dot(P, radius=0.2, color="#3D5A8F")
        ranges = VGroup()
        for (c, _, _, r), x in zip(segs, (-3.8, 0.0, 3.2)):
            ranges.add(VGroup(Dot(radius=0.12, color=c), txt(r, 24, NAVY, True)).arrange(RIGHT, buff=0.2).move_to([x, -2.15, 0]))
        a1c = VGroup(E("blood", 1.3), txt("A1C blood test", 22, NAVY, True)).arrange(DOWN, buff=0.2).move_to([-5.7, -0.3, 0])
        doctor = E("doctor_f", 2.7).move_to([5.9, -0.8, 0])
        self.line(0, Create(arcs), FadeIn(names), FadeIn(label), rt=1.6)
        self.line(1, FadeIn(a1c, scale=0.8), FadeIn(needle), FadeIn(pin), FadeIn(ranges), FadeIn(doctor, shift=LEFT * 0.6, scale=0.8), rt=0.8)
        float_(doctor, 0.07, 0.6)
        self.after(1, 1.1)
        self.play(Rotate(needle, angle=-60 * DEGREES, about_point=P), Indicate(arcs[1], scale_factor=1.04, color=NAVY), run_time=0.8)
        self.after(1, 2.5)
        self.play(Rotate(needle, angle=-60 * DEGREES, about_point=P), Indicate(arcs[2], scale_factor=1.04, color=NAVY), run_time=0.8)
        self.at(self.sc["end"] - 1.6)
        self.play(Rotate(needle, angle=60 * DEGREES, about_point=P), Indicate(arcs[1], scale_factor=1.06, color=NAVY), run_time=0.9)
        self.end_scene()

    # ------------------------------------------------------------ 3. what goes wrong inside the body
    def s3(self):
        self.begin("s03")
        self.title_bar("What Goes Wrong Inside the Body", NAVY, sky("#E3F6FF", "#FFE8F3"))

        def panel(x0, head, hc, ok):
            cell = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.9, fill_color=WHITE, fill_opacity=1,
                                    stroke_color=hc, stroke_width=6).move_to([x0, -0.1, 0])
            cl = txt("Cell", 22, NAVY, True).move_to(cell.get_bottom() + UP * 0.3)
            pill_ = RoundedRectangle(corner_radius=0.18, width=1.2, height=0.4,
                                     fill_color=(BLUE if ok else "#B8C4D6"), fill_opacity=1,
                                     stroke_width=0).move_to([x0 - 1.3, -0.1, 0])
            pl = txt("insulin", 18, WHITE, True).move_to(pill_)
            xm = VGroup()
            if not ok:
                xm = VGroup(Line([x0 - 1.5, 0.1, 0], [x0 - 1.1, -0.3, 0], color=RED, stroke_width=8),
                            Line([x0 - 1.5, -0.3, 0], [x0 - 1.1, 0.1, 0], color=RED, stroke_width=8))
            hd = txt(head, 30, hc, True, maxw=5.0).move_to([x0 - 0.75, 1.7, 0])
            hd.set_stroke(WHITE, 6, background=True)
            sg = txt("sugar", 18, NAVY, True).move_to([x0 - 2.8, -0.95, 0])
            dots = VGroup(*[Dot([x0 - 2.8, 0.7 - 0.3 * i, 0], radius=0.13, color=YELLOW) for i in range(5)])
            return VGroup(cell, cl, pill_, pl, xm, hd, sg), dots, pill_, xm

        xl, xr = -2.85, 4.35
        st_l, dots_l, pill_l, _ = panel(xl, "Healthy cells", GREEN, True)
        st_r, dots_r, _, xm_r = panel(xr, "Cells ignore insulin", RED, False)
        ok_cap = pill("Sugar enters the cells", GREEN, 22).move_to([xl - 0.75, -1.85, 0])
        bad_cap = pill("Sugar stays in the blood", RED, 22).move_to([xr - 0.75, -1.85, 0])
        arrow = Arrow([xr - 3.3, -0.8, 0], [xr - 3.3, 0.9, 0], color=RED, buff=0, stroke_width=10)
        tg_l = [[xl - 0.6, 0.35, 0], [xl, 0.35, 0], [xl + 0.6, 0.35, 0], [xl - 0.3, -0.15, 0], [xl + 0.3, -0.15, 0]]
        tg_r = [[xr - 2.05 + 0.25 * (i % 2), 0.55 - 0.27 * i, 0] for i in range(5)]
        self.line(0, FadeIn(st_l), FadeIn(st_r), FadeIn(dots_l), FadeIn(dots_r), rt=0.8)
        self.after(0, 1.4)
        self.play(AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_l, tg_l)], lag_ratio=0.2),
                  Indicate(pill_l, scale_factor=1.12, color=NAVY), run_time=2.2)
        self.play(FadeIn(ok_cap, shift=UP * 0.2), run_time=0.5)
        self.line(1, Indicate(xm_r, scale_factor=1.3, color=RED), rt=0.9)
        self.after(1, 1.1)
        self.play(AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_r, tg_r)], lag_ratio=0.2),
                  FadeIn(arrow, shift=UP * 0.2), FadeIn(bad_cap, shift=UP * 0.2), run_time=1.8)
        self.end_scene()

    # ------------------------------------------------------------ helper for the bubble scenes
    def bubble_scene(self, sid, title, tcolor, bg, items, r, eh, xs, y, lsize, ssize=20,
                     banner_text=None, bcolor=None, first=1, finish=None):
        self.begin(sid)
        self.title_bar(title, tcolor, bg)
        bn = banner(banner_text, bcolor) if banner_text else None
        if first == 1:
            self.line(0, *( [FadeIn(bn, shift=DOWN * 0.2)] if bn else [] ), rt=0.6)
        for i, (sprite, label, color, badge, sub) in enumerate(items):
            b = bubble(sprite, label, color, r=r, eh=eh, lsize=lsize, badge=badge, sub=sub, ssize=ssize).move_to([xs[i], y, 0])
            anims = [FadeIn(b, shift=UP * 0.4, scale=0.6)]
            if first == 0 and i == 0 and bn:
                anims.append(FadeIn(bn, shift=DOWN * 0.2))
            self.line(i + first, *anims, rt=0.7)
            float_(b, 0.07, 0.5, phase=i * 0.9)
        if finish:
            finish()
        self.end_scene()

    # ------------------------------------------------------------ 4. risks you can't change
    def s4(self):
        faces = VGroup(*[E(n, 0.6) for n in ("man_a", "woman_a", "man_b", "woman_b")]).arrange(RIGHT, buff=0.1).scale(0.9)
        globe = VGroup(E("globe", 1.3), faces).arrange(DOWN, buff=0.1)
        self.bubble_scene("s04", "Risks You Can't Change", NAVY, park_bg(), [
            (E("elder", 1.8), "Age", LILAC, "45+", "Risk rises after 45"),
            (E("family", 1.8), "Family history", CORAL, None, "Parent or sibling with\ntype 2 diabetes"),
            (globe, "Ethnic background", SKYB, None, "Middle Eastern, South Asian,\nAfrican, Hispanic"),
        ], r=1.4, eh=1.8, xs=[-4.4, 0, 4.4], y=0.65, lsize=26, ssize=20,
            banner_text="OUT OF YOUR CONTROL", bcolor=RED, first=1)

    # ------------------------------------------------------------ 5. lifestyle (all five cards stay on screen)
    def s5(self):
        diet = VGroup(E("burger", 1.0), E("fries", 0.9), E("cola", 1.0)).arrange(RIGHT, buff=0.05)
        sleep = VGroup(E("sleep", 1.0), E("moon", 0.7)).arrange(RIGHT, buff=0.1)
        self.bubble_scene("s05", "Lifestyle Risks You Can Change", MINTC, sky("#FFE8CC", "#E6FCF5"), [
            (E("balance", 1.3), "Excess\nweight", CORAL, None, None),
            (E("couch", 1.3), "Inactivity", LILAC, None, None),
            (diet, "Unhealthy\ndiet", ORNG, None, None),
            (E("smoke", 1.3), "Smoking", SKYB, None, None),
            (sleep, "Poor\nsleep", PINKB, None, None),
        ], r=1.15, eh=1.4, xs=[-5.6, -2.8, 0, 2.8, 5.6], y=0.7, lsize=22,
            banner_text="YOU CAN CHANGE THESE", bcolor=MINTC, first=1)

    # ------------------------------------------------------------ 6. health conditions (plain words)
    def s6(self):
        chol = VGroup(E("tube", 1.1), E("blood", 0.8)).arrange(RIGHT, buff=0.1)

        def warning():
            box = RoundedRectangle(corner_radius=0.2, width=8.4, height=0.7, fill_color=YELLOW, fill_opacity=0.4,
                                   stroke_color=YELLOW, stroke_width=4).move_to([0, -2.4, 0])
            msg = txt("High risk = a warning, not a diagnosis", 26, NAVY, True).move_to(box)
            self.line(5, FadeIn(box, shift=UP * 0.2), FadeIn(msg), rt=0.8)

        self.bubble_scene("s06", "Health Conditions That Raise Risk", NAVY, office_bg(), [
            (E("stethoscope", 1.3), "High blood\npressure", SKYB, None, None),
            (chol, "Unhealthy\ncholesterol\nor blood fats", ORNG, None, None),
            (E("woman", 1.4), "Hormone\ncondition in\nwomen (PCOS)", PINKB, None, None),
            (E("pregnant", 1.4), "High blood\nsugar during\npregnancy", LILAC, None, None),
            (E("heart_anat", 1.3), "Heart disease\nor stroke", CORAL, None, None),
        ], r=1.05, eh=1.3, xs=[-5.6, -2.8, 0, 2.8, 5.6], y=0.85, lsize=19,
            banner_text="HEALTH CONDITIONS", bcolor=SKYB, first=0, finish=warning)

    # ------------------------------------------------------------ 7. how do you find out (ranges on every card)
    def s7(self):
        self.begin("s07")
        self.title_bar("How Do You Find Out?", NAVY, hospital_bg())
        patient = E("patient", 1.7, flip=FLIP_PEOPLE)
        self.add(patient)
        self.line(0, walk(patient, [-7.5, -1.95, 0], [2.9, -1.95, 0], bobs=10), rt=3.0)
        cards = Group(
            test_card(E("blood", 0.95), "A1C Test", "2\u20133 month average", "Below 5.7%", "5.7% \u2013 6.4%"),
            test_card(E("moon", 0.95), "Fasting Blood Sugar", "After an overnight fast", "Below 100 mg/dL", "100 \u2013 125 mg/dL"),
            test_card(E("cola", 0.95), "Glucose Tolerance Test", "2 hours after a sweet drink", "Below 140 mg/dL", "140 \u2013 199 mg/dL"),
        ).arrange(RIGHT, buff=0.3).move_to([0, -0.3, 0])
        self.line(1, FadeOut(patient), rt=0.4)
        for card, off in zip(cards.submobjects, (0.8, 3.0, 5.0)):
            self.after(1, off)
            self.play(FadeIn(card, shift=UP * 0.4, scale=0.85), run_time=0.7)
        self.line(2, rt=0.4)
        self.end_scene()

    # ------------------------------------------------------------ 8. the good news
    def s8(self):
        self.begin("s08")
        self.title_bar("The Good News: You Can Lower Your Risk", NAVY, park_bg(sun_pos=None))
        sun = sun_obj(-4.2, 0.7, 1.25)
        tr = ValueTracker(0)
        num = always_redraw(lambda: txt(f"{int(tr.get_value())}%", 72, NAVY, True).move_to(np.array([-4.2, 0.7, 0])))
        cap = pill("lower risk of type 2 diabetes", GREEN, 22, maxw=5.0).move_to([-4.2, -1.55, 0])
        src = txt("Source: NIH Diabetes Prevention Program", 17, NAVY, True, maxw=5.4).move_to([-4.2, -2.3, 0])
        src.set_stroke(WHITE, 6, background=True)
        chips = Group(chip(E("balance", 0.7), "Lose 5\u20137% of body weight"),
                      chip(E("run1", 0.7, flip=FLIP_RUN), "150 minutes of activity a week"),
                      chip(E("salad", 0.7), "Eat more whole foods")).arrange(DOWN, buff=0.3).move_to([3.4, 0.5, 0])
        self.line(0, FadeIn(sun, scale=0.6), rt=0.8)
        self.add(num)
        runner = E("run1", 1.5, flip=FLIP_RUN)
        self.add(runner)
        foods = VGroup(*[E(n, 0.75) for n in ("apple", "broccoli", "carrot", "fish", "avocado")]).arrange(RIGHT, buff=0.35)
        foods.move_to([3.4, -1.75, 0])
        self.line(1, FadeIn(cap), FadeIn(src), rt=0.6)
        self.after(1, 0.9)
        self.play(tr.animate.set_value(58), walk(runner, [-8, -1.9, 0], [8, -1.9, 0], bobs=12), run_time=3.4)
        self.remove(runner)
        self.line(2, FadeIn(chips[0], shift=LEFT * 0.3, scale=0.9), rt=0.6)
        self.after(2, 0.9)
        self.play(FadeIn(chips[1], shift=LEFT * 0.3, scale=0.9), run_time=0.6)
        self.after(2, 1.8)
        self.play(FadeIn(chips[2], shift=LEFT * 0.3, scale=0.9), LaggedStart(*[GrowFromCenter(f) for f in foods], lag_ratio=0.2), run_time=1.2)
        self.end_scene()

    # ------------------------------------------------------------ 9. take action (closing slide, stays to the end)
    def s9(self):
        self.begin("s09")
        self.title_bar("Take Action Today", NAVY, park_bg("#FFA35E", "#FFEFB0", sun_pos=(5.9, 2.7)))
        items = [("clipboard", "Learn your risk factors"),
                 ("stethoscope", "Talk to your doctor about a blood test"),
                 ("run1", "Move more, eat well, sleep well"),
                 ("sprout", "Small steps now protect your health for years.")]
        rows = VGroup()
        for n, s in items:
            box = RoundedRectangle(corner_radius=0.25, width=10.2, height=0.68, fill_color=WHITE, fill_opacity=0.95,
                                   stroke_color=WHITE, stroke_width=3)
            icon = E(n, 0.5, flip=(FLIP_RUN if n == "run1" else False)).move_to(box.get_left() + RIGHT * 0.55)
            t = txt(s, 28, NAVY, True, maxw=8.9).next_to(icon, RIGHT, buff=0.3)
            rows.add(VGroup(box, icon, t))
        rows.arrange(DOWN, buff=0.1).move_to([0, 0.5, 0])
        panel = RoundedRectangle(corner_radius=0.25, width=12.6, height=1.9, fill_color=WHITE, fill_opacity=0.88,
                                 stroke_color=WHITE, stroke_width=3).move_to([0, -2.0, 0])
        purpose = txt(textwrap.fill(PURPOSE, 96), 19, NAVY, True, maxw=12.0).move_to([0, -1.55, 0])
        sources = txt(textwrap.fill(SOURCES, 100), 15, GREY, False, maxw=12.0).move_to([0, -2.28, 0])
        credit = txt(CREDIT, 13, GREY, False).move_to([0, -2.72, 0])
        info = VGroup(panel, purpose, sources, credit)
        self.line(0, rt=0.4)
        self.line(1, FadeIn(rows[0], shift=RIGHT * 0.3), rt=0.6)
        self.after(1, 1.0)
        self.play(FadeIn(rows[1], shift=RIGHT * 0.3), run_time=0.6)
        self.after(1, 2.0)
        self.play(FadeIn(rows[2], shift=RIGHT * 0.3), run_time=0.6)
        self.after(1, 3.0)
        self.play(FadeIn(rows[3], shift=RIGHT * 0.3), FadeIn(info, shift=UP * 0.2), run_time=0.8)
        self.line(2, rt=0.4)
