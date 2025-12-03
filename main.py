# main.py (Aggiornamento per test avanzato)
import os
from agent import get_peek_agent

def create_labyrinth():
    """Crea una struttura annidata per confondere l'agente standard."""
    base_dir = "messy_project"
    nested_dir = os.path.join(base_dir, "src", "config", "legacy")
    os.makedirs(nested_dir, exist_ok=True)
    
    # 1. Creiamo dei file "esca" nella root
    with open(os.path.join(base_dir, "README.md"), "w") as f:
        f.write("Questo è un progetto legacy. La configurazione è altrove.")
        
    # 2. Creiamo un file enorme inutile per tentare l'agente a leggerlo
    with open(os.path.join(base_dir, "big_log.log"), "w") as f:
        f.write("Log line...\n" * 10000)
        
    # 3. Nascondiamo il tesoro in profondità
    secret_file = os.path.join(nested_dir, ".env.production")
    with open(secret_file, "w") as f:
        f.write("# Configurazione nascosta\n")
        f.write("DB_HOST=192.168.1.1\n")
        f.write("STRIPE_API_KEY=sk_live_999999999_SUPER_SECRET\n") # IL BERSAGLIO
        f.write("DEBUG=False\n")
        
    print(f" -> Labirinto creato in '{nested_dir}'.")
    return base_dir

def main():
    target_dir = create_labyrinth()
    
    print("--- AVVIO AGENTE PEEK-A-BOO (Deep Search Mode) ---")
    
    try:
        agent = get_peek_agent()
        
        # Missione più difficile: non gli diciamo DOVE è il file.
        mission = f"""
        Esplora la cartella '{target_dir}'. 
        Devi trovare una API KEY di Stripe (inizia con 'sk_live_').
        Attento: è nascosta in qualche sottocartella. 
        NON leggere file inutili come i log.
        """
        
        print(f"Missione: {mission}\n")
        result = agent.run(mission)
        
        print("\n" + "="*30)
        print("REPORT MISSIONE:")
        print(result)
        print("="*30)
        
    except Exception as e:
        print(f"Errore critico: {e}")

if __name__ == "__main__":
    main()