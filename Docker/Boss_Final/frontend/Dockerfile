# filepath: c:\Users\joris\mars-rover\frontend\Dockerfile
# Utiliser une image Node pour construire et servir (pour le développement)
# Pour la production, utiliser un build multi-stage avec Nginx
FROM node:18-alpine

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code source
COPY . .

# Exposer le port du serveur de développement React
EXPOSE 3000

# Commande pour lancer le serveur de développement
CMD ["npm", "start"]