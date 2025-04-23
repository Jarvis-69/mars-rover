import os
import time
import sys
import psycopg2 # Bibliothèque pour se connecter à PostgreSQL

def check_db_connection():
    """Tente de se connecter à la base de données en utilisant les variables d'environnement."""
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT", 5432) # Port par défaut si non défini
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")

    if not all([db_host, db_name, db_user, db_password]):
        print("Erreur: Toutes les variables d'environnement DB_* ne sont pas définies.", file=sys.stderr)
        return False

    conn_string = f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_password}' port='{db_port}'"
    print(f"Tentative de connexion à la base de données sur {db_host}:{db_port}...")

    retries = 5
    delay = 3
    for i in range(retries):
        try:
            conn = psycopg2.connect(conn_string)
            print("Connexion à la base de données réussie !")
            conn.close()
            return True
        except psycopg2.OperationalError as e:
            print(f"Échec de la connexion (essai {i+1}/{retries}): {e}", file=sys.stderr)
            if i < retries - 1:
                print(f"Nouvelle tentative dans {delay} secondes...")
                time.sleep(delay)
            else:
                print("Nombre maximum de tentatives atteint.", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Erreur inattendue lors de la connexion: {e}", file=sys.stderr)
            return False

if __name__ == "__main__":
    if check_db_connection():
        print("Le conteneur 'app' a vérifié avec succès la connexion à la base de données.")
        # Garder le conteneur en vie pour l'exemple (ou faire autre chose)
        # time.sleep(3600)
    else:
        print("Impossible d'établir la connexion à la base de données.", file=sys.stderr)
        sys.exit(1) # Sortir avec un code d'erreur si la connexion échoue