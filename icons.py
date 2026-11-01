"""Drawn icons and layout helpers for the prediabetes video."""
import os

import numpy as np
from manim import *


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


