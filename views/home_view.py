import flet as ft
from db import get_connection


def HomeView(page: ft.Page, usuario_id: int) -> ft.View:
    # 4 columnas para la galería
    cols = [ft.Column(spacing=20, expand=True) for _ in range(4)]

    search_text = ft.TextField(label="Buscar instrumento...", expand=True)
    category_filter = ft.Dropdown(
        label="Categoría",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Cuerda"),
            ft.dropdown.Option("Viento"),
            ft.dropdown.Option("Percusión"),
        ],
        value="Todos",
    )

    def load_instruments():
        for col in cols:
            col.controls.clear()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, imagen, categoria FROM instrumentos")
        instrumentos = cursor.fetchall()
        conn.close()

        filtro_cat = category_filter.value
        texto = search_text.value.strip().lower() if search_text.value else ""

        filtrados = []
        for inst_id, nombre, imagen, categoria in instrumentos:
            if filtro_cat and filtro_cat != "Todos" and categoria != filtro_cat:
                continue
            if texto and texto not in nombre.lower():
                continue
            filtrados.append((inst_id, nombre, imagen, categoria))

        for i, (inst_id, nombre, imagen, categoria) in enumerate(filtrados):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=imagen or "assets/images/placeholder.png",
                                width=180,
                                height=180,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                            ft.Text(nombre, weight="bold"),
                            ft.Text(f"Categoría: {categoria}", size=12),
                            ft.ElevatedButton(
                                "Ver detalle",
                                on_click=lambda e, _id=inst_id: page.go(f"/detail/{_id}"),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=10,
                )
            )
            col_index = i % 4
            cols[col_index].controls.append(card)

        page.update()

    search_text.on_change = lambda e: load_instruments()
    category_filter.on_change = lambda e: load_instruments()

    def go_perfil(e):
        page.go("/perfil")

    def go_favoritos(e):
        page.go("/favoritos")

    def logout(e):
        page.client_storage.clear()
        page.go("/")

    nav_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("👤 Perfil", on_click=go_perfil),
            ft.ElevatedButton("⭐ Favoritos", on_click=go_favoritos),
            ft.OutlinedButton("⏻ Cerrar sesión", on_click=logout),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    search_row = ft.Row(
        controls=[search_text, category_filter],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    gallery = ft.Row(
        controls=cols,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )

    load_instruments()

    # 👇 Contenido con scroll vertical
    content = ft.Column(
        [
            nav_buttons,
            search_row,
            gallery,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,   # <- aquí se activa la barra de desplazamiento
    )

    return ft.View(
        "/home",
        controls=[
            ft.AppBar(title=ft.Text("InstrumentHub 🎸")),
            content,
        ],
    )
