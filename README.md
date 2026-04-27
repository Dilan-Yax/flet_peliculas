# Gestor de Películas

Este es un proyecto sencillo desarrollado en **Python** utilizando **Flet** para la interfaz de escritorio y **MySQL** para el almacenamiento de datos. El objetivo principal fue crear una aplicación funcional que conecte una interfaz gráfica con una base de datos relacional.

## ¿Qué hace la aplicación?

- **Administración de películas:** Permite agregar, ver, editar y borrar registros.
- **Buscador:** Filtra películas por nombre o director en tiempo real.
- **Métricas:** Muestra el total de películas y la puntuación promedio.
- **Validación:** Controla que no se guarden campos vacíos o puntuaciones fuera de rango.
- **Diseño:** Interfaz limpia con soporte para modo oscuro y claro.

## Tecnologías utilizadas

- **Python** (Lógica)
- **Flet** (Interfaz gráfica)
- **MySQL / SQLAlchemy** (Base de datos)
- **PyCharm** (IDE de desarrollo)

## Organización del código

El proyecto mantiene una estructura organizada para facilitar su lectura:
- `views/`: Pantallas y elementos visuales.
- `models/`: Estructura de las tablas de la base de datos.
- `services/`: Consultas y transacciones con MySQL.
- `components/`: Componentes reutilizables de la interfaz.

## Desarrollo y Colaboración

Este proyecto fue desarrollado íntegramente con la asistencia de **Gemini**.
Se utilizó la inteligencia artificial como herramienta principal para la arquitectura del código,
la resolución de errores, la lógica de base de datos y la estructuración de la interfaz de usuario.
