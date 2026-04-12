"""
Birthday Problem — Full Manim Animation
hanrius YouTube channel

Install: pip install manim
Run:     manim -pql birthday.py BirthdayProblem   (low quality, fast preview)
         manim -pqh birthday.py BirthdayProblem   (high quality, final render)

Scenes in order:
  1. Hook         — "23" on screen
  2. WrongIntuition — the 183 mistake
  3. RightQuestion  — pairs vs people, quadratic growth
  4. Complement     — telescoping product animation
  5. ProbCurve      — S-curve drawing itself
  6. Outro          — quant angle
"""

from manim import *
import numpy as np


# ── Palette ────────────────────────────────────────────────────────────────────
CORAL   = "#D85A30"
BLUE    = "#378ADD"
MUTED   = "#888888"
OFFWHITE = "#F0EEE8"
GREEN   = "#1D9E75"


# ══════════════════════════════════════════════════════════════════════════════
# 1. HOOK — "23" appears, then the question
# ══════════════════════════════════════════════════════════════════════════════
class Hook(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F"

        # Big "23"
        number = Text("23", font="Georgia", font_size=180, color=OFFWHITE)
        self.play(FadeIn(number, scale=0.85), run_time=1.2)
        self.wait(1.5)

        # Subtitle fades in below
        subtitle = Text(
            "this is all it takes",
            font="Georgia", font_size=32, color=MUTED, slant=ITALIC
        ).next_to(number, DOWN, buff=0.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(2)

        # Reveal the actual question
        question = Text(
            "How many people do you need in a room\n"
            "before there's a 50% chance two share a birthday?",
            font="Georgia", font_size=28, color=OFFWHITE,
            line_spacing=1.4
        ).move_to(ORIGIN)

        self.play(
            FadeOut(number, shift=UP * 0.3),
            FadeOut(subtitle, shift=UP * 0.3),
            run_time=0.6
        )
        self.play(FadeIn(question), run_time=1)
        self.wait(16)
        self.play(FadeOut(question))


# ══════════════════════════════════════════════════════════════════════════════
# 2. WRONG INTUITION — 365/2 = 183
# ══════════════════════════════════════════════════════════════════════════════
class WrongIntuition(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F"

        label = Text("the wrong intuition", font="Georgia",
                     font_size=18, color=CORAL, weight=BOLD)
        label.to_corner(UL, buff=0.6)
        self.play(FadeIn(label))
        self.wait(2)

        # "365 / 2 = 183"
        wrong = MathTex(
            r"\frac{365}{2}", r"= 183",
            font_size=90, color=OFFWHITE
        ).shift(UP * 0.5)
        self.play(Write(wrong[0]), run_time=1.2)
        self.wait(2)
        self.play(Write(wrong[1]), run_time=0.8)
        self.wait(1.5)

        # Explanation
        expl = Text(
            "Most people's instinct:\nhalve the days in a year.",
            font="Georgia", font_size=26, color=MUTED,
            slant=ITALIC, line_spacing=1.4
        ).next_to(wrong, DOWN, buff=0.65)
        self.play(FadeIn(expl))
        self.wait(5)

        # Cross it out
        strike = Line(
            wrong.get_left() + LEFT * 0.2,
            wrong.get_right() + RIGHT * 0.2,
            color=CORAL, stroke_width=5
        )
        self.play(Create(strike), run_time=0.6)
        self.wait(0.5)

        wrong_label = Text("wrong question", font="Georgia",
                           font_size=22, color=CORAL, slant=ITALIC)
        wrong_label.next_to(strike, DOWN, buff=0.4)
        self.play(FadeIn(wrong_label))
        self.wait(4)

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════════════════
# 3. RIGHT QUESTION — pairs grow quadratically
# ══════════════════════════════════════════════════════════════════════════════
class RightQuestion(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F" 

        label = Text("the right question", font="Georgia",
                     font_size=18, color=CORAL, weight=BOLD)
        label.to_corner(UL, buff=0.6)
        self.play(FadeIn(label))

        # Wrong framing
        wrong_q = Text(
            "Does anyone share MY birthday?",
            font="Georgia", font_size=30, color=MUTED, slant=ITALIC
        ).shift(UP * 1.8)
        self.play(FadeIn(wrong_q))
        self.wait(7.5)
 
        # Right framing
        right_q = Text(
            "Do ANY TWO people share a birthday?",
            font="Georgia", font_size=30, color=OFFWHITE
        ).next_to(wrong_q, DOWN, buff=0.5)
        self.play(FadeIn(right_q))
        self.wait(1)

        # Highlight "ANY TWO"
        highlight = SurroundingRectangle(right_q, color=CORAL, buff=0.12, corner_radius=0.1)
        self.play(Create(highlight))
        self.wait(7)

        # Pairs formula
        pairs_label = Text("number of pairs with 23 people:",
                           font="Georgia", font_size=24, color=MUTED)
        pairs_label.shift(DOWN * 0.5)
        pairs_formula = MathTex(
            r"\binom{23}{2} = \frac{23 \times 22}{2} = 253 \text{ pairs}",
            font_size=54, color=OFFWHITE
        ).next_to(pairs_label, DOWN, buff=0.3)

        self.play(FadeIn(pairs_label)) 
        self.wait(0.5)
        self.play(Write(pairs_formula), run_time = 4)
        self.wait(5)

        # Key insight
        insight = Text(
            "253 chances for a match — not 23.",
            font="Georgia", font_size=26, color=CORAL, slant=ITALIC
        ).next_to(pairs_formula, DOWN, buff=0.5)
        self.play(FadeIn(insight))
        self.wait(13)
 
        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════════════════
# 4. COMPLEMENT — telescoping product animates one fraction at a time
# ══════════════════════════════════════════════════════════════════════════════
class Complement(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F"

        label = Text("complement probability", font="Georgia",
                     font_size=18, color=CORAL, weight=BOLD)
        label.to_corner(UL, buff=0.6)
        self.play(FadeIn(label))

        # Strategy text
        strategy = Text(
            "Easier to compute P(no match), then subtract from 1.",
            font="Georgia", font_size=24, color=MUTED, slant=ITALIC
        ).shift(UP * 2.8)
        self.play(FadeIn(strategy))
        self.wait(13)

        # Show the product formula
        formula = MathTex(
            r"P(\text{no match}) =",
            r"\frac{365}{365}",
            r"\cdot \frac{364}{365}",
            r"\cdot \frac{363}{365}",
            r"\cdots",
            
            font_size=38, color=OFFWHITE
        ).shift(UP * 1.4)

        self.play(Write(formula[0]), run_time=1)
        for part in formula[1:]:
            self.play(Write(part), run_time=1.5)
            self.wait(4)
        self.wait(2)

        # Animate the running probability dropping
        prob_label = Text("P(no match) so far:", font="Georgia",
                          font_size=22, color=MUTED).shift(DOWN * 0.2)
        self.play(FadeIn(prob_label))

        prob = 1.0
        prob_display = DecimalNumber(
            prob, num_decimal_places=4,
            font_size=64, color=OFFWHITE
        ).next_to(prob_label, DOWN, buff=0.3)
        self.play(FadeIn(prob_display))

        person_label = Text("people: 1", font="Georgia",
                            font_size=20, color=MUTED).next_to(prob_display, DOWN, buff=0.3)
        self.play(FadeIn(person_label))

        # Step through 23 people
        for k in range(2, 24):
            prob *= (365 - k + 1) / 365
            new_prob = DecimalNumber(
                prob, num_decimal_places=4,
                font_size=64,
                color=CORAL if prob < 0.5 else OFFWHITE
            ).move_to(prob_display)

            new_person = Text(f"people: {k}", font="Georgia",
                              font_size=20, color=MUTED).move_to(person_label)

            self.play(
                Transform(prob_display, new_prob),
                Transform(person_label, new_person),
                run_time=0.2
            )

        self.wait(6)

        # P(at least one match)
        match_prob = 1 - prob
        result = MathTex(
            r"P(\text{match}) = 1 - " + f"{prob:.4f}",
            r"\approx " + f"{match_prob:.4f}",
            font_size=44, color=GREEN
        ).shift(DOWN * 2.0)
        self.play(Write(result), run_time=1.2)
        self.wait(0.5)

        over_fifty = Text("just over 50%  ✓", font="Georgia",
                          font_size=28, color=GREEN, slant=ITALIC)
        over_fifty.next_to(result, DOWN, buff=0.4)
        self.play(FadeIn(over_fifty))
        self.wait(4)

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════════════════
# 5. PROBABILITY CURVE — S-curve drawing itself
# ══════════════════════════════════════════════════════════════════════════════
class ProbCurve(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F"

        label = Text("the probability curve", font="Georgia",
                     font_size=18, color=CORAL, weight=BOLD)
        label.to_corner(UL, buff=0.6)
        self.play(FadeIn(label))

        # Compute data
        max_n = 60
        ns = list(range(1, max_n + 1))
        probs = []
        p_no = 1.0
        for n in ns:
            if n > 1:
                p_no *= (365 - n + 1) / 365
            probs.append(1 - p_no)

        # Axes
        axes = Axes(
            x_range=[1, 60, 10],
            y_range=[0, 1, 0.25],
            x_length=9,
            y_length=5,
            axis_config={"color": MUTED, "stroke_width": 1.5,
                         "include_tip": False},
            x_axis_config={"numbers_to_include": [10, 20, 30, 40, 50, 60]},
            y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0]},
        ).shift(DOWN * 0.3)

        x_label = Text("number of people", font="Georgia",
                       font_size=18, color=MUTED)
        x_label.next_to(axes, DOWN, buff=0.3)

        y_label = Text("P(at least one shared birthday)", font="Georgia",
                       font_size=18, color=MUTED).rotate(PI / 2)
        y_label.next_to(axes, LEFT, buff=0.4)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1)

        # 50% dashed line
        fifty_line = DashedLine(
            axes.c2p(1, 0.5),
            axes.c2p(60, 0.5),
            color=MUTED, dash_length=0.15, stroke_width=1.5
        )
        fifty_text = Text("50%", font="Georgia", font_size=16, color=MUTED)
        fifty_text.next_to(axes.c2p(1, 0.5), LEFT, buff=0.1)
        self.play(Create(fifty_line), FadeIn(fifty_text))

        # Draw the curve
        curve = axes.plot_line_graph(
            x_values=ns,
            y_values=probs,
            line_color=BLUE,
            stroke_width=3,
            add_vertex_dots=False
        )
        self.play(Create(curve), run_time=3) 
        self.wait(15)

        # Mark n=23
        dot_23 = Dot(axes.c2p(23, probs[22]), color=CORAL, radius=0.1)
        vline_23 = DashedLine(
            axes.c2p(23, 0),
            axes.c2p(23, probs[22]),
            color=CORAL, dash_length=0.12, stroke_width=1.5
        )
        label_23 = Text("n = 23\n≈ 50.7%", font="Georgia",
                        font_size=18, color=CORAL, line_spacing=1.2)
        label_23.next_to(dot_23, UR, buff=0.15)

        self.play(Create(vline_23), run_time=0.5)
        self.play(FadeIn(dot_23), FadeIn(label_23))
        self.wait(3.5)

        # Mark n=57 (~99%)
        dot_57 = Dot(axes.c2p(57, probs[56]), color=GREEN, radius=0.08)
        label_57 = Text("n = 57\n≈ 99%", font="Georgia",
                        font_size=16, color=GREEN, line_spacing=1.2)
        label_57.next_to(dot_57, UL, buff=0.15)
        self.play(FadeIn(dot_57), FadeIn(label_57))
        self.wait(9)
        #n = 30
        dot_30 = Dot(axes.c2p(30, probs[29]), color=GREEN, radius=0.08)
        label_30 = Text("n = 30\n≈ 70%", font="Georgia",
                        font_size=16, color=GREEN, line_spacing=1.2)
        label_30.next_to(dot_30, UL, buff=0.15)
        self.play(FadeIn(dot_30),FadeIn(label_30))
        self.wait(3)
        #n = 40
        dot_40 = Dot(axes.c2p(40, probs[39]), color=GREEN, radius=0.08)
        label_40 = Text("n = 40\n≈ 89%", font="Georgia",
                        font_size=16, color=GREEN, line_spacing=1.2)
        label_40.next_to(dot_40, UL, buff=0.15)
        self.play(FadeIn(dot_40),FadeIn(label_40))
        self.wait(2)
        

        self.play(FadeOut(Group(*self.mobjects)))


# ══════════════════════════════════════════════════════════════════════════════
# 6. OUTRO — quant angle + channel tag
# ══════════════════════════════════════════════════════════════════════════════
class Outro(Scene):
    def construct(self):
        self.camera.background_color = "#0F0F0F"

        takeaway = Text(
            "The takeaway",
            font="Georgia", font_size=18, color=CORAL, weight=BOLD
        ).to_corner(UL, buff=0.6)
        self.play(FadeIn(takeaway))

        lines = VGroup(
            Text("Pairs grow quadratically.", font="Georgia",
                 font_size=34, color=OFFWHITE),
            Text("Intuition thinks linearly.", font="Georgia",
                 font_size=34, color=OFFWHITE),
            Text("That gap is where probability surprises you.",
                 font="Georgia", font_size=28, color=MUTED, slant=ITALIC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(UP * 0.5)
        self.wait(1)
        for line in lines:
            self.play(FadeIn(line, shift=UP * 0.15), run_time=0.7)
            self.wait(1.5)
        self.wait(20)

   

        # Channel tag
        self.play(FadeOut(Group(*self.mobjects)))
        tag = Text("hanrius", font="Georgia", font_size=48, color=OFFWHITE)
        sub = Text("interesting probability problems everyone can understand",
                   font="Georgia", font_size=22, color=MUTED, slant=ITALIC)
        sub.next_to(tag, DOWN, buff=0.3)
        self.play(FadeIn(tag), FadeIn(sub))
        self.wait(3)
        self.play(FadeOut(tag), FadeOut(sub))


# ══════════════════════════════════════════════════════════════════════════════
# FULL VIDEO — runs all scenes back to back in one render
# ══════════════════════════════════════════════════════════════════════════════
class BirthdayProblem(Scene):
    def construct(self):
        Hook.construct(self)
        WrongIntuition.construct(self)
        RightQuestion.construct(self)
        Complement.construct(self)
        ProbCurve.construct(self)
        Outro.construct(self)
