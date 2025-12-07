# main.py - Test suite Peek-a-Boo
import os
import shutil
from agent import get_peek_agent


def create_labyrinth(base_dir: str = "messy_project"):
    """Crea struttura complessa per test."""
    # Pulisci se esiste
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)

    # Struttura directory
    dirs = [
        f"{base_dir}/src/config/legacy",
        f"{base_dir}/src/utils",
        f"{base_dir}/logs",
        f"{base_dir}/tests",
        f"{base_dir}/docs",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    # 1. File esca nella root
    with open(f"{base_dir}/README.md", "w") as f:
        f.write("# Progetto Legacy\n\nLa configurazione è altrove.\n")

    # 2. File log ENORME (trappola token)
    with open(f"{base_dir}/logs/app.log", "w") as f:
        for i in range(10000):
            f.write(f"[2024-01-{i%28+1:02d}] INFO: Processing request #{i}\n")

    # 3. Segreto nascosto in profondità
    with open(f"{base_dir}/src/config/legacy/.env.production", "w") as f:
        f.write("# Configurazione produzione\n")
        f.write("DB_HOST=192.168.1.1\n")
        f.write("DB_PASSWORD=super_secret_db_pass\n")
        f.write("STRIPE_API_KEY=sk_live_999999999_SUPER_SECRET\n")
        f.write("AWS_SECRET_KEY=AKIAIOSFODNN7EXAMPLE\n")
        f.write("DEBUG=False\n")

    # 4. Codice Python con TODO
    with open(f"{base_dir}/src/utils/helpers.py", "w") as f:
        f.write('''"""Utility functions."""

def calculate_total(items):
    # TODO: Aggiungere validazione input
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total

def format_currency(amount):
    # TODO: Supportare valute multiple
    return f"€{amount:.2f}"

def send_notification(user, message):
    # FIXME: Il rate limiting non funziona
    print(f"Sending to {user}: {message}")
    # TODO: Implementare retry logic
''')

    # 5. File di test con errori
    with open(f"{base_dir}/tests/test_helpers.py", "w") as f:
        f.write('''import pytest
from src.utils.helpers import calculate_total

def test_calculate_total():
    # TODO: Aggiungere più test case
    pass

def test_format_currency():
    # FIXME: Test fallisce con numeri negativi
    pass
''')

    # 6. Config JSON
    with open(f"{base_dir}/src/config/settings.json", "w") as f:
        f.write('''{
    "app_name": "MyApp",
    "version": "1.0.0",
    "api_endpoint": "https://api.example.com/v1",
    "max_retries": 3,
    "timeout": 30
}
''')

    # 7. Altro file log
    with open(f"{base_dir}/logs/error.log", "w") as f:
        for i in range(5000):
            if i % 100 == 0:
                f.write(f"[ERROR] Connection timeout at {i}\n")
            else:
                f.write(f"[DEBUG] Request processed\n")

    print(f"✓ Labirinto creato in '{base_dir}'")
    return base_dir


# --- MISSIONI DI TEST ---

MISSIONS = [
    {
        "name": "🔑 Trova Stripe API Key",
        "prompt": """Esplora 'messy_project'.
Trova la API KEY di Stripe (inizia con 'sk_live_').
NON leggere file di log.""",
    },
    {
        "name": "📝 Trova tutti i TODO",
        "prompt": """Cerca tutti i TODO e FIXME nel codice Python di 'messy_project'.
Riporta file e riga di ogni occorrenza.""",
    },
    {
        "name": "⚙️ Trova endpoint API",
        "prompt": """Trova l'endpoint API configurato nel progetto 'messy_project'.
Cerca nei file di configurazione (json, env, yaml).""",
    },
    {
        "name": "🔐 Trova tutte le credenziali",
        "prompt": """Esplora 'messy_project' e trova TUTTE le credenziali/secret:
- API keys
- Password
- Access keys
NON leggere i log.""",
    },
]


def run_mission(agent, mission: dict):
    """Esegue una singola missione."""
    print(f"\n{'='*60}")
    print(f"MISSIONE: {mission['name']}")
    print(f"{'='*60}")
    print(f"Prompt: {mission['prompt'][:100]}...")

    try:
        result = agent.run(mission["prompt"])
        print(f"\n✓ Missione completata")
        return True
    except Exception as e:
        print(f"\n✗ Errore: {e}")
        return False


def main():
    """Entry point principale."""
    print("🎭 PEEK-A-BOO - Test Suite\n")

    # Setup
    base_dir = create_labyrinth()

    try:
        agent = get_peek_agent()

        # Scegli quale missione eseguire (o eseguile tutte)
        print("\nMissioni disponibili:")
        for i, m in enumerate(MISSIONS):
            print(f"  {i+1}. {m['name']}")
        print(f"  0. Esegui TUTTE le missioni")

        choice = input("\nScegli missione (0-4) [default: 1]: ").strip() or "1"

        if choice == "0":
            # Esegui tutte
            for mission in MISSIONS:
                run_mission(agent, mission)
        else:
            # Esegui singola
            idx = int(choice) - 1
            if 0 <= idx < len(MISSIONS):
                run_mission(agent, MISSIONS[idx])
            else:
                print("Scelta non valida")
                return

        print("\n" + "="*60)
        print("✅ Test completato")
        print("="*60)

    except Exception as e:
        print(f"❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
