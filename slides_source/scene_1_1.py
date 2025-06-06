from manim import *

from .shared import PresentationColors

def Scene1_1_Title(self):
    # Temporary plane
    # grid = NumberPlane(color=YELLOW)
    # self.add(grid)
    self.play(FadeIn(Circle(radius=1, color=config.background_color)))
    self.next_slide()
    logo = SVGMobject("assets/vectorized_logo_scaled.svg")
    episteme_text = Text("Episteme", font_size=96, color=PresentationColors.ACCENT_MAIN, )
    subtitle = Paragraph(
        "Automatisierte Aggregation & NLP-gestützte\nAnalyse von Online-Finanzdiskursen",
        font_size=36,
        color=PresentationColors.TEXT_PRIMARY,
        alignment="center",
        line_spacing=0.9
    )
    self.play(DrawBorderThenFill(logo, stroke_color=PresentationColors.ACCENT_MAIN))
    
    self.play(logo.animate.shift(1.5*UP))

    episteme_text.next_to(logo, DOWN)
    subtitle.next_to(episteme_text, DOWN)

    self.play(Write(episteme_text))
    self.wait(0.2)
    self.play(FadeIn(subtitle))
    self.next_slide()
    title_group = VGroup(logo, episteme_text, subtitle)
    
    self.wipe(title_group, direction=UP)