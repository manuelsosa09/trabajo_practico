import flet as ft
from db import get_connection


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
                                src=imagen or "assets/images/placeholder.png",
                                width=60,
                                height=60,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            title=ft.Text(nombre),
                            subtitle=ft.Text(
                                f"Categoría: {categoria}", size=12
                            ),
                            on_click=lambda e, _id=inst_id: page.go(f"/detail/{_id}"),
                        )
                    )
                )

        page.update()

    def volver_home(e):
        page.go("/home")

    load_favorites()

    content = ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Tus favoritos", size=22, weight="bold"),
                    ft.ElevatedButton("Volver", on_click=volver_home),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            items_column,
        ],
        expand=True,
    )

    return ft.View(
        "/favoritos",
        controls=[
            ft.AppBar(title=ft.Text("Favoritos")),
            ft.Container(content=content, expand=True, padding=20),
        ],
    )
