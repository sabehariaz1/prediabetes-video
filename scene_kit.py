"""Bright scenery, illustrated people and animation helpers."""
import os

import numpy as np
from manim import *
from icons import *

SKY_TOP, SKY_BOT = "#5BC0FF", "#E3F6FF"
SUNY, CORAL, ORNG, LILAC = "#FFD43B", "#FF6B6B", "#FF922B", "#9775FA"
MINTC, SKYB, PINKB = "#20C997", "#4DABF7", "#F783AC"
GRASS1, GRASS2 = "#69DB7C", "#40C057"
ASSET_DIR = "assets"
FLIP_PEOPLE = False   # set True if the walking people move backwards
FLIP_RUN = False      # set True if the runner moves backwards


# ---------------------------------------------------------------- illustrations
def _fallback(name):
    table = {
        "couch": icon_sofa, "cola": icon_soda, "moon": icon_moon, "balance": icon_scale, "blood": icon_drop,
        "heart_anat": icon_heart_disease, "smoke": icon_smoke, "apple": icon_apple, "stethoscope": icon_gauge,
        "family": icon_family, "globe": icon_globe, "run1": icon_run, "run2": icon_run, "syringe": icon_glucometer,
        "doctor_f": lambda: person(BLUE, 1.6), "doctor_m": lambda: person(BLUE, 1.6),
        "patient": lambda: person(YELLOW, 1.2), "heart": lambda: heart(RED, 0.05),
    }
    if name.startswith("walk"):
        return lambda: person(NAVY, 1.2)
    return table.get(name)


def _generic(name):
    c = Circle(radius=0.5, fill_color=SOFT, fill_opacity=1, stroke_color=NAVY, stroke_width=3)
    return VGroup(c, txt(name[:6], 14, NAVY, True).move_to(c))


def E(name, h=1.0, flip=False, fallback=None):
    """An illustration by name (assets/<name>.svg), or a simple drawn stand-in."""
    m = None
    p = os.path.join(ASSET_DIR, name + ".svg")
    if os.path.exists(p):
        try:
            m = SVGMobject(p, height=h)
            m.set_stroke(width=0)
        except Exception as e:
            print("could not load", name, e)
            m = None
    if m is None:
        fb = fallback or _fallback(name)
        m = fb() if fb else _generic(name)
        m.scale_to_fit_height(h)
    if flip:
        m.flip(UP)
    return m


# ---------------------------------------------------------------- scenery
def sky(top=SKY_TOP, bot=SKY_BOT, n=12):
    h = 8.2 / n
    cols = color_gradient([top, bot], n)
    return VGroup(*[Rectangle(width=14.5, height=h + 0.02, fill_color=cols[i], fill_opacity=1,
                              stroke_width=0).move_to([0, 4.1 - h * (i + 0.5), 0]) for i in range(n)])


def cloud(x, y, s=1.0, speed=0.15):
    kw = dict(fill_color=WHITE, fill_opacity=0.95, stroke_width=0)
    c = VGroup(Circle(radius=0.45 * s, **kw).move_to([x, y, 0]),
               Circle(radius=0.6 * s, **kw).move_to([x + 0.5 * s, y + 0.15 * s, 0]),
               Circle(radius=0.45 * s, **kw).move_to([x + 1.0 * s, y, 0]),
               RoundedRectangle(corner_radius=0.2 * s, width=1.5 * s, height=0.45 * s, **kw).move_to([x + 0.5 * s, y - 0.15 * s, 0]))

    def upd(m, dt):
        m.shift(RIGHT * speed * dt)
        if m.get_left()[0] > 8:
            m.shift(LEFT * 17)

    c.add_updater(upd)
    return c


def sun_obj(x, y, r=0.7):
    center = np.array([x, y, 0.0])
    glow = Circle(radius=r * 1.5, fill_color=SUNY, fill_opacity=0.25, stroke_width=0).move_to(center)
    core = Circle(radius=r, fill_color=SUNY, fill_opacity=1, stroke_color="#FFE066", stroke_width=6).move_to(center)
    rays = VGroup(*[Line(center + dirv(a) * (r + 0.25), center + dirv(a) * (r + 0.55), color=SUNY, stroke_width=8)
                    for a in range(0, 360, 30)])
    rays.add_updater(lambda m, dt: m.rotate(dt * 0.4, about_point=center))
    return VGroup(glow, rays, core)


