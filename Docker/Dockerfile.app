# Utiliser une image Python légère
FROM python:3.11-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances Python (y compris les dépendances système pour psycopg2 sur Alpine)
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    pip install --no-cache-dir -r requirements.txt

# Copier le script de vérification
COPY check_db.py .

# Commande pour exécuter le script lorsque le conteneur démarre
CMD ["python", "check_db.py"]