from manim import *
from manim_slides import Slide

from slides_source.shared import PresentationColors
from slides_source import scene_1, scene_2, scene_3, scene_4



"""
=== IMPORTANT NOTE ===
Text objects that are supposed to be small are set to a font size of 100 and then scaled down.
This is because when manim renders text with a small font size the text starts looking janky and letter spacing is off.
To bypass this we set thet text to a large font size and scale accordingly.
"""


class Presentation(Slide):
    skip_reversing = True
    def construct(self):
        # self.Scene1_Title()
        # self.Scene2_Introduction()
        # self.Scene3_Goals_and_Functionalities()
        scene_1.Scene1_Title(self)




