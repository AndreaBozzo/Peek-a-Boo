<div align="center">
  <img src="docs/assets/images/logo.png" alt="Peek-a-Boo Logo" width="300"/>

  # Peek-a-Boo Agent

  Agente AI minimalista che estrae informazioni da file usando operazioni chirurgiche per minimizzare l'uso di token.
</div>

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

Il test suite offre 4 missioni:
1. **Trova Stripe API Key** - Cerca credenziali nascoste
2. **Trova TODO/FIXME** - Code review automatica
3. **Trova endpoint API** - Discovery configurazioni
4. **Trova tutte le credenziali** - Security audit

## Filosofia

L'agente segue il principio del "risparmio di token" - NON legge mai file interi se non strettamente necessario.

### Tool Disponibili

| Tool | Funzione | Use Case |
|------|----------|----------|
| **ListFiles** | Elenca file in una directory (non ricorsivo) | Orientamento iniziale |
| **FindFiles** | Cerca file per glob pattern (`*.env`, `*secret*`) ricorsivamente | Trovare tipi di file specifici |
| **ReadPreview** | Mostra prime 5 + ultime 5 righe | Capire struttura file |
| **GrepSearch** | Cerca keyword in UN file con contesto | Estrazione chirurgica |
| **GrepRecursive** | Cerca keyword in TUTTI i file di una directory | Ricerca globale |

### Strategia Chirurgica

```
Se cerchi un TIPO di file    → FindFiles con pattern
Se cerchi una KEYWORD nota   → GrepSearch su file specifico
Se cerchi una KEYWORD ignota → GrepRecursive su directory
```

### Supporto Regex

Tutti i tool di ricerca supportano regex con `use_regex=True`:
```python
GrepRecursive(directory=".", keyword="sk_live_[0-9]+", use_regex=True)
```

## Struttura Progetto

```
Peek-a-Boo/
├── agent.py      # Configurazione agente + system prompt
├── tools.py      # 5 tool chirurgici
├── main.py       # Test suite con 4 missioni
├── .env          # API key (da creare)
└── messy_project/  # Directory di test (generata automaticamente)
```

## Limiti di Sicurezza

I tool hanno limiti integrati per evitare esplosioni di token:
- **ListFiles**: max 30 entry
- **FindFiles**: max 20 risultati
- **ReadPreview**: max 50MB per file
- **GrepSearch**: max 3 match per file
- **GrepRecursive**: max 10 file, max 5 match totali

Directory ignorate automaticamente: `.git`, `node_modules`, `__pycache__`, `venv`, `.idea`, `.vscode`
