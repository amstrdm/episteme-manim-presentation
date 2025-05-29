from manim import *
from manim_slides.slide.animation import Wipe

def Scene6_Database(self):
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
    self.play(Wipe(VGroup(*self.mobjects), sqlalchemy_logo, shift=UP))
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
    self.play(Wipe(*self.mobjects, aktien_t, shift=UP))
    self.next_slide()

    # Google screenshot
    google_img = ImageMobject("assets/image.png")
    self.play(FadeIn(google_img))
    self.next_slide()
    
    # Fade out Google Screenshot
    self.play(FadeOut(google_img))
    self.next_slide()

    # type Goog text
    goog_t = Text("goog", font_size=100, color=PURPLE).scale(0.2)
    goog_t.next_to(aktien_t, DOWN, buff=0.2)
    cursor = Rectangle(
    color = GREY_A,
    fill_color = GREY_A,
    fill_opacity = 1.0,
    height = 1.1,
    width = 0.5,
    ).move_to(goog_t[0]) # Position the cursor

    self.play(TypeWithCursor(goog_t, cursor))
    self.play(Blink(cursor, blinks=2))
    self.play(FadeOut(cursor), run_time=0.1)
    self.next_slide()

    # Google Text
    google_t = Text("Google", font_size=100).scale(0.2)
    google_t.next_to(goog_t, DOWN, buff=2)

    # Arrow from goog to Google
    goog_googl_arrow = Arrow(goog_t, google_t, buff=0.1)

    self.play(GrowArrow(goog_googl_arrow))
    self.play(FadeIn(google_t))
    self.next_slide()

    # Visualize Trigrams
    trigram_group = VGroup()

    goo_tri = google_t[0:2].copy().set_color(YELLOW)
    trigram_group.add(goo_tri)
    self.play(trigram_group.animate.arrange(DOWN, buff=0.2).next_to(goog_googl_arrow, RIGHT))

    oog_tri = google_t[1:3].copy().set_color(YELLOW)
    trigram_group.add(oog_tri)
    self.play(trigram_group.animate.arrange(DOWN, buff=0.2).next_to(goog_googl_arrow, RIGHT))

    ogl_tri = google_t[2:4].copy().set_color(YELLOW)
    trigram_group.add(ogl_tri)
    self.play(trigram_group.animate.arrange(DOWN, buff=0.2).next_to(goog_googl_arrow, RIGHT))

    gle_tri = google_t[3:5].copy().set_color(YELLOW)
    trigram_group.add(gle_tri)
    self.play(trigram_group.animate.arrange(DOWN, buff=0.2).next_to(goog_googl_arrow, RIGHT))

    








