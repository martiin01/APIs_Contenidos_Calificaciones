import sys
from datetime import datetime, date
import psycopg2
import oracledb as PBD
def get_postgres_connection():
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='Contenidos',
            user='postgres',
            password='password' # Cambia esto según tu configuración
        )
        return conn
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        sys.exit(1)

def get_oracle_connection():
    ip = "localhost"
    puerto = 1521
    s_id = "xe"
    usuario = "system"
    contrasena = "12345"
    print("---Conectando a Oracle---")
    try:
        conexion = PBD.connect(
            user=usuario,
            password=contrasena,
            host=ip,
            port=puerto,
            sid=s_id
        )
        print("Conexión realizada a la base de datos Oracle")
        return conexion
    except PBD.DatabaseError as error:
        print("Error en la conexión a Oracle")
        print(error)
        sys.exit(1)
def normalize_row(row):
    normalized = []
    for item in row:
        if isinstance(item, date) and not isinstance(item, datetime):
            # Convertir date a datetime para Oracle
            item = datetime.combine(item, datetime.min.time())
            normalized.append(item)
        elif isinstance(item, datetime):
            # Eliminar microsegundos
            item = item.replace(microsecond=0)
            normalized.append(item)
        # Si el item es una cadena, eliminar espacios en blanco al principio y al final y convertir a minúsculas
        elif isinstance(item, str):
            normalized.append(item.strip().lower())
        else:
            normalized.append(item)
    return tuple(normalized)

def fetch_data(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    for row in columns:
        print(row)
    data = cursor.fetchall()
    cursor.close()

    for row in data:
        print(row)

    return columns, data

def sync_tables(postgres_conn, oracle_conn):
    postgres_query = "SELECT * FROM contenidos"
    oracle_query = "SELECT * FROM contenidos"

    pg_columns, pg_data = fetch_data(postgres_conn, postgres_query)
    or_columns, or_data = fetch_data(oracle_conn, oracle_query)

    # Verificar si las columnas de las tablas coinciden en número de columnas
    if len(pg_columns) != len(or_columns):
        print("Las columnas de las tablas no coinciden. Verifica la estructura de las tablas.")
        sys.exit(1)
    print("Las columnas de las tablas coinciden.")

    # Normalizar los datos
    pg_data_normalized = [normalize_row(row) for row in pg_data]
    or_data_normalized = [normalize_row(row) for row in or_data]

    # Crear diccionarios de datos basados en la clave primaria (ID)
    pg_data_dict = {row[0]: row for row in pg_data_normalized}
    or_data_dict = {row[0]: row for row in or_data_normalized}

    # Determinar los conjuntos de claves primarias
    pg_keys = set(pg_data_dict.keys())
    or_keys = set(or_data_dict.keys())

    # Determinar claves para insertar, actualizar y eliminar
    keys_to_insert = pg_keys - or_keys
    keys_to_delete = or_keys - pg_keys
    common_keys = pg_keys & or_keys

    # Identificar registros que han cambiado
    keys_to_update = []
    for key in common_keys:
        pg_row = pg_data_dict[key]
        or_row = or_data_dict[key]
        # Comparar los registros excluyendo la clave primaria
        if pg_row[1:] != or_row[1:]:
            keys_to_update.append(key)

    cursor = oracle_conn.cursor()

    # Insertar nuevos registros en Oracle
    if keys_to_insert:
        placeholders = ', '.join([':%d' % (i+1) for i in range(len(pg_columns))])
        insert_query = f"INSERT INTO contenidos ({', '.join(pg_columns)}) VALUES ({placeholders})"
        for key in keys_to_insert:
            row = pg_data_dict[key]
            print(f"Insertando registro en Oracle: ID={key}")
            cursor.execute(insert_query, row)
        print(f"Insertados {len(keys_to_insert)} registros nuevos en Oracle.")

    # Actualizar registros modificados en Oracle
    if keys_to_update:
        update_columns = pg_columns[1:]  # Excluir la clave primaria
        set_clause = ', '.join([f"{col} = :{i+1}" for i, col in enumerate(update_columns)])
        update_query = f"UPDATE contenidos SET {set_clause} WHERE {pg_columns[0]} = :{len(update_columns)+1}"
        for key in keys_to_update:
            pg_row = pg_data_dict[key]
            # Obtener los valores a actualizar (excluyendo la clave primaria)
            row = pg_row[1:]
            params = list(row) + [key]   # Agregar la clave primaria al final
            print(f"Actualizando registro en Oracle: ID={key}")
            cursor.execute(update_query, params)
        print(f"Actualizados {len(keys_to_update)} registros en Oracle.")

    # Eliminar registros de Oracle que no están en PostgreSQL
    if keys_to_delete:
        delete_query = f"DELETE FROM contenidos WHERE {pg_columns[0]} = :1"
        for key in keys_to_delete:
            print(f"Eliminando registro en Oracle con clave primaria: {key}")
            cursor.execute(delete_query, (key,))
        print(f"Eliminados {len(keys_to_delete)} registros de Oracle.")

    oracle_conn.commit()
    cursor.close()

def main():
    postgres_conn = get_postgres_connection()
    oracle_conn = get_oracle_connection()

    sync_tables(postgres_conn, oracle_conn)

    postgres_conn.close()
    oracle_conn.close()

if __name__ == "__main__":
    main()