def tree(x, y, s=1.0):
    trunk = RoundedRectangle(corner_radius=0.08 * s, width=0.28 * s, height=0.9 * s, fill_color="#8D5A2B",
                             fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    leaves = VGroup(
        Circle(radius=0.45 * s, fill_color=GRASS1, fill_opacity=1, stroke_width=0).move_to([x - 0.4 * s, y + 0.5 * s, 0]),
        Circle(radius=0.45 * s, fill_color=GRASS1, fill_opacity=1, stroke_width=0).move_to([x + 0.4 * s, y + 0.5 * s, 0]),
        Circle(radius=0.58 * s, fill_color=GRASS2, fill_opacity=1, stroke_width=0).move_to([x, y + 0.8 * s, 0]))
    return VGroup(trunk, leaves)


def park_bg(top=SKY_TOP, bot=SKY_BOT, sun_pos=(5.8, 2.9)):
    g = VGroup(sky(top, bot))
    if sun_pos is not None:
        g.add(sun_obj(sun_pos[0], sun_pos[1], 0.6))
    g.add(cloud(-4.5, 2.5, 0.9, 0.12), cloud(1.0, 3.1, 0.7, 0.1))
    g.add(Ellipse(width=18, height=4.6, fill_color="#8CE99A", fill_opacity=1, stroke_width=0).move_to([-3, -3.5, 0]),
          Ellipse(width=18, height=4.2, fill_color=GRASS1, fill_opacity=1, stroke_width=0).move_to([5, -3.7, 0]),
          Ellipse(width=13, height=0.9, fill_color="#FFE8A3", fill_opacity=0.95, stroke_width=0).move_to([0, -2.55, 0]))
    g.add(tree(-6.3, -1.9, 1.2), tree(6.5, -1.7, 1.1), tree(-3.0, -1.6, 0.8), tree(3.4, -1.5, 0.7))
    return g


def hospital_bg():
    g = VGroup(sky())
    g.add(sun_obj(-5.8, 2.9, 0.6), cloud(-3.0, 2.4, 0.9, 0.12))
    g.add(Rectangle(width=14.5, height=1.25, fill_color="#8CE99A", fill_opacity=1, stroke_width=0).move_to([0, -3.4, 0]),
          Rectangle(width=14.5, height=0.6, fill_color="#DEE2E6", fill_opacity=1, stroke_width=0).move_to([0, -2.65, 0]))
    g.add(Rectangle(width=5.6, height=3.9, fill_color="#F8FAFC", fill_opacity=1, stroke_color="#CBD5E1",
                    stroke_width=4).move_to([3.4, -0.45, 0]))
    for row_y, cols in ((0.9, (1.5, 2.7, 4.1, 5.3)), (0.0, (1.5, 2.7, 4.1, 5.3)), (-0.9, (1.5, 5.3))):
        for cx in cols:
            g.add(Square(side_length=0.7, fill_color="#A5D8FF", fill_opacity=1, stroke_color=WHITE,
                         stroke_width=4).move_to([cx, row_y, 0]))
    g.add(Rectangle(width=1.2, height=1.2, fill_color="#74C0FC", fill_opacity=1, stroke_color=WHITE,
                    stroke_width=4).move_to([3.4, -1.8, 0]))
    sign = Circle(radius=0.42, fill_color=RED, fill_opacity=1, stroke_color=WHITE, stroke_width=5).move_to([3.4, 1.85, 0])
    plus = VGroup(Rectangle(width=0.5, height=0.14, fill_color=WHITE, fill_opacity=1, stroke_width=0),
                  Rectangle(width=0.14, height=0.5, fill_color=WHITE, fill_opacity=1, stroke_width=0)).move_to(sign)
    g.add(sign, plus, tree(-5.4, -2.3, 1.1), tree(6.9, -2.3, 0.8))
    return g


def office_bg():
    g = VGroup(Rectangle(width=14.5, height=8.2, fill_color="#C3FAE8", fill_opacity=1, stroke_width=0),
               Rectangle(width=14.5, height=1.3, fill_color="#FFD8A8", fill_opacity=1, stroke_width=0).move_to([0, -3.45, 0]),
               Rectangle(width=14.5, height=0.12, fill_color="#FFC078", fill_opacity=1, stroke_width=0).move_to([0, -2.85, 0]))
    win = RoundedRectangle(corner_radius=0.1, width=2.2, height=1.8, fill_color=SKY_TOP, fill_opacity=1,
                           stroke_color=WHITE, stroke_width=10).move_to([-5.8, 1.5, 0])
    g.add(win, Line(win.get_top(), win.get_bottom(), color=WHITE, stroke_width=8),
          Line(win.get_left(), win.get_right(), color=WHITE, stroke_width=8))
    g.add(RoundedRectangle(corner_radius=0.08, width=0.7, height=0.55, fill_color="#E8590C", fill_opacity=1,
                           stroke_width=0).move_to([-6.4, -2.55, 0]),
          Ellipse(width=0.5, height=1.2, fill_color=GRASS2, fill_opacity=1, stroke_width=0).move_to([-6.6, -1.9, 0]),
          Ellipse(width=0.5, height=1.2, fill_color=GRASS1, fill_opacity=1, stroke_width=0).rotate(0.5).move_to([-6.2, -1.9, 0]))
    return g


# ---------------------------------------------------------------- small building blocks
def pill(text, color, size=30, tc=WHITE, maxw=None):
    t = txt(text, size, tc, True, maxw=maxw)
    b = RoundedRectangle(corner_radius=0.3, width=t.width + 0.8, height=t.height + 0.4, fill_color=color,
                         fill_opacity=1, stroke_color=WHITE, stroke_width=4)
    t.move_to(b)
    return VGroup(b, t)


def speech(text, tc=NAVY, size=26, color=WHITE):
    t = txt(text, size, tc, True)
    b = RoundedRectangle(corner_radius=0.3, width=t.width + 0.7, height=t.height + 0.45, fill_color=color,
                         fill_opacity=1, stroke_color=NAVY, stroke_width=3)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_color=NAVY, stroke_width=3).scale(0.18).rotate(PI)
    tri.next_to(b, DOWN, buff=-0.02)
    t.move_to(b)
    return VGroup(b, tri, t)


