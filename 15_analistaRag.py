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
from agno.utils.log import set_log_level_to_debug

load_dotenv()
# Mostra mensagens DEBUG do Agno durante indexação (PDF → chunks → embeddings → Chroma)
set_log_level_to_debug(level=2)

db = SqliteDb(db_file="tmp/agents.db")

# Banco de dados vectorial para armazenar os documentos
vector_db = ChromaDb(
    collection="empresas_relatios",
    path="tmp/chroma",
    embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    persistent_client=True,
)

# Base de conhecimento para o agente
knowledge = Knowledge(
     vector_db=vector_db
   )

# Adiciona o conteúdo do documento ao banco de dados vectorial
print("Iniciando PETR (indexação files/PETR)...", flush=True)
knowledge.add_content(
    path="files/PETR",
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Pedtrobras",
        "industry": "Petróleo e Gás",
        "country": "Brasil",
         },
         skip_if_exists=True # Se o documento já existe, não adiciona novamente
)
print("PETR ok.", flush=True)

print("Iniciando VALE (indexação files/VALE)...", flush=True)
knowledge.add_content(
    path="files/VALE",
    reader=PDFReader(
        chunking_strategy=SemanticChunking()
    ),
    metadata={
        "company": "Vale",
        "industry": "Mineração",
        "country": "Brasil",
         },
         skip_if_exists=True # Se o documento já existe, não adiciona novamente
)
print("VALE ok.", flush=True)


agent = Agent(
    name="analista_financeiro",
    model=OpenAIChat(id="gpt-5-nano", api_key=os.getenv("OPENAI_API_KEY")),
    tools=[YFinanceTools()],
    instructions="Voce é um analista e tem diferentes clientes. Lembre-se de cada cliente, suas informações e preferências.",
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

agent.print_response("Ola, qual foi o lucro liquido da petrobras em 2T25?", session_id="petrobras_session_4", user_id="analista_petrobras")
agent.print_response("Ola, o que foi comentado sobre o CAPEX da vale no 2T25?", session_id="vale_session_4", user_id="analista_vale")
