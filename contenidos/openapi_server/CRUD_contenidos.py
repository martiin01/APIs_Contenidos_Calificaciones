# CRUD_contenidos.py

from sqlalchemy.orm import Session
from sqlalchemy import desc
from openapi_server.databaseContenido import Contenido as ContenidoDB

def obtener_contenido_por_id(db: Session, contenido_id: int):
    """
    Obtiene un contenido específico de la base de datos dado su ID.

    Args:
        db (Session): La sesión de la base de datos SQLAlchemy.
        contenido_id (int): El ID del contenido a buscar.

    Returns:
        ContenidoDB: El objeto Contenido si se encuentra, None en caso contrario.

    Raises:
        Exception: Si ocurre un error durante la consulta a la base de datos.
    """
    try:
        contenido = db.query(ContenidoDB).filter(ContenidoDB.id_contenido == contenido_id).first()
        if contenido:
            return contenido
        else:
            return None
    except Exception as e:
        # Agregar lógica de manejo de excepciones
        print(f"Error al obtener contenido por ID {contenido_id}: {e}")
        raise

def obtener_catalogo(db: Session, genero: str = None, orden: str = None):
    """
    Obtiene un catálogo de contenidos de la base de datos, con opciones de filtrado por género y ordenamiento.

    Args:
        db (Session): La sesión de la base de datos SQLAlchemy.
        genero (str, optional): Filtra los contenidos por género (parcialmente coincidente). Defaults to None.
        orden (str, optional): Ordena los contenidos por 'popularidad' (rating descendente) o 'fecha' (año de lanzamiento descendente). Defaults to None.

    Returns:
        list[dict]: Una lista de diccionarios, donde cada diccionario representa un contenido.

    Raises:
        Exception: Si ocurre un error durante la consulta a la base de datos.
    """
    try:
        query = db.query(ContenidoDB)
        if genero:
            query = query.filter(ContenidoDB.genero.ilike(f'%{genero}%'))
        if orden:
            if orden.lower() == 'popularidad':
                query = query.order_by(desc(ContenidoDB.rating))
            elif orden.lower() == 'fecha':
                query = query.order_by(desc(ContenidoDB.año_lanzamiento))
        contenidos_db = query.all()
        contenidos_list = [contenido.to_dict() for contenido in contenidos_db]
        return contenidos_list
    except Exception as e:
        # Agregar lógica de manejo de excepciones
        print(f"Error al obtener catálogo: {e}")
        raise

def reproducir_contenido(db: Session, contenido_id: int):
    """
    Obtiene un contenido específico de la base de datos para su reproducción, dado su ID.

    Args:
        db (Session): La sesión de la base de datos SQLAlchemy.
        contenido_id (int): El ID del contenido a reproducir.

    Returns:
        ContenidoDB: El objeto Contenido si se encuentra, None en caso contrario.

    Raises:
        Exception: Si ocurre un error durante la consulta a la base de datos.
    """
    try:
        contenido = db.query(ContenidoDB).filter(ContenidoDB.id_contenido == contenido_id).first()
        if contenido:
            return contenido
        else:
            return None
    except Exception as e:
        # Agregar lógica de manejo de excepciones
        print(f"Error al reproducir contenido ID {contenido_id}: {e}")
        raise
