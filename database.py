import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Cargar las variables definidas en el archivo .env
load_dotenv()

# Obtener credenciales
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# Construir la URL de conexión
# Formato: mysql+pymysql://usuario:password@host:puerto/base
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la clase para manejar las sesiones de la base de datos
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán nuestros modelos
Base = declarative_base()

# Código de prueba para confirmar la conexión
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            print("✅ Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos: {e}")