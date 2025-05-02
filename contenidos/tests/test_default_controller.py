# test_default_controller.py

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from openapi_server.controllers.default_controller import (
    obtener_catalogo,
    contenidos_id_get,
    reproducir_contenido,
)

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

    # Pruebas existentes para calificaciones...
    # ...

    # -----------------------------------------
    # Pruebas para métodos relacionados con contenidos
    # -----------------------------------------

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_obtener_catalogo_success(self, mock_sessionlocal):
        # Tu código existente
        pass

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_obtener_catalogo_with_filters(self, mock_sessionlocal):
        # Tu código existente
        pass

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_contenidos_id_get_success(self, mock_sessionlocal):
        # Tu código existente
        pass

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_contenidos_id_get_not_found(self, mock_sessionlocal):
        mock_db_session = MagicMock()
        mock_sessionlocal.return_value = mock_db_session

        with patch('openapi_server.controllers.default_controller.CRUD_contenidos.obtener_contenido_por_id') as mock_obtener_contenido:
            mock_obtener_contenido.return_value = None
            response, status_code = contenidos_id_get(999)

            self.assertEqual(status_code, 404)
            self.assertEqual(response.get_json()['mensaje'], 'Contenido no encontrado')

    @patch('openapi_server.controllers.default_controller.SessionLocal')
    def test_reproducir_contenido_not_found(self, mock_sessionlocal):
        mock_db_session = MagicMock()
        mock_sessionlocal.return_value = mock_db_session

        with patch('openapi_server.controllers.default_controller.CRUD_contenidos.reproducir_contenido') as mock_reproducir_contenido:
            mock_reproducir_contenido.return_value = None
            response, status_code = reproducir_contenido(999)

            self.assertEqual(status_code, 404)
            self.assertEqual(response.get_json()['mensaje'], 'Contenido no encontrado')

if __name__ == '__main__':
    unittest.main()