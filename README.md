# Création d'Images Docker et Audit de Vulnérabilités
Ce document décrit les étapes pour créer trois images Docker différentes et les auditer pour les vulnérabilités en utilisant Docker Scout.


## 1. Image avec `curl`
Cette image installe `curl` et exécute `curl google.com` lors de son lancement.

**Construire l'image :**
```bash
# Construire l'image :
docker build -t curl-image -f Dockerfile.curl .
```

**Lancer le conteneur :**
```bash
# Lancer le conteneur :
docker run --rm curl-image
```


## 2. Image Servant du HTML Statique
Cette image utilise Nginx pour servir une simple page HTML statique.

**Construire l'image :**
```bash
# Construire l'image :
docker build -t static-html-image -f Dockerfile.nginx .
```

**Lancer le conteneur :**
```bash
# S'exécute en mode détaché, mappe le port hôte 8080 au port 80 du conteneur
docker run --rm -d -p 8080:80 static-html-image
```
*Accédez à la page via `http://localhost:8080` dans votre navigateur.*


## 3. Image avec un Serveur Web Python Basique
Cette image exécute un serveur web simple écrit en Python en utilisant le module intégré `http.server`.

**Construire l'image :**
```bash
# Créez d'abord le fichier factice web/index.html en exécutant server.py localement une fois
# ou créez manuellement le répertoire web et un fichier index.html à l'intérieur.
# Puis construisez :
docker build -t python-server -f Dockerfile.python .
```

**Lancer le conteneur :**
```bash
# S'exécute en mode détaché, mappe le port hôte 8001 au port 8000 du conteneur
docker run --rm -d -p 8001:8000 python-server
```
*Accédez au serveur via `http://localhost:8001` dans votre navigateur.*


## 4. Audit des Vulnérabilités avec Docker Scout
Docker Scout aide à identifier les Vulnérabilités et Expositions Communes (CVEs) dans vos images Docker.

**Auditer une image (ex: l'image du serveur Python) :**
```bash
# Assurez-vous que l'image est construite, par ex., python-server
docker scout cves python-server
```

**Corriger les Vulnérabilités (Exemple : `python-server`) :**

1.  **Exécuter l'audit :** `docker scout cves python-server`
2.  **Reconstruire :** `docker build -t python-server -f Dockerfile.python .`
3.  **Ré-auditer :** `docker scout cves python-server`. Comparez les résultats.


## 5. Communication entre Conteneurs via un Réseau Personnalisé
Docker permet de créer des réseaux personnalisés pour isoler et permettre la communication entre les conteneurs par leur nom.

**1. Créer un réseau Docker personnalisé :**
```bash
# Crée un réseau de type bridge nommé 'mon-reseau'
docker network create mon-reseau

# Lancer le premier conteneur
docker run -d --rm --name container1 --network mon-reseau alpine sleep infinity

# Lancer le second conteneur
docker run -d --rm --name container2 --network mon-reseau alpine sleep infinity

# Exécuter 'ping container2' depuis 'container1'
docker exec container1 ping -c 4 container2

# Arrêter les conteneurs
docker stop container1 container2

# Supprimer le réseau (les conteneurs doivent être arrêtés ou déconnectés d'abord)
docker network rm mon-reseau
```


## 6. Utilisation de Docker Compose pour Base de Données et Application
Docker Compose simplifie la gestion d'applications multi-conteneurs. Cet exemple lance un service de base de données PostgreSQL (`db`) et une application Python (`app`) qui vérifie la connexion à la base de données.

**Fichiers requis :**

*   `docker-compose.yml` : Définit les services, réseaux, volumes, variables d'environnement et health check.
*   `check_db.py` : Script Python pour l'application `app` qui tente de se connecter à la BDD.
*   `requirements.txt` : Liste les dépendances Python (ex: `psycopg2-binary`).
*   `Dockerfile.app` : Instructions pour construire l'image Docker de l'application `app`.

**Lancer les services :**

```bash
# Construit les images (si nécessaire) et démarre les conteneurs en arrière-plan
docker-compose up -d

# Afficher les logs du conteneur 'app'
docker-compose logs app

# Afficher les logs du conteneur 'db'
docker-compose logs db

# Arrête et supprime les conteneurs, réseaux et volumes définis dans le compose file
docker-compose down -v
```


## 7. Exemple Complet avec Docker Compose (DB, Backend, Frontend)
Cet exemple montre comment conteneuriser une application web complète avec une base de données PostgreSQL, une API backend Node.js/Express, et une interface frontend React.

**Lancer l'Application Complète :**

```bash
# Se placer dans le répertoire Boss_Final/
cd c:\Users\joris\mars-rover\Docker\Boss_Final

# Construire les images et démarrer tous les services en arrière-plan
docker-compose up -d --build