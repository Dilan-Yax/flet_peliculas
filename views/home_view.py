import flet as ft
from services.pelicula_service import obtener_todos, eliminar_pelicula, buscar_peliculas


def HomeView(page: ft.Page, on_navigate):
    # --- COMPONENTES DE ESTADÍSTICAS (Mantenidos) ---
    lbl_total = ft.Text("0", size=30, weight="bold", color=ft.Colors.AMBER)
    lbl_promedio = ft.Text("0.0", size=30, weight="bold", color=ft.Colors.AMBER)
    lbl_mejor = ft.Text("-", size=20, weight="bold", color=ft.Colors.WHITE, overflow=ft.TextOverflow.ELLIPSIS)

    stats_cards = ft.Row(
        [
            ft.Container(
                content=ft.Column([ft.Text("Total"), lbl_total], horizontal_alignment="center"),
                bgcolor=ft.Colors.BLUE_GREY_800, padding=15, border_radius=10, width=140
            ),
            ft.Container(
                content=ft.Column([ft.Text("Promedio"), lbl_promedio], horizontal_alignment="center"),
                bgcolor=ft.Colors.BLUE_GREY_800, padding=15, border_radius=10, width=140
            ),
            ft.Container(
                content=ft.Column([ft.Text("Top Movie"), lbl_mejor], horizontal_alignment="center"),
                bgcolor=ft.Colors.BLUE_GREY_800, padding=15, border_radius=10, width=220
            ),
        ],
        alignment="center",
        spacing=15
    )

    tf_buscar = ft.TextField(
        label="Buscar por título o director...",
        prefix_icon=ft.Icons.SEARCH,
        border_color=ft.Colors.AMBER,
        width=500,
        on_change=lambda _: cargar_datos()
    )

    data_table = ft.DataTable(
        border=ft.Border.all(1, ft.Colors.AMBER),
        border_radius=10,
        heading_row_color=ft.Colors.BLUE_GREY_800,
        columns=[
            ft.DataColumn(ft.Text("ID", weight="bold", color=ft.Colors.AMBER)),
            ft.DataColumn(ft.Text("Título", weight="bold", color=ft.Colors.AMBER)),
            ft.DataColumn(ft.Text("Director", weight="bold", color=ft.Colors.AMBER)),
            ft.DataColumn(ft.Text("Punt.", weight="bold", color=ft.Colors.AMBER)),
            ft.DataColumn(ft.Text("Acciones", weight="bold", color=ft.Colors.AMBER)),
        ],
        rows=[]
    )

    mensaje_vacio = ft.Text("No se encontraron resultados", size=16, italic=True, visible=False)

    def abrir_confirmacion(pelicula_id, titulo):
        def confirmar_si(e):
            # [MODIFICADO] Lógica PRO: Capturamos el resultado para saber si hubo error en BD
            resultado = eliminar_pelicula(pelicula_id)

            if resultado is True:
                cargar_datos()
                # Mensaje de ÉXITO seguro
                snack = ft.SnackBar(
                    ft.Text(f"🗑️ '{titulo}' eliminada con éxito"),
                    bgcolor="red"
                )
                page.overlay.append(snack)
                snack.open = True
            else:
                # Mensaje de ERROR si la base de datos falla
                snack = ft.SnackBar(
                    ft.Text(f"⚠️ Error al eliminar: {resultado}"),
                    bgcolor="red"
                )
                page.overlay.append(snack)
                snack.open = True

            dialogo.open = False
            page.update()

        def confirmar_no(e):
            dialogo.open = False
            page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar '{titulo}'?"),
            actions=[
                ft.TextButton("Sí, eliminar", on_click=confirmar_si, icon=ft.Icons.DELETE, icon_color=ft.Colors.RED),
                ft.TextButton("Cancelar", on_click=confirmar_no),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def cargar_datos():
        try:
            termino = tf_buscar.value
            peliculas = buscar_peliculas(termino) if termino else obtener_todos()

            total = len(peliculas)
            if total > 0:
                promedio = sum(p.puntuacion for p in peliculas) / total
                mejor_peli = max(peliculas, key=lambda p: p.puntuacion).titulo
            else:
                promedio = 0.0
                mejor_peli = "-"

            lbl_total.value = str(total)
            lbl_promedio.value = f"{promedio:.1f}"
            lbl_mejor.value = mejor_peli

            if not peliculas:
                mensaje_vacio.visible = True
                data_table.visible = False
            else:
                mensaje_vacio.visible = False
                data_table.visible = True
                data_table.rows.clear()
                for p in peliculas:
                    data_table.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(str(p.id))),
                            ft.DataCell(ft.Text(p.titulo)),
                            ft.DataCell(ft.Text(p.director)),
                            ft.DataCell(ft.Text(str(p.puntuacion))),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        icon_color=ft.Colors.BLUE_400,
                                        on_click=lambda _, pid=p.id: on_navigate("form", pid)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.RED_400,
                                        on_click=lambda _, pid=p.id, t=p.titulo: abrir_confirmacion(pid, t)
                                    ),
                                ])
                            ),
                        ])
                    )
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
        page.update()

    cargar_datos()

    return ft.Column(
        [
            ft.Icon(ft.Icons.MOVIE, size=60, color=ft.Colors.AMBER),
            ft.Text("Catálogo de Películas", size=32, weight="bold"),
            stats_cards,
            ft.Divider(height=10, color="transparent"),
            ft.Row([tf_buscar], alignment="center"),
            ft.Divider(height=20, color="transparent"),
            mensaje_vacio,
            ft.Column([data_table], scroll=ft.ScrollMode.ALWAYS, horizontal_alignment="center")
        ],
        horizontal_alignment="center",
        expand=True
    )