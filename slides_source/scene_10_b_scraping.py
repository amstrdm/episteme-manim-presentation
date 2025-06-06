from manim import *


def Scene_10_Bonus_Scraping(self):
    # Slide Header
    scraping_t = Text("Backend - Scraping", font_size=100).scale(0.48)
    scraping_t.to_edge(UP, buff=0.2)

    # Show .env icon and text
    env_icon = SVGMobject("assets/env_file_icon.svg", fill_color=GRAY_B)
    self.play(GrowFromCenter(env_icon))
    env_t = Text(".env", font_size=100).scale(0.25)
    env_t.next_to(env_icon, DOWN, buff=0.1)
    self.play(Write(env_t))
    self.next_slide()
    
    # Scale .env Icon and Text down and move to top left corner
    env_group = VGroup(env_icon, env_t)
    self.play(env_group.animate.scale(0.3))
    self.play(env_group.animate.to_corner(UL, buff=0.2))
    self.next_slide()

    # Spawn in Reddit logo in the center of the screen
    reddit_logo = SVGMobject("assets/reddit_logo.svg")
    reddit_logo.shift(UP * 2)
    self.play(DrawBorderThenFill(reddit_logo))
    self.next_slide()

    # Code Snippet for Reddit
    reddit_code_str = """
        import praw
            reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            )
            def find_reddit_posts(subreddit, stock_name, stock_ticker, timeframe, num_posts):
                subreddit_instance = reddit.subreddit(subreddit)
                query = f'"{stock_name}" OR "{stock_ticker}"'
                posts = subreddit_instance.search(query, limit=num_posts, time_filter=timeframe)
                filtered_data = [post for post in posts if len(post.selftext) > 100]
            
            def get_top_comments(submission, comment_limit=10):
                sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)
                top_comments = sorted_comments[:max(1, len(sorted_comments) // 4)]
    """
    reddit_code = Code(
        code_string=reddit_code_str,
        language="python",
        background="window",
        formatter_style="dracula",
        background_config={"stroke_color": "maroon"},
    ).scale(0.5)
    reddit_code.next_to(reddit_logo, DOWN, buff=0.2)
    self.play(Create(reddit_code), run_time=1.5)
    self.next_slide()

    # Make reddit code and logo small
    reddit_group = VGroup(reddit_logo, reddit_code)
    self.play(
        reddit_group.animate.scale(0.6).to_corner(UL, buff=0.2)
    )

    # Spawn in Seekingalpha logo in the center of the screen
    seekingalpha_logo = SVGMobject("assets/seekingalpha_logo.svg")
    seekingalpha_logo.shift(UP * 2)
    self.play(DrawBorderThenFill(seekingalpha_logo, stroke_color="#e74a18"))
    self.next_slide()

    # Code Snippet for Seekingalpha
    seekingalpha_code_str = """
        # --- Konzept Snippet: Seeking Alpha API Anfrage Flow ---

        # 1. Abrufen einer Liste von Artikel-IDs für einen bestimmten Ticker
        GET /analysis/v2/list?id=YOUR_STOCK_TICKER&size=NUM_POSTS

        # --- Dann, für jede „article_id“ aus der obigen Liste: ---

        # 2. Detaillierte Informationen zum jeweiligen Artikel abrufen
        GET /analysis/v2/get-details?id=SINGLE_ARTICLE_ID

        # 3. Abrufen der Kommentare des Artikels:
        #    a. Zuerst die Liste aller Kommentar IDs anfragen
                GET /comments/v2/list?id=SINGLE_ARTICLE_ID&sort=-top_parent_id

        #    b. Dann den Inhalt besagter Kommentare abrufen
                GET /comments/get-contents?id=SINGLE_ARTICLE_ID&comment_ids=COMMENT_ID_1,COMMENT_ID_2,...

        # --- Ende der Schleife ---    
    """
    seekingalpha_code = Code(
        code_string=seekingalpha_code_str,
        language="python",
        background="window",
        formatter_style="dracula",
        background_config={"stroke_color": "maroon"},
    ).scale(0.5)
    seekingalpha_code.next_to(seekingalpha_logo, DOWN, buff=0.2)
    self.play(Create(seekingalpha_code), run_time=1.5)
    self.next_slide()

    # Make seekingalpha code and logo small
    seekingalpha_group = VGroup(seekingalpha_logo, seekingalpha_code)
    self.play(
        seekingalpha_group.animate.scale(0.6).to_corner(UR, buff=0.2)
    )


    # Request Response below code 
    response_str = """
    {
        "source": "reddit",
        "subreddit": "wallstreetbets",
        "title": "$SPRY bet on the downfall of epi-pens",
        "author": "bakeshow55",
        "time_of_post": "16-08-2024",
        "upvotes": "27",
        "url": "https://www.reddit.com/r/wallstreetbets/comments/1etdjlg/spry_bet_on_the_downfall_of_epipens/",
        "content": "ARS Pharmaceuticals ($SPRY) just got approval for Neffy, a nasal spray...",
        "comments": [
            {
                "author": "None",
                "content": "The problem with the nasal spray, as I see it, is that it...",
                "url": "https://www.reddit.com/r/wallstreetbets/comments/1etdjlg/spry_bet_on_the_downfall_of_epipens/lico4jg/"
            },  
            {
                "author": "Chodemanbonbaglin",
                "content": "30 month shelf life, twice as long as the pen...",
                "url": "https://www.reddit.com/r/wallstreetbets/comments/1etdjlg/spry_bet_on_the_downfall_of_epipens/lickztm/"
            }
    }
    """
    response_code = Code(
        code_string=response_str,
        language="json",
        add_line_numbers=False,
        formatter_style="dracula",
        background="rectangle"
    ).scale(0.3)
    response_code.to_edge(DOWN)
    response_code.set_z_index(1)
    self.play(Create(response_code), run_time=1.5)
    self.next_slide()
    
    # Draw Arrows from code to request response

    # Reddit Arrow Points
    p0_r = reddit_code.get_bottom() + LEFT
    p1_r = np.array([p0_r[0], response_code.get_left()[1], 0])
    p2_r = response_code.get_left()

    reddit_req_arrow = Line(buff=0.2).set_points_as_corners([p0_r, p1_r, p2_r]).add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=0.15)
    
    # SeekingAlpha Arrow Points
    p0_s = seekingalpha_code.get_bottom() + RIGHT
    p1_s = np.array([p0_s[0], response_code.get_right()[1], 0])
    p2_s = response_code.get_right()

    seekingalpha_req_arrow = Line(buff=0.2).set_points_as_corners([p0_s, p1_s, p2_s]).add_tip(tip_shape=ArrowTriangleFilledTip, tip_length=0.15)
    
    # Animate Arrows
    self.play(Create(reddit_req_arrow), Create(seekingalpha_req_arrow))
    self.next_slide()

    self.play(response_code.animate.center().scale(1.4))
    self.next_slide()

    self.play(
        response_code.animate.scale(1/1.4).to_edge(DOWN)
    )
    self.next_slide()
    self.wipe(self.mobjects, direction=UP)