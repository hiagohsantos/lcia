import pyodbc
from queue import Queue
from threading import Lock

# Gerencia um pool com varias conexoes a diferentes SQLServers
class DatabaseConnectionPool:
    def __init__(self, max_size: int = 20, driver: str = "ODBC Driver 17 for SQL Server"):
        """Inicializa o pool de conexões."""
        self.pool = Queue(maxsize=max_size) 
        self.lock = Lock()  # Para segurança em múltiplas threads
        self.driver = driver
        self.connections = {}  # Armazena conexões com o banco cliente_id


    def _create_connection(self, server: str, database: str, username: str, password: str):
        """Cria uma nova conexão para o banco de dados."""
        conn_str = (
            f"DRIVER={{{self.driver}}};SERVER={server};DATABASE={database};"
            f"UID={username};PWD={password};Connection Timeout=60;"
        )
        return pyodbc.connect(conn_str)


    def get_connection(self, client_id: str, server: str, database: str, username: str, password: str):
        """Obtém ou cria uma conexão específica para o cliente."""
        with self.lock:
            if client_id in self.connections:
                return self.connections[client_id]

            connection = self._create_connection(server, database, username, password)
            self.connections[client_id] = connection

            self.pool.put(connection)
            return connection


    def release_connection(self, client_id: str):
        """Remove a conexão do cliente específico do pool."""
        with self.lock:
            if client_id in self.connections:
                connection = self.connections.pop(client_id)
                try:
                    connection.close()
                except Exception as e:
                    print(f"Erro ao fechar conexão do cliente {client_id}: {e}")


    def close_all(self):
        """Fecha todas as conexões no pool."""
        with self.lock:
            while not self.pool.empty():
                connection = self.pool.get()
                connection.close()
            self.connections.clear()
