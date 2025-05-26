from manim import *

from .shared import PresentationColors

import random
import numpy as np

def Scene2_Introduction(self):
    challenge_t = Text("Informationsüberflutung", font_size=100, color=PresentationColors.TEXT_PRIMARY).scale(0.48)
    challenge_t.to_edge(UP)
    self.play(Write(challenge_t))

    num_snippets = 25
    snippets = VGroup()
    
    for _ in range(num_snippets):
        snippet_box = RoundedRectangle(
            corner_radius=0.1,
            width=random.uniform(1.5,3), 
            height=random.uniform(0.3,0.5),
            color=PresentationColors.TEXT_SECONDARY, 
            fill_opacity=0.3, 
            stroke_width=1)

        snippet_box.move_to(
            np.array([
                random.uniform(-config.frame_width/2 + 1, config.frame_width/2 - 1),
                random.uniform(-config.frame_height/2 + 1, config.frame_height/2 - 3),
                0
            ])
        )
        snippets.add(snippet_box)
    
    magnifying_glass = SVGMobject("assets/magnifying_glass.svg").scale(0.3)
    
    self.next_slide()
    self.play(LaggedStart(*[FadeIn(s, scale=0.5) for s in snippets], lag_ratio=0.1), run_time=3)
    
    self.next_slide()
    self.play(FadeIn(magnifying_glass, scale=0.5))
    
    for _ in range(4):
        snippet = random.choice(snippets)
        self.play(magnifying_glass.animate.move_to(snippet))
        self.wait(0.2)

    self.play(FadeOut(magnifying_glass), FadeOut(challenge_t))
    central_shape = Circle(radius=1.2, color=PresentationColors.ACCENT_MAIN, fill_opacity=0.8)
    
    self.next_slide()
    self.play(
        LaggedStart(*[Transform(s, central_shape) for s in snippets], lag_ratio=0.05, run_time=3)
    )
    
    self.next_slide()
    
    logo = SVGMobject("assets/vectorized_logo_scaled.svg")
    self.play(Transform(snippets, logo))
    
    self.next_slide()
    
    self.play(snippets.animate.scale(0.7))
    
    self.next_slide()
    # Up Left (Quick Overview)
    ul_line = Line(LEFT+UP, 3.5*LEFT+2*UP)
    self.play(Create(ul_line))
    timer_text = Text("Schnelle Übersicht", font_size=100, color=PresentationColors.TEXT_PRIMARY).scale(0.35)
    timer_icon = SVGMobject("assets/timer.svg").scale_to_fit_height(timer_text.height)

    timer_text.next_to(
        ul_line.get_end(),
        UP,
        buff=0.2
    )
    timer_icon.next_to(timer_text, LEFT)
    self.play(DrawBorderThenFill(timer_icon), Write(timer_text))
    
    self.next_slide()
    # Up Right (Organized Arguments)
    ur_line = Line(RIGHT+UP, 3.5*RIGHT+2*UP)
    self.play(Create(ur_line))

    arrow_text = Text("Organisierte Argumente", font_size=100, color=PresentationColors.TEXT_PRIMARY).scale(0.35)
    arrow_icon = SVGMobject("assets/upanddownarrows.svg").scale_to_fit_height(arrow_text.height)

    arrow_text.next_to(
        ur_line.get_end(),
        UP,
        buff=0.2
    )
    arrow_icon.next_to(arrow_text, LEFT)
    self.play(DrawBorderThenFill(arrow_icon), Write(arrow_text))
    
    self.next_slide()
    # Down Left (Peer Reviewed Insights)
    dl_line = Line(LEFT+DOWN, 3.5*LEFT+2*DOWN)
    self.play(Create(dl_line))

    check_text = Text("Massengeprüfte Thesen", font_size=100, color=PresentationColors.TEXT_PRIMARY).scale(0.35)
    check_icon = SVGMobject("assets/check_mark.svg").scale_to_fit_height(check_text.height)

    check_text.next_to(
        dl_line.get_end(),
        DOWN,
        buff=0.2
    )
    # Shift the two Items at the bottom to the right so it looks a bit more clean
    check_text.shift(0.5*RIGHT)

    check_icon.next_to(check_text, LEFT)
    self.play(DrawBorderThenFill(check_icon), Write(check_text))
    
    self.next_slide()
    # Down Right (Sentiment Score)
    dr_line = Line(RIGHT+DOWN, 3.5*RIGHT+2*DOWN)
    self.play(Create(dr_line))

    smiley_text = Text("Sentiment Score", font_size=100, color=PresentationColors.TEXT_PRIMARY).scale(0.35)
    smiley_icon = SVGMobject("assets/smiley.svg").scale_to_fit_height(smiley_text.height)

    smiley_text.next_to(
        dr_line.get_end(),
        DOWN,
        buff=0.2
    )
    # Shift the two Items at the bottom to the right so it looks a bit more clean
    smiley_text.shift(0.5*RIGHT)
    
    smiley_icon.next_to(smiley_text, LEFT)
    self.play(DrawBorderThenFill(smiley_icon), Write(smiley_text))
    
    self.next_slide()
    
    self.wipe(self.mobjects)