from sqlalchemy import Column, Integer, String
# Importamos la clase Base que creamos en el paso anterior
from database import Base


class Pelicula(Base):
    # Definimos el nombre exacto que tendrá la tabla en MySQL
    __tablename__ = "peliculas"

    # Definimos las columnas
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(150), nullable=False)
    director = Column(String(150), nullable=False)
    puntuacion = Column(Integer, nullable=False)


# Código de prueba para confirmar que la clase funciona correctamente
if __name__ == "__main__":
    # Creamos un objeto de prueba en memoria (aún no se guarda en MySQL)
    peli_prueba = Pelicula(titulo="The Matrix", director="Lana y Lilly Wachowski", puntuacion=10)

    print(
        f"✅ Objeto de prueba creado: {peli_prueba.titulo} - Dirigida por {peli_prueba.director} (Puntuación: {peli_prueba.puntuacion}/10)")