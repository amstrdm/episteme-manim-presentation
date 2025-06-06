from manim import *
from manim_slides.slide.animation import Wipe

from .shared import PresentationColors

def Scene8_Bonus_Database(self):
    
    # 0. Configuration
    global_scale_factor = 0.7  # Overall scaling factor for the scene

    table_fill_color = BLUE_E
    table_stroke_color = BLUE_D
    table_text_color = WHITE
    column_text_color = LIGHT_GREY
    relationship_color = GOLD_A
    animation_run_time = 1.5  # Base run time for individual animation steps
    buff_space = 1.4 * global_scale_factor

    # 1. Define Tables (Entities) as Manim VGroups of Rectangles and Text
    def create_table_diagram(name, columns, fill_color, stroke_color, text_color, col_text_color):
        header_rect = Rectangle(
            width=4 * global_scale_factor,
            height=0.7 * global_scale_factor,
            fill_color=fill_color,
            fill_opacity=1,
            stroke_color=stroke_color,
            stroke_width=2 * global_scale_factor
        )
        table_name_text = Text(name, font_size=100 * global_scale_factor, color=text_color).scale(0.24).move_to(header_rect.get_center())
        header_group = VGroup(header_rect, table_name_text)

        column_rects_group = VGroup()
        internal_col_buff = 0.05 * global_scale_factor

        for col_name in columns:
            col_rect = Rectangle(
                width=4 * global_scale_factor,
                height=0.5 * global_scale_factor,
                fill_color=fill_color,
                fill_opacity=0.7,
                stroke_color=stroke_color,
                stroke_width=1.5 * global_scale_factor
            )
            if not column_rects_group:
                col_rect.next_to(header_rect, DOWN, buff=internal_col_buff)
            else:
                col_rect.next_to(column_rects_group[-1], DOWN, buff=internal_col_buff)
            
            col_text = Text(col_name, font_size=100 * global_scale_factor, color=col_text_color).scale(0.18).move_to(col_rect.get_center())
            column_rects_group.add(VGroup(col_rect, col_text))

        full_table_group = VGroup(header_group, column_rects_group)
        return full_table_group

    # Define column details
    ticker_cols = ["id (PK)", "symbol", "name", "description", "overall_sentiment_score", "last_analyzed", "description_last_analyzed"]
    post_cols = ["id (PK)", "ticker_id (FK)", "source", "title", "author", "link", "date_of_post", "content"]
    point_cols = ["id (PK)", "ticker_id (FK)", "post_id (FK)", "sentiment_score", "text", "criticism_exists", "embedding"]
    criticism_cols = ["id (PK)", "point_id (FK)", "comment_id (FK)", "text", "date_posted", "validity_score"]
    comment_cols = ["id (PK)", "post_id (FK)", "content", "link", "author"]

    # Create table Mobjects
    ticker_table = create_table_diagram("Ticker", ticker_cols, table_fill_color, table_stroke_color, table_text_color, column_text_color)
    post_table = create_table_diagram("Post", post_cols, table_fill_color, table_stroke_color, table_text_color, column_text_color)
    point_table = create_table_diagram("Point", point_cols, table_fill_color, table_stroke_color, table_text_color, column_text_color)
    criticism_table = create_table_diagram("Criticism", criticism_cols, table_fill_color, table_stroke_color, table_text_color, column_text_color)
    comment_table = create_table_diagram("Comment", comment_cols, table_fill_color, table_stroke_color, table_text_color, column_text_color)

    # 2. Position Tables Horizontally
    ticker_table.to_edge(LEFT, buff=buff_space * 0.5)
    post_table.next_to(ticker_table, RIGHT, buff=buff_space)
    point_shift_val = point_table.height / 2 * 1.2
    comment_shift_val = comment_table.height / 2 * 1.2
    point_table.next_to(post_table, RIGHT, buff=buff_space).shift(UP * point_shift_val)
    comment_table.next_to(post_table, RIGHT, buff=buff_space).shift(DOWN * comment_shift_val)
    criticism_table.next_to(point_table, RIGHT, buff=buff_space).align_to(post_table, UP)

    # 3. Define Relationships (Arrows)
    def get_column_vgroup(table_mobject, column_name_part):
        for col_vgroup in table_mobject[1]:
            if column_name_part.lower() in col_vgroup[1].text.lower():
                return col_vgroup[0]
        return table_mobject[0][0]

    arrow_stroke_width = 3 * global_scale_factor
    arrow_tip_length = 0.15 * global_scale_factor
    arrow_buff = 0.1 * global_scale_factor
    label_font_size = 20 * global_scale_factor # Using the font size as per your provided script
    label_buff = 0.05 * global_scale_factor

    # Ticker -> Post
    rel_ticker_post = Arrow(
        get_column_vgroup(ticker_table, "id (PK)").get_right(),
        get_column_vgroup(post_table, "ticker_id (FK)").get_left(),
        color=relationship_color, buff=arrow_buff, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_ticker_post_label = Tex("1..*", font_size=label_font_size, color=relationship_color).next_to(rel_ticker_post.get_center(), UP, buff=label_buff)

    # Ticker -> Point (Curved Arrow over Post)
    rel_ticker_point = CurvedArrow(
        get_column_vgroup(ticker_table, "id (PK)").get_top(),
        get_column_vgroup(point_table, "ticker_id (FK)").get_left(),
        angle=-PI / 3,
        color=relationship_color, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_ticker_point_label = Tex("1..*", font_size=label_font_size, color=relationship_color).next_to(rel_ticker_point.point_from_proportion(0.5), DOWN, buff=label_buff*2)

    # Post -> Point
    rel_post_point = Arrow(
        get_column_vgroup(post_table, "id (PK)").get_right(),
        get_column_vgroup(point_table, "post_id (FK)").get_left(),
        color=relationship_color, buff=arrow_buff, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_post_point_label = Tex("1..*", font_size=label_font_size, color=relationship_color).next_to(rel_post_point.get_center(), UL, buff=label_buff)

    # Post -> Comment
    rel_post_comment = Arrow(
        get_column_vgroup(post_table, "id (PK)").get_right(),
        get_column_vgroup(comment_table, "post_id (FK)").get_left(),
        color=relationship_color, buff=arrow_buff, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_post_comment_label = Tex("1..*", font_size=label_font_size, color=relationship_color).next_to(rel_post_comment.get_center(), DL, buff=label_buff)

    # Point -> Criticism
    rel_point_criticism = Arrow(
        get_column_vgroup(point_table, "id (PK)").get_right(),
        get_column_vgroup(criticism_table, "point_id (FK)").get_left(),
        color=relationship_color, buff=arrow_buff, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_point_criticism_label = Tex("1..*", font_size=label_font_size, color=relationship_color).next_to(rel_point_criticism.get_center(), UR, buff=label_buff)

    # Comment -> Criticism
    rel_comment_criticism = Arrow(
        get_column_vgroup(comment_table, "id (PK)").get_right(),
        get_column_vgroup(criticism_table, "comment_id (FK)").get_left(),
        color=relationship_color, buff=arrow_buff, stroke_width=arrow_stroke_width,
        tip_shape=ArrowTriangleFilledTip, tip_length=arrow_tip_length
    )
    rel_comment_criticism_label = Tex("0..*", font_size=label_font_size, color=relationship_color).next_to(rel_comment_criticism.get_center(), DR, buff=label_buff)

    # Group all visual elements to center them on screen
    all_diagram_elements = VGroup(
        ticker_table, post_table, point_table, comment_table, criticism_table,
        rel_ticker_post, rel_ticker_post_label,
        rel_ticker_point, rel_ticker_point_label,
        rel_post_point, rel_post_point_label,
        rel_post_comment, rel_post_comment_label,
        rel_point_criticism, rel_point_criticism_label,
        rel_comment_criticism, rel_comment_criticism_label
    )
    all_diagram_elements.move_to(ORIGIN) # Center the whole diagram

    # 4. Animate
    title_text = Text("Database Schema Visualization", font_size=100 * global_scale_factor).scale(0.5).to_edge(UP, buff=0.2 * global_scale_factor)
    
    # Initial state: Only title is implicitly there or nothing from the diagram yet.
    # All diagram elements are positioned but not yet added to the scene.

    self.play(Write(title_text), run_time=animation_run_time)
    self.next_slide()

    # Create Ticker table
    self.play(FadeIn(ticker_table, shift=LEFT * 0.2 * global_scale_factor), run_time=animation_run_time)
    self.next_slide()

    # Create Post table
    self.play(FadeIn(post_table, shift=LEFT * 0.2 * global_scale_factor), run_time=animation_run_time)
    self.next_slide()

    # Create arrow from Ticker to Post (and its label)
    self.play(GrowArrow(rel_ticker_post), Write(rel_ticker_post_label), run_time=animation_run_time)
    self.next_slide()

    # Create Point table
    self.play(FadeIn(point_table, shift=LEFT * 0.2 * global_scale_factor), run_time=animation_run_time)
    self.next_slide()

    # Create arrow from Ticker to Point (and its label)
    self.play(Create(rel_ticker_point), Write(rel_ticker_point_label), run_time=animation_run_time)
    self.next_slide()

    # Create arrow from Post to Point (and its label)
    self.play(GrowArrow(rel_post_point), Write(rel_post_point_label), run_time=animation_run_time)
    self.next_slide()

    # Create Comment table
    self.play(FadeIn(comment_table, shift=LEFT * 0.2 * global_scale_factor), run_time=animation_run_time)
    self.next_slide()

    # Create arrow from Post to Comment (and its label)
    self.play(GrowArrow(rel_post_comment), Write(rel_post_comment_label), run_time=animation_run_time)
    self.next_slide()

    # Create Criticism table
    self.play(FadeIn(criticism_table, shift=LEFT * 0.2 * global_scale_factor), run_time=animation_run_time)
    self.next_slide()

    # Create arrows from Point to Criticism and Comment to Criticism (and their labels) at the same time
    self.play(
        GrowArrow(rel_point_criticism), Write(rel_point_criticism_label),
        GrowArrow(rel_comment_criticism), Write(rel_comment_criticism_label),
        run_time=animation_run_time # You might want to increase run_time if it feels too fast for two arrows
    )
    self.next_slide() # Optional: slide break after the last animation, before final wait

    # Add sqlalchemy logo for Wipe in
    sqlalchemy_logo = SVGMobject("assets/sqlalchemy_logo.svg")
    sqlalchemy_logo.to_edge(UP)

    # Move everything out/in
    self.play(Wipe(Group(*self.mobjects), sqlalchemy_logo, shift=UP))
    self.next_slide()
    
    # Add sessionscope code snippet
    sessionscope_code_str = """
    @contextmanager
    def session_scope():
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    """
    sessioncope_code = Code(
        code_string=sessionscope_code_str,
        language="python",
        background="window",
        formatter_style="dracula",
    )
    sessioncope_code.scale(0.8).next_to(sqlalchemy_logo, DOWN, buff=0.3)
    self.play(Create(sessioncope_code))
    self.next_slide()

    # Aktien Vorschläge Folien Header
    aktien_t = Text("Aktien Vorschläge", font_size=100).scale(0.48)
    aktien_t.to_edge(UP, buff=0.2)

    # Wipe
    self.play(Wipe(Group(*self.mobjects), aktien_t, shift=UP))
    self.next_slide()

    # Google screenshot
    google_img = ImageMobject("assets/image.png")
    self.play(FadeIn(google_img))
    self.next_slide()
    
    # Fade out Google Screenshot
    self.play(FadeOut(google_img))
    self.next_slide()

    goog_str = "GOOG"
    # Type Goog text
    goog_t = Text(goog_str, color=PURPLE)
    goog_t.next_to(aktien_t, DOWN, buff=0.4)
    cursor = Rectangle(
    color = GREY_A,
    fill_color = GREY_A,
    fill_opacity = 1.0,
    height = 0.5,
    width = 0.25,
    ).move_to(goog_t[0]) # Position the cursor

    self.play(TypeWithCursor(goog_t, cursor))
    self.play(Blink(cursor, blinks=2))
    self.play(FadeOut(cursor), run_time=0.1)
    cursor.set_opacity(0)
    self.next_slide()

    # Google Text
    word = "GOOGLE"
    google = Text(word)
    google.next_to(goog_t, DOWN, buff=4)

    # Arrow from goog to Google
    goog_googl_arrow = Arrow(goog_t.get_bottom(), google.get_top(), buff=0.1)

    self.play(GrowArrow(goog_googl_arrow))
    self.play(FadeIn(google))
    self.next_slide()

    google_arrow_group = VGroup(goog_t, google, goog_googl_arrow)
    self.play(google_arrow_group.animate.shift(3 * LEFT))

    # Remove Arrow
    self.play(FadeOut(goog_googl_arrow))

    # Position 'GOOGLE' above the table
    self.play(google.animate.to_edge(RIGHT, buff=2).align_to(goog_t, UP))
    self.next_slide()

    # Define the Google trigrams
    tris = [word[i:i+3] for i in range(len(word) - 2)]

    # Create the table: one header row + one row per trigram
    table_data = [["Trigram", "Stock"]] + [[tri, "[Google]"] for tri in tris]
    table = Table(
        table_data,
        include_outer_lines=True,
    ).scale(0.7).next_to(google, DOWN, buff=0.5)
    table.get_rows().set_opacity(0)

    # Create Table
    self.play(Create(table), run_time=3)
    self.next_slide()

    self.play(table.get_rows()[0].animate.set_opacity(1))

    # Break 'GOOGLE' into individual letters at same position
    letters = VGroup(*[Text(c) for c in word])
    letters.arrange(RIGHT, buff=0.3).move_to(google.get_center())
    self.play(ReplacementTransform(google, letters))
    self.next_slide()

    # Animate each trigram: highlight, label, drag into table, remove box
    for i, tri in enumerate(tris, start=0):
        # Highlight the current three letters
        tri_chars = letters[i : i + 3]
        box = SurroundingRectangle(tri_chars, color=YELLOW, buff=0.1)
        self.play(Create(box), run_time=0.5)

        # Show the trigram text below
        tri_label = tri_chars.copy()

        # Drag the label into the corresponding table cell
        # Header row is index 1, data rows start at 2
        target = table.get_cell((i + 2, 1))
        self.play(tri_label.animate.move_to(target.get_center()).set_color(YELLOW), run_time=0.7)
        self.wait(0.2)

        # Remove only the highlight rectangle
        self.play(FadeOut(box))
        self.wait(0.2)
    self.next_slide()

    # Animate [Google] Columns in
    for i in range(len(tris)):
        # row = i+2, col = 2
        row_index = i + 2
        col_index = 2

        # Grab the Text mobject inside that cell.
        # If you’re using Manim’s Table, you can do:
        stock_text = table.get_entries((row_index, col_index))

        # Make sure it’s visible (in case you set opacity to 0 before):
        stock_text.set_opacity(1)

        # Animate it writing in / fading in:
        self.play(Write(stock_text), run_time=0.5)
    self.next_slide()

    # Split "GOOG" into letters, highlight its trigrams, and animate them
    letters_goog = VGroup(*[Text(c, color=PURPLE) for c in goog_str])
    letters_goog.arrange(RIGHT, buff=0.3).move_to(goog_t.get_center())
    self.play(ReplacementTransform(goog_t, letters_goog))
    self.next_slide()

    # 2. Build the list of "GOOG" trigrams and animate each in red, moving them below the word
    tris_goog = [ "GOO", "OOG" ]
    goo_label = None
    oog_label = None

    for i, tri in enumerate(tris_goog):
        # Highlight the three‐letter slice in red
        tri_chars_goog = letters_goog[i : i + 3]
        box_red = SurroundingRectangle(tri_chars_goog, color=RED, buff=0.1)
        self.play(Create(box_red), run_time=0.5)

        # Copy those three letters as a red label
        tri_label_goog = tri_chars_goog.copy().set_color(RED)

        # Decide where to drop it: just below “GOOG,” slightly left or right so they don't overlap
        base_center = letters_goog.get_center()
        if i == 0:
            # first trigram ("GOO") goes below + slightly left
            target_pos = base_center + DOWN * 1 + LEFT * 1.2
            goo_label = tri_label_goog
        else:
            # second trigram ("OOG") goes below + slightly right
            target_pos = base_center + DOWN * 1 + RIGHT * 1.2
            oog_label = tri_label_goog

        self.play(tri_label_goog.animate.move_to(target_pos), run_time=0.7)
        self.wait(0.1)

        # Remove only the red highlight rectangle
        self.play(FadeOut(box_red))
        self.wait(0.2)

    self.next_slide()

    # 3. Slide the "OOG" label straight down the left of the table, row by row,
    #    until it reaches the row where the table’s first‐column cell is also "OOG".
    #    Then surround that table row + the moving label with a green box.

    # Choose an x‐coordinate just to the left of the entire table
    left_of_table = table.get_left()[0] - 2

    # We know our original “google” trigrams were ['goo','oog','ogl','gle'] in rows 2..5.
    # So “OOG” lives in data‐row index = (tris.index("oog") + 2) = (1 + 2) = 3.
    target_row_oog = 3

    for row in range(2, len(tris) + 2):  # rows 2,3,4,5…
        # y‐position of the first‐column cell in this row:
        mid_y = table.get_cell((row, 1)).get_center()[1]
        # move "OOG" label to (left_of_table, mid_y)
        self.play(
            oog_label.animate.move_to([left_of_table, mid_y, 0]),
            run_time=0.3
        )
        if row == target_row_oog:
            # get the entire row as a VGroup
            row_mob = table.get_rows()[row - 1]  
            # Surround both that row and the "OOG" label in green
            highlight_oog = SurroundingRectangle(
                VGroup(row_mob, oog_label),
                color=PresentationColors.ACCENT_MAIN,
                buff=0.1
            )
            self.play(Create(highlight_oog))
            break

    self.wait(0.5)
    self.next_slide()

    # 4. Now repeat the same “drop” animation for "GOO":
    #    It should go down until it hits row 2 (since “goo” was the very first trigram).
    target_row_goo = 2

    for row in range(2, len(tris) + 2):
        mid_y = table.get_cell((row, 1)).get_center()[1]
        self.play(
            goo_label.animate.move_to([left_of_table, mid_y, 0]),
            run_time=0.3    
        )
        if row == target_row_goo:
            row_mob = table.get_rows()[row - 1]
            highlight_goo = SurroundingRectangle(
                VGroup(row_mob, goo_label),
                color=PresentationColors.ACCENT_MAIN,
                buff=0.1
            )
            self.play(Create(highlight_goo))
            break

    self.next_slide()

    # Title
    title = Text("Gewichtete Relevanz + Priorität", font_size=48)
    title.to_edge(UP)

    self.play(Wipe(Group(*self.mobjects), title, UP))
    
    # Bulleted explanation lines (one bullet per slide)
    lines = [
        "• Exact ticker matches → fixed score = 1.0",
        "• Partial ticker vs. query → SIMILARITY(ticker, query) * 0.8",
        "• Title match → SIMILARITY(title, query) * 0.2",
        "• Final relevance = max(exact_score, partial_ticker_score + title_score)",
        "• ORDER BY relevance DESC, LIMIT 10"
    ]

    # Pre-compute final positions of all bullets, but don’t draw them yet
    bullet_texts = VGroup(*[
        Text(line, font_size=20) for line in lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    bullet_texts.next_to(title, DOWN, buff=1)

    # Reveal each bullet on its own slide
    for bt in bullet_texts:
        self.next_slide()
        self.play(FadeIn(bt))

    # After all bullets have appeared, move to the next slide for the example
    self.next_slide()

    # “In practice, this means…” example (in BLUE)
    example_lines = [
        "Beispiel “NU”:",
        "  1. Ticker “NU” (score = 1.0)",
        "  2. Andere Ticker, welche “NU” beinhalten (z.B. “NUDI”), nach Ticker-Ähnlichkeit",
        "  3. Firmen, deren Namen “nu” beinhalten (z.B. “Nu Holdings Ltd.”)"
    ]
    example_texts = VGroup(*[
        Text(line, font_size=20, color=BLUE) for line in example_lines
    ]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    example_texts.next_to(bullet_texts, DOWN, buff=0.8, aligned_edge=LEFT)

    self.play(FadeIn(example_texts))

    self.next_slide()
    self.wipe(self.mobjects, direction=UP)