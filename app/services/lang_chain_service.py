from typing import List, Dict, Any
from app.services.groq_service import GroqClient
from langchain_openai.embeddings import OpenAIEmbeddings
#from pinecone_ import GerenciadorPinecone

from app.services.pinecone_service import PineconeService


class AplicacaoGerenciamento:
    """
    Classe responsável por gerenciar a integração entre Pinecone, GPT e o carregamento de dados,
    permitindo a inserção e busca de embeddings e a utilização do GPT para processar os dados.

    Métodos principais:
    -------------------
    1. carregar_pedidos: Carrega os dados dos pedidos e retorna uma lista contendo os nomes dos pedidos.
    2. gerar_embeddings: Gera embeddings para uma lista de textos e formata os vetores para inserção no Pinecone.
    3. inserir_embeddings_no_pinecone: Insere os embeddings gerados para os textos fornecidos no índice especificado no Pinecone, em lotes.
    4. buscar_embedding_proximo: Realiza uma busca no índice Pinecone para encontrar os embeddings mais similares.
    5. enviar_prompt: Envia um prompt ao GPT-4, utilizando embeddings baseados no dataframe de pedidos.

    Exemplos de uso:
    ---------------
    >>> aplicacao = AplicacaoGerenciamento()
    >>> pedidos = aplicacao.carregar_pedidos()
    >>> embeddings = aplicacao.gerar_embeddings(pedidos)
    >>> aplicacao.inserir_embeddings_no_pinecone("pedidos", pedidos)
    >>> resultado = aplicacao.buscar_embedding_proximo("pedidos", embeddings[0])
    >>> resposta = aplicacao.enviar_prompt("Qual é o pedido?", documento="Petição Inicial")

    Atributos:
    ----------
    data : Data
        Instância da classe Data para carregar os dados dos pedidos.
    gerenciador_pinecone : GerenciadorPinecone
        Instância da classe GerenciadorPinecone para gerenciar operações com o Pinecone.
    cliente_gpt : ClienteGPT
        Instância da classe ClienteGPT para interagir com a API do OpenAI GPT-4.
    embeddings_model : OpenAIEmbeddings
        Instância da classe OpenAIEmbeddings para gerar embeddings de textos.

    """

    def __init__(self):
        """
        Inicializa as instâncias necessárias para o funcionamento da aplicação, incluindo
        o gerenciador de dados, Pinecone, GPT e modelos de embeddings.

        Atributos:
        ----------
        data : Data

            Instância da classe Data para carregar os dados dos pedidos.
        gerenciador_pinecone : GerenciadorPinecone

            Instância da classe GerenciadorPinecone para gerenciar operações com o Pinecone.
        cliente_gpt : ClienteGPT

        embeddings_model : OpenAIEmbeddings
            Instância da classe OpenAIEmbeddings para gerar embeddings de text
        """

        self.client = GroqClient()
        self.embeddings_model = OpenAIEmbeddings()
        self.pinecone_service = PineconeService()

    
    def gerar_embeddings(self, textos: List[str]) -> List[Dict[str, Any]]:
        """
        Gera embeddings para uma lista de textos e formata os vetores para inserção no Pinecone.

        Parâmetros:
        -----------
        textos : List[str]
            Lista de textos para os quais serão gerados os embeddings.

        Retorna:
        --------
        List[Dict[str, Any]]
            Uma lista de dicionários formatados contendo os vetores, IDs e metadados.
        """
        embeddings = self.embeddings_model.embed_documents(textos)
        return [
            {"id": str(i), "values": vetor, "metadata": {}}
            for i, vetor in enumerate(embeddings)
        ]

    def inserir_embeddings_no_pinecone(self, nome_indice: str, textos: List[str], batch_size: int = 100) -> None:
        """
        Insere os embeddings gerados para os textos fornecidos no índice especificado no Pinecone, em lotes.

        Parâmetros:
        -----------
        nome_indice : str
            Nome do índice onde os vetores serão inseridos.
        textos : List[str]
            Lista de textos para os quais serão gerados e inseridos os embeddings.
        batch_size : int, opcional
            Número de vetores a serem inseridos por lote. Padrão é 100.
        """
        vetores = self.gerar_embeddings(textos)

        for i in range(0, len(vetores), batch_size):
            lote = vetores[i:i + batch_size]
            try:
                self.pinecone_service.inserir_vetores(nome_indice, lote)
                print(f"Lote de vetores {i}-{i+len(lote)} inserido com sucesso.")
            except Exception as e:
                print(f"Erro ao inserir o lote {i}-{i+len(lote)}: {e}")



    def buscar_embedding_proximo(self, nome_indice: str, vetor_consulta: List[float], k: int = 1) -> List[str]:
        """
        Realiza uma busca no índice Pinecone para encontrar os embeddings mais similares.

        Parâmetros:
        -----------
        nome_indice : str
            Nome do índice onde a busca será realizada.
        vetor_consulta : List[float]
            Vetor de consulta para encontrar os embeddings mais similares.
        k : int, opcional
            Número de vetores mais similares a serem retornados. Padrão é 1.

        Retorna:
        --------
        List[str]
            Uma lista com os textos ou IDs associados aos embeddings mais próximos.
        """
        resultados = self.pinecone_service.buscar_por_similaridade(nome_indice, vetor_consulta, top_k=k)

        if not resultados:
            raise ValueError("Nenhum resultado encontrado no índice Pinecone.")

        return [match["id"] for match in resultados]


    def enviar_prompt(self, prompt: str, documento: str, inserir_novos_embeddings: bool = False) -> str:
        """
        Envia um prompt ao GPT-4, utilizando embeddings baseados no dataframe de pedidos.

        Parâmetros:
        -----------
        prompt : str
            O texto de entrada que será enviado ao GPT-4.
        documento : str
            Texto do documento que será incluído no prompt.
        inserir_novos_embeddings : bool, opcional
            Indica se novos embeddings devem ser gerados e inseridos no Pinecone.

        Retorna:
        --------
        str
            Os nomes dos pedidos mais relevantes, formatados.
        """
        if inserir_novos_embeddings:
            pedidos = self.carregar_pedidos()
            self.inserir_embeddings_no_pinecone("pedidos", pedidos)

        # embedding_consulta = self.embeddings_model.embed_documents([documento])[0]
        # embedding_consulta = np.array(embedding_consulta).tolist()

        # pedidos_ids = self.buscar_embedding_proximo("pedidos", embedding_consulta, k=3)

        # pedidos = self.carregar_pedidos()
        # pedidos_dict = {str(i): pedido for i, pedido in enumerate(pedidos)}

        # pedidos_relevantes = [pedidos_dict.get(pedido_id, f"Pedido {pedido_id} não encontrado") for pedido_id in pedidos_ids]
        # pedidos_formatados = "\n".join([f"- {pedido}" for pedido in pedidos_relevantes])

        prompt_final = f"{prompt}\n\nDocumento fornecido:\n{documento}"

        system_message = "Forneça as informações no formato JSON conforme o esquema:"
        # schema = {
        #     "tipo": "resposta_formatada",
        #     "detalhes": {
        #         "relevancia": "Alta",
        #         "pedidos": "Lista de pedidos relacionados",
        #         "documento": "Texto analisado"
        #     }
        # }

        chat_completion = self.client.send_order(
            prompt=prompt_final,
            system_message=system_message,
            schema={}
                            )

        return chat_completion




