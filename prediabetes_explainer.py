"""
Prediabetes risk explainer (Manim), about 4 minutes, 1080p 60 fps.

Every picture is cued to the start of a narration sentence using the shared timeline in story.py,
so voice, captions and animation stay locked together.

Optional: images/<name>.png replaces a drawn icon (see icons.py `pic` names),
          music.mp3 replaces the music the mixer composes.
"""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from manim import *
from icons import *
from story import build, LEAD

try:
    POP = ease_out_back
except NameError:
    POP = smooth


def make_caption(text):
    t = txt(textwrap.fill(text, 60), 26, NAVY, False)
    if t.width > 12.4:
        t.scale_to_fit_width(12.4)
    box = RoundedRectangle(corner_radius=0.2, width=t.width + 0.6, height=t.height + 0.3,
                           fill_color=WHITE, fill_opacity=0.93, stroke_color=SOFT, stroke_width=2)
    return VGroup(box, t).move_to([0, -3.3, 0])


def banner(text, color):
    t = txt(text, 24, WHITE, True)
    b = RoundedRectangle(corner_radius=0.25, width=t.width + 0.9, height=0.55,
                         fill_color=color, fill_opacity=1, stroke_width=0)
    t.move_to(b)
    return VGroup(b, t).move_to([0, 2.3, 0])


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

    def title_bar(self, text, color=NAVY):
        t = txt(text, 40, color, True, maxw=12.5).to_edge(UP, buff=0.5)
        self.play(FadeIn(t, shift=DOWN * 0.2), run_time=0.45)
        return t

    def end_scene(self):
        self.at(self.sc["end"] - 0.45)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in self.keep], run_time=0.45)
        self.cap = None

    def cards_scene(self, sid, title, tcolor, btext, bcolor, cards, gap):
        self.begin(sid)
        self.title_bar(title, tcolor)
        row = Group(*cards).arrange(RIGHT, buff=gap).move_to([0, -0.15, 0])
        if row.width > 13.2:
            row.scale_to_fit_width(13.2)
        self.line(0, FadeIn(banner(btext, bcolor), shift=DOWN * 0.2))
        for i, c in enumerate(row.submobjects):
            self.line(i + 1, FadeIn(c, shift=UP * 0.3, scale=0.85))
        self.end_scene()

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

    # ------------------------------------------------------------ 1. hook + pictograph
    def s1(self):
        self.begin("s01")
        title = txt("Prediabetes: Are You at Risk?", 44, NAVY, True, maxw=12.5).to_edge(UP, buff=0.55)
        self.play(Write(title), run_time=0.45)
        grid = VGroup(*[person(NAVY, 0.5) for _ in range(25)]).arrange_in_grid(rows=5, cols=5, buff=0.24)
        grid.move_to([-3.6, -0.1, 0])
        reds = [1, 4, 7, 9, 12, 14, 16, 19, 21, 23]
        big = txt("2 in 5", 96, RED, True).move_to([3.6, 1.3, 0])
        sub = txt("US adults have\nprediabetes", 30, NAVY, True).next_to(big, DOWN, buff=0.25)
        unaware = txt("8 in 10 of them\ndon't know it", 32, YELLOW, True).move_to([3.6, -1.0, 0])
        nosym = txt("Often no symptoms", 30, GREEN, True).move_to([3.6, -2.0, 0])
        badges = VGroup()
        for idx in reds[:8]:
            b = VGroup(Circle(radius=0.15, fill_color=YELLOW, fill_opacity=1, stroke_width=0),
                       txt("?", 18, WHITE, True))
            b[1].move_to(b[0])
            badges.add(b.move_to(grid[idx].get_top() + UP * 0.2))
        self.line(0, LaggedStart(*[FadeIn(g, shift=UP * 0.2, scale=0.8) for g in grid], lag_ratio=0.05), rt=1.5)
        self.mid(0, 0.55)
        self.play(*[grid[i].animate.set_color(RED) for i in reds], FadeIn(big, scale=0.7), FadeIn(sub), run_time=0.8)
        self.line(1, LaggedStart(*[GrowFromCenter(b) for b in badges], lag_ratio=0.1),
                  FadeIn(unaware, shift=UP * 0.2), rt=1.2)
        self.line(2, FadeIn(nosym, shift=UP * 0.2), rt=0.7)
        q = txt("What raises\nyour risk?", 48, NAVY, True).move_to([3.6, 0.1, 0])
        self.line(3, FadeOut(big), FadeOut(sub), FadeOut(unaware), FadeOut(nosym), FadeIn(q, scale=0.8), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 2. what is prediabetes (gauge)
    def s2(self):
        self.begin("s02")
        self.title_bar("What Is Prediabetes?")
        P = np.array([0.0, -0.55, 0.0])
        R = 2.4
        segs = [(GREEN, 150, "Normal", "Below 5.7%"),
                (YELLOW, 90, "Prediabetes", "5.7% - 6.4%"),
                (RED, 30, "Diabetes", "6.5% or higher")]
        arcs = VGroup(*[Arc(radius=R, start_angle=(a + 28) * DEGREES, angle=-56 * DEGREES, arc_center=P,
                            color=c, stroke_width=36) for c, a, _, _ in segs])
        names = VGroup(*[txt(n, 26, NAVY, True).move_to(P + (R + 0.6) * dirv(a)) for _, a, n, _ in segs])
        label = txt("BLOOD SUGAR (A1C)", 32, NAVY, True).move_to(P + DOWN * 0.85)
        needle = Line(P, P + 1.75 * dirv(150), color=NAVY, stroke_width=8)
        pin = Dot(P, radius=0.18, color="#3D5A8F")
        ranges = VGroup()
        for (c, _, _, r), x in zip(segs, (-3.8, 0.0, 3.8)):
            ranges.add(VGroup(Dot(radius=0.12, color=c), txt(r, 24, NAVY, True)).arrange(RIGHT, buff=0.2).move_to([x, -2.15, 0]))
        a1c = VGroup(icon_drop().scale(1.1), txt("A1C blood test", 24, NAVY, True)).arrange(DOWN, buff=0.2).move_to([-5.6, -0.3, 0])
        self.line(0, Create(arcs), FadeIn(names), FadeIn(label), rt=1.6)
        self.line(1, FadeIn(a1c, scale=0.8), FadeIn(needle), FadeIn(pin), rt=0.7)
        self.line(2, FadeIn(ranges[0]), Indicate(arcs[0], scale_factor=1.04, color=NAVY), rt=0.8)
        self.line(3, Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[1]),
                  Indicate(arcs[1], scale_factor=1.04, color=NAVY), rt=0.9)
        self.line(4, Rotate(needle, angle=-60 * DEGREES, about_point=P), FadeIn(ranges[2]),
                  Indicate(arcs[2], scale_factor=1.04, color=NAVY), rt=0.9)
        self.end_scene()

    # ------------------------------------------------------------ 3. insulin resistance
    def s3(self):
        self.begin("s03")
        self.title_bar("What Goes Wrong Inside the Body")

        def panel(x0, head, hc, ok):
            cell = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.9, fill_color=WHITE, fill_opacity=1,
                                    stroke_color=hc, stroke_width=5).move_to([x0, -0.1, 0])
            cl = txt("Cell", 22, NAVY, True).move_to(cell.get_bottom() + UP * 0.3)
            pill = RoundedRectangle(corner_radius=0.18, width=1.2, height=0.4,
                                    fill_color=(BLUE if ok else "#B8C4D6"), fill_opacity=1,
                                    stroke_width=0).move_to([x0 - 1.3, -0.1, 0])
            pl = txt("insulin", 18, WHITE, True).move_to(pill)
            xm = VGroup()
            if not ok:
                xm = VGroup(Line([x0 - 1.5, 0.1, 0], [x0 - 1.1, -0.3, 0], color=RED, stroke_width=7),
                            Line([x0 - 1.5, -0.3, 0], [x0 - 1.1, 0.1, 0], color=RED, stroke_width=7))
            hd = txt(head, 30, hc, True, maxw=5.0).move_to([x0 - 0.75, 1.7, 0])
            sg = txt("sugar", 18, GREY).move_to([x0 - 2.8, -0.95, 0])
            dots = VGroup(*[Dot([x0 - 2.8, 0.7 - 0.3 * i, 0], radius=0.11, color=YELLOW) for i in range(5)])
            return VGroup(cell, cl, pill, pl, xm, hd, sg), dots, pill, xm

        xl, xr = -2.85, 4.35
        st_l, dots_l, pill_l, _ = panel(xl, "Healthy", GREEN, True)
        st_r, dots_r, _, xm_r = panel(xr, "Insulin resistance", RED, False)
        ok_cap = txt("Sugar enters the cells", 22, GREEN, True).move_to([xl - 0.75, -1.85, 0])
        bad_cap = txt("Sugar stays in the blood", 22, RED, True).move_to([xr - 0.75, -1.85, 0])
        arrow = Arrow([xr - 3.3, -0.8, 0], [xr - 3.3, 0.9, 0], color=RED, buff=0, stroke_width=8)
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

    # ------------------------------------------------------------ 4-6. card scenes
    def s4(self):
        kw = dict(w=3.9, h=4.0, tsize=28, ssize=20)
        self.cards_scene("s04", "Risks You Can't Change", NAVY, "OUT OF YOUR CONTROL", RED, [
            make_card(pic("age", icon_age), "Age", "Risk rises with age,\nespecially after 45", **kw),
            make_card(pic("family", icon_family), "Family history", "A parent or sibling with\ntype 2 diabetes", **kw),
            make_card(pic("ethnicity", icon_globe), "Ethnicity",
                      "Higher rates in some groups:\nBlack, Hispanic, Asian,\nNative American, Pacific Islander", **kw),
        ], 0.4)

    def s5(self):
        kw = dict(w=2.4, h=4.0, tsize=22)
        self.cards_scene("s05", "Lifestyle Risks You Can Change", GREEN, "YOU CAN CHANGE THESE", GREEN, [
            make_card(pic("weight", icon_scale), "Excess weight", "Extra weight,\nespecially at\nthe belly", **kw),
            make_card(pic("inactivity", icon_sofa), "Inactivity", "Little regular\nphysical\nactivity", **kw),
            make_card(pic("diet", icon_soda), "Sugary diet", "Sugary drinks &\nprocessed\nfoods", **kw),
            make_card(pic("smoking", icon_smoke), "Smoking", "Raises type 2\ndiabetes risk", **kw),
            make_card(pic("sleep", icon_moon), "Poor sleep", "Too little or\ndisrupted\nsleep", **kw),
        ], 0.25)

    def s6(self):
        kw = dict(w=2.4, h=4.0, tsize=22)
        self.cards_scene("s06", "Health Conditions That Raise Risk", NAVY, "HEALTH CONDITIONS", BLUE, [
            make_card(pic("bp", icon_gauge), "High blood\npressure", "Hypertension", **kw),
            make_card(pic("cholesterol", icon_chol), "Abnormal\ncholesterol", "Low HDL or high\ntriglycerides", **kw),
            make_card(pic("pcos", icon_female), "PCOS", "Polycystic ovary\nsyndrome", **kw),
            make_card(pic("gestational", icon_bump), "Gestational\ndiabetes", "Diabetes during\na past pregnancy", **kw),
            make_card(pic("heart", icon_heart_disease), "Heart disease\nor stroke", "A history of\neither", **kw),
        ], 0.25)

    # ------------------------------------------------------------ 7. risks add up
    def s7(self):
        self.begin("s07")
        self.title_bar("Risk Factors Add Up")
        C = np.array([0.0, 0.2, 0.0])
        circle = Circle(radius=1.0, fill_color=GREEN, fill_opacity=1, stroke_color=WHITE, stroke_width=6).move_to(C)
        word = txt("RISK", 26, WHITE, True).move_to(C + UP * 0.3)
        level = txt("LOW", 34, WHITE, True).move_to(C + DOWN * 0.25)
        chips = Group(chip(pic("family", icon_family), "Family history", w=4.4),
                      chip(pic("inactivity", icon_sofa), "Inactivity", w=4.4),
                      chip(pic("weight", icon_scale), "Extra weight", w=4.4),
                      chip(pic("diet", icon_soda), "Unhealthy eating", w=4.4))
        for c, pos in zip(chips.submobjects, ([-3.6, 1.5, 0], [3.6, 1.5, 0], [-3.6, -1.1, 0], [3.6, -1.1, 0])):
            c.move_to(pos)
        links = []
        for c in chips.submobjects:
            d = c.get_center() - C
            links.append(Line(C + d / np.linalg.norm(d) * 1.0, c.get_center(), color=SOFT, stroke_width=5))
        changes = [None, ("ELEVATED", YELLOW), None, ("HIGH", RED)]
        self.line(0, FadeIn(circle, scale=0.7), FadeIn(word), FadeIn(level), rt=0.8)
        for i in range(4):
            anims = [FadeIn(links[i]), FadeIn(chips[i], shift=UP * 0.2, scale=0.85)]
            if changes[i]:
                new = txt(changes[i][0], 26, WHITE, True, maxw=1.7).move_to(level)
                anims += [circle.animate.set_fill(changes[i][1]), Transform(level, new)]
            self.line(i + 1, *anims, rt=0.8)
        self.line(5, Indicate(circle, scale_factor=1.12, color=WHITE), rt=1.0)
        box = RoundedRectangle(corner_radius=0.2, width=9.0, height=0.75, fill_color=YELLOW, fill_opacity=0.25,
                               stroke_color=YELLOW, stroke_width=3).move_to([0, -2.4, 0])
        msg = txt("High risk = a warning, not a diagnosis", 28, NAVY, True).move_to(box)
        self.line(6, FadeIn(box, shift=UP * 0.2), FadeIn(msg), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 8. self-check
    def s8(self):
        self.begin("s08")
        self.title_bar("Quick Self-Check")
        qs = ["Are you over 45?", "Parent or sibling with type 2 diabetes?", "Inactive, or carrying extra weight?"]
        cols = [GREEN, YELLOW, RED]
        rows, boxes, ticks, yeses, lights = [], [], [], [], []
        for i, q in enumerate(qs):
            y = 1.35 - 1.15 * i
            box = RoundedRectangle(corner_radius=0.2, width=9.2, height=0.95, fill_color=WHITE, fill_opacity=1,
                                   stroke_color=SOFT, stroke_width=3).move_to([-1.4, y, 0])
            cb = Square(side_length=0.5, stroke_color=NAVY, stroke_width=4, fill_color=WHITE,
                        fill_opacity=1).move_to(box.get_left() + RIGHT * 0.7)
            t = txt(q, 30, NAVY, True, maxw=7.0).next_to(cb, RIGHT, buff=0.4)
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
            lights.append(Circle(radius=0.3, stroke_color=SOFT, stroke_width=5, fill_opacity=0).move_to([5.3, y, 0]))
        meter = VGroup(*lights)
        meter_label = txt("Risk", 24, GREY, True).move_to([5.3, 2.25, 0])
        self.line(0, FadeIn(meter), FadeIn(meter_label), rt=0.7)
        for i in range(3):
            self.line(i + 1, FadeIn(rows[i], shift=RIGHT * 0.3), rt=0.6)
            self.mid(i + 1, 0.9)
            self.play(Create(ticks[i]), FadeIn(yeses[i], scale=0.7),
                      lights[i].animate.set_fill(cols[i], opacity=1).set_stroke(cols[i]), run_time=0.3)
        self.line(4, Indicate(meter, scale_factor=1.15, color=NAVY), rt=1.0)
        note = VGroup(heart(RED, 0.022), txt("2 or more yes answers: talk to your doctor", 28, NAVY, True, maxw=10))
        note.arrange(RIGHT, buff=0.3).move_to([0, -2.35, 0])
        self.line(5, FadeIn(note, shift=UP * 0.2), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 9. testing
    def s9(self):
        self.begin("s09")
        self.title_bar("How Do You Find Out?")
        hero = icon_glucometer().scale_to_fit_height(2.6).move_to([0, 0.0, 0])
        kw = dict(w=3.9, h=4.0, tsize=28, ssize=20)
        cards = Group(
            make_card(pic("a1c", icon_drop), "A1C test", "Average blood sugar\nover 2-3 months", **kw),
            make_card(pic("fasting", icon_glucometer), "Fasting glucose", "Blood sugar after\nnot eating overnight", **kw),
            make_card(pic("ogtt", icon_glass), "Glucose tolerance", "Blood sugar before and\n2 hours after a sugary drink", **kw),
        ).arrange(RIGHT, buff=0.4).move_to([0, -0.1, 0])
        note = txt("Ask your doctor how often you should be screened", 28, NAVY, True, maxw=12).move_to([0, -2.4, 0])
        self.line(0, FadeIn(hero, scale=0.6), rt=0.8)
        self.line(1, FadeOut(hero), FadeIn(cards[0], shift=UP * 0.3, scale=0.85), rt=0.7)
        self.line(2, FadeIn(cards[1], shift=UP * 0.3, scale=0.85), rt=0.7)
        self.line(3, FadeIn(cards[2], shift=UP * 0.3, scale=0.85), rt=0.7)
        self.line(4, FadeIn(note, shift=UP * 0.2), rt=0.8)
        self.end_scene()

    # ------------------------------------------------------------ 10. good news
    def s10(self):
        self.begin("s10")
        self.title_bar("The Good News: You Can Lower Your Risk", GREEN)
        tr = ValueTracker(0)
        num = always_redraw(lambda: txt(f"{int(tr.get_value())}%", 120, GREEN, True).move_to(np.array([-3.9, 0.45, 0])))
        hrt = heart(GREEN, 0.035).move_to([-3.9, 2.0, 0])
        cap = txt("lower risk of type 2 diabetes\nwith lifestyle changes", 26, NAVY, True, maxw=5.6).move_to([-3.9, -0.95, 0])
        src = txt("Diabetes Prevention Program (NIH study)", 18, GREY, maxw=5.6).move_to([-3.9, -1.8, 0])
        chips = Group(chip(pic("scale", icon_scale), "Lose 5-7% of body weight"),
                      chip(pic("activity", icon_run), "150 minutes of activity a week"),
                      chip(pic("apple", icon_apple), "Eat more whole foods")).arrange(DOWN, buff=0.35).move_to([3.4, -0.1, 0])
        self.add(num)
        self.line(0, GrowFromCenter(hrt), rt=0.7)
        self.line(1, FadeIn(cap), FadeIn(src), rt=0.6)
        self.mid(1, 0.55)
        self.play(tr.animate.set_value(58), run_time=2.0)
        for i in range(3):
            self.line(i + 2, FadeIn(chips[i], shift=LEFT * 0.3, scale=0.9), rt=0.7)
        self.end_scene()

    # ------------------------------------------------------------ 11. call to action
    def s11(self):
        self.begin("s11")
        self.title_bar("Take Action Today", GREEN)
        items = ["Learn your risk factors", "Talk to your doctor about a blood test",
                 "Move more, eat well, sleep well", "Small steps now protect your health"]
        rows = VGroup(*[VGroup(check_icon(), txt(s, 34, NAVY, True)).arrange(RIGHT, buff=0.4) for s in items])
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0, 0.2, 0])
        if rows.width > 12.5:
            rows.scale_to_fit_width(12.5)
        src = txt("Sources: CDC, American Diabetes Association, NIH Diabetes Prevention Program", 18, GREY, maxw=12).move_to([0, -2.45, 0])
        self.line(0, rt=0.4)
        for i in range(4):
            self.line(i + 1, FadeIn(rows[i], shift=RIGHT * 0.3), rt=0.7)
        self.line(5, FadeIn(src), rt=0.8)
        self.end_scene()
