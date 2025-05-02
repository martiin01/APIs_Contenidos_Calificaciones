# default_controller.py

import connexion
from flask import jsonify
from openapi_server.database_logica import SessionLocal
from openapi_server import CRUD_contenidos

def obtener_catalogo(genero=None, orden=None):
    """Obtener catálogo completo de contenidos"""
    db = SessionLocal()
    try:
        contenidos_list = CRUD_contenidos.obtener_catalogo(db, genero, orden)
        return jsonify(contenidos_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def contenidos_id_get(contenido_id):
    """Obtener detalles de un contenido específico por su ID"""
    db = SessionLocal()
    try:
        contenido = CRUD_contenidos.obtener_contenido_por_id(db, contenido_id)
        if contenido:
            return jsonify(contenido.to_dict())
        else:
            return jsonify({'mensaje': 'Contenido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

def reproducir_contenido(contenido_id):
    """Reproducir contenido en alta calidad"""
    db = SessionLocal()
    try:
        contenido = CRUD_contenidos.reproducir_contenido(db, contenido_id)
        if contenido:
            return jsonify({'url_reproduccion': contenido.url_video})
        else:
            return jsonify({'mensaje': 'Contenido no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

