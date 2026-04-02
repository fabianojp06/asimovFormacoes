# agno-estudo

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](#pré-requisitos)
[![Agno](https://img.shields.io/badge/Framework-Agno-black)](https://docs.agno.com)
[![uv](https://img.shields.io/badge/Env-uv-7c3aed)](https://docs.astral.sh/uv/)

Estudos com [**Agno**](https://github.com/agno-agi/agno): agentes (OpenAI/Groq), ferramentas (Tavily/YFinance/DuckDuckGo), **memória** com SQLite, **RAG** com ChromaDB e **AgentOS** via ASGI/Uvicorn.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Setup](#setup)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Como rodar](#como-rodar)
- [RAG (PDFs)](#rag-pdfs)
- [AgentOS](#agentos)
- [Troubleshooting](#troubleshooting)
- [Segurança](#segurança)
- [Referências](#referências)

## Pré-requisitos

- **Python 3.12+** (ver `.python-version`)
- **uv** (recomendado)

## Setup

```bash
git clone <url-do-repositorio>
cd agno-estudo
uv sync
```

Crie o `.env` a partir do exemplo:

```bash
cp .env.example .env
```

No PowerShell (Windows):

```powershell
Copy-Item .env.example .env
```

## Variáveis de ambiente

Edite `.env` e preencha as chaves.

| Variável | Obrigatória quando | Usada em |
|----------|--------------------|----------|
| `OPENAI_API_KEY` | modelos OpenAI e embeddings | `OpenAIChat`, `OpenAIResponses`, `OpenAIEmbedder` |
| `GROQ_API_KEY` | usar Groq | `agno.models.groq.Groq` |
| `TAVILY_API_KEY` | usar Tavily | `agno.tools.tavily.TavilyTools` |

## Como rodar

Execute qualquer script com `uv run`:

```bash
uv run python 0_llm_call.py
uv run python 1.1.researcher.py
uv run python 14_analista.py
uv run python 15_analistaRag.py
```

### Scripts incluídos

| Arquivo | O que demonstra |
|---------|------------------|
| `0_llm_call.py` | chamada direta ao modelo Groq com `Message` |
| `1.1.researcher.py` | agente com `TavilyTools` + Groq |
| `1.3.own_tools.py` | tool customizada (ex.: conversão °C → °F) |
| `14_analista.py` | analista com YFinance + memória/histórico (SQLite) |
| `15_analistaRag.py` | RAG com PDFs + ChromaDB (`tmp/chroma`) |
| `16_meuTesteBuscaCert.py` | variação de teste para busca/RAG |
| `test_agentos.py` | AgentOS (ASGI) com múltiplos agentes |

## RAG (PDFs)

O `15_analistaRag.py` indexa PDFs a partir de pastas locais:

- Petrobras: `files/PETR/`
- Vale: `files/VALE/`

Notas:

- Os PDFs **não** são versionados: `files/**/*.pdf` está no `.gitignore`.
- O índice do Chroma fica em `tmp/chroma/` (também ignorado).
- Se você adicionar novos PDFs e quiser reindexar do zero, apague `tmp/chroma/` e rode novamente.

## AgentOS

O `test_agentos.py` sobe um app ASGI e chama:

- `agent_os.serve("test_agentos:app", reload=True)`

Para rodar:

```bash
uv run python test_agentos.py
```

## Troubleshooting

- **`ImportError: The 'chromadb' package is not installed`**
  - Garanta que está usando `uv` neste repo e rode `uv sync`.

- **Windows: erro ao instalar/usar `readline`**
  - Remova `readline` do script ou use alternativa compatível (ex.: `pyreadline3` com import condicional).

- **`TAVILY_API_KEY not provided`**
  - Preencha `TAVILY_API_KEY` no `.env` e use `load_dotenv()` no script.

## Segurança

- **Nunca commite `.env`** (está no `.gitignore`).
- Evite chaves hardcoded em `.py` (use `os.getenv(...)`).
- Se uma chave vazar, revogue no provedor e gere outra.

## Referências

- Agno Docs: [docs.agno.com](https://docs.agno.com)
- uv Docs: [docs.astral.sh/uv](https://docs.astral.sh/uv/)
