import flet as ft
import utils as u
import database as db
def main(page: ft.Page):
    page.title = "Somnus"
    page.window.width = 360
    page.window.height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(color_scheme_seed="green")
    page.fonts = {
        "Lettera" : "fonts/LetteraMonoLLCondLight-Regular.otf",
        "Pixel" : "fonts/Ndot-55.otf",
        "NTypeRegular" : "fonts/NType82-Regular.otf",
        "NTypeMono" : "fonts/NType82Mono-Regular.otf",
    }

    

    def init():
        if db.is_db():
            page.go("/home")
        return ft.Column(
            [
                ft.Container(
                    padding=16,
                    alignment=ft.alignment.center,
                    content=ft.Text(value="SOMNUS", size=32, color=ft.colors.WHITE, font_family="Pixel")
                ),
                ft.Container(
                    padding=30,
                    alignment=ft.alignment.center,
                    content=ft.Text(value='"Never waste any time you can spend sleeping." — Frank H. Knight', size=16, color=ft.colors.WHITE, font_family="Lettera")
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.cupertino_icons.PERSON_ADD, color=ft.colors.WHITE),
                    title=ft.Text("Quick start", color=ft.colors.WHITE, size=20, font_family="Lettera"),
                    on_click=lambda _: page.go("/create_config")
                )
            ]
        )

    def create_config():
        def save_config(e):
            db.create_db()
            try:
                db.insert_config("user", name.value)
                db.insert_config("wake_up_hour", wake_up_hour.value)
                sleep_hour = u.calculate_sleep_hour(wake_up_hour.value, float(duration.value))
                db.insert_config("sleep_hour", sleep_hour)
                db.insert_config("duration", duration.value)
                page.go("/home")
            except Exception as e:
                print(f"Error saving configuration: {e}")

        #TODO: Enhance the UI with a better layout, more screens and RangeSlider for the duration

        name = ft.TextField(prefix_icon=ft.icons.DRIVE_FILE_RENAME_OUTLINE_OUTLINED, text_style=ft.TextStyle(color=ft.colors.WHITE, font_family="Lettera"), hint_text="Your name")
        wake_up_hour = ft.TextField(prefix_icon=ft.icons.SUNNY_SNOWING, text_style=ft.TextStyle(color=ft.colors.WHITE, font_family="Lettera"), hint_text="Wake up hour")
        duration = ft.TextField(prefix_icon=ft.icons.ACCESS_TIME_OUTLINED, text_style=ft.TextStyle(color=ft.colors.WHITE, font_family="Lettera"), hint_text="Sleep hours")
        title = ft.Container(
                    padding=16,
                    alignment=ft.alignment.center,
                    content=ft.Text(value="SOMNUS", size=32, color=ft.colors.WHITE, font_family="Pixel")
                )
        submit = ft.ListTile(
                    leading=ft.Icon(ft.icons.SAVE, color=ft.colors.WHITE),
                    title=ft.Text(value="Guardar", font_family="Lettera", size=20),
                    on_click=save_config
                )

        return ft.Column(
            [
                title,
                name,
                wake_up_hour,
                duration,
                submit
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def home():

        def register_sleep(e):
            page.go("/register_sleep")
        def debt(e):
            page.go("/debt")
        def schedule(e):
            page.go("/schedule")
        def routines(e):
            page.go("/routines")
        def reminders(e):
            page.go("/reminders")

        welcome_text = "Welcome, " + db.get_user() + "!" if db.is_db() else "Welcome!"
        return ft.Column(
            [
                ft.Container(
                    padding=6,
                    alignment=ft.alignment.center,
                    content=ft.Text(value="SOMNUS", size=32, color=ft.colors.WHITE, font_family="Pixel"),
                ),
                ft.Container(
                    ft.Container(
                        padding=4,
                        alignment=ft.alignment.center,
                        border=ft.border.only(
                            top=ft.border.BorderSide(1, ft.colors.WHITE),
                            bottom=ft.border.BorderSide(1, ft.colors.WHITE)
                        ),
                        content=ft.Text(value="HOME", size=25, color=ft.colors.WHITE, font_family="NTypeMono")
                    ),
                    padding=10,
                    alignment=ft.alignment.center
                ),
                ft.Container(padding=10, content=ft.Text(value=welcome_text, size=16, color=ft.colors.WHITE, font_family="Lettera")),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.BED_OUTLINED, color=ft.colors.WHITE),
                    title=ft.Text("Register sleep", color=ft.colors.WHITE, size=18, font_family="Lettera"),
                    on_click=register_sleep
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.AUTO_GRAPH_OUTLINED, color=ft.colors.WHITE),
                    title=ft.Text("Sleep debt", color=ft.colors.WHITE, size=18, font_family="Lettera"),
                    on_click=debt
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, color=ft.colors.WHITE),
                    title=ft.Text("Sleep Plan", color=ft.colors.WHITE, size=18, font_family="Lettera"),
                    on_click=schedule
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.REPEAT_OUTLINED, color=ft.colors.WHITE),
                    title=ft.Text("Circadian Routines", color=ft.colors.WHITE, size=18, font_family="Lettera"),
                    on_click=routines
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.NOTIFICATIONS_ACTIVE_OUTLINED, color=ft.colors.WHITE),
                    title=ft.Text("Reminders", color=ft.colors.WHITE, size=18, font_family="Lettera"),
                    on_click=reminders
                )
            ]
        )

    def register_sleep():
        return ft.Column(
            [
                ft.Text(value="Somnus", size=32, color=ft.colors.WHITE),
                ft.Text(value="¿Cuántas horas dormiste esta noche?", size=20, color=ft.colors.WHITE),
                ft.TextField(label="Horas", hint_text="e.g. 8.5"),
                ft.FilledTonalButton(text="Guardar")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def debt():
        return ft.Column(
            [
                ft.Text(value="Somnus", size=32, color=ft.colors.WHITE),
                ft.Text(value="Deuda de sueño", size=20, color=ft.colors.WHITE),
                ft.Text(value="Tu deuda de sueño es de 8 horas.", size=16, color=ft.colors.WHITE),
                ft.FilledTonalButton(text="Volver", on_click=lambda: page.go("/home"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def schedule():
        return ft.Column(
            [
                ft.Text(value="Somnus", size=32, color=ft.colors.WHITE),
                ft.Text(value="Horarios objetivo", size=20, color=ft.colors.WHITE),
                ft.Text(value="Despierta a las 6:30, duerme a las 22:00.", size=16, color=ft.colors.WHITE),
                ft.FilledTonalButton(text="Volver", on_click=lambda: page.go("/home"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def routines():
        return ft.Column(
            [
                ft.Text(value="Somnus", size=32, color=ft.colors.WHITE),
                ft.Text(value="Rutinas", size=20, color=ft.colors.WHITE),
                ft.Text(value="Rutina de inicio: Apaga la luz azul.", size=16, color=ft.colors.WHITE),
                ft.Text(value="Rutina de desconexión: Evita la cafeína.", size=16, color=ft.colors.WHITE),
                ft.FilledTonalButton(text="Volver", on_click=lambda: page.go("/home"))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def route_change(route):
        views = {
            "/": init(),
            "/create_config": create_config(),
            "/home": home(),
            "/register_sleep": register_sleep(),
            "/debt": debt(),
            "/schedule": schedule(),
            "/routines": routines()
        }
        page.views.clear()
        page.views.append(views.get(page.route, views["/"]))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(main, "android", assets_dir="assets")
