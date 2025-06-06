from manim import *
from manim_slides import Slide

from slides_source.shared import PresentationColors
from slides_source import scene_10_b_scraping, scene_11_b_4problems, scene_1_1, scene_1_2, scene_2, scene_3, scene_4, scene_5, scene_8_b_database, scene_9_b_analysis_endpoints

import numpy as np

"""
=== IMPORTANT NOTE ===
Text objects that are supposed to be small are set to a font size of 100 and then scaled down.
This is because when manim renders text with a small font size the text starts looking janky and letter spacing is off.
To bypass this we set thet text to a large font size and scale accordingly.
"""    

class Presentation(Slide):
    skip_reversing = True
    def construct(self):
        self.wait_time_between_slides = 0.1
        scene_1_1.Scene1_1_Title(self)
        scene_1_2.Scene1_2_Introduction(self)
        scene_2.Scene2_Goals_and_Functionalities(self)
        scene_3.Scene3_Technology_Stack(self)
        scene_4.Scene_4_Cosine_Similarity(self)
        

        scene_8_b_database.Scene8_Bonus_Database(self)
        scene_9_b_analysis_endpoints.Scene9_Bonus_Analysis_Pipeline(self)
        scene_10_b_scraping.Scene_10_Bonus_Scraping(self)
        scene_11_b_4problems.Scene11_Bonus_Introduction(self)