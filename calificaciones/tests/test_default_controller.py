# test_default_controller.py

# test_default_controller.py

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from openapi_server.controllers.default_controller import calificar_contenido, calificaciones_id_get

class TestDefaultController(unittest.TestCase):

    def setUp(self):
        # Crear una aplicación de Flask para pruebas
        self.app = Flask(__name__)
        # Establecer el contexto de la aplicación
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Eliminar el contexto de la aplicación
        self.app_context.pop()

    @patch('openapi_server.controllers.default_controller.connexion')
    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_calificar_contenido_success(self, mock_sessionlocal, mock_connexion):
        mock_connexion.request.is_json = True
        mock_connexion.request.get_json.return_value = {
            'idContenido': 1,
            'idUsuario': 2,
            'puntuacion': 5,
            'comentario': 'Excelente contenido'
        }
        mock_db_session = MagicMock()
        mock_sessionlocal.return_value = mock_db_session

        with patch('openapi_server.controllers.default_controller.CRUD_calificaciones.agregar_calificacion') as mock_agregar:
            mock_agregar.return_value = {
                'id_calificacion': 1,
                'idContenido': 1,
                'idUsuario': 2,
                'puntuacion': 5,
                'comentario': 'Excelente contenido',
                'fecha': '2023-10-01'
            }
            response, status_code = calificar_contenido()

            self.assertEqual(status_code, 201)
            self.assertEqual(response.json['id_calificacion'], 1)

    @patch('openapi_server.controllers.default_controller.connexion')
    def test_calificar_contenido_invalid_json(self, mock_connexion):
        mock_connexion.request.is_json = False
        response, status_code = calificar_contenido()
        self.assertEqual(status_code, 400)
        self.assertEqual(response.json['mensaje'], 'Datos inválidos, se esperaba JSON')

    @patch('openapi_server.controllers.default_controller.connexion')
    def test_calificar_contenido_missing_field(self, mock_connexion):
        mock_connexion.request.is_json = True
        mock_connexion.request.get_json.return_value = {
            'idContenido': 1,
            'puntuacion': 5
        }
        response, status_code = calificar_contenido()
        self.assertEqual(status_code, 400)
        self.assertIn('Falta el campo requerido', response.json['mensaje'])

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_calificaciones_id_get_success(self, mock_sessionlocal):
        mock_db_session = MagicMock()
        mock_sessionlocal.return_value = mock_db_session

        with patch('openapi_server.controllers.default_controller.CRUD_calificaciones.obtener_calificaciones_por_contenido') as mock_obtener:
            mock_obtener.return_value = [
                {
                    'id_calificacion': 1,
                    'idContenido': 1,
                    'idUsuario': 2,
                    'puntuacion': 5,
                    'comentario': 'Excelente contenido',
                    'fecha': '2023-10-01'
                }
            ]
            response = calificaciones_id_get(1)

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)
            self.assertEqual(len(response.json), 1)

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_calificaciones_id_get_no_content(self, mock_sessionlocal):
        mock_db_session = MagicMock()
        mock_sessionlocal.return_value = mock_db_session

        with patch('openapi_server.controllers.default_controller.CRUD_calificaciones.obtener_calificaciones_por_contenido') as mock_obtener:
            mock_obtener.return_value = []
            response, status_code = calificaciones_id_get(1)

            self.assertEqual(status_code, 404)
            self.assertEqual(response.json['mensaje'], 'No hay calificaciones para este contenido')

if __name__ == '__main__':
    unittest.main()