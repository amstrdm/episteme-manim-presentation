from manim import *

from .shared import PresentationColors


def Scene11_Bonus_Introduction(self):
    logo = SVGMobject("assets/vectorized_logo_scaled.svg")
    self.play(logo.animate.scale(0.7))
    
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