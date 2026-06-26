import flet as ft
from db import get_connection
from datetime import datetime


def DetailView(page: ft.Page, instrumento_id: int, usuario_id: int | None) -> ft.View:
    mensaje = ft.Text("")
    comentarios_list = ft.Column(spacing=5, expand=True)

    nombre_text = ft.Text("", size=24, weight="bold")
    categoria_text = ft.Text("")
    historia_text = ft.Text("", expand=True)
    material_text = ft.Text("", expand=True)
    origen_text = ft.Text("", expand=True)

    def get_image_src(imagen):
        if imagen:
            return imagen.replace("assets/", "")
        return "images/piano.png"

    imagen = ft.Image(
        src="images/piano.png",
        width=300,
        height=300,
        fit="contain",
    )

    comentario_input = ft.TextField(label="Agregar comentario", expand=True)

    def load_instrument():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT nombre, categoria, historia, material, origen, imagen
            FROM instrumentos
            WHERE id = ?
            """,
            (instrumento_id,),
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            nombre_text.value = "Instrumento no encontrado"
            page.update()
            return

        nombre, categoria, historia, material, origen, img = row

        nombre_text.value = nombre
        categoria_text.value = f"Categoría: {categoria}"
        historia_text.value = f"Historia: {historia}"
        material_text.value = f"Material: {material}"
        origen_text.value = f"Origen: {origen}"
        imagen.src = get_image_src(img)

        page.update()

    def load_comments():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT c.comentario, c.fecha, u.nombre
            FROM comentarios c
            LEFT JOIN usuarios u ON c.id_usuario = u.id
            WHERE c.id_instrumento = ?
            ORDER BY c.fecha DESC
            """,
            (instrumento_id,),
        )
        rows = cursor.fetchall()
        conn.close()

        comentarios_list.controls.clear()

        if not rows:
            comentarios_list.controls.append(
                ft.Text("Aún no hay comentarios. ¡Sé el primero!", size=12)
            )
        else:
            for comentario, fecha, nombre in rows:
                info = f"{nombre or 'Anónimo'} – {fecha}"
                comentarios_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(comentario),
                        subtitle=ft.Text(info, size=11),
                    )
                )

        page.update()

    def add_comment(e):
        texto = comentario_input.value.strip()

        if usuario_id is None:
            mensaje.value = "Debes estar logueado para comentar."
        elif texto == "":
            mensaje.value = "El comentario está vacío."
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO comentarios (id_usuario, id_instrumento, comentario, fecha)
                VALUES (?, ?, ?, ?)
                """,
                (
                    usuario_id,
                    instrumento_id,
                    texto,
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ),
            )
            conn.commit()
            conn.close()

            comentario_input.value = ""
            mensaje.value = "Comentario agregado."
            load_comments()

        page.update()

    def add_favorite(e):
        if usuario_id is None:
            mensaje.value = "Debes estar logueado para agregar a favoritos."
            page.update()
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM favoritos WHERE usuario_id = ? AND instrumento_id = ?",
            (usuario_id, instrumento_id),
        )

        if cursor.fetchone():
            mensaje.value = "Ya está en favoritos."
        else:
            cursor.execute(
                "INSERT INTO favoritos (usuario_id, instrumento_id) VALUES (?, ?)",
                (usuario_id, instrumento_id),
            )
            conn.commit()
            mensaje.value = "Agregado a favoritos."

        conn.close()
        page.update()

    def volver_home(e):
        page.go("/home")

    load_instrument()
    load_comments()

    content = ft.Column(
        controls=[
            nombre_text,
            categoria_text,
            ft.Row(
                controls=[
                    imagen,
                    ft.Column(
                        controls=[
                            historia_text,
                            material_text,
                            origen_text,
                        ],
                        expand=True,
                        spacing=5,
                    ),
                ],
                spacing=20,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Agregar a favoritos",
                        on_click=add_favorite,
                    ),
                ],
                spacing=10,
            ),
            mensaje,
            ft.Text("Comentarios", size=18, weight="bold"),
            ft.Row(
                controls=[
                    comentario_input,
                    ft.ElevatedButton("Enviar", on_click=add_comment),
                ],
                spacing=10,
            ),
            ft.Container(
                content=comentarios_list,
                expand=True,
                padding=10,
            ),
            ft.ElevatedButton("Volver a Home", on_click=volver_home),
        ],
        spacing=15,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.View(
        route=f"/detail/{instrumento_id}",
        controls=[
            ft.AppBar(title=ft.Text("Detalle del instrumento")),
            ft.Container(content=content, expand=True, padding=20),
        ],
        scroll=ft.ScrollMode.AUTO,
    )