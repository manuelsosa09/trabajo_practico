import flet as ft
from auth import login_user


def LoginView(page: ft.Page) -> ft.View:
    mensaje = ft.Text("", color="red")

    correo_input = ft.TextField(
        label="Correo",
        width=350,
    )

    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=350,
    )

    def login(e):
        correo = correo_input.value.strip()
        password = password_input.value.strip()

        if not correo or not password:
            mensaje.value = "Completa correo y contraseña."
            page.update()
            return

        user = login_user(correo, password)

        if user:
            usuario_id, nombre = user
            page.usuario_id = usuario_id
            page.usuario_nombre = nombre
            mensaje.value = ""
            page.go("/home")
        else:
            mensaje.value = "Correo o contraseña incorrectos"

        page.update()

    formulario = ft.Container(
        width=430,
        padding=30,
        border_radius=15,
        bgcolor="#1E1E1E",
        content=ft.Column(
            controls=[
                ft.Text(
                    "InstrumentHub 🎵",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Iniciar sesión",
                    size=18,
                    text_align=ft.TextAlign.CENTER,
                ),
                correo_input,
                password_input,
                ft.ElevatedButton(
                    "Entrar",
                    width=350,
                    on_click=login,
                ),
                ft.TextButton(
                    "Registrarse",
                    on_click=lambda e: page.go("/register"),
                ),
                mensaje,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    return ft.View(route="/", controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=formulario,
            )
        ],
    )
