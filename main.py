import os
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
    page.bgcolor = "#101014"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    init_db()

    def get_usuario_id():
        return getattr(page, "usuario_id", None)

    def route_change(e=None):
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
            if usuario_id is None:
                page.go("/")
                return

            try:
                inst_id = int(route.split("/")[-1])
                page.views.append(
                    DetailView(page, instrumento_id=inst_id, usuario_id=usuario_id)
                )
            except ValueError:
                page.views.append(
                    ft.View(route="/", controls=[
                            ft.Text("ID de instrumento invalido", color="red")
                        ],
                    )
                )

        else:
            page.views.append(
                ft.View(route="/", controls=[
                        ft.Text("Página no encontrada", color="red")
                    ],
                )
            )

        page.update()

    page.on_route_change = route_change
    route_change()


if __name__ == "__main__":
    os.environ["FLET_FORCE_WEB_SERVER"] = "true"

    port = int(os.environ.get("PORT", 8550))

    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        host="0.0.0.0",
        port=port,
        assets_dir="assets",
    )
