from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# Base para las clases del modelo
Base = declarative_base()

# Definición de la tabla Contenidos
class Contenido(Base):
    __tablename__ = 'contenidos'
    
    id_contenido = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text)
    genero = Column(String(100))
    duracion = Column(Integer)
    año_lanzamiento = Column(Integer)
    rating = Column(Float)
    url_video = Column(String(255))
    thumbnail = Column(String(255))
    def to_dict(self):
        return {
            "id_contenido": self.id_contenido,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "genero": self.genero,
            "duracion": self.duracion,
            "año_lanzamiento": self.año_lanzamiento,
            "rating": self.rating,
            "url_video": self.url_video,
            "thumbnail": self.thumbnail
        }


