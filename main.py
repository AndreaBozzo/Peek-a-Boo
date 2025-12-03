from agent import get_peek_agent

# Creiamo un file fake per testare se non esiste
def create_dummy_data():
    import os
    if not os.path.exists("secrets.conf"):
        with open("secrets.conf", "w") as f:
            f.write("user=admin\n" * 50) # Riempitivo
            f.write("GOOGLE_SECRET_KEY=AIza-TOP-SECRET-VALUE\n")
            f.write("host=localhost\n" * 50) # Riempitivo
        print(" -> File 'secrets.conf' creato per il test.")

def main():
    # Setup dati finti per provare
    create_dummy_data()

    print("--- AVVIO AGENTE PEEK-A-BOO (Powered by Google Gemini) ---")
    
    try:
        # Ottieni l'agente configurato
        agent = get_peek_agent()
        
        # Definisci la missione
        mission = "Esplora la cartella corrente, capisci quale file contiene configurazioni e trovami la 'GOOGLE_SECRET_KEY'."
        
        print(f"Missione: {mission}\n")
        
        # Esegui
        result = agent.run(mission)
        
        print("\n" + "="*30)
        print("RISULTATO FINALE:")
        print(result)
        print("="*30)
        
    except Exception as e:
        print(f"Errore critico: {e}")

if __name__ == "__main__":
    main()