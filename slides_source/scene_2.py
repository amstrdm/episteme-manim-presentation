from manim import *

from .shared import PresentationColors

import random
import numpy as np

from manim_slides.slide.animation import Wipe
class NNColors:
    NODE_STROKE_INACTIVE = ManimColor("#58c6e0")  # Tailwind Gray-500
    NODE_STROKE_ACTIVE = ManimColor("#fb5d59")    # Tailwind Blue-500
    NODE_FILL_INACTIVE = ManimColor(PresentationColors.BACKGROUND)    # Tailwind Gray-200
    # Or for a "hollow" look when inactive: NODE_FILL_INACTIVE = BACKGROUND
    NODE_FILL_ACTIVE = ManimColor("#fb5d59")      # Tailwind Blue-300

    LINE_INACTIVE = ManimColor("#FFFFFF")         # Tailwind Gray-400
    LINE_ACTIVE = ManimColor("#fb5d59")           # Tailwind Blue-400

config.background_color = PresentationColors.BACKGROUND

def create_neural_network_mobjects(
    layer_sizes,
    position=ORIGIN,
    scale_factor=1.0,
    style_colors=None  # For initial appearance (mostly inactive styles)
):
    """
    Creates the mobjects for a neural network in their initial state.
    Does NOT add them to the scene.

    Args:
        layer_sizes (list): Nodes per layer.
        position (np.ndarray): Center position.
        scale_factor (float): Overall scale.
        style_colors (dict, optional): Dict to override default initial/inactive styles.
                                       Keys: "node_stroke", "node_fill", "line_stroke".

    Returns:
        dict: Contains 'main_mobject' (VGroup), 'layers_node_groups' (VGroup of VGroups),
              'lines_between_layers_groups' (list of VGroups),
              'all_nodes_flat' (list of nodes), 'all_lines_flat' (list of lines).
    """
    _initial_styles = {
        "node_stroke": NNColors.NODE_STROKE_INACTIVE,
        "node_fill": NNColors.NODE_FILL_INACTIVE,
        "line_stroke": NNColors.LINE_INACTIVE,
    }
    if style_colors:
        _initial_styles.update(style_colors)

    node_radius = 0.22 * scale_factor
    node_stroke_width = 2.5 * scale_factor
    line_stroke_width = 2.0 * scale_factor
    layer_x_spacing = 2.3 * scale_factor
    node_y_spacing_within_layer = 1.0 * scale_factor

    network_mobject_group = VGroup()
    layers_node_groups_vg = VGroup()
    all_nodes_flat_list = []
    all_lines_flat_list = []

    network_width = (len(layer_sizes) - 1) * layer_x_spacing
    current_x_pos = -network_width / 2
    
    for num_nodes_in_layer in layer_sizes:
        layer_node_vgroup = VGroup()
        layer_height = (num_nodes_in_layer - 1) * node_y_spacing_within_layer
        current_y_pos = -layer_height / 2
        
        for _ in range(num_nodes_in_layer):
            node = Circle(
                radius=node_radius, stroke_width=node_stroke_width,
                stroke_color=_initial_styles["node_stroke"],
                fill_color=_initial_styles["node_fill"], fill_opacity=1.0
            )
            # Store initial/inactive colors on the mobject for easy reset by animation function
            node.inactive_stroke_color = _initial_styles["node_stroke"]
            node.inactive_fill_color = _initial_styles["node_fill"]
            
            node.move_to(Point([current_x_pos, current_y_pos, 0]))
            node.set_z_index(2)
            layer_node_vgroup.add(node)
            all_nodes_flat_list.append(node)
            current_y_pos += node_y_spacing_within_layer
        layers_node_groups_vg.add(layer_node_vgroup)
        current_x_pos += layer_x_spacing
    network_mobject_group.add(layers_node_groups_vg)

    lines_between_layers_groups_list = []
    for i in range(len(layers_node_groups_vg) - 1):
        source_layer_nodes = layers_node_groups_vg[i]
        target_layer_nodes = layers_node_groups_vg[i+1]
        connection_lines_vg = VGroup()
        for src_node in source_layer_nodes:
            for tgt_node in target_layer_nodes:
                line = Line(
                    src_node.get_center(), tgt_node.get_center(),
                    stroke_width=line_stroke_width, stroke_color=_initial_styles["line_stroke"]
                )
                line.inactive_stroke_color = _initial_styles["line_stroke"] # Store for reset

                line.set_z_index(1)
                connection_lines_vg.add(line)
                all_lines_flat_list.append(line)
        lines_between_layers_groups_list.append(connection_lines_vg)
        network_mobject_group.add(connection_lines_vg)

    network_mobject_group.move_to(position)

    return {
        "main_mobject": network_mobject_group,
        "layers_node_groups": layers_node_groups_vg,
        "lines_between_layers_groups": lines_between_layers_groups_list,
        "all_nodes_flat": all_nodes_flat_list,
        "all_lines_flat": all_lines_flat_list,
    }

