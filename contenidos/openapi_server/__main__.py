import connexion
from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server import encoder
from openapi_server.databaseContenido import Contenido
from flask import Flask
from flask_cors import CORS


def main():
    """
    This is the main function that starts the Connexion application.

    It initializes the application, sets the JSON encoder, adds the API,
    enables CORS, and runs the application on port 8081.
    """
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Contenidos API'}, pythonic_params=True)
     # Habilita CORS en la aplicación Flask subyacente
    CORS(app.app)

    app.run(port=8081)

if __name__ == '__main__':
    main()
