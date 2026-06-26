import unicodedata
import flet as ft
from db import get_connection


FALLBACK_IMAGE = "images/piano.png"


def reparar_texto(texto):
    if texto is None:
        return ""

    texto = str(texto)

    try:
        texto = texto.encode("latin1").decode("utf-8")
    except Exception:
        pass

    return texto


def normalizar(texto):
    texto = reparar_texto(texto)
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


def get_image_src(imagen):
    if not imagen:
        return FALLBACK_IMAGE

    imagen = str(imagen).replace("\\", "/")

    if imagen.startswith("assets/"):
        imagen = imagen.replace("assets/", "", 1)

    return imagen


def HomeView(page: ft.Page, usuario_id: int) -> ft.View:
    cols = [ft.Column(spacing=20, expand=True) for _ in range(4)]

    search_text = ft.TextField(
        label="Buscar instrumento...",
        expand=True,
    )

    category_filter = ft.Dropdown(
        label="Categoria",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Cuerda"),
            ft.dropdown.Option("Viento"),
            ft.dropdown.Option("Percusion"),
            ft.dropdown.Option("Teclado"),
        ],
        value="Todos",
        width=220,
    )

    contador_text = ft.Text("", size=12)

    def load_instruments(e=None):
        for col in cols:
            col.controls.clear()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, imagen, categoria FROM instrumentos")
        instrumentos = cursor.fetchall()
        conn.close()

        filtro_cat = category_filter.value or "Todos"
        filtro_cat_norm = normalizar(filtro_cat)

        texto_busqueda = search_text.value or ""
        texto_busqueda_norm = normalizar(texto_busqueda)

        filtrados = []

        for inst_id, nombre, imagen, categoria in instrumentos:
            nombre_mostrado = reparar_texto(nombre)
            categoria_mostrada = reparar_texto(categoria)

            nombre_norm = normalizar(nombre)
            categoria_norm = normalizar(categoria)

            if filtro_cat_norm != "todos" and categoria_norm != filtro_cat_norm:
                continue

            if texto_busqueda_norm and texto_busqueda_norm not in nombre_norm:
                continue

            filtrados.append(
                (
                    inst_id,
                    nombre_mostrado,
                    imagen,
                    categoria_mostrada,
                )
            )

        contador_text.value = f"Instrumentos encontrados: {len(filtrados)}"

        if not filtrados:
            cols[0].controls.append(
                ft.Text(
                    "No se encontraron instrumentos para esta categoria.",
                    size=14,
                )
            )

        for i, (inst_id, nombre, imagen, categoria) in enumerate(filtrados):
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Image(
                                src=get_image_src(imagen),
                                width=180,
                                height=180,
                                fit="contain",
                            ),
                            ft.Text(
                                nombre,
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                f"Categoria: {categoria}",
                                size=12,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.ElevatedButton(
                                "Ver detalle",
                                on_click=lambda e, _id=inst_id: page.go(
                                    f"/detail/{_id}"
                                ),
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

    def aplicar_filtro(e=None):
        load_instruments(e)

    search_text.on_change = aplicar_filtro
    category_filter.on_change = aplicar_filtro

    filter_button = ft.ElevatedButton(
        "Filtrar",
        on_click=aplicar_filtro,
    )

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
            ft.OutlinedButton("Cerrar sesion", on_click=logout),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    search_row = ft.Row(
        controls=[
            search_text,
            category_filter,
            filter_button,
        ],
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
            contador_text,
            gallery,
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    view = ft.View(
        route="/home",
        controls=[
            ft.AppBar(title=ft.Text("InstrumentHub")),
            ft.Container(
                content=content,
                expand=True,
                padding=10,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    load_instruments()

    return view