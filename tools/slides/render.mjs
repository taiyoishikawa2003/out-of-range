// node tools/slides/render.mjs <dir with *.html> : renders each to .jpg (1080x1920)
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import fs from 'fs'; import path from 'path';
const dir = process.argv[2]; const only = process.argv[3];
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox', '--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.html') && (!only || f.includes(only))).sort()) {
  await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.resolve(dir, f.replace('.html', '.jpg')), type: 'jpeg', quality: 88 });
}
await b.close();
