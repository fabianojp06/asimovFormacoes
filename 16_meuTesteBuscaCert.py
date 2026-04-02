import os

from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb


from agno.vectordb.chroma import ChromaDb
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking
from agno.knowledge.embedder.openai import OpenAIEmbedder


from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agents.db")

# Banco de dados vectorial para armazenar os documentos
vector_db = ChromaDb(
    collection="funcionario_cert",
    path="tmp/chroma",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    persistent_client=True,
)

# Base de conhecimento para o agente
knowledge = Knowledge(
     vector_db=vector_db
   )

# Adiciona o conteúdo do documento ao banco de dados vectorial
knowledge.add_content(
    path="filess",
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "funcionario",
        "industry": "certificados",
        "country": "Brasil",
         },
         skip_if_exists=True # Se o documento já existe, não adiciona novamente
)

#knowledge.add_content(
#    path="files/VALE",
#    reader=PDFReader(
#        chunking_strategy=SemanticChunking()
#    ),
#    metadata={
#        "company": "Vale",
#        "industry": "Mineração",
#        "country": "Brasil",
#         },
#         skip_if_exists=True # Se o documento já existe, não adiciona novamente
#)   


agent = Agent(
    name="busca_certificado",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[YFinanceTools()],
    instructions="Voce é um analista de certificados de tecnologia da informação. Lembre-se de cada funcionario, suas informações e preferências.",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    enable_user_memories=True,
    add_memories_to_context=True,
    enable_agentic_memory=True,
    knowledge=knowledge,
    add_knowledge_to_context=True
)

# agent.print_response("Ola, prefiro as respostas em formato de tabelas, gosto de poucas informacoes.", session_id="petrobras_session_1", user_id="analista_petrobras")
# agent.print_response("Ola, prefiro as respostas em formato de texto, gosto de bastante detalhes.", session_id="vale_session_1", user_id="analista_vale")

# agent.print_response("Qual é a cotação da petrobras?", session_id="petrobras_session_2", user_id="analista_petrobras")
# agent.print_response("Qual é a cotação da vale?", session_id="vale_session_2", user_id="analista_vale")

#agent.print_response("Ola, qual foi o lucro liquido da petrobras em 2T25?", session_id="petrobras_session_4", user_id="analista_petrobras")
#agent.print_response("Ola, o que foi comentado sobre o CAPEX da vale no 2T25?", session_id="vale_session_4", user_id="analista_vale")

agent.print_response("Olá quais funcionarios têm certificação de PO, peciso da data de validade da certificação?", session_id="RH_01", user_id="analista_Ingrid")
agent.print_response("quantos funcionario temos cadastrados?", session_id="RH_01", user_id="analista_Ingrid")
