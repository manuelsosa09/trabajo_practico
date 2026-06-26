import os
import shutil
import flet as ft
from db import get_connection


DEFAULT_AVATAR = "images/avatar_1.png"


def get_image_src(imagen):
    if not imagen:
        return DEFAULT_AVATAR

    imagen = str(imagen).replace("\\", "/")

    if imagen.startswith("assets/"):
        imagen = imagen.replace("assets/", "", 1)

    return imagen


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

    avatar_db = user[2] if user and user[2] else None

    avatar_image = ft.Image(
        src=get_image_src(avatar_db),
        width=150,
        height=150,
        fit="cover",
        border_radius=75,
    )

    mensaje = ft.Text("")
    file_picker = ft.FilePicker()

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

        page.usuario_nombre = nombre
        mensaje.value = "Perfil actualizado."
        page.update()

    def on_file_result(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        src = e.files[0].path

        if not src:
            mensaje.value = "No se pudo obtener la ruta de la imagen seleccionada."
            page.update()
            return

        os.makedirs(os.path.join("assets", "images"), exist_ok=True)

        extension = os.path.splitext(src)[1].lower()

        if extension not in [".png", ".jpg", ".jpeg", ".webp"]:
            extension = ".png"

        dst = os.path.join("assets", "images", f"avatar_{usuario_id}{extension}")
        avatar_path_db = dst.replace("\\", "/")

        try:
            shutil.copy(src, dst)

            avatar_image.src = get_image_src(avatar_path_db)

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET avatar = ? WHERE id = ?",
                (avatar_path_db, usuario_id),
            )
            conn.commit()
            conn.close()

            mensaje.value = "Avatar actualizado."
        except Exception as error:
            mensaje.value = f"No se pudo actualizar el avatar: {error}"

        page.update()

    file_picker.on_result = on_file_result

    def cambiar_avatar(e):
        if file_picker not in page.overlay:
            page.overlay.append(file_picker)
            page.update()

        file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["png", "jpg", "jpeg", "webp"],
        )

    def volver_home(e):
        page.go("/home")

    content = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    avatar_image,
                    ft.Column(
                        controls=[
                            nombre_field,
                            correo_field,
                        ],
                        spacing=10,
                    ),
                ],
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bio_field,
            mensaje,
            ft.Row(
                controls=[
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
        route="/perfil",
        controls=[
            ft.AppBar(title=ft.Text("Mi perfil")),
            ft.Container(content=content, padding=20),
        ],
        scroll=ft.ScrollMode.AUTO,
    )