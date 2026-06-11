import flet as ft
import os
import shutil
from db import get_connection


def ProfileView(page: ft.Page, usuario_id: int) -> ft.View:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT nombre, correo, avatar, biografia FROM usuarios WHERE id = ?",
        (usuario_id,),
    )
    user = cursor.fetchone()
    conn.close()

    nombre_field = ft.TextField(
        label="Nombre",
        value=user[0] if user else "",
        width=300,
    )
    correo_field = ft.TextField(
        label="Correo",
        value=user[1] if user else "",
        width=300,
        disabled=True,
    )
    bio_field = ft.TextField(
        label="Biografía",
        value=user[3] if user and user[3] else "",
        multiline=True,
        width=400,
        height=100,
    )

    avatar_path = user[2] if user and user[2] else "assets/images/avatar_default.png"
    avatar_image = ft.Image(
        src=avatar_path,
        width=150,
        height=150,
        border_radius=75,
    )

    mensaje = ft.Text("")

    def guardar(e):
        nombre = nombre_field.value.strip()
        bio = bio_field.value.strip()
        if not nombre:
            mensaje.value = "El nombre no puede estar vacío."
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre = ?, biografia = ? WHERE id = ?",
            (nombre, bio, usuario_id),
        )
        conn.commit()
        conn.close()
        mensaje.value = "Perfil actualizado."
        page.update()

    file_picker = ft.FilePicker()

    def on_file_result(e: ft.FilePickerResultEvent):
        nonlocal avatar_path
        if not e.files:
            return
        src = e.files[0].path

        if not os.path.exists("assets/images"):
            os.makedirs("assets/images", exist_ok=True)

        dst = os.path.join("assets/images", f"avatar_{usuario_id}.png")
        try:
            shutil.copy(src, dst)
            avatar_path = dst
            avatar_image.src = avatar_path
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET avatar = ? WHERE id = ?",
                (avatar_path, usuario_id),
            )
            conn.commit()
            conn.close()
            mensaje.value = "Avatar actualizado."
        except Exception:
            mensaje.value = "No se pudo actualizar el avatar."
        page.update()

    file_picker.on_result = on_file_result

    def cambiar_avatar(e):
        if file_picker not in page.overlay:
            page.overlay.append(file_picker)
            page.update()
        file_picker.pick_files(allow_multiple=False)

    def volver_home(e):
        page.go("/home")

    content = ft.Column(
        [
            ft.Row(
                [
                    avatar_image,
                    ft.Column(
                        [
                            nombre_field,
                            correo_field,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=20,
            ),
            bio_field,
            mensaje,
            ft.Row(
                [
                    ft.ElevatedButton("Guardar cambios", on_click=guardar),
                    ft.ElevatedButton("Cambiar avatar", on_click=cambiar_avatar),
                    ft.ElevatedButton("Volver", on_click=volver_home),
                ],
                spacing=10,
            ),
        ],
        spacing=15,
    )

    return ft.View(
        "/perfil",
        controls=[
            file_picker,
            ft.AppBar(title=ft.Text("Mi perfil")),
            ft.Container(content=content, padding=20),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
