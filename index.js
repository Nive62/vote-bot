const puppeteer = require('puppeteer');

async function voter() {
  const heure = new Date().toLocaleString();
  console.log(`⏳ Démarrage du vote à ${heure}`);

  let browser;

  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setDefaultNavigationTimeout(60000); // 60s timeout

    await page.goto('https://moncube.eu/vote/', { waitUntil: 'domcontentloaded' });

    await page.type('#pseudo', 'Bapt62');
    await page.click('#submit-button');

    await new Promise(resolve => setTimeout(resolve, 3000));

    console.log(`✅ Vote envoyé à ${heure}`);
  } catch (err) {
    console.error(`❌ Erreur pendant le vote à ${heure} :`, err.message);
  } finally {
    if (browser) await browser.close();
  }
}

// Premier vote immédiat
voter();

// Puis toutes les 1h01
setInterval(voter, 61 * 60 * 1000);
