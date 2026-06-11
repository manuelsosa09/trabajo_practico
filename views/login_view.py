import flet as ft
from auth import login_user


def LoginView(page: ft.Page) -> ft.View:
    mensaje = ft.Text("")

    correo_input = ft.TextField(label="Correo", expand=True)
    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        expand=True,
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
            page.client_storage.set("usuario_id", usuario_id)
            page.client_storage.set("usuario_nombre", nombre)
            mensaje.value = ""
            page.go("/home")
        else:
            mensaje.value = "Correo o contraseña incorrectos"
        page.update()

    content = ft.Column(
        [
            ft.Text("InstrumentHub 🎵", size=30, weight="bold"),
            correo_input,
            password_input,
            ft.ElevatedButton("Entrar", on_click=login),
            ft.TextButton(
                "Registrarse", on_click=lambda e: page.go("/register")
            ),
            mensaje,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.View(
        "/",
        controls=[content],
    )