if __name__ == "__main__":
    from app.services.orders_service import OrdersService
    aplicacao = AplicacaoGerenciamento()
    # texto = aplicacao.carregar_pedidos()
    # aplicacao.inserir_embeddings_no_pinecone("pedidos", texto)
    documento = OrdersService().carregar_texto_docx('copia integral-2-13.docx')

    prompt = """
    Leia atentamente o documento fornecido e extraia as seguintes informações:
    Quais os pedidos feitos pelo autor?
    Há valor especificado nos pedidos? Se sim, qual?
    Existe cobrança de juros? (Sim/Não)
    Se sim: Qual é o percentual dos juros?
    Correção Monetária: Existe menção a correção monetária? Se sim, qual o índice requerido (informar exatamente como no documento)?
    Multa: Existe previsão de multa? Se sim, qual percentual ou valor?
    Honorários: Há pedido de honorários advocatícios? Se sim, qual o valor ou percentual?
    """

    # # resposta_com_insercao = aplicacao.enviar_prompt(prompt, documento=documento, inserir_novos_embeddings=True)
    # # print("Resposta com inserção de embeddings:")
    # # print(resposta_com_insercao)

    resposta_com_busca = aplicacao.enviar_prompt(prompt, documento=documento, inserir_novos_embeddings=False)
    print("Resposta com busca de embeddings:")
    print(resposta_com_busca)