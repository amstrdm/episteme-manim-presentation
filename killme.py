from manim import *

class F1ScoreAnimation(Scene):
    """
    A Manim animation to visualize the F1 Score vs. Threshold
    for different language models.
    """
    def construct(self):
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
        x_label = axes.get_x_axis_label("Threshold", edge=DOWN, direction=DOWN)
        y_label = axes.get_y_axis_label("F1 Score", edge=LEFT, direction=LEFT, buff=0.4)
        title   = Title("Performance Curves: F1 Score vs Threshold", color=WHITE)

        # 3. Group everything (axes + labels), then shift it DOWN
        axes_group = VGroup(axes, x_label, y_label) \
            .to_edge(LEFT, buff=0.8) \
            .shift(DOWN * 0.2)  # ← shift down by 0.5 units

        # 4. Animate Title and Axes Group
        self.play(Write(title))  
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
        self.wait(3)
