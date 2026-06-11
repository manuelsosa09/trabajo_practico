import flet as ft
from auth import register_user


def RegisterView(page: ft.Page) -> ft.View:
    mensaje = ft.Text("")

    nombre_input = ft.TextField(label="Nombre", expand=True)
    correo_input = ft.TextField(label="Correo", expand=True)
    password_input = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        expand=True,
    )
    password2_input = ft.TextField(
        label="Confirmar contraseña",
        password=True,
        can_reveal_password=True,
        expand=True,
    )

    def register(e):
        nombre = nombre_input.value.strip()
        correo = correo_input.value.strip()
        pwd1 = password_input.value.strip()
        pwd2 = password2_input.value.strip()

        if not nombre or not correo or not pwd1 or not pwd2:
            mensaje.value = "Todos los campos son obligatorios."
            page.update()
            return

        if "@" not in correo or "." not in correo:
            mensaje.value = "Correo no válido."
            page.update()
            return

        if len(pwd1) < 6:
            mensaje.value = "La contraseña debe tener al menos 6 caracteres."
            page.update()
            return

        if pwd1 != pwd2:
            mensaje.value = "Las contraseñas no coinciden."
            page.update()
            return

        if register_user(nombre, correo, pwd1):
            mensaje.value = "Usuario registrado. Ahora inicia sesión."
        else:
            mensaje.value = "No se pudo registrar. ¿El correo ya existe?"
        page.update()

    content = ft.Column(
        [
            ft.Text("Registrarse en InstrumentHub 🎵", size=25, weight="bold"),
            nombre_input,
            correo_input,
            password_input,
            password2_input,
            ft.ElevatedButton("Registrarse", on_click=register),
            ft.TextButton("Volver al login", on_click=lambda e: page.go("/")),
            mensaje,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    return ft.View(
        "/register",
        controls=[content],
    )
