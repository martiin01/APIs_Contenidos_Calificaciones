# CRUD_calificaciones.py

from sqlalchemy.orm import Session
from openapi_server.databaseCalificaciones import Calificacion as CalificacionDB
from datetime import datetime

def obtener_calificaciones_por_contenido(db: Session, id_contenido: int):
    """
    Obtiene todas las calificaciones asociadas a un contenido específico.

    Args:
        db (Session): La sesión de la base de datos SQLAlchemy.
        id_contenido (int): El ID del contenido del cual se quieren obtener las calificaciones.

    Returns:
        list[dict]: Una lista de diccionarios, donde cada diccionario representa una calificación.
                     Retorna una lista vacía si no hay calificaciones para el contenido.

    Raises:
        Exception: Si ocurre algún error durante la consulta a la base de datos.
    """
    try:
        calificaciones = db.query(CalificacionDB).filter(CalificacionDB.id_contenido == id_contenido).all()
        return [calificacion.to_dict() for calificacion in calificaciones]
    except Exception as e:
        raise e

def agregar_calificacion(db: Session, id_contenido: int, id_usuario: int, puntuacion: int, comentario: str = None):
    """
    Agrega una nueva calificación a la base de datos.

    Args:
        db (Session): La sesión de la base de datos SQLAlchemy.
        id_contenido (int): El ID del contenido que se está calificando.
        id_usuario (int): El ID del usuario que está realizando la calificación.
        puntuacion (int): La puntuación dada al contenido.
        comentario (str, optional): Un comentario opcional sobre la calificación. Defaults to None.

    Returns:
        dict: Un diccionario que representa la calificación recién creada.

    Raises:
        Exception: Si ocurre algún error durante la inserción en la base de datos.
    """
    try:
        nueva_calificacion = CalificacionDB(
            id_contenido=id_contenido,
            id_usuario=id_usuario,
            puntuacion=puntuacion,
            comentario=comentario,
            fecha=datetime.now()
        )
        db.add(nueva_calificacion)
        db.commit()
        db.refresh(nueva_calificacion)
        return nueva_calificacion.to_dict()
    except Exception as e:
        db.rollback()
        raise e