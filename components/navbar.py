import flet as ft

def NavBar(on_change):
    return ft.Container(
        content=ft.Row(
            [
                # Logo y Nombre
                ft.Row([
                    ft.Icon(ft.Icons.MOVIE_FILTER, color=ft.Colors.AMBER, size=30),
                    ft.Text("Flet Películas", size=20, weight="bold", color=ft.Colors.WHITE)
                ]),
                # Botones de navegación
                ft.Row([
                    ft.TextButton(
                        "Inicio",
                        icon=ft.Icons.HOME,
                        on_click=lambda _: on_change("home")
                    ),
                    ft.TextButton(
                        "Agregar",
                        icon=ft.Icons.ADD,
                        on_click=lambda _: on_change("form")
                    ),
                ], spacing=20),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=ft.Colors.BLUE_GREY_800,
        border_radius=10,
    )