def animate_neural_network_activation_loop(
    scene,
    nn_data,  # The dictionary returned by create_neural_network_mobjects
    activation_colors=None, # Colors for the active state
    timings=None  # Animation timings
):
    """
    Animates one cycle of a "pulse" activation and deactivation
    on pre-built NN mobjects.
    """
    layers_node_groups_vg = nn_data["layers_node_groups"]
    lines_between_layers_groups_list = nn_data["lines_between_layers_groups"]
    # all_nodes_flat_list = nn_data["all_nodes_flat"] # Not directly used in pulse reset
    # all_lines_flat_list = nn_data["all_lines_flat"] # Not directly used in pulse reset

    _act_colors = {
        "node_stroke_active": NNColors.NODE_STROKE_ACTIVE,
        "node_fill_active": NNColors.NODE_FILL_ACTIVE,
        "line_stroke_active": NNColors.LINE_ACTIVE,
    }
    if activation_colors:
        _act_colors.update(activation_colors)

    # Faster and snappier default timings, with new keys for pulse logic
    _timings_defaults = {
        "initial_node_activation_run_time": 0.25, # Time for the very first input layer to light up
        "pulse_step_run_time": 0.25,             # Time for each subsequent pulse step (lines on/nodes off, then nodes on/lines off)
        "node_lag_ratio": 0.05,                 # Lag for nodes within a layer
        "line_lag_ratio": 0.02,                 # Lag for lines between layers
        "hold_output_active_time": 0.3,         # How long the output nodes stay lit before reset
        "reset_output_time": 0.3,               # Time for output nodes to dim
        "pause_at_end_of_loop": 0.25,           # Pause before visual loop restarts
    }
    _timings_final = _timings_defaults.copy()
    if timings:
        _timings_final.update(timings)

    # --- Animation Pulse Cycle ---

    # 1. Initial activation of input nodes (L0)
    input_layer_nodes = layers_node_groups_vg[0]
    scene.play(
        LaggedStart(*[
            node.animate.set_style(
                fill_color=_act_colors["node_fill_active"],
                stroke_color=_act_colors["node_stroke_active"]
            ) for node in input_layer_nodes
        ], lag_ratio=_timings_final["node_lag_ratio"], run_time=_timings_final["initial_node_activation_run_time"])
    )

    # 2. Propagation pulse through layers
    for i in range(len(lines_between_layers_groups_list)):
        current_nodes = layers_node_groups_vg[i]
        current_lines = lines_between_layers_groups_list[i]
        next_nodes = layers_node_groups_vg[i+1]

        # Step A: Activate lines from current_nodes, simultaneously deactivate current_nodes
        anims_lines_on = [
            line.animate.set_stroke(_act_colors["line_stroke_active"])
            for line in current_lines
        ]
        anims_current_nodes_off = [
            node.animate.set_style(
                fill_color=node.inactive_fill_color, # Use stored inactive color
                stroke_color=node.inactive_stroke_color # Use stored inactive color
            ) for node in current_nodes
        ]
        
        scene.play(
            LaggedStart(*anims_lines_on, lag_ratio=_timings_final["line_lag_ratio"], run_time=_timings_final["pulse_step_run_time"]),
            LaggedStart(*anims_current_nodes_off, lag_ratio=_timings_final["node_lag_ratio"], run_time=_timings_final["pulse_step_run_time"])
        )

        # Step B: Activate next_nodes, simultaneously deactivate current_lines
        anims_next_nodes_on = [
            node.animate.set_style(
                fill_color=_act_colors["node_fill_active"],
                stroke_color=_act_colors["node_stroke_active"]
            ) for node in next_nodes
        ]
        anims_lines_off = [
            line.animate.set_stroke(line.inactive_stroke_color) # Use stored inactive color
            for line in current_lines
        ]
        
        scene.play(
            LaggedStart(*anims_next_nodes_on, lag_ratio=_timings_final["node_lag_ratio"], run_time=_timings_final["pulse_step_run_time"]),
            LaggedStart(*anims_lines_off, lag_ratio=_timings_final["line_lag_ratio"], run_time=_timings_final["pulse_step_run_time"])
        )

    # 3. After loop, only the output layer nodes are active. Hold this state briefly.
    scene.wait(_timings_final["hold_output_active_time"])

    # 4. Reset: Output layer nodes (which are the only ones lit) turn off.
    output_layer_nodes = layers_node_groups_vg[-1]
    reset_output_nodes_anims = [
        node.animate.set_style(
            fill_color=node.inactive_fill_color, # Use stored inactive color
            stroke_color=node.inactive_stroke_color # Use stored inactive color
        ) for node in output_layer_nodes
    ]
    if reset_output_nodes_anims: # Ensure there are output nodes to animate
        scene.play(
            LaggedStart(*reset_output_nodes_anims, lag_ratio=_timings_final["node_lag_ratio"], run_time=_timings_final["reset_output_time"])
        )
    
    scene.wait(_timings_final["pause_at_end_of_loop"])

