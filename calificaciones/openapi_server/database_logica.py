# database_logic.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configura la URL de conexión a PostgreSQL para contenidos
DATABASE_URL = "postgresql://postgres:password@localhost:5432/NombreBaseDeDatos"
# Reemplaza 'password' con la contraseña real de tu base de datos PostgreSQL
# Reemplaza 'NombreBaseDeDatos' con el nombre real de tu base de datos

# Crea la base de datos para contenidos con SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

