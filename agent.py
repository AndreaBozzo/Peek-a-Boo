import os
from dotenv import load_dotenv
from datapizza.agents import Agent  # type: ignore
from datapizza.clients import ClientFactory  # type: ignore
from tools import peek_tools # Importiamo i tool dal file separato

# Carica variabili d'ambiente
load_dotenv()

def get_peek_agent():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Manca GOOGLE_API_KEY nel file .env")

    # 1. Prompt di Sistema "Tirchio"
    system_instruction = """
    Sei l'Agente Peek-a-Boo. Il tuo credo è il risparmio di token.
    NON leggere MAI un file intero se non strettamente necessario.

    Procedura operativa standard:
    1. ListFiles -> Orientati.
    2. ReadPreview -> Capisci la struttura dei file interessanti.
    3. GrepSearch -> Estrai l'informazione chirurgicamente.

    Se l'utente chiede "trova la password", NON fare 'read file'. Fai 'grep password'.
    """

    # 2. Configurazione Client per Google Gemini
    # Datapizza gestirà la connessione alle API Gemini
    client = ClientFactory.create(
        provider="google",
        api_key=api_key,
        model="gemini-2.0-flash-exp", # Modello veloce ed economico, perfetto per i tool
        system_prompt=system_instruction,
        temperature=0.0 # Vogliamo precisione, non creatività
    )

    # 3. Creazione Agente
    agent = Agent(
        name="Minimalist Auditor",
        client=client,
        tools=peek_tools,
        system_prompt=system_instruction
    )
    
    return agent