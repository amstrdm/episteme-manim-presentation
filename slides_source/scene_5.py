from manim import *
from manim_slides.slide.animation import Wipe

from .shared import PresentationColors

def Scene_5_Stock_Recommendations(self):
    # Aktien Vorschläge Folien Header
    aktien_t = Text("Aktien Vorschläge", font_size=100).scale(0.48)
    aktien_t.to_edge(UP, buff=0.2)

    # Wipe
    self.play(Write(aktien_t))
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