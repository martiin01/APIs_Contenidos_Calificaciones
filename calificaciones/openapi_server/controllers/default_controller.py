# default_controller.py

import connexion
from flask import jsonify
from openapi_server.database_logica import SessionLocal
from openapi_server import CRUD_calificaciones

def calificar_contenido():
    """Calificar contenido
    Esta función recibe una solicitud JSON con la información de la calificación,
    valida los datos, y agrega la calificación a la base de datos.
    """
    db = None  # Inicializar 'db' como None para asegurar que se pueda cerrar en el bloque finally
    if not connexion.request.is_json:
        return jsonify({'mensaje': 'Datos inválidos, se esperaba JSON'}), 400

    try:
        # Obtener los datos de la calificación desde la solicitud JSON
        calificacion_data = connexion.request.get_json()
        # Definir los campos requeridos en la solicitud
        required_fields = ['idContenido', 'idUsuario', 'puntuacion']
        # Validar que todos los campos requeridos estén presentes
        for field in required_fields:
            if field not in calificacion_data:
                return jsonify({'mensaje': f'Falta el campo requerido: {field}'}), 400

        # Extraer los valores de los campos
        id_contenido = calificacion_data['idContenido']
        id_usuario = calificacion_data['idUsuario']
        puntuacion = calificacion_data['puntuacion']
        # Obtener el comentario, si está presente
        comentario = calificacion_data.get('comentario', None)

        # Crear una nueva sesión de base de datos
        db = SessionLocal()
        # Agregar la calificación a la base de datos utilizando la función CRUD
        nueva_calificacion = CRUD_calificaciones.agregar_calificacion(
            db, id_contenido, id_usuario, puntuacion, comentario
        )
        # Devolver la nueva calificación con un código de estado 201 (creado)
        return jsonify(nueva_calificacion), 201
    except Exception as e:
        # En caso de error, devolver un mensaje de error con un código de estado 500
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos, independientemente de si hubo un error o no
        if db:
            db.close()

def calificaciones_id_get(id_contenido):
    """Obtener calificaciones de un contenido
    Esta función recibe un ID de contenido y devuelve todas las calificaciones
    asociadas a ese contenido desde la base de datos.
    """
    # Crear una nueva sesión de base de datos
    db = SessionLocal()
    try:
        # Obtener las calificaciones por ID de contenido utilizando la función CRUD
        calificaciones = CRUD_calificaciones.obtener_calificaciones_por_contenido(db, id_contenido)
        if calificaciones:
            # Si hay calificaciones, devolverlas en formato JSON
            return jsonify(calificaciones)
        else:
            # Si no hay calificaciones, devolver un mensaje indicando que no hay calificaciones
            return jsonify({'mensaje': 'No hay calificaciones para este contenido'}), 404
    except Exception as e:
        # En caso de error, devolver un mensaje de error con un código de estado 500
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar la sesión de la base de datos
        db.close()