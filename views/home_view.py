import unicodedata
import flet as ft
from db import get_connection


def HomeView(page: ft.Page, usuario_id: int) -> ft.View:
    cols = [ft.Column(spacing=20, expand=True) for _ in range(4)]

    search_text = ft.TextField(label="Buscar instrumento...", expand=True)

    def normalizar(texto):
        if texto is None:
            return ""
        texto = str(texto).strip().lower()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        return texto

    def get_image_src(imagen):
        if imagen:
            return imagen.replace("assets/", "")
        return "images/piano.png"

    category_filter = ft.Dropdown(
        label="Categoría",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Cuerda"),
            ft.dropdown.Option("Teclado"),
            ft.dropdown.Option("Percusión"),
            ft.dropdown.Option("Viento"),
        ],
        value="Todos",
        width=220,
    )

    def load_instruments():
        for col in cols:
            col.controls.clear()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, imagen, categoria FROM instrumentos")
        instrumentos = cursor.fetchall()
        conn.close()

        filtro_cat = category_filter.value or "Todos"
        filtro_cat_norm = normalizar(filtro_cat)
        texto = normalizar(search_text.value) if search_text.value else ""

        filtrados = []

        for inst_id, nombre, imagen, categoria in instrumentos:
            categoria_norm = normalizar(categoria)
            nombre_norm = normalizar(nombre)

            if filtro_cat_norm != "todos" and categoria_norm != filtro_cat_norm:
                continue

            if texto and texto not in nombre_norm:
                continue

            filtrados.append((inst_id, nombre, imagen, categoria))

        for i, (inst_id, nombre, imagen, categoria) in enumerate(filtrados):
            imagen_src = get_image_src(imagen)

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=imagen_src,
                                width=180,
                                height=180,
                                fit="contain",
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
        page.usuario_id = None
        page.usuario_nombre = None
        page.go("/")

    nav_buttons = ft.Row(
        controls=[
            ft.ElevatedButton("Perfil", on_click=go_perfil),
            ft.ElevatedButton("Favoritos", on_click=go_favoritos),
            ft.OutlinedButton("Cerrar sesión", on_click=logout),
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

    content = ft.Column(
        controls=[
            nav_buttons,
            search_row,
            gallery,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    load_instruments()

    return ft.View(
        route="/home",
        controls=[
            ft.AppBar(title=ft.Text("InstrumentHub")),
            content,
        ],
    )