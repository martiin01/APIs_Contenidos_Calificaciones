import unittest

from flask import json

from openapi_server.models.calificacion import Calificacion  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_calificaciones_id_get(self):
        """Test case for calificaciones_id_get

        Obtener calificaciones de un contenido
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/calificaciones/{id}'.format(id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_calificar_contenido(self):
        """Test case for calificar_contenido

        Calificar contenido
        """
        calificacion = {"fecha":"2000-01-23","puntuacion":1,"idContenido":0,"idUsuario":6,"comentario":"comentario"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/calificaciones',
            method='POST',
            headers=headers,
            data=json.dumps(calificacion),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
