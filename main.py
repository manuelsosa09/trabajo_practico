import flet as ft
from db import init_db
from views.login_view import LoginView
from views.register_view import RegisterView
from views.home_view import HomeView
from views.detail_view import DetailView
from views.profile_view import ProfileView
from views.favorites_view import FavoritesView


def main(page: ft.Page):
    page.title = "InstrumentHub 🎵"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START

    init_db()

    def get_usuario_id():
        return page.client_storage.get("usuario_id")

    def route_change(e):
        route = page.route or "/"
        page.views.clear()
        usuario_id = get_usuario_id()

        if route == "/":
            page.views.append(LoginView(page))

        elif route == "/register":
            page.views.append(RegisterView(page))

        elif route == "/home":
            if usuario_id is None:
                page.go("/")
                return
            page.views.append(HomeView(page, usuario_id))

        elif route == "/perfil":
            if usuario_id is None:
                page.go("/")
                return
            page.views.append(ProfileView(page, usuario_id))

        elif route == "/favoritos":
            if usuario_id is None:
                page.go("/")
                return
            page.views.append(FavoritesView(page, usuario_id))

        elif route.startswith("/detail/"):
            try:
                inst_id = int(route.split("/")[-1])
            except ValueError:
                page.views.append(ft.View("/", [ft.Text("ID de instrumento inválido")]))
            else:
                page.views.append(
                    DetailView(page, instrumento_id=inst_id, usuario_id=usuario_id)
                )

        else:
            page.views.append(ft.View("/", [ft.Text("Página no encontrada")]))

        page.update()

    page.on_route_change = route_change
    page.go(page.route or "/")


ft.app(target=main)
