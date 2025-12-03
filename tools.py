from datapizza.tools import Tool
from datapizza.agents import Agent
from datapizza.core.clients import ClientManager

from main import search_content

# 1. Creiamo gli oggetti Tool
# Le descrizioni sono fondamentali: l'LLM le legge per capire QUANDO usarli.
tools = [
    Tool(
        name="ListFiles",
        func=fast_list_files,
        description="USALO PER PRIMO. Mostra i file nella cartella corrente. Input opzionale: directory path."
    ),
    Tool(
        name="ReadPreview",
        func=read_head_tail,
        description="Usa questo per capire la struttura di un file (CSV headers, log format) leggendo solo inizio/fine. Input: filepath."
    ),
    Tool(
        name="GrepSearch",
        func=search_content,
        description="Usa questo per trovare informazioni specifiche (password, errori, chiavi) dentro un file senza leggerlo tutto. Input: filepath, keyword."
    )
]