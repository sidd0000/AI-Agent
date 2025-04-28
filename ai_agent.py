# ai_agent.py
import os
from dotenv import load_dotenv

# 1) load keys
load_dotenv()
GROQ_API_KEY    = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY  = os.getenv("TAVILY_API_KEY")

if not (GROQ_API_KEY and OPENAI_API_KEY and TAVILY_API_KEY):
    raise RuntimeError(
        "Missing one of GROQ_API_KEY, OPENAI_API_KEY or TAVILY_API_KEY in environment"
    )

# 2) imports
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # choose LLM with correct key
    prov = provider.lower()
    if prov == "groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif prov == "openai":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
    else:
        raise ValueError(f"Unknown provider: {provider!r}")

    # optional search tool
    tools = []
    if allow_search:
        tools.append(
            TavilySearchResults(
                api_key=TAVILY_API_KEY,
                max_results=2
            )
        )

    # build and run agent
    agent = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )
    state = {"messages": query}
    response = agent.invoke(state)

    # extract last AIMessage.content
    messages = response.get("messages", [])
    ai_texts = [m.content for m in messages if isinstance(m, AIMessage)]
    return ai_texts[-1] if ai_texts else ""