def Scene2_Goals_and_Functionalities(self):
    search_bar = SVGMobject("assets/search_bar.svg").scale(0.3)
    search_bar.shift(2*UP+4.5*LEFT)
    self.play(DrawBorderThenFill(search_bar))
    self.next_slide()
    search_bar_text = "Apple"

    text_area_width = search_bar.width * 0.8
    text_area_height = search_bar.height * 0.6

    goog_text = Text(
        search_bar_text, 
        color=WHITE, 
        width=text_area_width, 
        height=text_area_height
    )

    current_text_width = goog_text.width
    current_text_height = goog_text.height

    if current_text_width > 0 and current_text_height > 0: # Proceed only if text has dimensions
        scale_factor = 1.0
    # Check if scaling for width is needed
    if current_text_width > text_area_width:
        scale_factor = text_area_width / current_text_width
    
    # After scaling for width, check if height (proportionally scaled) is still too much
    if current_text_height * scale_factor > text_area_height:
        # Adjust scale_factor further to fit height
        scale_factor *= (text_area_height / (current_text_height * scale_factor)) 
    
    goog_text.scale(scale_factor)


    text_start_x_coord = search_bar.get_left()[0]
    goog_text.move_to(np.array([text_start_x_coord, search_bar.get_center()[1], 0]), aligned_edge=LEFT)
    
    cursor_height = goog_text.height * 0.9
    cursor = Line(ORIGIN, UP * cursor_height, stroke_width=3, color=WHITE)
    cursor.move_to(goog_text[0])

    self.play(TypeWithCursor(goog_text, cursor))
    self.play(Blink(cursor, blinks=2))

    self.play(FadeOut(cursor), run_time=0.2)
    cursor.set_opacity(0)
    
    self.next_slide()
    self.play(Indicate(search_bar), Indicate(goog_text))
    
    criticial_point_buff = np.array([
        search_bar.get_critical_point(RIGHT)[0] + 0.15,
        search_bar.get_critical_point(RIGHT)[1],
        search_bar.get_critical_point(RIGHT)[2]
    ])

    # Points for the Line(s) to go to
    P0 = criticial_point_buff
    P1 = P0 + 2 * RIGHT
    P2_up = P1 + UP
    P2_down = P1 + DOWN
    P3_up = P2_up + RIGHT
    P3_down = P2_down + RIGHT
    line_up = VMobject(stroke_width=5, joint_type=LineJointType.ROUND).set_points_as_corners([P0, P1, P2_up, P3_up])
    line_down = VMobject(stroke_width=5, joint_type=LineJointType.ROUND).set_points_as_corners([P0, P1, P2_down, P3_down])
    self.play(Create(line_up), Create(line_down))
    
    reddit_logo = SVGMobject("assets/reddit_logo.svg").scale(0.5)
    reddit_logo.next_to(line_up.get_end(), buff=0.3)

    seekingalpha_logo = SVGMobject("assets/seekingalpha_logo.svg", stroke_color="#e74a18").scale_to_fit_width(reddit_logo.width)
    seekingalpha_logo.next_to(line_down.get_end(), buff=0.3)

    self.play(DrawBorderThenFill(reddit_logo, stroke_color="#e74a18"), DrawBorderThenFill(seekingalpha_logo, stroke_color="#e74a18"))

    self.next_slide(loop=True)

    flash_stroke_width = line_up.get_stroke_width() * 2.5

    self.play(
        ShowPassingFlash(
            line_up.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width),  
            time_width=0.2,
            run_time=1.5
        ),
        ShowPassingFlash(
            line_down.copy().set_stroke(color=PresentationColors.ACCENT_MAIN, width=flash_stroke_width),
            time_width=0.2,
            run_time=1.5
        )
    )
    self.wait(1)

    self.next_slide()

    social_group = VGroup(reddit_logo, seekingalpha_logo)
    social_group.set_z_index(2)

    social_box = SurroundingRectangle(
        social_group, 
        color=PresentationColors.ACCENT_MAIN, 
        fill_color=self.camera.background_color,
        fill_opacity=1,
        buff=MED_SMALL_BUFF, 
        corner_radius=0.2
    )
    social_box.set_z_index(1)

    self.play(DrawBorderThenFill(social_box))

    # 1. Draw a line from the right of social_box further to the right.
    line_social_process_start = social_box.get_right() + LEFT * 0.6 # Extend the start by half of the max width of the snippet in the left direction so that the snippet starts completely behind the social box 
    line_social_process_end = line_social_process_start + RIGHT * 4.1 # Path length is 4 units plus the max width of the snippet divided by 2

    path_social_process = Line(line_social_process_start, line_social_process_end, stroke_width=5)

    processing_box = RoundedRectangle(
        corner_radius=0.2,
        width=3,
        height=3,
        color=PresentationColors.ACCENT_MAIN,
        fill_color=self.camera.background_color,
        fill_opacity=1
    )
    processing_box.move_to(path_social_process.get_end() - 0.6*RIGHT)
    processing_box.set_z_index(1)
    
    thesenextraktion_t = Text("Thesenextrahierung", font_size=100).scale(0.2)
    thesenextraktion_t.move_to(processing_box.get_top() + 0.3*DOWN)
    thesenextraktion_t.set_z_index(2)
    self.play(Create(path_social_process), Create(processing_box))  
    self.play(Write(thesenextraktion_t))

    # 2. Rectangles emerge and move along the line.
    num_rectangles = 8
    max_vertical_jitter = 0.2

    rect_anims = []

    for _ in range(num_rectangles):
        snippet_width = random.uniform(0.8, 1.2)  # Was 0.4-0.9
        snippet_height = random.uniform(0.25, 0.4) # Was 0.08-0.16
        
        snippet_box = RoundedRectangle(
            corner_radius=0.075, # Was 0.1, adjusted for new, larger dimensions
            width=snippet_width, 
            height=snippet_height,
            color=PresentationColors.TEXT_SECONDARY, 
            fill_opacity=random.uniform(0.4, 0.7), # Was 0.2-0.5, made slightly more opaque
            stroke_width=2.0, # Was random 0.5-1.5, now a fixed, more visible stroke
            stroke_color=PresentationColors.TEXT_SECONDARY.darker(0.3)
        )
        snippet_box.set_z_index(0)

        snippet_vertical_offset = random.uniform(-max_vertical_jitter, max_vertical_jitter)
        individual_snippet_path = path_social_process.copy().shift(UP*snippet_vertical_offset)
        
        path_start_point = individual_snippet_path.get_start()
        snippet_box.move_to(path_start_point)

        rect_anims.append(
            MoveAlongPath(
                snippet_box,
                individual_snippet_path,
                run_time=random.uniform(1.8, 2.8), # Was 2.5-5.5; shorter for a path of length 3
                rate_func=linear
            )
        )
    
    # 3. Rectangles go into the processing unit

    # Add the neural network animation on top of the box
    nn_data_dict = create_neural_network_mobjects(
        layer_sizes=[5, 8, 5],
        scale_factor=0.3
    )
    
    nn_data_dict["main_mobject"].next_to(thesenextraktion_t, DOWN * 0.5)
    self.play(LaggedStart(*rect_anims, lag_ratio=0.25), run_time=5.5) # Adjusted run_time to better fit natural duration
    
    self.next_slide()
    self.play(DrawBorderThenFill(nn_data_dict["main_mobject"]))
    self.next_slide(loop=True)
    animate_neural_network_activation_loop(
        self,
        nn_data_dict,
    )
    self.next_slide()

    # Sentiment Analysis Box
    line_process_sentiment_start = processing_box.get_bottom() + UP * 0.3
    line_process_sentiment_end = line_process_sentiment_start + DOWN * 3.3

    path_process_sentiment = Line(line_process_sentiment_start, line_process_sentiment_end)

    sentiment_box = RoundedRectangle(
        corner_radius=0.2,
        width=3,
        height=2.5,
        color=PresentationColors.ACCENT_MAIN,
        fill_color=self.camera.background_color,
        fill_opacity=1
    )
    sentiment_box.move_to(line_process_sentiment_end)
    sentiment_box.set_z_index(0)

    sentiment_t = Text("Sentiment Analyse", font_size=100).scale(0.2)
    sentiment_t.move_to(sentiment_box.get_top() + DOWN * 0.3)
    sentiment_t.set_z_index(1)

    self.play(Create(path_process_sentiment), Create(sentiment_box), Write(sentiment_t))
    
    stacked_group = VGroup() # This VGroup will be our animated "structured data"
    
    for i in range(3):  # Create 3 identical rectangles
        post_snippet = RoundedRectangle(
            width=1,
            height=0.3,
            corner_radius=0.06,
            color=PresentationColors.TEXT_SECONDARY,
            fill_opacity=0.65,
            stroke_width=1.5,
            stroke_color=PresentationColors.TEXT_SECONDARY.darker(),
        )

        post_snippet.shift(RIGHT * 0.07 * i + UP * 0.07 * i)
        stacked_group.add(post_snippet)
    
    stacked_group.move_to(path_social_process.get_start())
    stacked_group.set_z_index(0.5)
    self.play(MoveAlongPath(stacked_group, path_process_sentiment), run_time=4)
    self.next_slide()

    line_sentiment_critical_start = path_process_sentiment.get_end()
    line_sentiment_critical_end = line_sentiment_critical_start + LEFT * 3.8

    path_sentiment_critical = Line(line_sentiment_critical_start, line_sentiment_critical_end)
    path_sentiment_critical.set_z_index(-1)
    critical_box = RoundedRectangle(
        corner_radius=0.2,
        width=3,
        height=2.5,
        color=PresentationColors.ACCENT_MAIN,
        fill_color=self.camera.background_color,
        fill_opacity=1
    )
    critical_box.next_to(line_sentiment_critical_end, LEFT, buff=0)
    critical_box.set_z_index(0)

    critical_t = Text("Kritik Auswertung", font_size=100).scale(0.2)
    critical_t.move_to(critical_box.get_top() + DOWN * 0.3)
    critical_t.set_z_index(1)
    self.play(Create(critical_box), Create(path_sentiment_critical), Write(critical_t))
    self.next_slide()

    # --- Scanning, Pulsing, and Emerging Loop ---
    scan_line_width = sentiment_box.width * 1.2
    scan_line_x_center = sentiment_box.get_center()[0]
    scan_start_y = sentiment_box.get_top()[1] + 0.2
    scan_end_y = sentiment_box.get_bottom()[1] - 0.2

    iteration_sentiments = [
        {"pulse": PresentationColors.ACCENT_BULLISH, "name": "Bullish"},
        {"pulse": PresentationColors.ACCENT_BEARISH, "name": "Bearish"},
        {"pulse": PresentationColors.ACCENT_BULLISH, "name": "Bullish"},
    ]

    output_snippets_group = VGroup()
    for i in range(len(iteration_sentiments)):
        current_sentiment_color = iteration_sentiments[i]["pulse"]
        # Move snippet to start of path fluidly to avoid ugly adjustemnts to path
        self.play(stacked_group[i].animate.move_to(path_sentiment_critical.get_start()))
        # --- 1. Visual Scan of Box ---
        scan_line = Line(
            [scan_line_x_center - scan_line_width / 2, scan_start_y, 0],
            [scan_line_x_center + scan_line_width / 2, scan_start_y, 0],
            color=PresentationColors.SCANNER_BLUE,
            stroke_width=4
        )
        scan_line.set_z_index(3)

        self.play(Create(scan_line), run_time=0.3)
        self.play(
            scan_line.animate.move_to(np.array([scan_line_x_center, scan_end_y, 0])),
            run_time=1.2
        )
        self.play(FadeOut(scan_line), run_time=0.3)
        self.wait(0.2)

        # --- 2. Sentiment Box Pulsing ---
        self.play(
            sentiment_box.animate.set_fill(color=current_sentiment_color, opacity=0.6).scale(1.3),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.wait(0.3)
        self.play(stacked_group[i].animate.set_color(current_sentiment_color))
        
        self.play(MoveAlongPath(stacked_group[i], path_sentiment_critical), run_time=1.2)
        output_snippets_group.add(stacked_group[i])
        self.play(
            output_snippets_group.animate.arrange(DOWN, buff=0.2).move_to(critical_box.get_center()),
            run_time=0.8
        )
        self.next_slide()

    snippet_critiqued_group = VGroup()
    # ===== 4. Critical Assessment for the current output_snippet =====
    for idx, snippet in enumerate(output_snippets_group):
        
        
        if idx == 0:
            icon_char = "✗"
            accent_color = PresentationColors.ACCENT_BEARISH
            
            circle = Circle(radius=0.2, color=accent_color)

            icon = Text(icon_char, font_size=100, color=accent_color).scale(0.3)
            icon.move_to(circle.get_center())
            
            comment_icon_group = VGroup(circle, icon).scale(0.7)
            comment_icon_group.move_to(snippet.get_corner(DR))
            comment_icon_group.set_z_index(2)
            self.play(Create(circle))
            self.play(Create(icon))

            checked_snippet_group = VGroup(snippet, comment_icon_group)
            self.next_slide()
            self.play(FadeOut(checked_snippet_group))
        
        elif idx == 1:
            icon_char = "✓"
            accent_color = PresentationColors.ACCENT_BULLISH
            
            circle = Circle(radius=0.2, color=accent_color)
            icon = Text(icon_char, font_size=100, color=accent_color).scale(0.3)
            icon.move_to(circle.get_center())
            
            comment_icon_group = VGroup(circle, icon).scale(0.7)
            comment_icon_group.move_to(snippet.get_corner(DR))
            comment_icon_group.set_z_index(2)
            
            self.play(Create(circle))
            self.play(Create(icon))

            checked_snippet_group = VGroup(snippet, comment_icon_group)
            self.next_slide()
            self.play(FadeOut(comment_icon_group))
            snippet_critiqued_group.add(snippet)

        elif idx == 2:
            icon_char = "-"
            accent_color = PresentationColors.ACCENT_NEUTRAL
            
            circle = Circle(radius=0.2, color=accent_color)
            icon = Text(icon_char, font_size=100, color=accent_color).scale(0.3)
            icon.move_to(circle.get_center())
            
            comment_icon_group = VGroup(circle, icon).scale(0.7)
            comment_icon_group.move_to(snippet.get_corner(DR))
            comment_icon_group.set_z_index(2)

            self.play(Create(circle))
            self.play(Create(icon))

            checked_snippet_group = VGroup(snippet, comment_icon_group)
            snippet_critiqued_group.add(checked_snippet_group)
        
        self.next_slide()
    
    # ===== 5. Setup Dashboard Box and Path from Critical Box =====
    dashboard_box = RoundedRectangle(
        corner_radius=0.2,
        width=3.5,
        height=critical_box.height * 1.2,
        color=PresentationColors.ACCENT_MAIN,
        fill_color=self.camera.background_color,
        fill_opacity=1.0
    )
    dashboard_box.next_to(critical_box, LEFT, buff=1.0)
    dashboard_box.set_z_index(0)

    dashboard_t = Text("Dashboard", font_size=100, color=WHITE).scale(0.2)
    dashboard_t.next_to(dashboard_box.get_top(), DOWN, buff=0.1)
    dashboard_t.set_z_index(1)

    path_crit_to_dash = Line(
        critical_box.get_center(),
        dashboard_box.get_right(),
        stroke_width=4,
        color=PresentationColors.TEXT_PRIMARY
    ).set_z_index(-1)

    self.play(
        Create(dashboard_box),
        Write(dashboard_t),
        Create(path_crit_to_dash),
    )
    self.next_slide()

    # ===== 6. Create two zones inside Dashboard =====
    zone_h = dashboard_box.height * 0.8
    zone_w = (dashboard_box.width / 2) * 0.9

    bullish_zone = RoundedRectangle(
        width=zone_w, height=zone_h,
        fill_color=PresentationColors.ACCENT_BULLISH, fill_opacity=0.3,
        stroke_color=PresentationColors.ACCENT_BULLISH, stroke_width=2,
        corner_radius=0.2
    )
    bearish_zone = RoundedRectangle(
        width=zone_w, height=zone_h,
        fill_color=PresentationColors.ACCENT_BEARISH, fill_opacity=0.3,
        stroke_color=PresentationColors.ACCENT_BEARISH, stroke_width=2,
        corner_radius=0.2
    )

    zones = VGroup(bullish_zone, bearish_zone).arrange(RIGHT, buff=0.2)
    zones.move_to(dashboard_box.get_center() + DOWN * 0.2)
    zones.set_z_index(1)

    self.play(
        DrawBorderThenFill(bullish_zone),
        DrawBorderThenFill(bearish_zone)
    )
    self.next_slide()

    # ===== 7. Move critiqued rows (snippet+icon) into their zones =====
    # snippet_critiqued_group is a VGroup of VGroups: [snippet, icon]
    # Move all rows along the path in one go
    self.play(snippet_critiqued_group.animate.move_to(critical_box.get_center()))
    self.play(
        MoveAlongPath(
            snippet_critiqued_group,
            path_crit_to_dash,
            run_time=1.5
        )
    )
    self.next_slide()

    # Split into bullish vs. bearish, keeping rows intact
    bullish_rows = VGroup()
    bearish_rows = VGroup()
    for row in snippet_critiqued_group:
        snippet = row[0]
        if snippet.fill_color == PresentationColors.ACCENT_BULLISH:
            bullish_rows.add(row)
        else:
            bearish_rows.add(row)

    # Arrange each pile inside its zone, aligning left edges
    anims = []
    if bullish_rows:
        anims.append(
            bullish_rows.animate
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
                .move_to(bullish_zone.get_center())
        )
    if bearish_rows:
        anims.append(
            bearish_rows.animate
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
                .move_to(bearish_zone.get_center())
        )

    self.play(*anims, run_time=1.0)
    self.next_slide()
    self.wipe(self.mobjects, direction=UP)
