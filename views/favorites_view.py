import flet as ft
from db import get_connection


FALLBACK_IMAGE = "images/piano.png"


def get_image_src(imagen):
    if not imagen:
        return FALLBACK_IMAGE

    imagen = str(imagen).replace("\\", "/")

    if imagen.startswith("assets/"):
        imagen = imagen.replace("assets/", "", 1)

    return imagen


def FavoritesView(page: ft.Page, usuario_id: int) -> ft.View:
    items_column = ft.Column(spacing=10, expand=True)

    def load_favorites():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT i.id, i.nombre, i.imagen, i.categoria
            FROM favoritos f
            JOIN instrumentos i ON f.instrumento_id = i.id
            WHERE f.usuario_id = ?
            ORDER BY i.nombre
            """,
            (usuario_id,),
        )
        favoritos = cursor.fetchall()
        conn.close()

        items_column.controls.clear()

        if not favoritos:
            items_column.controls.append(
                ft.Text("Aún no tienes favoritos.", size=14)
            )
        else:
            for inst_id, nombre, imagen, categoria in favoritos:
                items_column.controls.append(
                    ft.Card(
                        content=ft.ListTile(
                            leading=ft.Image(
                                src=get_image_src(imagen),
                                width=60,
                                height=60,
                                fit="contain"
                            ),
                            title=ft.Text(nombre),
                            subtitle=ft.Text(f"Categoría: {categoria}", size=12),
                            on_click=lambda e, _id=inst_id: page.go(f"/detail/{_id}"),
                        )
                    )
                )

    def volver_home(e):
        page.go("/home")

    load_favorites()

    content = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Tus favoritos", size=22, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Volver", on_click=volver_home),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            items_column,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.View(
        route="/favoritos",
        controls=[
            ft.AppBar(title=ft.Text("Favoritos")),
            ft.Container(content=content, expand=True, padding=20),
        ],
        scroll=ft.ScrollMode.AUTO,
    )