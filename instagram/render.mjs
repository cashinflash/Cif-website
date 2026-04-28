// Render all 12 Instagram post HTML files to 1080x1080 PNGs.
// Usage:  node render.mjs
// Outputs to ./renders/post-XX.png
import { chromium } from 'playwright';
import { mkdir, readdir } from 'fs/promises';
import { fileURLToPath, pathToFileURL } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outDir = join(__dirname, 'renders');
await mkdir(outDir, { recursive: true });

const files = (await readdir(__dirname))
  .filter(f => /^post-\d{2}-.*\.html$/.test(f))
  .sort();

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width: 1080, height: 1080 },
  deviceScaleFactor: 2,
});

for (const file of files) {
  const page = await context.newPage();
  const url = pathToFileURL(join(__dirname, file)).href;
  await page.goto(url, { waitUntil: 'networkidle' });
  // Wait for fonts to settle
  await page.evaluate(() => document.fonts.ready);
  const post = await page.locator('.post').first();
  const out = join(outDir, file.replace('.html', '.png'));
  await post.screenshot({ path: out, omitBackground: false });
  console.log('✓', file, '→', out);
  await page.close();
}

await browser.close();
console.log(`\nRendered ${files.length} posts to ${outDir}`);
