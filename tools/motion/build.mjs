// Build a motion video: node tools/motion/build.mjs <page name> <out path without lang/ext> [langs...]
// Needs: a static server for the repo (BASE, default http://localhost:8765), one for the NASA photo folder (ASSETS),
// the full music tracks in $MUSIC (Kevin MacLeod, CC BY 4.0, from incompetech.com) and ffmpeg.
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import { spawn, execFileSync } from 'child_process';
import fs from 'fs'; import path from 'path'; import os from 'os';
const [name, out, ...langArgs] = process.argv.slice(2); const langs = langArgs.length ? langArgs : ['ja', 'en'];
const BASE = process.env.BASE || 'http://localhost:8765', ASSETS = process.env.ASSETS || 'http://localhost:8766', MUSIC = process.env.MUSIC || '/home/claude/music';
const HERE = path.dirname(new URL(import.meta.url).pathname), FPS = 30;
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
for (const lang of langs) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); });
  await p.goto(`${BASE}/tools/motion/${name}.html?lang=${lang}&assets=${encodeURIComponent(ASSETS)}`, { waitUntil: 'load' });
  await p.waitForFunction('window.__ready === true', null, { timeout: 15000 });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  const M = await p.evaluate(() => window.__motion); const N = Math.round(M.dur * FPS);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mo-')); const vid = `${tmp}/v.mp4`, aud = `${tmp}/a.m4a`;
  if (process.env.STILLS) {   // quick preview: STILLS="1,3.5,7" -> /tmp/v/<name>_<lang>_<t>.jpg
    for (const t of process.env.STILLS.split(',')) { await p.evaluate(x => window.__seek(x), +t); await p.screenshot({ path: `/tmp/v/${name}_${lang}_${t}.jpg`, type: 'jpeg', quality: 80 }); }
    await p.close(); fs.rmSync(tmp, { recursive: true }); continue;
  }
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-r', String(FPS), vid], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < N; f++) {
    await p.evaluate(x => window.__seek(x), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (Math.abs(f / FPS - M.poster) < 0.5 / FPS) fs.writeFileSync(`${out}.poster.${lang}.jpg`, await p.screenshot({ type: 'jpeg', quality: 86 }));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await p.close();
  // sound: music beds + interface sounds placed at the times the page declared
  const ins = [], fl = []; let k = 0;
  for (const m of M.music) {
    const d = m.until - m.at; ins.push('-i', `${MUSIC}/${m.src}.mp3`);
    fl.push(`[${k}:a]atrim=${m.from}:${m.from + d},asetpts=N/SR/TB,afade=t=in:st=0:d=${m.fadeIn},afade=t=out:st=${Math.max(0, d - m.fadeOut)}:d=${m.fadeOut},volume=${m.gain},adelay=${Math.round(m.at * 1000)}:all=1[a${k}]`); k++;
  }
  for (const e of M.events) { ins.push('-i', `${HERE}/sfx/${e.s}.wav`); fl.push(`[${k}:a]volume=${e.g},adelay=${Math.round(e.t * 1000)}:all=1[a${k}]`); k++; }
  const mix = Array.from({ length: k }, (_, i) => `[a${i}]`).join('') + `amix=inputs=${k}:duration=longest:normalize=0,apad=whole_dur=${M.dur},atrim=0:${M.dur},loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st=${M.dur - 0.35}:d=0.35[o]`;
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...ins, '-filter_complex', fl.join(';') + ';' + mix, '-map', '[o]', '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '128k', aud]);
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', vid, '-i', aud, '-c', 'copy', '-movflags', '+faststart', '-shortest', `${out}.${lang}.mp4`]);
  fs.rmSync(tmp, { recursive: true }); console.log('wrote', `${out}.${lang}.mp4`, M.dur + 's', M.events.length, 'sfx');
}
await b.close();
