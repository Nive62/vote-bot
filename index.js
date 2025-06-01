const puppeteer = require('puppeteer');

async function voter() {
  const heure = new Date().toLocaleString();
  console.log(`⏳ Démarrage du vote à ${heure}`);

  let browser;

  try {
    browser = await puppeteer.launch({
      headless: "new", // ✅ évite le warning de dépréciation
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(60000); // timeout de 60s

    await page.goto('https://moncube.eu/vote/', { waitUntil: 'domcontentloaded' });

    await page.type('#pseudo', 'Bapt62');
    await page.click('#submit-button');

    // ✅ Attendre une confirmation visible dans la page
    try {
      await page.waitForFunction(
        () => document.body.innerText.includes('Merci'),
        { timeout: 10000 }
      );
      console.log(`✅ Vote confirmé à ${heure}`);
    } catch {
      console.warn(`⚠️ Vote tenté mais pas confirmé à ${heure}`);
    }

  } catch (err) {
    console.error(`❌ Erreur pendant le vote à ${heure} :`, err.message);
  } finally {
    if (browser) await browser.close();
  }
}

// ✅ Premier vote immédiat
voter();

// ✅ Puis toutes les 1h01
setInterval(voter, 61 * 60 * 1000);

// ✅ Garde le conteneur Docker actif
setInterval(() => {}, 1 << 30);