def bubble(sprite, label, color, r=1.2, eh=1.4, lsize=26, badge=None):
    c = Circle(radius=r, fill_color=color, fill_opacity=1, stroke_color=WHITE, stroke_width=8)
    sprite.scale_to_fit_height(eh)
    if sprite.width > 1.55 * r:
        sprite.scale_to_fit_width(1.55 * r)
    sprite.move_to(c)
    lab = pill(label, NAVY, lsize, maxw=2 * r + 0.9).next_to(c, DOWN, buff=0.15)
    parts = [c, sprite, lab]
    if badge:
        parts.append(pill(badge, CORAL, 24).move_to(c.get_corner(UR) + LEFT * 0.15 + DOWN * 0.1))
    return VGroup(*parts)


def float_(m, amp=0.08, speed=0.5, phase=0.0):
    """Gentle up-and-down float. Call after the object has finished appearing."""
    state = {"t": phase, "base": m.get_center().copy()}

    def upd(mob, dt):
        state["t"] += dt
        mob.move_to(state["base"] + UP * amp * np.sin(state["t"] * TAU * speed))

    m.add_updater(upd)
    return m


def walk(m, start, end, bobs=8, amp=0.1):
    start, end = np.array(start, dtype=float), np.array(end, dtype=float)
    m.move_to(start)

    def f(mob, a):
        mob.move_to(start + (end - start) * a + UP * amp * abs(np.sin(a * bobs * PI)))

    return UpdateFromAlphaFunc(m, f, rate_func=linear)
