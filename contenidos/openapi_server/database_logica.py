# database_logic.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
password = "password"  # Cambia esto por la contraseña real de tu base de datos PostgreSQL
# Reemplaza 'password' con la contraseña real de tu base de datos PostgreSQL
# Configura la URL de conexión a PostgreSQL para contenidos
DATABASE_URL = "postgresql://postgres:" + password +"@localhost:5432/NombreBaseDatos"  # Cambia esto según tu configuración

# Crea la base de datos para contenidos con SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

