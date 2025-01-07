from flask import current_app as app
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any



class PineconeService:
    """
    Classe responsável por gerenciar operações com o Pinecone, como criar índices e inserir vetores.

    Métodos principais:
    -------------------
    1. criar_indice: Cria um índice no Pinecone.
    2. inserir_vetores: Insere vetores em um índice existente.
    """

    def __init__(self) -> None:
        """
        Inicializa a conexão com o Pinecone.

        Exceções:
        ---------
        ValueError
            Lançada se a chave da API do Pinecone não for encontrada nas variáveis de ambiente.
        """
        self.pinecone_key = app.config['PINECONE_API_KEY']
        self.cliente = Pinecone(api_key=self.pinecone_key)

    def criar_indice(self, nome_indice: str, dimensao: int, metadados_config: Dict[str, Any] = None) -> None:
        """
        Cria um índice no Pinecone.

        Parâmetros:
        -----------
        nome_indice : str
            Nome do índice a ser criado.
        dimensao : int
            Dimensão dos vetores que serão armazenados no índice.
        metadados_config : Dict[str, Any], opcional
            Configurações adicionais para o índice, como chaves de metadados.

        Exceções:
        ---------
        ValueError
            Lançada se o índice já existir.
        """
        if nome_indice in self.cliente.list_indexes().names():
            raise ValueError(f"O índice '{nome_indice}' já existe no Pinecone.")

        self.cliente.create_index(
            name=nome_indice,
            dimension=dimensao,
            metric='cosine', 
            spec=ServerlessSpec(cloud='aws', region='us-east-1') 
        )
        print(f"Índice '{nome_indice}' criado com sucesso.")


    def inserir_vetores(self, nome_indice: str, vetores: List[Dict[str, Any]]) -> None:
        """
        Insere vetores em um índice existente, com metadados para facilitar buscas.

        Parâmetros:
        -----------
        nome_indice : str
            Nome do índice onde os vetores serão inseridos.
        vetores : List[Dict[str, Any]]
            Lista de vetores a serem inseridos no índice. Cada vetor deve ser um dicionário
            com as chaves:
            - "id": Identificador único do vetor.
            - "values": Vetor de valores numéricos (float).
            - "metadata": Metadados adicionais associados ao vetor (opcional).
        """
        if nome_indice not in self.cliente.list_indexes().names():
            raise ValueError(f"O índice '{nome_indice}' não existe no Pinecone.")

        indice = self.cliente.Index(nome_indice)

        for vetor in vetores:
            vetor.setdefault("metadata", {})["tag"] = "all_vectors"

        vetores_formatados = [
            (vetor["id"], vetor["values"], vetor["metadata"])
            for vetor in vetores
        ]

        indice.upsert(vectors=vetores_formatados)
        print(f"Vetores inseridos com sucesso no índice '{nome_indice}'.")

    def buscar_por_similaridade(
        self, 
        nome_indice: str, 
        vetor_consulta: List[float], 
        top_k: int = 10, 
        incluir_valores: bool = False, 
        incluir_metadados: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Realiza uma busca por similaridade em um índice com base em um vetor de consulta.

        Parâmetros:
        -----------
        nome_indice : str
            Nome do índice onde a busca será realizada.
        vetor_consulta : List[float]
            Vetor de consulta para a busca por similaridade.
        top_k : int, opcional
            Número de resultados a serem retornados (padrão: 10).
        incluir_valores : bool, opcional
            Se True, inclui os valores dos vetores nos resultados (padrão: False).
        incluir_metadados : bool, opcional
            Se True, inclui os metadados dos vetores nos resultados (padrão: False).

        Retorna:
        --------
        List[Dict[str, Any]]
            Lista de resultados, onde cada resultado contém o ID, score e outras informações.
        """
        if nome_indice not in self.cliente.list_indexes().names():
            raise ValueError(f"O índice '{nome_indice}' não existe no Pinecone.")

        indice = self.cliente.Index(nome_indice)

        resposta = indice.query(
            namespace="",
            vector=vetor_consulta,
            top_k=top_k,
            include_values=incluir_valores,
            include_metadata=incluir_metadados
        )

        return resposta["matches"]
    

if __name__ == '__main__':
    gerenciador = PineconeService()