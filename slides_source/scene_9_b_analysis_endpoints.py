from manim import *

from .shared import PresentationColors

import random

# Helper function to create endpoint box
def create_endpoint_box(text, color=BLUE):
    box = RoundedRectangle(width=4.0, height=1.0, corner_radius=0.2, color=color, fill_opacity=0.1)
    text_obj = Text(text, font_size=24).move_to(box.get_center())
    return VGroup(box, text_obj)

# Helper function to create user icon (simplified)
def create_user_icon(label_text=""):
    icon = SVGMobject("assets/user_icon.svg", fill_color=GREEN_C, stroke_color=GREEN_C).scale(0.5)
    if label_text:
        label = Text(label_text, font_size=18).next_to(icon, DOWN, buff=0.1)
        return VGroup(icon, label)
    return icon

def Scene9_Bonus_Analysis_Pipeline(self):
        # 0. Initial Scene Setup
        scene_title = Text("API Endpoint Interactions", font_size=48).to_edge(UP)
        self.play(Write(scene_title))
        self.next_slide()

        # --- Interaction 1: /check-analysis ---

        user_icon1 = create_user_icon().to_edge(LEFT, buff=1).shift(DOWN * 1)
        check_analysis_box = create_endpoint_box("/check-analysis").to_edge(RIGHT, buff=1).shift(DOWN * 1)
        self.play(FadeIn(user_icon1), FadeIn(check_analysis_box)) 
        self.next_slide()

        arrow_req1 = Arrow(user_icon1.get_right(), check_analysis_box.get_left(), buff=0.1, color=BLUE_C)
        self.play(GrowArrow(arrow_req1))
        self.next_slide()

        # Passing Flash Animation for Request
        flash_stroke_width1 = arrow_req1.stroke_width
        self.play(
            ShowPassingFlash(
                arrow_req1.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width1),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        response_text1_val = "true, 05-01-2025"
        response_text1 = Text(response_text1_val, font_size=20, color=GREEN_D).next_to(arrow_req1, DOWN, buff=0.3).align_to(check_analysis_box.get_left(), RIGHT)
        arrow_resp1 = Arrow(check_analysis_box.get_left() + DOWN*0.3, user_icon1.get_right() + DOWN*0.3, buff=0.1, color=GREEN_C)
        
        # Animate response appearing near endpoint first, then arrow
        response_text1.move_to(check_analysis_box.get_center() + DOWN*1.0)
        self.play(Write(response_text1), run_time=0.5)
        self.next_slide()

        self.play(GrowArrow(arrow_resp1), response_text1.animate.next_to(arrow_resp1, DOWN, buff=0.1))
        self.next_slide()

        flash_stroke_width2 = arrow_resp1.stroke_width
        self.play(
            ShowPassingFlash(
                arrow_resp1.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width2),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        interaction1_elements = VGroup(user_icon1, check_analysis_box, arrow_req1, arrow_resp1, response_text1)

        # --- Interaction 2: /generate-analysis ---
        self.play(interaction1_elements.animate.shift(UP*3).scale(0.6)) # Move previous interaction up
        self.next_slide()

        user_icon2 = create_user_icon().to_edge(LEFT, buff=1).shift(DOWN*1)
        generate_analysis_box = create_endpoint_box("/generate-analysis", color=ORANGE).to_edge(RIGHT, buff=1).shift(DOWN*1)

        self.play(FadeIn(user_icon2), FadeIn(generate_analysis_box))
        self.next_slide()

        arrow_req2 = Arrow(user_icon2.get_right(), generate_analysis_box.get_left(), buff=0.1, color=BLUE_C)
        self.play(GrowArrow(arrow_req2))
        self.next_slide()

        flash_stroke_width3 = arrow_req2.stroke_width
        self.play(
            ShowPassingFlash(
                arrow_req2.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width3),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        response_text2_val = "task_uuid (615f74-ba9c)"
        response_text2 = Text(response_text2_val, font_size=20, color=ORANGE).next_to(arrow_req2, DOWN, buff=0.3).align_to(generate_analysis_box.get_left(), RIGHT)
        arrow_resp2 = Arrow(generate_analysis_box.get_left() + DOWN*0.3, user_icon2.get_right() + DOWN*0.3, buff=0.1, color=ORANGE)

        response_text2.move_to(generate_analysis_box.get_center() + DOWN*1.0)
        self.play(Write(response_text2), run_time=0.5)
        self.next_slide()
        
        response_text2_redis = response_text2.copy()

        redis_logo = SVGMobject("assets/redis_logo.svg").scale(0.3).next_to(response_text2, DOWN, buff=0.6)
        self.play(DrawBorderThenFill(redis_logo))
        self.next_slide()
        
        self.play(response_text2_redis.animate.move_to(redis_logo.get_center()).scale(0))
        self.next_slide()

        self.play(GrowArrow(arrow_resp2), response_text2.animate.next_to(arrow_resp2, DOWN, buff=0.1))
        self.next_slide()

        flash_stroke_width4 = arrow_resp2.stroke_width
        self.play(
            ShowPassingFlash(
                arrow_resp2.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width4),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        interaction2_elements = VGroup(user_icon2, generate_analysis_box, arrow_req2, arrow_resp2, response_text2)

        # --- Interaction 3: /analysis-status (Polling) ---
        self.play(
            interaction2_elements.animate.next_to(interaction1_elements, DOWN, buff=0.3).scale(0.6), # Move previous interaction up
            FadeOut(redis_logo)
        )
        self.next_slide()

        user_icon3 = create_user_icon().to_edge(LEFT, buff=1).shift(DOWN*1)
        analysis_status_box = create_endpoint_box("/analysis-status", color=PURPLE).to_edge(RIGHT, buff=1).shift(DOWN * 1)

        self.play(FadeIn(user_icon3), FadeIn(analysis_status_box))
        self.next_slide()

        # Initial Request for polling
        arrow_req3_initial = Arrow(user_icon3.get_right(), analysis_status_box.get_left(), buff=0.1, color=BLUE_C)
        self.play(GrowArrow(arrow_req3_initial))
        self.next_slide()
        
        flash_stroke_width5 = arrow_req3_initial.width
        self.play(
            ShowPassingFlash(
                arrow_req3_initial.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width5),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        # Status Bar Creation
        status_bar_width_val = 2.0 
        status_bar_bg = RoundedRectangle(width=status_bar_width_val, height=0.3, corner_radius=0.05, color=DARK_GREY, fill_opacity=0.5).next_to(user_icon3, DOWN, buff=0.3)
        status_bar_fill = status_bar_bg.copy().set_fill(color=BLUE_D, opacity=1).stretch_to_fit_width(0.001).align_to(status_bar_bg, LEFT)
        status_bar_text_val = 0 
        status_bar_text_obj = Text(f"{status_bar_text_val}%", font_size=16, color=WHITE).move_to(status_bar_bg.get_center())
        status_bar = VGroup(status_bar_bg, status_bar_fill, status_bar_text_obj)
        self.play(FadeIn(status_bar))
        self.next_slide()
        
        current_status_val_from_endpoint = 0 
        total_progress = 100
        max_polls = 5 # Total polls to display (0 to 5 means 6 states: 0%, 10%, ..., 100%)
        
        # This VGroup will hold arrows that need to be faded out before the next poll request
        current_poll_arrows = VGroup(arrow_req3_initial) 
        endpoint_status_text = Text("") # Placeholder for the number text by the endpoint

        # Redis Logo
        redis_logo.next_to(analysis_status_box, DOWN, buff=1)
        self.play(DrawBorderThenFill(redis_logo))
        self.next_slide()

        status_redis_arrow = Arrow(analysis_status_box.get_bottom() + RIGHT * 0.1, redis_logo.get_top() + RIGHT * 0.1, buff=0.1, color=RED)
        self.play(GrowArrow(status_redis_arrow))
        self.next_slide()

        self.play(
            ShowPassingFlash(
                status_redis_arrow.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=status_redis_arrow.width),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()
        
        redis_status_arrow = Arrow(redis_logo.get_top() + LEFT*0.1, analysis_status_box.get_bottom() + LEFT * 0.1, color=RED, buff=0.1)
        self.play(GrowArrow(redis_status_arrow))
        self.next_slide()

        self.play(
            ShowPassingFlash(
                redis_status_arrow.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=redis_status_arrow.width),
                time_width=0.2,
                run_time=1.5
            )
        )
        self.next_slide()

        # --- First Poll (0% -> 10%) ---
        current_status_val_from_endpoint = 10 # Initial poll response
        endpoint_status_text = Text(str(current_status_val_from_endpoint), font_size=24, color=PURPLE_B).next_to(redis_status_arrow, LEFT, buff=0.3)
        self.play(FadeIn(endpoint_status_text))
        self.next_slide()

        arrow_resp_poll_0 = Arrow(analysis_status_box.get_left() + DOWN*0.3, user_icon3.get_right() + DOWN*0.3, buff=0.1, color=PURPLE_C)
        current_poll_arrows.add(arrow_resp_poll_0)
        
        temp_response_anim_obj = endpoint_status_text.copy()
        self.play(
            GrowArrow(arrow_resp_poll_0),
            temp_response_anim_obj.animate.next_to(arrow_resp_poll_0, DOWN, buff=0.1).scale(0.8),
            run_time=0.4
        )
        self.next_slide()

        flash_stroke_width6 = arrow_resp_poll_0.width
        self.play(
            ShowPassingFlash(
                arrow_resp_poll_0.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width6),
                time_width=0.2,
                run_time=1.5
            ),
            FadeOut(temp_response_anim_obj)
        )
        self.next_slide()

        progress_ratio_0 = current_status_val_from_endpoint / total_progress
        new_fill_width_0 = progress_ratio_0 * (status_bar_bg.width - 0.01)
        new_fill_width_0 = max(0.001, new_fill_width_0)
        new_status_bar_text_0 = Text(f"{current_status_val_from_endpoint}%", font_size=16, color=WHITE).move_to(status_bar_bg.get_center())
        
        self.play(
            status_bar_fill.animate.stretch_to_fit_width(new_fill_width_0).align_to(status_bar_bg, LEFT),
            Transform(status_bar_text_obj, new_status_bar_text_0),
            run_time=0.5
        )
        self.next_slide()

        # --- Subsequent Polls Loop (Poll 2 onwards, i.e., i_poll from 1 to max_polls) ---
        for i_poll_loop in range(1, max_polls + 1): # Starts from 1 because poll 0 is done
            # Fade out arrows from the previous poll
            self.play(FadeOut(current_poll_arrows), run_time=0.3)
            current_poll_arrows = VGroup() # Reset for current poll's arrows

            # New request for the current poll
            arrow_req_loop = Arrow(user_icon3.get_right(), analysis_status_box.get_left(), buff=0.1, color=BLUE_C)
            current_poll_arrows.add(arrow_req_loop)
            self.play(GrowArrow(arrow_req_loop), run_time=0.3)
            
            flash_stroke_width7 = arrow_req_loop.width
            self.play(
                ShowPassingFlash(
                    arrow_req_loop.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width7),
                    time_width=0.2,
                    run_time=1.5
                )
            )

            # Update status value from endpoint
            self.play(FadeOut(endpoint_status_text, shift=DOWN*0.2), run_time=0.2)
            
            if current_status_val_from_endpoint < 80:
                current_status_val_from_endpoint += int(15 + random.uniform(-3, 8))
            
            if current_status_val_from_endpoint >= 80 and current_status_val_from_endpoint < total_progress:
                current_status_val_from_endpoint = total_progress
            
            if i_poll_loop == max_polls and current_status_val_from_endpoint < total_progress: # Ensure 100% on the last defined poll
                current_status_val_from_endpoint = total_progress
            
            current_status_val_from_endpoint = min(current_status_val_from_endpoint, total_progress)
            
            endpoint_status_text = Text(str(current_status_val_from_endpoint), font_size=24, color=PURPLE_B).next_to(redis_status_arrow, LEFT, buff=0.3)
            self.play(FadeIn(endpoint_status_text, shift=UP*0.2), run_time=0.2)
        
            # Animate response arrow for current poll
            arrow_resp_loop = Arrow(analysis_status_box.get_left() + DOWN*0.3, user_icon3.get_right() + DOWN*0.3, buff=0.1, color=PURPLE_C)
            current_poll_arrows.add(arrow_resp_loop)
            
            temp_response_anim_obj_loop = endpoint_status_text.copy()
            self.play(
                GrowArrow(arrow_resp_loop),
                temp_response_anim_obj_loop.animate.next_to(arrow_resp_loop, DOWN, buff=0.1).scale(0.8),
                run_time=0.4
            )
            
            flash_stroke_width8 = arrow_resp_loop.width
            self.play(
                ShowPassingFlash(
                    arrow_resp_loop.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width8),
                    time_width=0.2,
                    run_time=1.5
                ),
                FadeOut(temp_response_anim_obj_loop)
            )

            # Update status bar
            progress_ratio_loop = current_status_val_from_endpoint / total_progress
            new_fill_width_loop = progress_ratio_loop * (status_bar_bg.width - 0.01)
            new_fill_width_loop = max(0.001, new_fill_width_loop)
            new_status_bar_text_loop = Text(f"{current_status_val_from_endpoint}%", font_size=16, color=WHITE).move_to(status_bar_bg.get_center())
            
            self.play(
                status_bar_fill.animate.stretch_to_fit_width(new_fill_width_loop).align_to(status_bar_bg, LEFT),
                Transform(status_bar_text_obj, new_status_bar_text_loop),
                run_time=0.5
            )

            if current_status_val_from_endpoint == total_progress:
                self.play(FadeOut(current_poll_arrows), run_time=0.3) # Fade out last set of arrows
                break 
            
            # Short wait if not the absolute final state, to make loop iterations distinct
            if i_poll_loop < max_polls :
                self.wait(0.1)
            
        self.play(FadeOut(endpoint_status_text))
        self.next_slide()
