FROM node:20-slim

RUN apt-get update && apt-get install -y chromium

ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

WORKDIR /app

COPY package.json ./
RUN npm install

COPY index.js ./

CMD ["npm", "start"]
