// Plays every built lesson in headless Chromium the way a child would:
// press Start, then on every slide tap everything, answer every check
// (one wrong try first, then right), and press Next. Fails on any JS error,
// broken image, or slide that never becomes "done".
//
//   node tools/playtest.js [lesson-folder ...] [--shots DIR]
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(path.join(process.execPath, '../../lib/node_modules/playwright'))); }

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const shotsIdx = args.indexOf('--shots');
const shots = shotsIdx >= 0 ? args[shotsIdx + 1] : null;
const dirs = args.filter((a, i) => !a.startsWith('--') && !(shotsIdx >= 0 && i === shotsIdx + 1));

function lessons() {
  const out = [];
  const base = path.join(ROOT, 'tools', 'lessons');
  for (const f of fs.readdirSync(base).filter(f => /^g\d+q\d+w\d+d\d+\.py$/.test(f)).sort()) {
    const m = f.match(/g(\d+)q(\d+)w(\d+)d(\d+)/);
    out.push(path.join(ROOT, `SPT/ENG/GRADE${m[1]}/Q${m[2]}/WEEK${m[3]}/DAY${m[4]}/INTERACTIVE/index.html`));
  }
  return out;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  let failures = 0;
  const targets = (dirs.length ? dirs.map(d => path.resolve(d)) : lessons());
  for (const file of targets) {
    const errors = [];
    page.removeAllListeners('pageerror');
    page.on('pageerror', e => errors.push('JS: ' + e.message));
    page.on('requestfailed', r => { if (!/fonts|jsdelivr|\/speech\//.test(r.url())) errors.push('missing: ' + r.url().split('/INTERACTIVE/').pop()); });
    await page.goto('file://' + file);
    // speech files may not exist yet: make the browser voice finish instantly in tests
    await page.evaluate(() => {
      window.speechSynthesis.speak = (u) => setTimeout(() => u.onend && u.onend(), 30);
      window.speechSynthesis.cancel = () => {};
    });
    const name = file.split('/SPT/ENG/')[1].replace('/INTERACTIVE/index.html', '');
    await page.click('.start-btn');
    const n = await page.evaluate(() => LESSON.slides.length);
    const notDone = [];
    for (let i = 0; i < n; i++) {
      await page.waitForTimeout(250);
      const t = await page.evaluate(() => LESSON.slides[cur].type);
      if (shots) {
        fs.mkdirSync(shots, { recursive: true });
        await page.screenshot({ path: path.join(shots, `${name.replace(/\//g, '_')}_${String(i + 1).padStart(2, '0')}_${t}.png`) });
      }
      await page.evaluate(async () => {
        const wait = (ms) => new Promise(r => setTimeout(r, ms));
        const s = LESSON.slides[cur];
        const click = async (sel) => { const el = document.querySelector(sel); if (el) { el.click(); await wait(150); } };
        if (s.type === 'cards' || s.type === 'langs') for (let k = 0; k < s.items.length; k++) await click('#card' + k);
        if (s.type === 'word') await click('.giant-word');
        if (s.type === 'sentence') await click('#card0');
        if (s.type === 'chant') { for (let k = 0; k < s.lines.length; k++) await click('#cl' + k); }
        if (s.type === 'talk') await click('.big-btn.green');
        if (s.type === 'pick') {
          for (let r = 0; r < s.rounds.length; r++) {
            const ch = s.rounds[slideState.round].choices;
            const bad = ch.findIndex(c => !c.ok); if (bad >= 0) await click('#ch' + bad);
            await click('#ch' + ch.findIndex(c => c.ok));
            await wait(400);
          }
        }
        if (s.type === 'order') {
          await click('#ord' + (s.items.length - 1));
          for (let k = 0; k < s.items.length; k++) await click('#ord' + k);
          await wait(1800);
        }
        if (s.type === 'act') {
          for (let k = 0; k < s.cmds.length; k++) {
            const c = s.cmds[slideState.step];
            const should = s.simon ? !!c.simon : true;
            if (s.simon) await click(should ? '.big-btn.gray' : '.big-btn.green');
            await click(should ? '.big-btn.green' : '.big-btn.gray');
            await wait(300);
          }
        }
        await wait(800);
      });
      if (shots && ['pick', 'order', 'act', 'cards', 'sentence'].includes(t)) {
        await page.screenshot({ path: path.join(shots, `${name.replace(/\//g, '_')}_${String(i + 1).padStart(2, '0')}_${t}_done.png`) });
      }
      const done = await page.evaluate(() => doneSlides.has(cur));
      if (!done) notDone.push(`${i + 1}:${t}`);
      await page.evaluate(() => nextSlide());
    }
    const stars = await page.evaluate(() => stars);
    const broken = await page.evaluate(() => [...document.images].filter(im => im.complete && im.naturalWidth === 0).map(im => im.src.split('/').slice(-2).join('/')));
    const ok = !errors.length && !notDone.length && !broken.length;
    failures += !ok;
    console.log(`${ok ? 'PASS' : 'FAIL'} ${name}: ${n} slides, ${stars} stars` +
      (notDone.length ? `\n   never finished: ${notDone.join(', ')}` : '') +
      (errors.length ? '\n   ' + [...new Set(errors)].join('\n   ') : '') +
      (broken.length ? '\n   broken images: ' + broken.join(', ') : ''));
  }
  await browser.close();
  process.exit(failures ? 1 : 0);
})();
