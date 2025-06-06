from manim import *

from .shared import PresentationColors

import numpy as np

def Scene_4_Cosine_Similarity(self):
    # This initial part of your code remains unchanged
    header_t = Text("Duplikate ausfiltern", font_size=48)
    header_t.to_edge(UP, buff=0.2)
    self.play(Write(header_t))
    self.next_slide()

    temp_sentences = ["EPS grew by 5% YOY", "Earnings increased slightly"]

    similar_sentences = [
        {"content": "I enjoy reading books daily", "embedding": [[1.0000], [0.0000]]},
        {"content": "I love reading books daily", "embedding": [[0.9848], [0.1736]]}
    ]
    distinct_sentences = [
        {"content": "Cats chase mice all night", "embedding": [[1.0], [0.1]]},
        {"content": "Cars speed down highways fast", "embedding": [[0.1], [1.0]]}
    ]
    opposite_sentences = [
        {"content": "I enjoy reading books daily", "embedding": [[1.0000], [0.0000]]},
        {"content": "I hate reading books daily", "embedding": [[-0.9848], [0.1736]]}
    ]

    temp_sentence_1 = Text(temp_sentences[0], font_size=20, color=RED).to_edge(LEFT, buff=2)
    temp_sentence_2 = Text(temp_sentences[1], font_size=20, color=BLUE).to_edge(LEFT, buff=2)
    temp_sentence_1.shift(UP * 2)
    temp_sentence_2.next_to(temp_sentence_1, DOWN, buff=1.5, aligned_edge=LEFT)

    sim_sentence_1 = Text(similar_sentences[0]["content"], font_size=20, color=RED).to_edge(LEFT, buff=2)
    sim_sentence_2 = Text(similar_sentences[1]["content"], font_size=20, color=BLUE).to_edge(LEFT, buff=2)
    sim_sentence_1.shift(UP * 2)
    sim_sentence_2.next_to(sim_sentence_1, DOWN, buff=1.5, aligned_edge=LEFT)

    sentence_group = VGroup(sim_sentence_1, sim_sentence_2)

    self.play(Write(temp_sentence_1), Write(temp_sentence_2))
    self.next_slide()

    self.play(ReplacementTransform(temp_sentence_1, sim_sentence_1), ReplacementTransform(temp_sentence_2, sim_sentence_2))
    self.next_slide()

    st_t = Text("Sentence Transformer", font_size=25, color=PresentationColors.ACCENT_MAIN)
    st_t.set_z_index(2)
    self.play(Write(st_t))
    self.next_slide()

    st_box = Rectangle(color=WHITE, height=2, width=4, fill_color=PresentationColors.BACKGROUND, fill_opacity=1.0)
    st_box.to_edge(DOWN, buff=0.3)
    st_box.set_z_index(1)

    self.play(Create(st_box), st_t.animate.move_to(st_box.get_center()))
    self.next_slide()

    matrix_dict = {}
    for idx, sentence in enumerate(sentence_group):
        sent_temp = sentence.copy()
        sent_temp.set_z_index(0)
        self.play(sent_temp.animate.next_to(st_box, LEFT, buff=1))
        self.next_slide()
        self.play(sent_temp.animate.move_to(st_box.get_center()).scale(0.3))
        self.play(FadeOut(sent_temp, run_time=0.1))
        self.next_slide()
        matrix = Matrix(similar_sentences[idx]["embedding"], h_buff=1.5, element_to_mobject=DecimalNumber).scale_to_fit_height(st_box.height * 0.4).set_z_index(0)
        matrix.set_color(RED if idx == 0 else BLUE)
        matrix.move_to(st_box.get_center())
        matrix_dict[f"matrix_{idx}"] = matrix
        self.play(matrix.animate.next_to(st_box, buff=1))
        self.wait(1)
        self.play(matrix.animate.next_to(sentence_group[idx], RIGHT, buff=0.2))
        self.next_slide()

    self.play(FadeOut(st_box), FadeOut(st_t))
    self.next_slide()

    sentence_embedding_group = VGroup(sentence_group, *matrix_dict.values())
    self.play(sentence_embedding_group.animate.to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=1))
    self.next_slide()

    axes = Axes(x_range=[-1.2, 1.2, 0.4], y_range=[-1.2, 1.2, 0.4], axis_config={"include_tip": True, "stroke_width": 2, "font_size": 24}).add_coordinates(font_size=20)
    axes.center().to_edge(UP, buff=0.8)

    v1_coords = np.array(similar_sentences[0]["embedding"]).flatten()
    v2_coords = np.array(similar_sentences[1]["embedding"]).flatten()

    vector_1 = Arrow(start=axes.c2p(0, 0), end=axes.c2p(v1_coords[0], v1_coords[1]), buff=0, color=RED, stroke_width=5)
    vector_2 = Arrow(start=axes.c2p(0, 0), end=axes.c2p(v2_coords[0], v2_coords[1]), buff=0, color=BLUE, stroke_width=5)
    
    self.play(Create(axes), LaggedStart(GrowArrow(vector_1), GrowArrow(vector_2)))
    self.next_slide()
    
    angle_obj = Angle(vector_1, vector_2, radius=min(vector_1.get_length(), vector_2.get_length()) * 0.8, color=YELLOW)
    angle_val = DecimalNumber(angle_obj.get_value(degrees=True), num_decimal_places=1, color=YELLOW, font_size=30)
    angle_label = VGroup(angle_val, MathTex(r"^\circ", color=YELLOW, font_size=30)).arrange(RIGHT, buff=0.05)
    angle_label.move_to(angle_obj.point_from_proportion(0.5) * 1.2)

    formula_placeholders = MathTex(r"\text{sim} = \cos(\theta) = \frac{A \cdot B}{\|A\| \cdot \|B\|}", font_size=36).to_edge(RIGHT, buff=1.5).to_edge(DOWN, buff=2)
    self.play(Create(angle_obj), Write(angle_label))
    self.play(Write(formula_placeholders))
    self.next_slide()

    v1_x_tracker = ValueTracker(v1_coords[0])
    v1_y_tracker = ValueTracker(v1_coords[1])
    v2_x_tracker = ValueTracker(v2_coords[0])
    v2_y_tracker = ValueTracker(v2_coords[1])
    
    initial_angle_in_degrees = np.degrees(np.arccos(np.clip(np.dot(v1_coords, v2_coords) / (np.linalg.norm(v1_coords) * np.linalg.norm(v2_coords)), -1, 1)))
    cos_theta_val = DecimalNumber(initial_angle_in_degrees, num_decimal_places=1, color=YELLOW, font_size=36)
    
    dot_v1x = DecimalNumber(v1_coords[0], font_size=30)
    dot_v1y = DecimalNumber(v1_coords[1], font_size=30)
    dot_v2x = DecimalNumber(v2_coords[0], font_size=30)
    dot_v2y = DecimalNumber(v2_coords[1], font_size=30)
    norm_A_v1x = DecimalNumber(v1_coords[0], font_size=30, color=RED)
    norm_A_v1y = DecimalNumber(v1_coords[1], font_size=30, color=RED)
    norm_B_v2x = DecimalNumber(v2_coords[0], font_size=30, color=BLUE)
    norm_B_v2y = DecimalNumber(v2_coords[1], font_size=30, color=BLUE)
    
    formula_intro = VGroup(MathTex(r"\cos("), cos_theta_val, MathTex(r"^\circ) =")).arrange(RIGHT, buff=0.05)
    dot_prod_calc = VGroup(MathTex("("), dot_v1x, MathTex(r"\cdot"), dot_v2x, MathTex(") + ("), dot_v1y, MathTex(r"\cdot"), dot_v2y, MathTex(")")).arrange(RIGHT, buff=0.1)
    norm_A_calc = VGroup(MathTex(r"\sqrt{"), norm_A_v1x, MathTex("^2+"), norm_A_v1y, MathTex("^2}"), color=RED).arrange(RIGHT, buff=0.05)
    norm_B_calc = VGroup(MathTex(r"\sqrt{"), norm_B_v2x, MathTex("^2+"), norm_B_v2y, MathTex("^2}"), color=BLUE).arrange(RIGHT, buff=0.05)
    denominator_calc = VGroup(norm_A_calc, MathTex(r"\cdot"), norm_B_calc).arrange(RIGHT, buff=0.1)
    
    line_calc = Line(LEFT, RIGHT).set_width(denominator_calc.width + 0.2)
    fraction_calc = VGroup(dot_prod_calc, line_calc, denominator_calc).arrange(DOWN, buff=0.35)
    full_formula_calc = VGroup(formula_intro, fraction_calc).arrange(RIGHT, buff=0.2).scale(0.7).move_to(formula_placeholders)

    self.play(ReplacementTransform(formula_placeholders, full_formula_calc))
    self.next_slide()

    initial_sim_val = np.dot(v1_coords, v2_coords) / (np.linalg.norm(v1_coords) * np.linalg.norm(v2_coords))
    final_sim_value = DecimalNumber(initial_sim_val, num_decimal_places=4, font_size=36, color=YELLOW).move_to(full_formula_calc)
    sim_t = Text("sim =", font_size=36).next_to(final_sim_value, LEFT, buff=0.2)
    sim_group = VGroup(final_sim_value, sim_t)

    self.play(
        FadeOut(fraction_calc),
        ReplacementTransform(formula_intro, sim_group)
    )
    self.next_slide()
    
    # Attach all updaters
    vector_1.add_updater(lambda m: m.put_start_and_end_on(axes.c2p(0,0), axes.c2p(v1_x_tracker.get_value(), v1_y_tracker.get_value())))
    vector_2.add_updater(lambda m: m.put_start_and_end_on(axes.c2p(0,0), axes.c2p(v2_x_tracker.get_value(), v2_y_tracker.get_value())))
    
    def angle_object_updater(mob):
        radius = min(vector_1.get_length(), vector_2.get_length()) * 0.8
        mob.become(Angle(vector_1, vector_2, radius=radius, color=YELLOW))
    angle_obj.add_updater(angle_object_updater)

    # --- THIS IS THE CORRECTED UPDATER ---
    # This updater is now self-contained and does not rely on the angle_obj mobject,
    # which prevents issues with the .become() method.
    def angle_label_updater(mob):
        # Create a temporary Angle to get the value, which is more reliable.
        temp_angle = Angle(vector_1, vector_2)
        mob[0].set_value(temp_angle.get_value(degrees=True))
        mob.arrange(RIGHT, buff=0.05)
        
        # For positioning, we need to recreate the arc geometry from the live vectors
        temp_pos_arc = Angle(vector_1, vector_2, radius=min(vector_1.get_length(), vector_2.get_length()) * 0.8)
        mob.move_to(temp_pos_arc.point_from_proportion(0.5) * 1.2)
    
    angle_label.add_updater(angle_label_updater)
    # --- END OF FIX ---

    matrix_1 = matrix_dict["matrix_0"]
    matrix_2 = matrix_dict["matrix_1"]
    matrix_1.get_entries()[0].add_updater(lambda m: m.set_value(v1_x_tracker.get_value()))
    matrix_1.get_entries()[1].add_updater(lambda m: m.set_value(v1_y_tracker.get_value()))
    matrix_2.get_entries()[0].add_updater(lambda m: m.set_value(v2_x_tracker.get_value()))
    matrix_2.get_entries()[1].add_updater(lambda m: m.set_value(v2_y_tracker.get_value()))
    
    def final_sim_updater(mob):
        v1 = np.array([v1_x_tracker.get_value(), v1_y_tracker.get_value()])
        v2 = np.array([v2_x_tracker.get_value(), v2_y_tracker.get_value()])
        norm_prod = np.linalg.norm(v1) * np.linalg.norm(v2)
        sim = np.dot(v1, v2) / norm_prod if norm_prod != 0 else 0
        mob[0].set_value(sim)
        
    sim_group.add_updater(final_sim_updater)

    new_sentence_1 = Text(distinct_sentences[0]["content"], font_size=20, color=RED).move_to(sim_sentence_1)
    new_sentence_2 = Text(distinct_sentences[1]["content"], font_size=20, color=BLUE).move_to(sim_sentence_2)
    
    self.play(
        ReplacementTransform(sim_sentence_1, new_sentence_1),
        ReplacementTransform(sim_sentence_2, new_sentence_2),
        matrix_dict["matrix_0"].animate.next_to(new_sentence_1, RIGHT, buff=0.2),
        matrix_dict["matrix_1"].animate.next_to(new_sentence_2, RIGHT, buff=0.2),
        v1_x_tracker.animate.set_value(distinct_sentences[0]["embedding"][0][0]),
        v1_y_tracker.animate.set_value(distinct_sentences[0]["embedding"][1][0]),
        v2_x_tracker.animate.set_value(distinct_sentences[1]["embedding"][0][0]),
        v2_y_tracker.animate.set_value(distinct_sentences[1]["embedding"][1][0]),
        run_time=4
    )
    self.next_slide()

    title = Title("Leistungs Kurven: F1 Score vs Obergrenze", color=WHITE)
    self.wipe(self.mobjects, title, direction=UP)

    # Data from the user
    evaluation_summary = {
        "ada-002": [
            {"threshold": 0.10, "f1": 0.730}, {"threshold": 0.15, "f1": 0.730},
            {"threshold": 0.20, "f1": 0.730}, {"threshold": 0.25, "f1": 0.730},
            {"threshold": 0.30, "f1": 0.730}, {"threshold": 0.35, "f1": 0.730},
            {"threshold": 0.40, "f1": 0.730}, {"threshold": 0.45, "f1": 0.730},
            {"threshold": 0.50, "f1": 0.730}, {"threshold": 0.55, "f1": 0.730},
            {"threshold": 0.60, "f1": 0.730}, {"threshold": 0.65, "f1": 0.730},
            {"threshold": 0.70, "f1": 0.730}, {"threshold": 0.75, "f1": 0.730},
            {"threshold": 0.80, "f1": 0.868}, {"threshold": 0.85, "f1": 0.978},
            {"threshold": 0.90, "f1": 0.955}
        ],
        "3-small": [
            {"threshold": 0.10, "f1": 0.730}, {"threshold": 0.15, "f1": 0.730},
            {"threshold": 0.20, "f1": 0.754}, {"threshold": 0.25, "f1": 0.780},
            {"threshold": 0.30, "f1": 0.868}, {"threshold": 0.35, "f1": 0.939},
            {"threshold": 0.40, "f1": 0.939}, {"threshold": 0.45, "f1": 0.957},
            {"threshold": 0.50, "f1": 0.957}, {"threshold": 0.55, "f1": 0.957},
            {"threshold": 0.60, "f1": 0.978}, {"threshold": 0.65, "f1": 0.955},
            {"threshold": 0.70, "f1": 0.878}, {"threshold": 0.75, "f1": 0.821},
            {"threshold": 0.80, "f1": 0.562}, {"threshold": 0.85, "f1": 0.083},
            {"threshold": 0.90, "f1": 0.000}
        ],
        "MiniLM": [
            {"threshold": 0.10, "f1": 0.730}, {"threshold": 0.15, "f1": 0.807},
            {"threshold": 0.20, "f1": 0.902}, {"threshold": 0.25, "f1": 0.920},
            {"threshold": 0.30, "f1": 0.979}, {"threshold": 0.35, "f1": 0.979},
            {"threshold": 0.40, "f1": 1.000}, {"threshold": 0.45, "f1": 0.978},
            {"threshold": 0.50, "f1": 0.930}, {"threshold": 0.55, "f1": 0.878},
            {"threshold": 0.60, "f1": 0.850}, {"threshold": 0.65, "f1": 0.821},
            {"threshold": 0.70, "f1": 0.789}, {"threshold": 0.75, "f1": 0.647},
            {"threshold": 0.80, "f1": 0.296}, {"threshold": 0.85, "f1": 0.083},
            {"threshold": 0.90, "f1": 0.083}
        ],
        "FinLang": [
            {"threshold": 0.10, "f1": 0.742}, {"threshold": 0.15, "f1": 0.742},
            {"threshold": 0.20, "f1": 0.754}, {"threshold": 0.25, "f1": 0.836},
            {"threshold": 0.30, "f1": 0.852}, {"threshold": 0.35, "f1": 0.939},
            {"threshold": 0.40, "f1": 0.958}, {"threshold": 0.45, "f1": 0.958},
            {"threshold": 0.50, "f1": 0.936}, {"threshold": 0.55, "f1": 0.957},
            {"threshold": 0.60, "f1": 0.930}, {"threshold": 0.65, "f1": 0.930},
            {"threshold": 0.70, "f1": 0.850}, {"threshold": 0.75, "f1": 0.850},
            {"threshold": 0.80, "f1": 0.757}, {"threshold": 0.85, "f1": 0.414},
            {"threshold": 0.90, "f1": 0.231}
        ]
    }
    
    # 1. Create Axes WITH add_coordinates(), but NO numbers_to_include
    axes = Axes(
        x_range=[0.05, 0.95, 0.1],
        y_range=[0, 1.1, 0.2],
        x_length=9,
        y_length=5.5,
        axis_config={"color": BLUE},
        x_axis_config={"include_tip": False},
        y_axis_config={"include_tip": False},
    ).add_coordinates()  # Labels at every tick: 0.1, 0.2, …, 0.9 on x

    # 2. Create Labels and Title
    x_label = axes.get_x_axis_label("Obergrenze", edge=DOWN, direction=DOWN)
    y_label = axes.get_y_axis_label("F1 Score", edge=LEFT, direction=LEFT, buff=0.4)

    # 3. Group everything (axes + labels), then shift it DOWN
    axes_group = VGroup(axes, x_label, y_label) \
        .to_edge(LEFT, buff=0.8) \
        .shift(DOWN * 0.2)  # ← shift down by 0.5 units

    # 4. Animate Title and Axes Group  
    self.play(Create(axes_group))
    self.wait(0.5)

    # 5. Plot each model & build legend (exactly as before)
    model_colors = [YELLOW, GREEN, RED, PURPLE]
    legend_items = []

    for model, color in zip(evaluation_summary.keys(), model_colors):
        # Plot line + dots
        pts = [axes.coords_to_point(e["threshold"], e["f1"])
                for e in evaluation_summary[model]]
        line = VMobject(color=color).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, color=color, radius=0.05) for p in pts])

        self.play(Create(line), run_time=2)
        self.play(FadeIn(dots, scale=0.5), run_time=1)

        # Legend entry for this model
        legend_item = VGroup(
            Text(model, font_size=24, color=WHITE),
            Line(color=color, stroke_width=10).scale(0.3)
        ).arrange(RIGHT, buff=0.2).scale(0.7)
        legend_items.append(legend_item)

    # 6. Group and position the legend, then shift it DOWN to match
    legend = VGroup(*legend_items) \
        .arrange(DOWN, aligned_edge=RIGHT, buff=0.3) \
        .to_corner(UP + RIGHT, buff=0.5) \
        .shift(DOWN * 1)  # ← shift down by 0.5 units

    self.play(Write(legend))
    self.next_slide()

    self.wipe(self.mobjects, direction=UP)