// Build a motion video: node tools/motion/build.mjs <page name> <out path without lang/ext> [langs...]
// Needs: a static server for the repo (BASE, default http://localhost:8765), one for the NASA photo folder (ASSETS),
// the full music tracks in $MUSIC (Kevin MacLeod, CC BY 4.0, from incompetech.com) and ffmpeg.
import { chromium } from '/opt/npm-tools/node_modules/playwright/index.mjs';
import { execFileSync } from 'child_process';
import fs from 'fs'; import path from 'path'; import os from 'os';
const [name, out, ...langArgs] = process.argv.slice(2); const langs = langArgs.length ? langArgs : ['ja', 'en'];
const BASE = process.env.BASE || 'http://localhost:8765', ASSETS = process.env.ASSETS || 'http://localhost:8766', MUSIC = process.env.MUSIC || '/home/claude/music';
const HERE = path.dirname(new URL(import.meta.url).pathname), FPS = 30;
const [VW, VH] = (process.env.VIEW || '1080x1920').split('x').map(Number), REPO = path.resolve(HERE, '..', '..');
const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox'] });
for (const lang of langs) {
  const p = await b.newPage({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('response', r => { if (r.status() >= 400) console.log('HTTP', r.status(), r.url()); }); p.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); });
  await p.goto(`${BASE}/tools/motion/${name}.html?lang=${lang}&assets=${encodeURIComponent(ASSETS)}`, { waitUntil: 'load' });
  await p.waitForFunction('window.__ready === true', null, { timeout: 15000 });
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
    await Promise.all([...document.querySelectorAll('video')].map(v => v.readyState >= 2 ? 0 : new Promise(r => { v.onloadeddata = v.onerror = r; }))); });
  const M = await p.evaluate(() => window.__motion); const N = Math.round(M.dur * FPS);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'mo-')); const vid = `${tmp}/v.mp4`, aud = `${tmp}/a.m4a`;
  if (process.env.STILLS) {   // quick preview: STILLS="1,3.5,7" -> /tmp/v/<name>_<lang>_<t>.jpg
    for (const t of process.env.STILLS.split(',')) { await p.evaluate(x => window.__seek(x), +t); await p.screenshot({ path: `/tmp/v/${name}_${lang}_${t}.jpg`, type: 'jpeg', quality: 80 }); }
    await p.close(); fs.rmSync(tmp, { recursive: true }); continue;
  }
  if (!process.env.AUDIO_ONLY) {
  // Frames go to disk first, then ffmpeg reads them as numbered files (piping JPEGs lost frames on wide pages).
  for (let f = 0; f < N; f++) {
    await p.evaluate(x => window.__seek(x), f / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
    fs.writeFileSync(`${tmp}/f_${String(f).padStart(5, '0')}.jpg`, buf);
    if (Math.abs(f / FPS - M.poster) < 0.5 / FPS) fs.writeFileSync(`${out}.poster.${lang}.jpg`, await p.screenshot({ type: 'jpeg', quality: 86 }));
  }
  await p.close();
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', `${tmp}/f_%05d.jpg`, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-r', String(FPS), vid]);
  const got = +execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=nb_frames', '-of', 'csv=p=0', vid]).toString().trim();
  if (got !== N) throw new Error(`frame count ${got} != ${N}`);
  } else await p.close();
  // sound: music beds + interface sounds placed at the times the page declared
  // Input 0 is a silent track of the full length: amix takes its clock from the first input, so it has to start at 0.
  const ins = ['-f', 'lavfi', '-t', String(M.dur), '-i', 'anullsrc=r=48000:cl=stereo'], fl = ['[0:a]anull[a0]']; let k = 1;
  for (const m of M.music) {
    const d = m.until - m.at; ins.push('-i', m.src.includes('/') ? path.resolve(REPO, m.src) : `${MUSIC}/${m.src}.mp3`);
    fl.push(`[${k}:a]atrim=${m.from}:${m.from + d},asetpts=N/SR/TB,afade=t=in:st=0:d=${m.fadeIn},afade=t=out:st=${Math.max(0, d - m.fadeOut)}:d=${m.fadeOut},volume=${m.gain},adelay=${Math.round(m.at * 1000)}:all=1[a${k}]`); k++;
  }
  for (const e of M.events) { ins.push('-i', `${HERE}/sfx/${e.s}.wav`); fl.push(`[${k}:a]volume=${e.g},adelay=${Math.round(e.t * 1000)}:all=1[a${k}]`); k++; }
  const mix = Array.from({ length: k }, (_, i) => `[a${i}]`).join('') + `amix=inputs=${k}:duration=longest:normalize=0,apad=whole_dur=${M.dur},atrim=0:${M.dur},loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=out:st=${M.dur - 0.35}:d=0.35[o]`;
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...ins, '-filter_complex', fl.join(';') + ';' + mix, '-map', '[o]', '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '128k', aud]);
  if (process.env.AUDIO_ONLY) { fs.copyFileSync(aud, process.env.AUDIO_ONLY); fs.writeFileSync(process.env.AUDIO_ONLY + '.txt', fl.join(';\n') + ';\n' + mix); fs.rmSync(tmp, { recursive: true }); continue; }
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', vid, '-i', aud, '-c', 'copy', '-movflags', '+faststart', '-t', String(M.dur), `${out}.${lang}.mp4`]);
  fs.rmSync(tmp, { recursive: true }); console.log('wrote', `${out}.${lang}.mp4`, M.dur + 's', M.events.length, 'sfx');
}
await b.close();
