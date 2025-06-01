const puppeteer = require('puppeteer');

async function voter() {
  const heure = new Date().toLocaleString();
  console.log(`⏳ Démarrage du vote à ${heure}`);

  let browser;

  try {
    browser = await puppeteer.launch({
      headless: "new",
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(60000);

    await page.goto('https://moncube.eu/vote/', { waitUntil: 'domcontentloaded' });

    await page.type('#pseudo', 'Bapt62');
    await page.click('#submit-button');

    // ✅ Attente de l’apparition du message de vote validé
    await page.waitForSelector('#vote-validated', { timeout: 10000 });

    console.log(`✅ Vote confirmé à ${heure}`);
  } catch (err) {
    console.warn(`⚠️ Vote tenté mais pas confirmé à ${heure} :`, err.message);
  } finally {
    if (browser) await browser.close();
  }
}

// ✅ Premier vote immédiat
voter();

// ✅ Puis toutes les 1h01
setInterval(voter, 61 * 60 * 1000);

// ✅ Garde le conteneur actif
setInterval(() => {}, 1 << 30);
