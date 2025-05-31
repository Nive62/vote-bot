const express = require('express');
const puppeteer = require('puppeteer');

const app = express();

app.get('/', (req, res) => {
  res.send('Vote bot actif ✅');
});

const PORT = process.env.PORT || 3000;
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
    console.log(`✅ Vote envoyé à ${new Date().toLocaleString()}`);
    await page.waitForTimeout(3000);
    await browser.close();
  } catch (err) {
    console.error('❌ Erreur pendant le vote :', err);
  }
}

voter();
setInterval(voter, 61 * 60 * 1000);