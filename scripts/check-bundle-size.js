// Simple bundle size check (fail CI if too large)
// Adjust thresholds as needed
import { statSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const DIST_DIR = new URL('../dist/assets', import.meta.url);

function getFiles(dirUrl) {
  const dirPath = dirUrl.pathname;
  try {
    const files = readdirSync(dirPath);
    return files.map(f => join(dirPath, f));
  } catch {
    return [];
  }
}

function main() {
  const files = getFiles(DIST_DIR);
  if (!files.length) {
    console.log('No dist/assets files to check. Skipping size gate.');
    process.exit(0);
  }

  const MAX_JS_KB = 1024; // 1 MB per chunk baseline
  let ok = true;

  for (const f of files) {
    if (!/\.js$/.test(f)) continue;
    const s = statSync(f);
    const kb = Math.round(s.size / 1024);
    if (kb > MAX_JS_KB) {
      console.error(`❌ ${f} is ${kb} KB (> ${MAX_JS_KB} KB)`);
      ok = false;
    } else {
      console.log(`✅ ${f} is ${kb} KB`);
    }
  }

  if (!ok) process.exit(1);
}

main();



