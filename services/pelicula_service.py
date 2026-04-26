from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 💡 URL DE CONEXIÓN
DATABASE_URL = "mysql+pymysql://root:Abimaely8.@localhost:3306/flet_peliculas_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Pelicula(Base):
    __tablename__ = "peliculas"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    director = Column(String(255))
    puntuacion = Column(Integer)


def obtener_todos():
    session = SessionLocal()
    try:
        return session.query(Pelicula).all()
    finally:
        session.close()


def crear_pelicula(datos):
    session = SessionLocal()
    try:
        titulo = datos.get('titulo')
        director = datos.get('director')

        if not titulo or str(titulo).strip() == "":
            return "El título no puede estar vacío."

        if not director or str(director).strip() == "":
            return "El director no puede estar vacío."

        try:
            puntuacion = int(datos.get('puntuacion'))
            if not (1 <= puntuacion <= 10):
                return "La puntuación debe estar entre 1 y 10."
        except (ValueError, TypeError):
            return "La puntuación debe ser un número entero válido."

        nueva_pelicula = Pelicula(
            titulo=titulo.strip(),
            director=director.strip(),
            puntuacion=puntuacion
        )

        session.add(nueva_pelicula)
        session.commit()
        return True

    except Exception as e:
        session.rollback()
        print(f"❌ Error crítico en el servicio: {e}")
        return "Ocurrió un error interno al procesar la solicitud."
    finally:
        session.close()


def actualizar_pelicula(pelicula_id, datos):
    session = SessionLocal()
    try:
        peli = session.query(Pelicula).filter(Pelicula.id == pelicula_id).first()

        if peli:
            peli.titulo = datos.get('titulo').strip()
            peli.director = datos.get('director').strip()
            peli.puntuacion = int(datos.get('puntuacion'))

            session.commit()
            return True
        return "Película no encontrada"
    except Exception as e:
        session.rollback()
        return str(e)
    finally:
        session.close()


def obtener_por_id(pelicula_id):
    session = SessionLocal()
    try:
        return session.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    finally:
        session.close()


# [NUEVO] FASE 11: Función para eliminar de la base de datos
def eliminar_pelicula(pelicula_id):
    session = SessionLocal()
    try:
        # Buscamos el registro por su ID
        peli = session.query(Pelicula).filter(Pelicula.id == pelicula_id).first()

        if peli:
            session.delete(peli)
            session.commit()
            return True  # Indica éxito
        return "Película no encontrada"
    except Exception as e:
        session.rollback()
        print(f"❌ Error al eliminar: {e}")
        return str(e)
    finally:
        session.close()

# ... (mantén todo lo anterior)

def buscar_peliculas(termino):
    session = SessionLocal()
    try:
        # Usamos .ilike() para que no importe si es mayúscula o minúscula
        return session.query(Pelicula).filter(
            (Pelicula.titulo.ilike(f"%{termino}%")) |
            (Pelicula.director.ilike(f"%{termino}%"))
        ).all()
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return []
    finally:
        session.close()