from agno.agent import Agent
#from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()


def celsius_to_fahrenheit(celsius: float) -> str:
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}C = {fahrenheit:.2f}F"
    """
    Converte graus Celsius para graus Fahrenheit.
    Args:
        celsius: float - A temperatura em graus Celsius.
    Returns:
        str - A temperatura em graus Fahrenheit.
    """



agent = Agent(
    #model=Groq(id="llama-3.3-70b-versatile"),
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        TavilyTools(),
        celsius_to_fahrenheit
        ],
    debug_mode=True,
)


agent.print_response("Qual a temperatura no Rio de Janeiro - RJ - Brasil? hoje?")