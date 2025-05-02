import unittest

from flask import json

from openapi_server.models.contenido import Contenido  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_contenidos_id_get(self):
        """Test case for contenidos_id_get

        Obtener detalles de un contenido
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/contenidos/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_obtener_catalogo(self):
        """Test case for obtener_catalogo

        Obtener catálogo completo de contenidos
        """
        query_string = [('genero', 'genero_example'),
                        ('orden', 'orden_example')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/contenidos',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_reproducir_contenido(self):
        """Test case for reproducir_contenido

        Reproducir contenido en alta calidad
        """
        headers = { 
        }
        response = self.client.open(
            '/api/contenidos/{id}/reproducir'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
