/**
 * Frame-perfect MP4 export for the Comeback meme.
 *
 * It loads index.html in headless Chrome, then for each frame calls
 * window.__seek(t) and screenshots — so motion is perfectly smooth and
 * independent of how fast your machine renders. ffmpeg stitches the PNGs.
 *
 *   node render.js                 # 1080x1920 (vertical), 60fps -> out.mp4
 *   FPS=30 W=1080 H=1080 node render.js
 *   OUT=comeback.mp4 node render.js
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const puppeteer = require('puppeteer');

const FPS = parseInt(process.env.FPS || '60', 10);
const W   = parseInt(process.env.W   || '1080', 10);
const H   = parseInt(process.env.H   || '1920', 10);
const OUT = process.env.OUT || 'out.mp4';

const htmlPath = path.join(__dirname, 'index.html');
const fileUrl  = 'file://' + htmlPath;

(async () => {
  // sanity: ffmpeg present?
  try { execFileSync('ffmpeg', ['-version'], { stdio: 'ignore' }); }
  catch { console.error('\n✗ ffmpeg not found. Install it:  brew install ffmpeg\n'); process.exit(1); }

  const framesDir = fs.mkdtempSync(path.join(os.tmpdir(), 'comeback-'));
  console.log(`→ launching headless Chrome  (${W}x${H} @ ${FPS}fps)`);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--force-color-profile=srgb', '--hide-scrollbars'],
    defaultViewport: { width: W, height: H, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  // stop the real-time loop so we control time ourselves
  await page.evaluate(() => { window.playing = false; });
  await page.evaluate(async () => { if (document.fonts) await document.fonts.ready; });

  const duration = await page.evaluate(() => window.__duration);
  const totalFrames = Math.ceil((duration / 1000) * FPS);
  console.log(`→ rendering ${totalFrames} frames (${(duration/1000).toFixed(1)}s)`);

  for (let i = 0; i < totalFrames; i++) {
    const t = (i / FPS) * 1000;
    await page.evaluate((tt) => window.__seek(tt), t);
    const file = path.join(framesDir, `f${String(i).padStart(5, '0')}.png`);
    await page.screenshot({ path: file });
    if (i % FPS === 0) process.stdout.write(`\r   ${i}/${totalFrames}`);
  }
  process.stdout.write(`\r   ${totalFrames}/${totalFrames}\n`);
  await browser.close();

  console.log('→ encoding MP4 with ffmpeg');
  execFileSync('ffmpeg', [
    '-y',
    '-framerate', String(FPS),
    '-i', path.join(framesDir, 'f%05d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '18',
    '-preset', 'slow',
    '-movflags', '+faststart',
    path.join(__dirname, OUT),
  ], { stdio: 'inherit' });

  fs.rmSync(framesDir, { recursive: true, force: true });
  console.log(`\n✓ done →  ${path.join(__dirname, OUT)}`);
})().catch((e) => { console.error(e); process.exit(1); });
