from manim import *

# Configure global theme colors matching your design reference
BG_COLOR = "#EBF3FC"          # Soft Medical Light Blue
TEXT_COLOR = "#1B3B6F"        # Deep Navy Blue
ACCENT_RED = "#FF4B5C"        # Warning / Blood Drop Red
ACCENT_GREEN = "#2EC4B6"      # Normal / Safe Green
ACCENT_YELLOW = "#FF9F1C"     # Prediabetes Warning Yellow


class PrediabetesExplainer(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = BG_COLOR

        # ==========================================
        # SCENE 1: THE HOOK & RISK ASSESSMENT INTRO
        # ==========================================
        title = Text("Understanding Your Prediabetes Risk", font_size=38, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.8)

        subtitle = Text("A High Risk Score is an Early Warning, Not a Final Diagnosis.", font_size=22, color=TEXT_COLOR)
        subtitle.next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=UP), Write(subtitle), run_time=1.5)

        # Dashboard meter: top half-circle, drawn left -> over the top -> right
        meter_arc = Arc(radius=2.2, start_angle=PI, angle=-PI, color=TEXT_COLOR, stroke_width=8)
        meter_arc.shift(DOWN * 0.5)

        # Color zones on the arc (left = low, middle = warning, right = high)
        zone_blue = Arc(radius=2.2, start_angle=PI, angle=-PI / 3, color=BLUE_D, stroke_width=14).shift(DOWN * 0.5)
        zone_yellow = Arc(radius=2.2, start_angle=PI - PI / 3, angle=-PI / 3, color=ACCENT_YELLOW, stroke_width=14).shift(DOWN * 0.5)
        zone_red = Arc(radius=2.2, start_angle=PI - 2 * PI / 3, angle=-PI / 3, color=ACCENT_RED, stroke_width=14).shift(DOWN * 0.5)

        labels_group = VGroup(
            Text("Low", font_size=18, color=TEXT_COLOR).move_to(meter_arc.point_from_proportion(0.15) + DOWN * 0.4),
            Text("Warning", font_size=18, color=TEXT_COLOR).move_to(meter_arc.point_from_proportion(0.5) + DOWN * 0.4),
            Text("High", font_size=18, color=TEXT_COLOR).move_to(meter_arc.point_from_proportion(0.85) + DOWN * 0.4),
        )

        meter_group = VGroup(meter_arc, zone_blue, zone_yellow, zone_red, labels_group)
        self.play(Create(meter_group), run_time=2)

        # Needle pointing into the Warning (Prediabetes) zone
        needle = Line(start=ORIGIN, end=UP * 1.4, color=TEXT_COLOR, stroke_width=6)
        needle.shift(DOWN * 0.5)
        needle.rotate(-PI / 12, about_point=DOWN * 0.5)  # leans slightly toward red, still in yellow

        pin = Dot(point=DOWN * 0.5, color=TEXT_COLOR)

        self.play(Create(needle), FadeIn(pin), run_time=1)

        warning_box = RoundedRectangle(corner_radius=0.1, width=6.5, height=0.8, color=ACCENT_YELLOW, fill_opacity=0.2)
        warning_box.to_edge(DOWN, buff=0.6)
        warning_text = Text("Result: High Risk Score (Warning Zone)", font_size=20, color=TEXT_COLOR).move_to(warning_box.get_center())

        self.play(FadeIn(warning_box, shift=UP), Write(warning_text), run_time=1)
        self.wait(2)

        # ==========================================
        # SCENE 2: TRANSITION TO CLEAR MEANING
        # ==========================================
        self.play(
            FadeOut(warning_box), FadeOut(warning_text),
            FadeOut(needle), FadeOut(pin), FadeOut(meter_group),
            FadeOut(subtitle)
        )

        expl_title = Text("What Does 'High Risk' Actually Mean?", font_size=32, color=TEXT_COLOR)
        expl_title.to_edge(UP, buff=0.8)
        self.play(Transform(title, expl_title))

        # Bullet points representing clear facts
        bullet1 = Text("• It is a probability signal based on lifestyle & history.", font_size=20, color=TEXT_COLOR)
        bullet2 = Text("• NOT a medical diagnosis—prediabetes has no early symptoms.", font_size=20, color=TEXT_COLOR)
        bullet3 = Text("• The only way to confirm is a clinical blood test (HbA1c).", font_size=20, color=TEXT_COLOR)

        bullets = VGroup(bullet1, bullet2, bullet3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullets.shift(DOWN * 0.8)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT), run_time=0.8)
            self.wait(0.5)

        self.wait(2)

        # ==========================================
        # SCENE 3: ACTIONABLE PREVENTION (THE FIX)
        # ==========================================
        self.play(FadeOut(bullets), FadeOut(title))

        final_title = Text("Take Action: Prediabetes is Reversible!", font_size=32, color=ACCENT_GREEN)
        final_title.to_edge(UP, buff=1.0)

        step1 = RoundedRectangle(corner_radius=0.2, width=7, height=1.0, color=TEXT_COLOR, fill_opacity=0.05)
        step1_text = Text("1. Schedule an HbA1c blood test with your doctor.", font_size=18, color=TEXT_COLOR)
        if step1_text.width > 6.6:
            step1_text.scale_to_fit_width(6.6)
        step1_text.move_to(step1.get_center())
        grp1 = VGroup(step1, step1_text).shift(UP * 0.8)

        step2 = RoundedRectangle(corner_radius=0.2, width=7, height=1.0, color=TEXT_COLOR, fill_opacity=0.05)
        step2_text = Text("2. Adopt balanced nutrition & daily physical activity.", font_size=18, color=TEXT_COLOR)
        if step2_text.width > 6.6:
            step2_text.scale_to_fit_width(6.6)
        step2_text.move_to(step2.get_center())
        grp2 = VGroup(step2, step2_text).shift(DOWN * 0.6)

        self.play(Write(final_title), FadeIn(grp1, shift=UP), FadeIn(grp2, shift=UP), run_time=1.5)
        self.wait(3)
