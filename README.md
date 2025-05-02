# Descripción General del Proyecto

Este repositorio contiene dos microservicios separados para una aplicación de streaming de vídeo:

1.  **API [`contenidos`](contenidos):** Gestiona el catálogo de contenido de vídeo. Se encarga de recuperar la lista de contenido disponible, obtener detalles de elementos específicos (descripción, duración, género, calificación), filtrar/ordenar el catálogo y proporcionar información de reproducción. Este servicio interactúa con una base de datos PostgreSQL.
2.  **API [`calificaciones`](calificaciones):** Gestiona las calificaciones y comentarios de los usuarios para el contenido de vídeo. Permite a los usuarios enviar calificaciones (1-5 estrellas) y comentarios para contenido específico y recupera las calificaciones existentes para un ID de contenido determinado. Este servicio también interactúa con una base de datos PostgreSQL.

Ambas APIs están construidas usando Python con Flask y la librería Connexion, aprovechando las especificaciones OpenAPI para definir las rutas y modelos de la API. Se utiliza SQLAlchemy para la interacción con la base de datos.

## Configuración de la Base de Datos

**Importante:** Antes de ejecutar las APIs, es necesario configurar las bases de datos PostgreSQL correspondientes.

1.  **Creación de las Bases de Datos:** Cada API (`contenidos` y `calificaciones`) requiere su propia base de datos PostgreSQL. Debes crear estas bases de datos manualmente en tu servidor PostgreSQL.
2.  **Modificación de la Configuración:** Una vez creadas las bases de datos, necesitas actualizar la configuración de conexión dentro del código de cada API. Busca los archivos de configuración o las variables de entorno donde se definen los parámetros de conexión a la base de datos (como el nombre de usuario, contraseña, host, puerto y nombre de la base de datos) y modifícalos para que coincidan con tu entorno.

## Ejecución de los Servicios

Cada API se ejecuta de forma independiente. Asegúrate de haber configurado la base de datos correspondiente antes de iniciar cada servicio.

### Ejecución de la API [`contenidos`](contenidos)

1.  Navega al directorio [`contenidos`](contenidos):
    ```bash
    cd contenidos
    ```
2.  Instala las dependencias:
    ```bash
    pip3 install -r requirements.txt
    ```
3.  Ejecuta el servidor (por defecto en el puerto 8081):
    ```bash
    python3 -m openapi_server
    ```
4.  La interfaz de usuario de la API estará disponible en `http://localhost:8081/api/ui/` y la definición OpenAPI en `http://localhost:8081/api/openapi.json`.

### Ejecución de la API [`calificaciones`](calificaciones)

1.  Navega al directorio [`calificaciones`](calificaciones):
    ```bash
    cd calificaciones
    ```
2.  Instala las dependencias:
    ```bash
    pip3 install -r requirements.txt
    ```
3.  Ejecuta el servidor (por defecto en el puerto 8082):
    ```bash
    python3 -m openapi_server
    ```
4.  La interfaz de usuario de la API estará disponible en `http://localhost:8082/api/ui/` y la definición OpenAPI en `http://localhost:8082/api/openapi.json`.

### Ejecución con Docker (para cada servicio)

También puedes ejecutar cada servicio dentro de un contenedor Docker. Desde el directorio del servicio respectivo ([`calificaciones`](calificaciones) o [`contenidos`](contenidos)):

**Nota:** Asegúrate de que la configuración de la base de datos dentro de la imagen Docker apunte a una base de datos accesible desde el contenedor (podría ser una base de datos en otro contenedor o en el host).

1.  Construye la imagen Docker:
    ```bash
    # Reemplaza 'openapi_server' con un nombre único si lo deseas, ej., 'calificaciones_api' o 'contenidos_api'
    docker build -t openapi_server .
    ```
2.  Ejecuta el contenedor (mapea el puerto 8080 del contenedor a un puerto del host, ej., 8081 para contenidos, 8082 para calificaciones):
    ```bash
    # Para la API de contenidos
    docker run -p 8081:8080 openapi_server

    # Para la API de calificaciones
    docker run -p 8082:8080 openapi_server
    ```

## Pruebas (Testing)

Las pruebas de integración para cada servicio se pueden ejecutar usando `tox`. Desde el directorio del servicio respectivo ([`calificaciones`](calificaciones) o [`contenidos`](contenidos)):

1.  Instala tox (si no está ya instalado):
    ```bash
    pip install tox
    # o sudo pip install tox dependiendo de tu entorno
    ```
2.  Ejecuta las pruebas:
    ```bash
    tox
    ```
