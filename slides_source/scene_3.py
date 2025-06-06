from manim import *

from .shared import PresentationColors


def Scene3_Technology_Stack(self):
    # Slide Header
    bausteine_t = Text("Die Bausteine", font_size=100).scale(0.48)
    bausteine_t.to_edge(UP, buff=0.2)
    self.play(Write(bausteine_t))
    self.next_slide()

    # PostgreSQL Logo
    postgresql_logo = SVGMobject("assets/postgresql_logo.svg").scale(0.5)
    postgresql_logo.to_edge(DOWN, buff=0.5)
    
    postgresql_t = Text("PostgreSQL", font_size=100).scale(0.2)
    postgresql_t.next_to(postgresql_logo, DOWN, buff=0.1)
    self.play(Create(postgresql_logo), Write(postgresql_t))
    postgresql_logo_group = VGroup(postgresql_logo, postgresql_t)
    self.next_slide()

    # Moving Logo over to left side
    self.play(postgresql_logo_group.animate.to_edge(buff=1.5))
    self.next_slide()

    # Database Text
    datenbank_t = Text("Datenbank", color=PresentationColors.ACCENT_MAIN, font_size=100).scale(0.25)
    db_ul = Underline(datenbank_t, color=PresentationColors.ACCENT_MAIN, stroke_width=1)
    datenbank_t_ul = VGroup(datenbank_t, db_ul)

    datenbank_list = BulletedList(
        "Strukturierte Daten", 
        "Relational",
        "Leistung",
        height=postgresql_logo.height,
        buff=MED_SMALL_BUFF,
        font_size=20
        )

    datenbank_t_group = VGroup(datenbank_t_ul, datenbank_list)
    datenbank_t_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)

    datenbank_t_group.align_to(postgresql_logo_group, DOWN).shift(UP*0.2)
    
    # Write database Paragraph
    self.play(Write(datenbank_t_ul))
    self.next_slide()

    for point in datenbank_list: 
        self.play(Write(point))
        self.next_slide()

    backend_group = VGroup()
    
    # Python Logo
    python_logo = SVGMobject("assets/python.svg").scale(0.5)
    python_t = Text("Python", font_size=100).scale(0.2)
    python_t.next_to(python_logo, DOWN, buff=0.1)

    python_logo_group = VGroup(python_logo, python_t)
    
    backend_group.add(python_logo_group)
    self.play(
        Create(python_logo),
        Write(python_t),
        backend_group.animate.arrange(RIGHT)
    )
    self.next_slide()

    # FastAPI Logo
    fastapi_logo = SVGMobject("assets/fastapi_logo.svg").scale_to_fit_height(python_logo.height)
    fastapi_t = Text("FastAPI", font_size=100).scale(0.2)
    fastapi_t.next_to(fastapi_logo, DOWN, buff=0.1)

    fastapi_logo_group = VGroup(fastapi_logo, fastapi_t)
    backend_group.add(fastapi_logo_group)
    self.play(
        Create(fastapi_logo),
        Write(fastapi_t),
        backend_group.animate.arrange(RIGHT)
    )
    self.next_slide()

    # SQLAlchemy Logo
    sqla_logo = SVGMobject("assets/sqla_logo.svg", fill_color=RED).scale_to_fit_height(postgresql_logo.height)
    sqla_t = Text("SQLalchemy", font_size=100).scale(0.2)
    sqla_t.next_to(sqla_logo, DOWN, buff=0.2)

    sqla_logo_group = VGroup(sqla_logo, sqla_t)
    backend_group.add(sqla_logo_group)
    self.play(
        Create(sqla_logo),
        Write(sqla_t),
        backend_group.animate.arrange(RIGHT, aligned_edge=UP)
    )
    self.next_slide()

    # Move backend logos above Postgresql
    dx = postgresql_logo.get_x() - fastapi_logo_group.get_x()
    self.play(backend_group.animate.shift(RIGHT * dx + DOWN * 0.6))

    # Draw Lines from postgresql to Backend objects
    for element in backend_group:
        line_start = postgresql_logo.get_top() + UP * 0.1
        line_end = element.get_bottom() + DOWN * 0.1

        path_postgresql_element = Line(line_start, line_end)

        self.play(Create(path_postgresql_element))
    self.next_slide()

    # Backend Text
    backend_t = Text("Backend", color=PresentationColors.ACCENT_MAIN, font_size=100).scale(0.25)
    backend_ul = Underline(backend_t, color=PresentationColors.ACCENT_MAIN, stroke_width=1)
    backend_t_ul = VGroup(backend_t, backend_ul)

    backend_list = BulletedList(
        "Gut geeignet für KI/ML",
        "Modern und Simpel",
        "ORM zum Vereinfachen des Programmierens",
        height=postgresql_logo.height,
        buff=MED_SMALL_BUFF,
        font_size=20
        )

    backend_t_group = VGroup(backend_t_ul, backend_list)
    backend_t_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    backend_t_group.align_to(backend_group, UP).shift(UP*0.3)
    backend_t_group.align_to(datenbank_t_group, LEFT)

    # Write backend Paragraph
    self.play(Write(backend_t_ul))
    self.next_slide()

    for point in backend_list: 
        self.play(Write(point))
        self.next_slide()
    
    # React Logo
    react_logo = SVGMobject("assets/react_logo.svg").scale_to_fit_height(postgresql_logo.height)
    react_t = Text("React.js (Vite & Tailwind)", font_size=100).scale(0.2)
    react_t.next_to(react_logo, DOWN, buff=0.2)

    react_logo_group = VGroup(react_logo, react_t)
    react_logo_group.next_to(fastapi_logo_group, UP, buff=0.8).shift(RIGHT * 4.5)

    self.play(Create(react_logo), Write(react_t))
    self.next_slide()

    # Moving Logo over to left side
    self.play(react_logo_group.animate.next_to(fastapi_logo_group, UP, buff=0.8))
    
    # Draw Line from Fastapi Logo to React Logo
    fastapi_react_line_start = fastapi_logo_group.get_top()
    fastapi_react_line_end = react_logo_group.get_bottom()
    
    path_fastapi_react = Line(fastapi_react_line_start, fastapi_react_line_end, buff=0.1)
    self.play(Create(path_fastapi_react))
    
    self.next_slide()

    # Frontend Text
    frontend_t = Text("Frontend", color=PresentationColors.ACCENT_MAIN, font_size=100).scale(0.25)
    frontend_ul = Underline(frontend_t, color=PresentationColors.ACCENT_MAIN, stroke_width=1)
    frontend_t_ul = VGroup(frontend_t, frontend_ul)

    frontend_list = BulletedList(
        "Funktions orientiertes Programmieren", 
        "Dynamisches UI",
        "SPA, daher Vite",
        height=postgresql_logo.height,
        buff=MED_SMALL_BUFF,
        font_size=20
    )

    frontend_t_group = VGroup(frontend_t_ul, frontend_list)
    frontend_t_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)

    frontend_t_group.align_to(react_logo, UP).shift(UP*0.3)
    frontend_t_group.align_to(backend_t_group, LEFT)
    
    # Write Frontend Paragraph
    self.play(Write(frontend_t_ul))
    self.next_slide()

    for point in frontend_list: 
        self.play(Write(point))
        self.next_slide()

    # Box for Deployment Cluster
    deployment_box = RoundedRectangle(
        width=4.5,
        height=1.5,
        corner_radius=0.2
    )
    deployment_t = Text("Deployment", font_size=100, color=PresentationColors.ACCENT_MAIN).scale(0.25)

    deployment_t.move_to(deployment_box.get_top() + DOWN*0.3)
    deployment_group = VGroup(deployment_box, deployment_t)

    deployment_group.to_corner(UR, buff=0)
    self.play(Create(deployment_box), Write(deployment_t))

    self.next_slide()

    vps_logo = SVGMobject("assets/vps.svg")
    gunicorn_logo = SVGMobject("assets/gunicorn_logo.svg")
    vercel_logo = SVGMobject("assets/vercel_logo.svg", fill_color=WHITE)
    redis_logo = SVGMobject("assets/redis_logo.svg")

    deployment_logo_group = VGroup(vps_logo, gunicorn_logo, vercel_logo, redis_logo)
    # 1. Scale each logo to, say, half the box height
    for logo in deployment_logo_group:
        logo.scale_to_fit_height(deployment_box.height * 0.5)

    # 2. Arrange them in a row with some spacing
    deployment_logo_group.arrange(RIGHT, buff=0.15)

    # 3. Move them just below the “Deployment” text, and center horizontally in the box
    deployment_logo_group.next_to(deployment_t, DOWN, buff=0.1)
    deployment_logo_group.align_to(deployment_box, X_AXIS)
    deployment_logo_group.shift(LEFT * 0.15)

    # 4. Finally, show them
    self.play(Create(vps_logo), DrawBorderThenFill(gunicorn_logo, stroke_color=gunicorn_logo.fill_color), DrawBorderThenFill(vercel_logo, stroke_color=vercel_logo.fill_color), Create(redis_logo))
    self.next_slide()
    self.wipe(self.mobjects, direction=UP)