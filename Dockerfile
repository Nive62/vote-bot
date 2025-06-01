FROM node:20-slim

# Installer Chromium
RUN apt-get update && apt-get install -y chromium

# Définir la variable d'environnement pour Puppeteer (non obligatoire avec puppeteer >=20)
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Dossier de travail
WORKDIR /app

# Copie des fichiers
COPY package.json ./
RUN npm install

COPY index.js ./

# Lancement du bot
CMD ["npm", "start"]
