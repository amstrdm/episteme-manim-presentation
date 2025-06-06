from manim import *

from .shared import PresentationColors

import random
import numpy as np

def Scene1_2_Introduction(self):
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
    self.wipe(self.mobjects)