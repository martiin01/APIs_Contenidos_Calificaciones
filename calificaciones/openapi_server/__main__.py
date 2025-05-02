#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS
import connexion

from openapi_server import encoder


def main():
    # Crea una instancia de la aplicación Connexion, que utiliza OpenAPI para definir las rutas
    app = connexion.App(__name__, specification_dir='./openapi/')
    # Asigna un codificador JSON personalizado para la aplicación Flask subyacente
    app.app.json_encoder = encoder.JSONEncoder
    # Añade la API definida en el archivo openapi.yaml
    # 'title' se utiliza para la documentación de la API
    # 'pythonic_params' permite utilizar nombres de parámetros estilo Python en las funciones de vista
    app.add_api('openapi.yaml',
                arguments={'title': 'Cineverse Calificaciones API'},
                pythonic_params=True)
     # Habilita CORS en la aplicación Flask subyacente
    CORS(app.app)
    # Ejecuta la aplicación en el puerto 8082 con el modo de depuración activado
    app.run(port=8082, debug=True)


if __name__ == '__main__':
    main()
