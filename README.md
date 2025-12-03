# Peek-a-Boo Agent

Agente AI minimalista che estrae informazioni da file usando operazioni chirurgiche per minimizzare l'uso di token.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install datapizza-ai datapizza-ai-clients-google python-dotenv
```

## Configurazione

Crea un file `.env` con la tua API key di Google:

```
GOOGLE_API_KEY=your_api_key_here
```

## Utilizzo

```bash
python3 main.py
```

## Filosofia

L'agente segue il principio del "risparmio di token":
1. **ListFiles** → Si orienta nella directory
2. **ReadPreview** → Capisce la struttura dei file (prime/ultime 5 righe)
3. **GrepSearch** → Estrae informazioni specifiche senza leggere file interi

## Struttura

- `agent.py` - Configurazione agente con Google Gemini
- `tools.py` - Tool personalizzati (ListFiles, ReadPreview, GrepSearch)
- `main.py` - Entry point dell'applicazione
