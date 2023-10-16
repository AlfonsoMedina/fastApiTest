import psycopg2   
import time

DATABASE_CONFIG = {
                    'dbname': 'db_sfe_production',
					'user': 'user_dev',
					'password': 'lP1zZIq7DIhP1wY1bLTxbTEu56JsSi',
					'host': '192.168.50.215',
					'port': '5432'}

def monitor_table_traffic():
      conn = psycopg2.connect(**DATABASE_CONFIG)
      cur = conn.cursor()
      print(time.ctime())

      # Crea una función que registre las consultas en un archivo
      def log_query(query):
          with open("logs/tramites.txt", "a") as log_file:
              print(f"{time.ctime()}: {query}\n")
              log_file.write(f"{time.ctime()}: {query}\n")

      # Escucha la tabla que te interesa
      table_name = 'tramites'
      cur.execute(f"LISTEN {table_name};")
      
      try:
          while True:
              # Si detecta actividad en la tabla, registra la consulta en el archivo
              conn.poll()
              while conn.notifies:
                  notify = conn.notifies.pop(0)
                  log_query(notify.payload)
      except KeyboardInterrupt:
          # Cierra la conexión cuando termines
          cur.close()
          conn.close()

if __name__ == '__main__':
    monitor_table_traffic()