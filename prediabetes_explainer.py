"""
Prediabetes risk explainer, version 3: bright scenes with illustrated people, hospital, park and food.
Every picture is cued to the start of a narration sentence (timeline in story.py).
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
        self.play(*anims, run_time=0.32)
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
        for scene in (self.s1, self.s2, self.s3, self.s4, self.s5, self.s6,
                      self.s7, self.s8, self.s9, self.s10, self.s11):
            scene()
        self.at(self.total)

    # ------------------------------------------------------------ 1. hook: a crowd in the park
    def s1(self):
        self.begin("s01")
        self.title_bar("Prediabetes: Are You at Risk?", NAVY, park_bg())
        names = ["walk1", "walk2", "walk3", "walk4", "walk5"] * 2
        xs = np.linspace(-5.4, 5.4, 10)
        y = -1.35
        walkers = []
        for n in names:
            sprite = E(n, 1.5, flip=FLIP_PEOPLE)
            halo = Circle(radius=0.85, fill_color=RED, fill_opacity=0, stroke_color=RED, stroke_width=0).move_to(sprite)
            walkers.append(VGroup(halo, sprite))
        self.add(*walkers)
        starts = [[x - 13, y, 0] for x in xs]
        reds = [1, 4, 6, 9]
        self.line(0, LaggedStart(*[walk(w, s, [x, y, 0], bobs=8) for w, s, x in zip(walkers, starts, xs)], lag_ratio=0.08), rt=3.6)
        p1 = pill("2 in 5 US adults", CORAL, 46).move_to([0, 1.75, 0])
        self.mid(0, 0.7)
        self.play(*[walkers[i][0].animate.set_fill(RED, opacity=0.4).set_stroke(RED, width=6) for i in reds],
                  FadeIn(p1, scale=0.7), run_time=0.8)
        for k, w in enumerate(walkers):
            float_(w, 0.04, 1.1, phase=k * 0.7)
        p2 = pill("8 in 10 of them don't know it", ORNG, 34).move_to([0, 0.75, 0])
        marks = VGroup()
        for i in reds[:3]:
            q = VGroup(Circle(radius=0.2, fill_color=YELLOW, fill_opacity=1, stroke_color=WHITE, stroke_width=3), txt("?", 24, WHITE, True))
            q[1].move_to(q[0])
            marks.add(q.move_to(walkers[i].get_top() + UP * 0.35))
        self.line(1, FadeIn(p2, shift=UP * 0.2), LaggedStart(*[GrowFromCenter(q) for q in marks], lag_ratio=0.15), rt=1.0)
        p3 = pill("Often no symptoms", MINTC, 32).move_to([0, -0.2, 0])
        fine = speech("I feel fine!", NAVY, 24).next_to(walkers[4], UP, buff=0.15)
        self.line(2, FadeIn(p3, shift=UP * 0.2), FadeIn(fine, scale=0.8), rt=0.8)
        board = RoundedRectangle(corner_radius=0.2, width=5.2, height=1.5, fill_color="#A9743A", fill_opacity=1,
                                 stroke_color="#6B4423", stroke_width=6)
        board_t = txt("What raises\nyour risk?", 40, WHITE, True).move_to(board)
        post = Rectangle(width=0.3, height=1.4, fill_color="#6B4423", fill_opacity=1, stroke_width=0).next_to(board, DOWN, buff=0)
        sign = VGroup(post, board, board_t).move_to([0, 0.5, 0])
        self.line(3, FadeOut(p1), FadeOut(p2), FadeOut(p3), FadeOut(fine), FadeOut(marks),
                  FadeIn(sign, scale=0.7, shift=UP * 0.3), rt=0.9)
        self.end_scene()

    # ------------------------------------------------------------ 2. what is prediabetes (gauge + doctor)
    def s2(self):
        self.begin("s02")
        self.title_bar("What Is Prediabetes?", NAVY, sky("#FFF1B8", "#FFD9EC"))
        P = np.array([0.0, -0.55, 0.0])
        R = 2.4
        segs = [(GREEN, 150, "Normal", "Below 5.7%"),
                (YELLOW, 90, "Prediabetes", "5.7% - 6.4%"),
                (RED, 30, "Diabetes", "6.5% or higher")]
        arcs = VGroup(*[Arc(radius=R, start_angle=(a + 28) * DEGREES, angle=-56 * DEGREES, arc_center=P,
                            color=c, stroke_width=44) for c, a, _, _ in segs])
        names = VGroup(*[txt(n, 26, NAVY, True).move_to(P + (R + 0.65) * dirv(a)) for _, a, n, _ in segs])
        label = txt("BLOOD SUGAR (A1C)", 32, NAVY, True).move_to(P + DOWN * 0.85)
        needle = Line(P, P + 1.75 * dirv(150), color=NAVY, stroke_width=9)
        pin = Dot(P, radius=0.2, color="#3D5A8F")
        ranges = VGroup()
        for (c, _, _, r), x in zip(segs, (-3.8, 0.0, 3.2)):
            ranges.add(VGroup(Dot(radius=0.12, color=c), txt(r, 24, NAVY, True)).arrange(RIGHT, buff=0.2).move_to([x, -2.15, 0]))
        a1c = VGroup(E("blood", 1.3), txt("A1C blood test", 24, NAVY, True)).arrange(DOWN, buff=0.2).move_to([-5.7, -0.3, 0])
        doctor = E("doctor_f", 2.7).move_to([5.9, -0.8, 0])
        self.line(0, Create(arcs), FadeIn(names), FadeIn(label), rt=1.6)
        self.line(1, FadeIn(a1c, scale=0.8), FadeIn(needle), FadeIn(pin), FadeIn(doctor, shift=LEFT * 0.6, scale=0.8), rt=0.8)
        float_(doctor, 0.07, 0.6)
        self.line(2, FadeIn(ranges[0]), Indicate(arcs[0], scale_factor=1.04, color=NAVY), rt=0.8)
        self.line(3, Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[1]),
                  Indicate(arcs[1], scale_factor=1.04, color=NAVY), rt=0.9)
        self.line(4, Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[2]),
                  Indicate(arcs[2], scale_factor=1.04, color=NAVY), rt=0.9)
        self.end_scene()

    # ------------------------------------------------------------ 3. insulin resistance
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
        st_l, dots_l, pill_l, _ = panel(xl, "Healthy", GREEN, True)
        st_r, dots_r, _, xm_r = panel(xr, "Insulin resistance", RED, False)
        ok_cap = pill("Sugar enters the cells", GREEN, 22).move_to([xl - 0.75, -1.85, 0])
        bad_cap = pill("Sugar stays in the blood", RED, 22).move_to([xr - 0.75, -1.85, 0])
        arrow = Arrow([xr - 3.3, -0.8, 0], [xr - 3.3, 0.9, 0], color=RED, buff=0, stroke_width=10)
        tg_l = [[xl - 0.6, 0.35, 0], [xl, 0.35, 0], [xl + 0.6, 0.35, 0], [xl - 0.3, -0.15, 0], [xl + 0.3, -0.15, 0]]
        tg_r = [[xr - 2.05 + 0.25 * (i % 2), 0.55 - 0.27 * i, 0] for i in range(5)]
        self.line(0, FadeIn(st_l), FadeIn(st_r), FadeIn(dots_l), FadeIn(dots_r), rt=1.0)
        self.line(1, AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_l, tg_l)], lag_ratio=0.2),
                  Indicate(pill_l, scale_factor=1.12, color=NAVY), rt=2.4)
        self.mid(1, 0.75)
        self.play(FadeIn(ok_cap, shift=UP * 0.2), run_time=0.5)
        self.line(2, Indicate(xm_r, scale_factor=1.3, color=RED), rt=0.9)
        self.line(3, AnimationGroup(*[d.animate.move_to(t) for d, t in zip(dots_r, tg_r)], lag_ratio=0.2),
                  FadeIn(arrow, shift=UP * 0.2), FadeIn(bad_cap, shift=UP * 0.2), rt=2.0)
        self.end_scene()

    # ------------------------------------------------------------ helper for the bubble scenes
    def bubble_scene(self, sid, title, tcolor, bg, btext, bcolor, items, r, eh, xs, y, lsize, gap_after=None):
        self.begin(sid)
        self.title_bar(title, tcolor, bg)
        bn = banner(btext, bcolor)
        self.line(0, FadeIn(bn, shift=DOWN * 0.2), rt=0.6)
        for i, (sprite, label, color, badge) in enumerate(items):
            b = bubble(sprite, label, color, r=r, eh=eh, lsize=lsize, badge=badge).move_to([xs[i], y, 0])
            self.line(i + 1, FadeIn(b, shift=UP * 0.4, scale=0.6), rt=0.7)
            float_(b, 0.07, 0.5, phase=i * 0.9)
        self.end_scene()

    # ------------------------------------------------------------ 4. risks you can't change (family park)
    def s4(self):
        faces = VGroup(*[E(n, 0.6) for n in ("man_a", "woman_a", "man_b", "woman_b")])
        globe = VGroup(E("globe", 1.3), faces.arrange(RIGHT, buff=0.1).scale(0.9)).arrange(DOWN, buff=0.1)
        self.bubble_scene("s04", "Risks You Can't Change", NAVY, park_bg(), "OUT OF YOUR CONTROL", RED, [
            (E("elder", 1.8), "Age", LILAC, "45+"),
            (E("family", 1.8), "Family history", CORAL, None),
            (globe, "Ethnicity", SKYB, None),
        ], r=1.5, eh=1.9, xs=[-4.4, 0, 4.4], y=0.5, lsize=28)

    # ------------------------------------------------------------ 5. lifestyle (things you can change)
    def s5(self):
        diet = VGroup(E("burger", 1.0), E("fries", 0.9), E("cola", 1.0)).arrange(RIGHT, buff=0.05)
        sleep = VGroup(E("sleep", 1.0), E("moon", 0.7)).arrange(RIGHT, buff=0.1)
        self.bubble_scene("s05", "Lifestyle Risks You Can Change", MINTC, sky("#FFE8CC", "#E6FCF5"),
                          "YOU CAN CHANGE THESE", MINTC, [
                              (E("balance", 1.3), "Extra weight", CORAL, None),
                              (E("couch", 1.3), "Inactivity", LILAC, None),
                              (diet, "Sugary diet", ORNG, None),
                              (E("smoke", 1.3), "Smoking", SKYB, None),
                              (sleep, "Poor sleep", PINKB, None),
                          ], r=1.15, eh=1.4, xs=[-5.5, -2.75, 0, 2.75, 5.5], y=0.5, lsize=24)

    # ------------------------------------------------------------ 6. health conditions (doctor's office)
    def s6(self):
        chol = VGroup(E("tube", 1.1), E("blood", 0.8)).arrange(RIGHT, buff=0.1)
        self.bubble_scene("s06", "Health Conditions That Raise Risk", NAVY, office_bg(),
                          "HEALTH CONDITIONS", SKYB, [
                              (E("stethoscope", 1.3), "High blood\npressure", SKYB, None),
                              (chol, "Abnormal\ncholesterol", ORNG, None),
                              (E("woman", 1.4), "PCOS", PINKB, None),
                              (E("pregnant", 1.4), "Gestational\ndiabetes", LILAC, None),
                              (E("heart_anat", 1.3), "Heart disease\nor stroke", CORAL, None),
                          ], r=1.1, eh=1.3, xs=[-5.5, -2.75, 0, 2.75, 5.5], y=0.6, lsize=22)

    # ------------------------------------------------------------ 7. risks add up
    def s7(self):
        self.begin("s07")
        self.title_bar("Risk Factors Add Up", NAVY, sky("#E7F5FF", "#FFF4E6"))
        C = np.array([0.0, 0.2, 0.0])
        circle = Circle(radius=1.0, fill_color=GREEN, fill_opacity=1, stroke_color=WHITE, stroke_width=8).move_to(C)
        word = txt("RISK", 26, WHITE, True).move_to(C + UP * 0.3)
        level = txt("LOW", 34, WHITE, True).move_to(C + DOWN * 0.25)
        chips = Group(chip(E("family", 0.7), "Family history", w=4.4),
                      chip(E("couch", 0.7), "Inactivity", w=4.4),
                      chip(E("balance", 0.7), "Extra weight", w=4.4),
                      chip(E("burger", 0.7), "Unhealthy eating", w=4.4))
        for c, pos in zip(chips.submobjects, ([-3.6, 1.5, 0], [3.6, 1.5, 0], [-3.6, -1.1, 0], [3.6, -1.1, 0])):
            c.move_to(pos)
        links = []
        for c in chips.submobjects:
            d = c.get_center() - C
            links.append(Line(C + d / np.linalg.norm(d) * 1.0, c.get_center(), color=WHITE, stroke_width=7))
        changes = [None, ("ELEVATED", YELLOW), None, ("HIGH", RED)]
        self.line(0, FadeIn(circle, scale=0.7), FadeIn(word), FadeIn(level), rt=0.8)
        for i in range(4):
            anims = [FadeIn(links[i]), FadeIn(chips[i], shift=UP * 0.2, scale=0.85)]
            if changes[i]:
                new = txt(changes[i][0], 26, WHITE, True, maxw=1.7).move_to(level)
                anims += [circle.animate.set_fill(changes[i][1]), Transform(level, new)]
            self.line(i + 1, *anims, rt=0.8)
        self.line(5, Indicate(circle, scale_factor=1.12, color=WHITE), rt=1.0)
        box = RoundedRectangle(corner_radius=0.2, width=9.0, height=0.75, fill_color=YELLOW, fill_opacity=0.35,
                               stroke_color=YELLOW, stroke_width=4).move_to([0, -2.4, 0])
        msg = txt("High risk = a warning, not a diagnosis", 28, NAVY, True).move_to(box)
        self.line(6, FadeIn(box, shift=UP * 0.2), FadeIn(msg), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 8. self-check with the doctor
    def s8(self):
        self.begin("s08")
        self.title_bar("Quick Self-Check", NAVY, office_bg())
        qs = ["Are you over 45?", "Parent or sibling with type 2 diabetes?", "Inactive, or carrying extra weight?"]
        rows, ticks, yeses = [], [], []
        for i, q in enumerate(qs):
            y = 1.35 - 1.15 * i
            box = RoundedRectangle(corner_radius=0.2, width=8.6, height=0.95, fill_color=WHITE, fill_opacity=1,
                                   stroke_color=SOFT, stroke_width=3).move_to([-1.5, y, 0])
            cb = Square(side_length=0.5, stroke_color=NAVY, stroke_width=4, fill_color=WHITE,
                        fill_opacity=1).move_to(box.get_left() + RIGHT * 0.7)
            t = txt(q, 30, NAVY, True, maxw=6.2).next_to(cb, RIGHT, buff=0.4)
            c = cb.get_center()
            tick = VMobject(stroke_color=GREEN, stroke_width=9).set_points_as_corners(
                [c + np.array([-0.12, 0.0, 0]), c + np.array([-0.03, -0.12, 0]), c + np.array([0.15, 0.13, 0])])
            yes = VGroup(RoundedRectangle(corner_radius=0.2, width=1.1, height=0.55, fill_color=GREEN,
                                           fill_opacity=1, stroke_width=0), txt("YES", 24, WHITE, True))
            yes[1].move_to(yes[0])
            yes.move_to(box.get_right() + LEFT * 0.9)
            rows.append(Group(box, cb, t))
            ticks.append(tick)
            yeses.append(yes)
        face = E("face_smile", 1.3).move_to([5.4, 2.0, 0])
        doctor = E("doctor_f", 3.0).move_to([5.4, -0.9, 0])
        face_names = ["face_neutral", "face_worried", "face_worried"]
        self.line(0, FadeIn(doctor, shift=LEFT * 0.6, scale=0.8), FadeIn(face, scale=0.7), rt=0.8)
        float_(doctor, 0.06, 0.6)
        for i in range(3):
            self.line(i + 1, FadeIn(rows[i], shift=RIGHT * 0.3), rt=0.6)
            self.mid(i + 1, 0.9)
            new_face = E(face_names[i], 1.3).move_to(face)
            self.play(Create(ticks[i]), FadeIn(yeses[i], scale=0.7), FadeTransform(face, new_face), run_time=0.35)
            face = new_face
        self.line(4, Indicate(face, scale_factor=1.25), rt=1.0)
        note = speech("Talk to your doctor!", NAVY, 28).move_to([1.8, -2.2, 0])
        self.line(5, FadeIn(note, shift=UP * 0.2, scale=0.8), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 9. going to the hospital for tests
    def s9(self):
        self.begin("s09")
        self.title_bar("How Do You Find Out?", NAVY, hospital_bg())
        patient = E("patient", 1.7, flip=FLIP_PEOPLE)
        self.add(patient)
        self.line(0, walk(patient, [-7.5, -1.95, 0], [2.9, -1.95, 0], bobs=10), rt=3.2)
        doctor = E("doctor_f", 2.3).move_to([1.2, -1.5, 0])
        tests = [("A1C test", E("blood", 0.9), CORAL), ("Fasting glucose", E("moon", 0.9), LILAC),
                 ("Glucose tolerance test", E("cola", 0.9), ORNG)]
        for i, (label, sprite, color) in enumerate(tests):
            circ = Circle(radius=0.7, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=6)
            sprite.move_to(circ)
            lab = txt(label, 28, NAVY, True, maxw=3.6)
            lab.set_stroke(WHITE, 8, background=True)
            row = VGroup(circ, sprite)
            lab.next_to(circ, RIGHT, buff=0.3)
            g = VGroup(row, lab).move_to([-4.3, 1.55 - 1.35 * i, 0])
            anims = [FadeIn(g, shift=RIGHT * 0.4, scale=0.8)]
            if i == 0:
                anims += [FadeOut(patient), FadeIn(doctor, scale=0.8)]
            self.line(i + 1, *anims, rt=0.7)
        note = banner("Ask your doctor how often to be screened", NAVY, x=-2.3)
        self.line(4, FadeIn(note, shift=DOWN * 0.2), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 10. the good news: sunshine, exercise, food
    def s10(self):
        self.begin("s10")
        self.title_bar("The Good News: You Can Lower Your Risk", NAVY, park_bg(sun_pos=None))
        sun = sun_obj(-4.2, 0.7, 1.25)
        tr = ValueTracker(0)
        num = always_redraw(lambda: txt(f"{int(tr.get_value())}%", 72, NAVY, True).move_to(np.array([-4.2, 0.7, 0])))
        cap = pill("lower risk of type 2 diabetes", GREEN, 24, maxw=5.4).move_to([-4.2, -1.55, 0])
        src = txt("Diabetes Prevention Program (NIH study)", 18, NAVY, True, maxw=5.4).move_to([-4.2, -2.3, 0])
        src.set_stroke(WHITE, 6, background=True)
        chips = Group(chip(E("balance", 0.7), "Lose 5-7% of body weight"),
                      chip(E("run1", 0.7, flip=FLIP_RUN), "150 minutes of activity a week"),
                      chip(E("salad", 0.7), "Eat more whole foods")).arrange(DOWN, buff=0.3).move_to([3.4, 0.5, 0])
        self.line(0, FadeIn(sun, scale=0.6), rt=0.8)
        self.add(num)
        self.line(1, FadeIn(cap), FadeIn(src), rt=0.6)
        self.mid(1, 0.55)
        self.play(tr.animate.set_value(58), run_time=2.0)
        self.line(2, FadeIn(chips[0], shift=LEFT * 0.3, scale=0.9), rt=0.7)
        runner = E("run1", 1.5, flip=FLIP_RUN)
        self.add(runner)
        self.line(3, FadeIn(chips[1], shift=LEFT * 0.3, scale=0.9), walk(runner, [-8, -1.9, 0], [8, -1.9, 0], bobs=14), rt=3.4)
        self.remove(runner)
        foods = VGroup(*[E(n, 0.75) for n in ("apple", "broccoli", "carrot", "fish", "avocado")]).arrange(RIGHT, buff=0.35)
        foods.move_to([3.4, -1.75, 0])
        self.line(4, FadeIn(chips[2], shift=LEFT * 0.3, scale=0.9), LaggedStart(*[GrowFromCenter(f) for f in foods], lag_ratio=0.2), rt=1.4)
        self.end_scene()

    # ------------------------------------------------------------ 11. call to action: sunrise walk
    def s11(self):
        self.begin("s11")
        self.title_bar("Take Action Today", NAVY, park_bg("#FFA35E", "#FFEFB0", sun_pos=(5.9, 2.7)))
        items = [("clipboard", "Learn your risk factors"), ("stethoscope", "Talk to your doctor about a blood test"),
                 ("run1", "Move more, eat well, sleep well"), ("sprout", "Small steps now protect your health")]
        rows = VGroup()
        for n, s in items:
            box = RoundedRectangle(corner_radius=0.25, width=9.8, height=0.85, fill_color=WHITE, fill_opacity=0.93,
                                   stroke_color=WHITE, stroke_width=3)
            icon = E(n, 0.62, flip=(FLIP_RUN if n == "run1" else False)).move_to(box.get_left() + RIGHT * 0.65)
            t = txt(s, 30, NAVY, True, maxw=8.3).next_to(icon, RIGHT, buff=0.35)
            rows.add(VGroup(box, icon, t))
        rows.arrange(DOWN, buff=0.2).move_to([0, 0.1, 0])
        src = txt("Sources: CDC, ADA, NIH Diabetes Prevention Program  |  Illustrations: Twemoji (CC-BY 4.0)", 18, NAVY, True, maxw=12)
        src.set_stroke(WHITE, 6, background=True)
        src.move_to([0, 2.35, 0])
        walker = E("walk1", 0.9, flip=FLIP_PEOPLE)
        self.add(walker)
        self.line(0, FadeIn(src), rt=0.4)
        for i in range(4):
            self.line(i + 1, FadeIn(rows[i], shift=RIGHT * 0.3), rt=0.7)
        self.line(5, walk(walker, [-7.5, -2.45, 0], [6.5, -2.45, 0], bobs=14, amp=0.07), rt=4.0)
        self.end_scene()
