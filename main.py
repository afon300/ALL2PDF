# main.py
from converter import *
from functions_usb import *
import time
import json

try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)
except FileNotFoundError:
    print("❌ Fichier settings.json non trouvé. Utilisation des paramètres par défaut.")
        
except json.JSONDecodeError:
    print("❌ Erreur de lecture du fichier settings.json. Vérifiez le format JSON. Utilisation des paramètres par défaut.")

if __name__ == "__main__":
    print("Programme de conversion d'images en PDF démarré.")
    print("Insérez une clé USB pour commencer le traitement.")


    while True:
        usb_path = wait_for_usb_drive(settings["timeout_usb_connection"])

        if usb_path:
            print(f"\n✅ Clé USB détectée : {usb_path}")
            print(f"Contenu de {usb_path}:")
            try:
                for item in os.listdir(usb_path):
                    print(f"  - {item}")
                
                # Appelez la fonction de traitement des fichiers sur la clé USB
                # process_files_at_root(usb_path)
                
            except Exception as e:
                print(f"❌ Erreur lors de l'accès ou du traitement de la clé USB ({usb_path}): {e}")
            

            print(f"\nTraitement de {usb_path} terminé. Veuillez retirer cette clé USB si vous avez fini.")
            print("En attente de déconnexion de la clé actuelle...")
            
            wait_for_usb_disconnection(usb_path)
            print("Clé USB déconnectée. Prêt pour la prochaine clé.")
            
        else:

            print("\n❌ Aucune clé USB détectée dans le délai imparti. Réessai...")
            time.sleep(5)