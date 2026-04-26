import subprocess
from sqlalchemy import text
from database import engine


def preparar_entorno():
    print("🔍 Verificando estado de migraciones previas...")
    try:
        # Usamos el engine de nuestra database.py para limpiar versiones previas dañadas
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
        print("✅ Entorno preparado.")
    except Exception as e:
        print(f"⚠️ Error al preparar el entorno: {e}")


def ejecutar_migraciones():
    print("🚀 Generando nueva estructura (autogenerate)...")
    try:
        # Generar revisión
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", "inicial"], check=True)

        print("🚀 Aplicando los cambios en MySQL (upgrade head)...")
        # Aplicar revisión
        subprocess.run(["alembic", "upgrade", "head"], check=True)

        print("🎉 ¡Migraciones completadas con éxito! Tu tabla está lista.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la migración: {e}")


if __name__ == "__main__":
    preparar_entorno()
    ejecutar_migraciones()