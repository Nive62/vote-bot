
const puppeteer = require('puppeteer');

async function voter() {
  console.log("⏳ Démarrage du vote à", new Date().toLocaleTimeString());

  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();

  try {
    await page.goto('https://moncube.eu/vote/', { waitUntil: 'domcontentloaded' });

    await page.type('#pseudo', 'Bapt62');
    await page.click('#submit-button');

    // Petite attente après le clic
    await new Promise(resolve => setTimeout(resolve, 3000));

    console.log("✔️ Vote tenté à", new Date().toLocaleTimeString());
  } catch (err) {
    console.error("❌ Erreur pendant le vote :", err);
  }

  await browser.close();
}

// Premier vote immédiat
voter();

// Ensuite toutes les 1h01
setInterval(voter, 61 * 60 * 1000);
