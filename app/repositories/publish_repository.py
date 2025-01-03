import pyodbc
from app.models.process_model import ProcessModel

import pyodbc
from app.models.process_model import ProcessModel

class LCDatabaseConnection:
    def __init__(self, server: str, database: str, username: str, password: str, driver: str = "ODBC Driver 17 for SQL Server"):
        """Inicializa as configurações de conexão com o SQLServer."""
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.connection = None

    def connect(self):
        """Estabelece uma conexão com o banco de dados, caso ainda não esteja aberta."""
        if not self.connection:
            try:
                conn_str = (
                    f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};"
                    f"UID={self.username};PWD={self.password};Connection Timeout=60;"
                )
                self.connection = pyodbc.connect(conn_str)
            except Exception as e:
                print(f"Erro ao conectar ao banco de dados: {e}")
                raise e

    def close(self):
        """Fecha a conexão com o banco de dados, se estiver aberta."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_cursor(self):
        """Retorna o cursor para a conexão ativa."""
        if not self.connection:
            self.connect()
        return self.connection.cursor()


class PublishRepository:
    def __init__(self, db_connection: LCDatabaseConnection, table_name: str):
        """Inicializa o repositório com a conexão do banco de dados e o nome da tabela."""
        self.db_connection = db_connection
        self.table_name = table_name

    def get_publish_from_LC(self, publish_id: str):
        """Consulta dados na tabela configurada por ID."""
        try:
            cursor = self.db_connection.get_cursor()
            query = f"SELECT * FROM [dbo].[{self.table_name}] WHERE [pcml_Id] = ?"
            cursor.execute(query, (str(publish_id),))
            result = cursor.fetchall()
            if result:
                return ProcessModel(
                    id=result[0][0],
                    sentence=result[0][4]
                )
            return None
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return None

