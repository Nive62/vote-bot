const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
const PORT = process.env.PORT || 8080;

let lastVoteTime = null;

app.get('/', (req, res) => {
  res.send('✅ Vote bot actif');
});

app.get('/last-vote', (req, res) => {
  res.json({
    lastVote: lastVoteTime ? lastVoteTime.toISOString() : 'Aucun vote effectué pour le moment'
  });
});

app.get('/force', async (req, res) => {
  await voter();
  res.send('✅ Vote forcé à ' + new Date().toLocaleString());
});

app.listen(PORT, () => {
  console.log(`🌐 Serveur en ligne sur le port ${PORT}`);
});

async function voter() {
  try {
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.goto('https://moncube.eu/vote/', { waitUntil: 'networkidle2' });
    await page.type('#pseudo', 'Bapt62');
    await page.click('#submit-button');

    lastVoteTime = new Date();
    console.log(`✅ Vote envoyé à ${lastVoteTime.toLocaleString()}`);

    await new Promise(resolve => setTimeout(resolve, 3000));
    await browser.close();
  } catch (err) {
    console.error('❌ Erreur pendant le vote :', err);
  }
}

voter();
setInterval(voter, 61 * 60 * 1000);
