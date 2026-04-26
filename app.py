import flet as ft
from views.home_view import HomeView
from views.form_view import FormView
from components.navbar import NavBar

def main(page: ft.Page):
    page.title = "🎞️ Movie Manager PRO"
    page.theme_mode = ft.ThemeMode.DARK
    # CORRECCIÓN: ft.Colors con C mayúscula
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.padding = 20

    def cambiar_tema(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = ft.Colors.BLUE_GREY_50
            e.control.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = ft.Colors.BLUE_GREY_900
            e.control.icon = ft.Icons.LIGHT_MODE
        page.update()

    # AppBar con mayúsculas corregidas
    page.appbar = ft.AppBar(
        leading=ft.Icon(icon=ft.Icons.MOVIE_FILTER_OUTLINED, color=ft.Colors.AMBER),
        title=ft.Text("Movie Manager PRO", weight="bold"),
        bgcolor=ft.Colors.BLUE_GREY_800,
        actions=[
            ft.IconButton(
                icon=ft.Icons.LIGHT_MODE,
                on_click=cambiar_tema,
                tooltip="Cambiar tema"
            ),
        ],
    )

    content_area = ft.Column(expand=True, horizontal_alignment="center")

    def change_view(route, id_pelicula=None):
        content_area.controls.clear()
        if route == "home":
            content_area.controls.append(HomeView(page, on_navigate=change_view))
        elif route == "form":
            content_area.controls.append(FormView(page, on_navigate=change_view, id_edit=id_pelicula))
        page.update()

    page.add(
        NavBar(on_change=change_view),
        ft.Divider(height=10, color="transparent"),
        content_area
    )

    change_view("home")

if __name__ == "__main__":
    ft.run(main)