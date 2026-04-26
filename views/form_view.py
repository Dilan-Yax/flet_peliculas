import flet as ft
# [MODIFICADO] Importamos las nuevas funciones necesarias para editar
from services.pelicula_service import crear_pelicula, actualizar_pelicula, obtener_por_id


# [MODIFICADO] Agregamos id_edit=None para que el formulario sepa si va a editar
def FormView(page: ft.Page, on_navigate, id_edit=None):
    # [NUEVO] Función limpia para quitar errores
    def limpiar_error(e):
        campo_nombre = e.control.data  # Usamos .data para identificar qué campo es
        e.control.border_color = "amber"

        # Ocultamos el mensaje de error correspondiente
        if campo_nombre == "titulo":
            err_titulo.visible = False
        elif campo_nombre == "director":
            err_director.visible = False
        elif campo_nombre == "puntuacion":
            err_puntuacion.visible = False

        page.update()

    # --- CAMPOS DE TEXTO ---
    # Agregamos .data para identificarlos en limpiar_error
    tf_titulo = ft.TextField(label="Título", border_color="amber", width=400, on_change=limpiar_error, data="titulo")
    tf_director = ft.TextField(label="Director", border_color="amber", width=400, on_change=limpiar_error,
                               data="director")
    tf_puntuacion = ft.TextField(label="Puntuación (1-10)", border_color="amber", width=400, on_change=limpiar_error,
                                 data="puntuacion")

    # --- [LA SOLUCIÓN] NUESTROS PROPIOS MENSAJES DE ERROR ---
    # Estos textos están ocultos (visible=False) pero listos para aparecer
    err_titulo = ft.Text(color="red", visible=False, size=12)
    err_director = ft.Text(color="red", visible=False, size=12)
    err_puntuacion = ft.Text(color="red", visible=False, size=12)

    # [NUEVO] Si recibimos un ID, buscamos la película y rellenamos los campos
    if id_edit:
        pelicula = obtener_por_id(id_edit)
        if pelicula:
            tf_titulo.value = pelicula.titulo
            tf_director.value = pelicula.director
            tf_puntuacion.value = str(pelicula.puntuacion)

    def guardar_click(e):
        # --- VALIDACIÓN CON TEXTOS PERSONALIZADOS ---
        hay_error = False

        if not tf_titulo.value or not tf_titulo.value.strip():
            tf_titulo.border_color = "red"
            err_titulo.value = "⚠️ El título es obligatorio"
            err_titulo.visible = True
            hay_error = True

        if not tf_director.value or not tf_director.value.strip():
            tf_director.border_color = "red"
            err_director.value = "⚠️ El director es obligatorio"
            err_director.visible = True
            hay_error = True

        # Validación específica para la puntuación
        val_punt = tf_puntuacion.value.strip() if tf_puntuacion.value else ""
        if not val_punt:
            tf_puntuacion.border_color = "red"
            err_puntuacion.value = "⚠️ La puntuación es obligatoria"
            err_puntuacion.visible = True
            hay_error = True
        elif not val_punt.isdigit():
            tf_puntuacion.border_color = "red"
            err_puntuacion.value = "⚠️ Error: Solo se permiten números enteros"
            err_puntuacion.visible = True
            hay_error = True
        elif not (1 <= int(val_punt) <= 10):
            tf_puntuacion.border_color = "red"
            err_puntuacion.value = "⚠️ El rango debe ser de 1 a 10"
            err_puntuacion.visible = True
            hay_error = True

        # Si hay error, actualizamos la página entera para que se redibujen los textos ocultos
        if hay_error:
            page.update()
            return
        # -------------------------------------------------------

        # --- RASTREO EN TERMINAL (Mantenido) ---
        print("\n>>> BOTÓN PRESIONADO <<<")
        print(f"Datos a enviar: {tf_titulo.value}, {tf_director.value}, {tf_puntuacion.value}")

        nueva_data = {
            "titulo": tf_titulo.value,
            "director": tf_director.value,
            "puntuacion": tf_puntuacion.value
        }

        # [MODIFICADO] Lógica inteligente: Si hay ID editamos, si no creamos
        if id_edit:
            print(f"Editando película ID: {id_edit}")
            resultado = actualizar_pelicula(id_edit, nueva_data)
        else:
            print("Creando nueva película")
            resultado = crear_pelicula(nueva_data)

        print(f"Resultado del servicio: {resultado}")

        if resultado is True:
            print("Operación exitosa. Navegando al home...")
            snack = ft.SnackBar(
                ft.Text("✅ Cambios guardados" if id_edit else "✅ Película guardada"),
                bgcolor="green"
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
            on_navigate("home")
        else:
            print(f"Fallo: {resultado}")
            snack = ft.SnackBar(ft.Text(f"⚠️ {resultado}"), bgcolor="red")
            page.overlay.append(snack)
            snack.open = True
            page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    ft.Icons.EDIT_NOTE if id_edit else ft.Icons.ADD_TASK,
                    size=50, color="amber"
                ),
                # [MODIFICADO] Título dinámico
                ft.Text(
                    "Editar Película" if id_edit else "Registrar Nueva Película",
                    size=28, weight="bold"
                ),

                # --- AQUÍ AGRUPAMOS LOS CAMPOS CON SUS MENSAJES DE ERROR ---
                ft.Column([tf_titulo, err_titulo], spacing=2, horizontal_alignment="start"),
                ft.Column([tf_director, err_director], spacing=2, horizontal_alignment="start"),
                ft.Column([tf_puntuacion, err_puntuacion], spacing=2, horizontal_alignment="start"),

                ft.Row(
                    [
                        ft.ElevatedButton(
                            # [MODIFICADO] Texto del botón dinámico
                            "Actualizar" if id_edit else "Guardar Película",
                            icon=ft.Icons.SAVE,
                            bgcolor="amber",
                            color="black",
                            on_click=guardar_click
                        ),
                        ft.OutlinedButton(
                            "Cancelar",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: on_navigate("home")
                        ),
                    ],
                    alignment="center",
                    spacing=20
                ),
            ],
            horizontal_alignment="center",
            spacing=15,
        ),
        padding=40
    )