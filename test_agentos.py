from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv

load_dotenv()

agent_storage: str = "tmp/agents.db"

web_agent = Agent(
    name="Web Agent",
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[DuckDuckGoTools()],
    instructions=["You are a helpful AI assistant that can help with web search and information gathering."],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[YFinanceTools()],
    instructions=["Always use tables to display data"],
    db=SqliteDb(db_file=agent_storage),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

agent_os = AgentOS(agents=[web_agent, finance_agent])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve("test_agentos:app", reload=True)
