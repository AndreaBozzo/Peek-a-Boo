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
    1. ListFiles -> Orientati nella directory corrente.
    2. FindFiles -> Cerca file per pattern (*.env, *secret*, *.py) in tutto l'albero.
    3. ReadPreview -> Capisci la struttura dei file interessanti (head+tail).
    4. GrepSearch -> Cerca keyword in UN file specifico.
    5. GrepRecursive -> Cerca keyword in TUTTI i file di una directory.

    Strategia chirurgica:
    - Se cerchi un tipo di file (es. config): usa FindFiles con pattern.
    - Se cerchi una keyword in un file noto: usa GrepSearch.
    - Se cerchi una keyword ma non sai dove sia: usa GrepRecursive.
    - Supporto REGEX: passa use_regex=True per pattern complessi (es. "sk_live_[0-9]+").

    Esempio: "trova la Stripe API key"
    -> GrepRecursive(directory=".", keyword="sk_live_", pattern="*.env")
    NON leggere file interi!
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