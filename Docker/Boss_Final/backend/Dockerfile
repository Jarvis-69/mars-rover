# filepath: c:\Users\joris\mars-rover\backend\Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code source
COPY . .

# Exposer le port que le serveur Node écoute
EXPOSE 5000

# Commande pour lancer le serveur
CMD ["node", "server.js"]