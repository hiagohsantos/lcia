
from app.models.organization import Organization
from app.models.process_model import ProcessModel
from flask import current_app
import pyodbc

class LCRepository:
    def __init__(self, organization: Organization):
        """Inicializa o repositório com as credenciais e tabela específicas."""
        self.db_pool = current_app.config['DB_POOL']
        self.client_id = organization.id
        self.server = organization.db_server
        self.database = organization.db_name
        self.username = organization.db_user
        self.password = organization.db_password


    def get_publish_by_id(self, publish_id: str, table_name = "lcr_CC_Publish", column_name = "pubi_PublishId"):
        """Consulta dados na tabela configurada por ID."""
        try:
            # Obtém conexão do pool
            connection = self.db_pool.get_connection(
                self.client_id, self.server, self.database, self.username, self.password
            )
            cursor = connection.cursor()

            # Executa a consulta
            query = f"SELECT * FROM [dbo].[{table_name}] WHERE [{column_name}] = ?"
            cursor.execute(query, (str(publish_id),))
            result = cursor.fetchall()

            if result:
                return ProcessModel(
                    id=result[0][0],
                    sentence=result[0][7]
                )
            return None
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return None
        

    def get_process_by_id(self, process_id: str, table_name = "lcr_CC_Process", column_name = "prcs_ProcessId"):
        """Consulta dados na tabela configurada por ID."""
        try:
            # Obtém conexão do pool
            connection = self.db_pool.get_connection(
                self.client_id, self.server, self.database, self.username, self.password
            )
            cursor = connection.cursor()

            # Executa a consulta
            query = f"SELECT * FROM [dbo].[{table_name}] WHERE [{column_name}] = ?"
            cursor.execute(query, (str(process_id),))
            result = cursor.fetchall()
            print(result)
            if result:
                return ProcessModel(
                    id=result[0][0],
                    sentence=result[0][7]
                )
            return None
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return None


    def group_xml_fragments(self, rows):
        xml_fragments = []
        for row in rows:
            xml_fragments.append(row[0])
        
        xml_data = ''.join(xml_fragments)
        return xml_data
                 

    def get_process_client_position(self, process_id: str):
        """Consulta dados na tabela configurada por ID."""
        try:
            # Obtém conexão do pool
            connection = self.db_pool.get_connection(
                self.client_id, self.server, self.database, self.username, self.password
            )

            with connection.cursor() as cursor:
                # Configurando a execução da stored procedure com parâmetros
                sql = """
                    EXEC dbo.lcr_p_CC_GetProcessClientPosition @processId = ?;
                """
                cursor.execute(sql, (process_id))
                 # Loop para capturar o resultado do output
                rows = cursor.fetchall()
                print(rows)
                data = self.group_xml_fragments(rows)

                print(data)
                
                return None
            
        except Exception as e:
            print(f"Erro na consulta: {e}")
            return None


# class LCDatabaseConnection:
#     def __init__(self, server: str, database: str, username: str, password: str, driver: str = "ODBC Driver 17 for SQL Server"):
#         """Inicializa as configurações de conexão com o SQLServer."""
#         self.server = server
#         self.database = database
#         self.username = username
#         self.password = password
#         self.driver = driver
#         self.connection = None

#     def connect(self):
#         """Estabelece uma conexão com o banco de dados, caso ainda não esteja aberta."""
#         if not self.connection:
#             try:
#                 conn_str = (
#                     f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};"
#                     f"UID={self.username};PWD={self.password};Connection Timeout=60;"
#                 )
#                 self.connection = pyodbc.connect(conn_str)
#             except Exception as e:
#                 print(f"Erro ao conectar ao banco de dados: {e}")
#                 raise e

#     def close(self):
#         """Fecha a conexão com o banco de dados, se estiver aberta."""
#         if self.connection:
#             self.connection.close()
#             self.connection = None

#     def get_cursor(self):
#         """Retorna o cursor para a conexão ativa."""
#         if not self.connection:
#             self.connect()
#         return self.connection.cursor()


# class PublishRepository:
#     def __init__(self, db_connection: LCDatabaseConnection, table_name: str):
#         """Inicializa o repositório com a conexão do banco de dados e o nome da tabela."""
#         self.db_connection = db_connection
#         self.table_name = table_name

#     def get_publish_from_LC(self, publish_id: str):
#         """Consulta dados na tabela configurada por ID."""
#         try:
#             cursor = self.db_connection.get_cursor()
#             query = f"SELECT * FROM [dbo].[{self.table_name}] WHERE [pcml_Id] = ?"
#             cursor.execute(query, (str(publish_id),))
#             result = cursor.fetchall()
#             if result:
#                 return ProcessModel(
#                     id=result[0][0],
#                     sentence=result[0][4]
#                 )
#             return None
#         except Exception as e:
#             print(f"Erro na consulta: {e}")
#             return None






