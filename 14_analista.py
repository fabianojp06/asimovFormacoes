from agno.agent import Agent
from agno.tools.yfinance import YFinanceTools
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
#from agno.memory.user import UserMemory


from dotenv import load_dotenv
load_dotenv()

db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    name="Analista de Finanças",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[YFinanceTools()],
    instructions="Você é um analista e tem vários clientes. Lembre-se de cada cliente, suas informações e preferências",
    db=db,
    add_history_to_context=True,
    enable_user_memories=True,
    add_memories_to_context=True,
    enable_agentic_memory=True,
    num_history_runs=3    
)


#agent.print_response("Ola, prefiro as respostas em formato de tabelas, gosto de poucas informacoes.", session_id="petrobras_session_1", user_id="analista_petrobras")
#agent.print_response("Ola, prefiro as respostas em formato de texto, gosto de bastante detalhes.", session_id="vale_session_1", user_id="analista_vale")

agent.print_response("Qual é a cotação da petrobras?", session_id="petrobras_session_2", user_id="analista_petrobras")
agent.print_response("Qual é a cotação da vale?", session_id="vale_session_2", user_id="analista_vale")