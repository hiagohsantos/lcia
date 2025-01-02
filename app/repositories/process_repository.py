import pyodbc
from app.models.process_model import ProcessModel


class ProcessRepository:
    @staticmethod
    def get_by_id(process_id: str):
        try: 
            conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.95.201.18;DATABASE=lcr_LegalControl_Vigna_atc;UID=LCVigna;PWD=2016@Vigna;Connection Timeout=60;"
            connection = pyodbc.connect(conn_str)

            cursor_process = connection.cursor()

            cursor_process.execute("SELECT * FROM [dbo].[lcr_AI_PublicationMachineLearning] WHERE [pcml_Id] = ?", (str(process_id),))
            result_process = cursor_process.fetchall()
       
            connection.close()
            
            if result_process:
                return ProcessModel(
                    id=result_process[0][0],
                    sentence=result_process[0][4]
                    )

        except Exception as e:
            print(e)
            return None
