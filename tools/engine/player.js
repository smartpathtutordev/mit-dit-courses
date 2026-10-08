/* =========================================================================
   SMARTPATH GRADE 1 LESSON PLAYER
   Built on the Week 1 Day 1 design: one teacher voice, big pictures,
   "listen first, then your turn", stars for every try, no fail states.
   Lesson content lives in LESSON (injected by tools/build.py).
   ========================================================================= */

/* ---------- tiny helpers ---------- */
const $ = (id) => document.getElementById(id);
function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
const ICON = {
  speaker: '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>',
  star: '<svg width="22" height="22" viewBox="0 0 24 24" fill="#F59E0B"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>',
  play: '<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
  check: '<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
  hand: '<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M23 5.5V20c0 2.2-1.8 4-4 4h-7.3c-1.08 0-2.1-.43-2.85-1.19L1 14.83s1.26-1.23 1.3-1.25c.22-.19.49-.29.79-.29.22 0 .42.06.6.16.04.01 4.31 2.46 4.31 2.46V4c0-.83.67-1.5 1.5-1.5S11 3.17 11 4v7h1V1.5c0-.83.67-1.5 1.5-1.5S15 .67 15 1.5V11h1V2.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5V11h1V5.5c0-.83.67-1.5 1.5-1.5s1.5.67 1.5 1.5z"/></svg>',
  stop: '<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8 0-1.85.63-3.55 1.69-4.9L16.9 18.31C15.55 19.37 13.85 20 12 20zm6.31-3.1L7.1 5.69C8.45 4.63 10.15 4 12 4c4.42 0 8 3.58 8 8 0 1.85-.63 3.55-1.69 4.9z"/></svg>',
  note: '<svg width="34" height="34" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>',
  mic: '<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z"/></svg>',
  book: '<svg width="64" height="64" viewBox="0 0 24 24" fill="#D97706"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/></svg>',
  heart: '<svg class="verse-heart-svg" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>',
  trophy: '<svg width="80" height="80" viewBox="0 0 24 24" fill="#F59E0B"><path d="M19 5h-2V3H7v2H5c-1.1 0-2 .9-2 2v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.76 2.72 3.19 3.39V19H8v2h8v-2h-2.58v-2.67c1.43-.67 2.56-1.89 3.19-3.39C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v3.82C5.84 10.4 5 9.3 5 8zm14 0c0 1.3-.84 2.4-2 2.82V7h2v1z"/></svg>'
};

/* ---------- sound effects (synthesized, no files needed) ---------- */
class SoundEngine {
  constructor() { this.ctx = null; this.muted = false; }
  init() {
    if (!this.ctx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) this.ctx = new AC();
    }
    if (this.ctx && this.ctx.state === 'suspended') this.ctx.resume();
  }
  tone(freq, type, start, dur, vol) {
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, start);
    g.gain.setValueAtTime(vol, start);
    g.gain.exponentialRampToValueAtTime(0.01, start + dur);
    osc.connect(g).connect(this.ctx.destination);
    osc.start(start);
    osc.stop(start + dur + 0.01);
    return osc;
  }
  pop() {
    if (this.muted) return; this.init(); if (!this.ctx) return;
    const now = this.ctx.currentTime;
    const o = this.tone(440, 'sine', now, 0.08, 0.3);
    o.frequency.exponentialRampToValueAtTime(880, now + 0.08);
  }
  star() {
    if (this.muted) return; this.init(); if (!this.ctx) return;
    const now = this.ctx.currentTime;
    [523.25, 659.25, 783.99, 1046.5].forEach((f, i) => this.tone(f, 'triangle', now + i * 0.07, 0.25, 0.22));
  }
  soft() {
    if (this.muted) return; this.init(); if (!this.ctx) return;
    const now = this.ctx.currentTime;
    this.tone(330, 'sine', now, 0.18, 0.18);
    this.tone(262, 'sine', now + 0.12, 0.22, 0.15);
  }
  cheer() { this.star(); }
}
const sound = new SoundEngine();

/* =========================================================================
   VOICE: one channel for everything the teacher says.
   Plays speech/<name>.mp3, then .wav; if neither exists, the browser
   reads the same words aloud so the lesson always works.
   ========================================================================= */
const audio = $('audioNarrator');
const Voice = {
  token: 0,
  mode: 'idle',          // 'file' | 'tts' | 'idle'
  isNarration: false,
  ttsVoice: null,
  clean(t) {
    return String(t || '').replace(/\(pause(?:\s*\d+)?\)/gi, ' ').replace(/\s+/g, ' ').trim();
  },
  pickVoice() {
    if (!('speechSynthesis' in window)) return null;
    const vs = speechSynthesis.getVoices().filter(v => /^en/i.test(v.lang));
    const pref = ['Samantha', 'Google US English', 'Microsoft Aria', 'Microsoft Jenny', 'Karen', 'Moira', 'Tessa', 'Zira', 'Female'];
    for (const p of pref) {
      const v = vs.find(x => x.name.indexOf(p) !== -1);
      if (v) return v;
    }
    return vs[0] || null;
  },
  stop() {
    this.token++;
    try { audio.pause(); } catch (e) {}
    if ('speechSynthesis' in window) speechSynthesis.cancel();
    this.mode = 'idle';
  },
  /* clip = {a: 'speech/name', t: 'words to say'} */
  play(clip, opts) {
    opts = opts || {};
    this.stop();
    const my = ++this.token;
    this.isNarration = !!opts.narration;
    if (!clip || (!clip.a && !clip.t)) { if (opts.onend) opts.onend(); return; }
    const done = () => {
      if (my !== this.token) return;
      this.mode = 'idle';
      onVoiceEnded(this.isNarration);
      if (opts.onend) opts.onend();
    };
    onVoiceStarted(this.isNarration);
    const tryTts = () => {
      if (my !== this.token) return;
      if (!('speechSynthesis' in window) || !clip.t) { done(); return; }
      this.mode = 'tts';
      const parts = String(clip.t).split(/\(pause(?:\s*\d+)?\)/i).map(p => p.trim()).filter(Boolean);
      if (!this.ttsVoice) this.ttsVoice = this.pickVoice();
      parts.forEach((p, i) => {
        const u = new SpeechSynthesisUtterance(p);
        u.rate = 0.86; u.pitch = 1.08; u.lang = 'en-US';
        if (this.ttsVoice) u.voice = this.ttsVoice;
        if (i === parts.length - 1) { u.onend = done; u.onerror = done; }
        speechSynthesis.speak(u);
      });
      if (!parts.length) done();
    };
    if (!clip.a) { tryTts(); return; }
    const exts = ['.mp3', '.wav'];
    const tryFile = (k) => {
      if (my !== this.token) return;
      if (k >= exts.length) { tryTts(); return; }
      audio.onended = done;
      audio.onerror = () => tryFile(k + 1);
      audio.src = clip.a + exts[k];
      audio.currentTime = 0;
      this.mode = 'file';
      audio.play().catch((err) => {
        if (err && err.name === 'NotAllowedError') { done(); return; }
      });
    };
    tryFile(0);
  }
};
if ('speechSynthesis' in window) {
  speechSynthesis.onvoiceschanged = () => { Voice.ttsVoice = Voice.pickVoice(); };
}

/* =========================================================================
   PLAYER STATE
   ========================================================================= */
let cur = 0;
let stars = 0;
let isAutoAdvance = false;
let autoTimer = null;
let slideState = {};
const doneSlides = new Set();

const stagewrap = $('stagewrap');
const stage = $('stage');
const charActorWrap = $('charActorWrap');
const charImg = $('charImg');
const charNameLabel = $('charNameLabel');
const actorPulse = $('actorPulse');
const area = $('activityStageArea');
const body = $('stageCanvasBody');
const seekSlider = $('seekSlider');

function fitStage() {
  const scale = stagewrap.clientWidth / 1600;
  stage.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', fitStage);
fitStage();

function initDots() {
  const box = $('slideDotsIndicator');
  box.innerHTML = '';
  LESSON.slides.forEach((s, i) => {
    const d = document.createElement('div');
    d.className = 'slide-dot' + (i === cur ? ' active' : '') + (doneSlides.has(i) ? ' seen' : '');
    d.onclick = () => goToSlide(i);
    box.appendChild(d);
  });
}

function addStar() {
  stars++;
  $('starCounter').textContent = stars;
  const pill = $('starPill');
  pill.classList.add('bump');
  setTimeout(() => pill.classList.remove('bump'), 400);
  sound.star();
  if (window.confetti) confetti({ particleCount: 35, spread: 60, origin: { y: 0.8 } });
}

function fx(kind) {
  const list = (LESSON.fx && LESSON.fx[kind]) || [];
  if (!list.length) return null;
  return list[Math.floor(Math.random() * list.length)];
}

function playActorCheer() {
  charImg.style.transform = 'scale(1.1) rotate(3deg)';
  setTimeout(() => (charImg.style.transform = ''), 300);
  Voice.play(fx('cheer'));
}

/* ---------- listen first, then your turn ---------- */
function phaseBadgeHTML(s) {
  return `<div class="phase-status-badge listening" id="phaseBadge">
      <span class="speaking-pulse"></span><span>Listen to ${esc(s.who.name)}...</span>
      <button class="skip-phase-btn" onclick="unlockEarly(event)">Tap Now</button>
    </div>`;
}
function setPhase(listening) {
  const zone = $('interactiveZone');
  const badge = $('phaseBadge');
  if (!zone || !badge) return;
  if (listening) {
    zone.classList.add('locked'); zone.classList.remove('unlocked');
  } else {
    zone.classList.remove('locked'); zone.classList.add('unlocked');
    badge.className = 'phase-status-badge interactive bouncy';
    const s = LESSON.slides[cur];
    badge.innerHTML = `${ICON.hand.replace(/30/g, '22')}<span>${esc(s.yourTurn || 'Your turn! Tap!')}</span>`;
  }
}
function unlockEarly(e) {
  if (e) e.stopPropagation();
  Voice.stop();
  onVoiceEnded(true);
  sound.pop();
}

function onVoiceStarted(isNarration) {
  actorPulse.style.display = 'inline-block';
  setPlayPauseUI(false);
  if (isNarration) setPhase(true);
}
function onVoiceEnded(isNarration) {
  actorPulse.style.display = 'none';
  setPlayPauseUI(true);
  if (!isNarration) return;
  setPhase(false);
  const s = LESSON.slides[cur];
  if (s && s.passive) markDone();
  if (s && s.onNarrationEnd) s.onNarrationEnd();
  if (isAutoAdvance && cur < LESSON.slides.length - 1 && s && s.passive) {
    clearTimeout(autoTimer);
    autoTimer = setTimeout(nextSlide, 4000);
  }
}

/* slide finished: invite the child forward */
function markDone() {
  if (doneSlides.has(cur)) { $('btnNextSlide').classList.add('go-glow'); return; }
  doneSlides.add(cur);
  $('btnNextSlide').classList.add('go-glow');
  initDots();
}

/* audio progress bar (only for recorded files) */
audio.addEventListener('timeupdate', () => {
  if (!audio.duration) return;
  seekSlider.value = Math.floor((audio.currentTime / audio.duration) * 1000);
  $('currTime').textContent = fmt(audio.currentTime);
  $('totTime').textContent = fmt(audio.duration);
});
function fmt(s) {
  if (!s || isNaN(s)) return '0:00';
  const m = Math.floor(s / 60), x = Math.floor(s % 60);
  return `${m}:${x < 10 ? '0' : ''}${x}`;
}

/* =========================================================================
   SLIDE RENDERING
   ========================================================================= */
function poseSrc(who) {
  return `${LESSON.posesRoot}/${who.char}/${who.pose}`;
}
function imgTag(src, alt, cls) {
  if (!src) return '';
  return `<img src="${esc(src)}" alt="${esc(alt || '')}" class="${cls || ''}" draggable="false">`;
}
function itemPic(it) {
  if (it.img) return `<div class="pic-frame">${imgTag(it.img, it.word)}</div>`;
  if (it.pose) return `<div class="pic-frame pose">${imgTag(`${LESSON.posesRoot}/${it.pose}`, it.word)}</div>`;
  return '';
}

function renderSlide(idx) {
  clearTimeout(autoTimer);
  Voice.stop();
  cur = idx;
  const s = LESSON.slides[idx];
  slideState = {};
  $('btnNextSlide').classList.remove('go-glow');
  if (doneSlides.has(idx)) $('btnNextSlide').classList.add('go-glow');
  initDots();
  $('slideCounterBadge').textContent = `${idx + 1} / ${LESSON.slides.length}`;
  seekSlider.value = 0;
  $('currTime').textContent = '0:00';
  $('totTime').textContent = '0:00';

  if (s.bg) $('scenicBg').style.backgroundImage = `url('${s.bg}')`;
  else $('scenicBg').style.backgroundImage = `url('${LESSON.bg}')`;

  const story = s.type === 'story';
  body.classList.toggle('story-mode', story);
  charActorWrap.classList.toggle('minimized', story);
  const right = !story && s.side === 'right';
  body.classList.toggle('char-on-right', right);
  charActorWrap.classList.toggle('right-side', right);
  charImg.src = poseSrc(s.who);
  charNameLabel.textContent = s.who.name;

  area.innerHTML = '';
  const fn = RENDER[s.type];
  if (fn) fn(s); else area.innerHTML = `<div class="big-card"><p>Missing slide type: ${esc(s.type)}</p></div>`;

  if (s.narration) Voice.play(s.narration, { narration: true });
}

const RENDER = {
  cover(s) {
    area.innerHTML = `
      <div class="big-card bouncy">
        ${ICON.book}
        <h1 style="font-size:58px;font-weight:800;color:#92400E;line-height:1.15;">${esc(s.title)}</h1>
        <p style="font-size:26px;font-weight:700;color:#4B5563;">${esc(LESSON.label)}</p>
        <div style="display:flex;flex-direction:column;gap:14px;text-align:left;background:#FFFBEB;padding:22px 34px;border-radius:22px;border:3px solid #FDE68A;width:100%;max-width:700px;">
          <div style="font-size:22px;font-weight:800;color:#B45309;letter-spacing:1px;">TODAY I WILL...</div>
          ${s.goals.map(g => `<div style="font-size:30px;font-weight:800;color:#78350F;display:flex;align-items:center;gap:12px;">${ICON.star}<span>${esc(g)}</span></div>`).join('')}
        </div>
        <button class="btn-dock amber" style="font-size:32px;padding:16px 56px;border-radius:26px;margin-top:6px;" onclick="sound.pop();nextSlide();">Let's Begin!</button>
      </div>`;
  },

  cards(s) {
    const n = s.items.length;
    slideState.heard = new Set();
    area.innerHTML = `
      <div class="big-card ${s.theme || ''}">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div class="pic-grid n${n}">
            ${s.items.map((it, i) => `
              <div class="pic-card ${it.img || it.pose ? '' : 'text-only'}" id="card${i}" style="animation-delay:${i * 0.12}s" onclick="tapCard(${i})">
                ${itemPic(it)}
                <div class="pic-word">${esc(it.word)}</div>
                ${it.sub ? `<div class="pic-sub">${esc(it.sub)}</div>` : ''}
                <div class="audio-tap-badge">${ICON.speaker.replace(/22/g, '15')} Tap</div>
              </div>`).join('')}
          </div>
          <div class="progress-pips" id="pips">${s.items.map(() => '<span></span>').join('')}</div>
        </div>
      </div>`;
  },

  word(s) {
    area.innerHTML = `
      <div class="big-card ${s.theme || ''}">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <div class="word-focus-row">
            ${s.img ? `<div class="word-focus-pic">${imgTag(s.img, s.word)}</div>` : ''}
            <div>
              <div class="giant-word" onclick="tapWord()" title="Tap to hear!">
                <span>${esc(s.word)}</span>${ICON.speaker.replace(/22/g, '44')}
              </div>
              ${s.sub ? `<div class="word-sub-lang">${esc(s.sub)}</div>` : ''}
            </div>
          </div>
          <div class="word-meaning-banner">${esc(s.mean)}</div>
          ${s.model ? `<div class="model-sentence-box"><span style="color:#0D9488;">Say: </span>"${esc(s.model)}"</div>` : ''}
        </div>
      </div>`;
  },

  sentence(s) {
    area.innerHTML = `
      <div class="big-card teal-theme">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div class="interactive-sentence-builder">
            <span>${esc(s.pre)}</span>
            <span class="blank-slot" id="targetSlot">______</span>
            <span>${esc(s.post || '')}</span>
          </div>
          <div class="pic-grid n${s.options.length}">
            ${s.options.map((o, i) => `
              <div class="pic-card ${o.img || o.pose ? '' : 'text-only'}" id="card${i}" onclick="pickSentence(${i})">
                ${itemPic(o)}
                <div class="pic-word">${esc(o.word)}</div>
              </div>`).join('')}
          </div>
        </div>
      </div>`;
  },

  story(s) {
    area.innerHTML = `
      <div class="story-page">
        ${imgTag(s.img, s.title, 'story-pic')}
        ${s.page ? `<div class="page-badge">${esc(s.page)}</div>` : ''}
        <div class="story-caption-overlay">
          <div class="story-tag">${esc(s.title)}</div>
          <div class="story-text">${s.lines.map((l, i) => `<span class="story-line" id="sl${i}">${esc(l)}</span>`).join('')}</div>
        </div>
      </div>`;
  },

  pick(s) {
    slideState.round = 0;
    area.innerHTML = `
      <div class="big-card purple-theme">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div id="pickRound" style="display:flex;flex-direction:column;align-items:center;gap:20px;width:100%;"></div>
          <div class="progress-pips" id="pips">${s.rounds.map(() => '<span></span>').join('')}</div>
        </div>
      </div>`;
    drawPickRound(false);
  },

  order(s) {
    slideState.next = 0;
    slideState.shuffled = s.items.map((it, i) => i);
    // deterministic shuffle so the first card is never already in place
    slideState.shuffled.push(slideState.shuffled.shift());
    if (s.items.length > 2) slideState.shuffled.reverse();
    area.innerHTML = `
      <div class="big-card purple-theme">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div class="order-slots">${s.slots.map((l, i) => `<div class="order-slot" id="slot${i}">${i + 1}. ${esc(l)}</div>`).join('')}</div>
          <div class="pic-grid n${s.items.length}">
            ${slideState.shuffled.map((k) => {
              const it = s.items[k];
              return `<div class="pic-card" id="ord${k}" onclick="tapOrder(${k})">${itemPic(it)}<div class="pic-sub" style="color:#1F2937;font-size:22px;">${esc(it.word)}</div></div>`;
            }).join('')}
          </div>
          <div class="feedback-line" id="feedback"></div>
        </div>
      </div>`;
  },

  act(s) {
    slideState.step = 0;
    area.innerHTML = `
      <div class="big-card ${s.simon ? 'purple-theme' : ''}">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div id="actBox"></div>
          <div class="feedback-line" id="feedback"></div>
          <div class="progress-pips" id="pips">${s.cmds.map(() => '<span></span>').join('')}</div>
        </div>
      </div>`;
    s.onNarrationEnd = () => { if (cur === LESSON.slides.indexOf(s) && slideState.step === 0 && !slideState.started) { slideState.started = true; drawAct(true); } };
    drawAct(false);
  },

  chant(s) {
    slideState.heard = new Set();
    area.innerHTML = `
      <div class="big-card">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div style="display:flex;gap:30px;align-items:center;width:100%;justify-content:center;">
            ${s.img ? `<div class="word-focus-pic" style="width:300px;height:300px;flex-shrink:0;">${imgTag(s.img, s.title)}</div>` : ''}
            <div class="chant-lines">
              ${s.lines.map((l, i) => `<div class="chant-line" id="cl${i}" onclick="tapChant(${i})"><span class="note-ic">${ICON.note}</span><span>${esc(l.text)}</span></div>`).join('')}
            </div>
          </div>
          <button class="big-btn amber" onclick="chantAll()">${ICON.play} ${esc(s.allLabel || 'Say it all together!')}</button>
        </div>
      </div>`;
  },

  talk(s) {
    const frame = esc(s.frame).replace(/_{3,}/g, '<span class="gap"></span>');
    area.innerHTML = `
      <div class="big-card teal-theme">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          ${s.img ? `<div class="word-focus-pic" style="height:220px;width:340px;">${imgTag(s.img, s.title)}</div>` : ''}
          <div class="talk-frame">${frame}</div>
          ${s.example ? `<div class="talk-example"><button class="hear-btn" onclick="hearExample()">${ICON.speaker}</button><span>${esc(s.example.label || 'Listen to Tala')}: "${esc(s.example.text)}"</span></div>` : ''}
          <button class="big-btn green" onclick="saidIt(this)">${ICON.mic} I said it!</button>
        </div>
      </div>`;
  },

  langs(s) {
    slideState.heard = new Set();
    area.innerHTML = `
      <div class="big-card teal-theme">
        <div class="interactive-zone locked" id="interactiveZone">
          ${phaseBadgeHTML(s)}
          <h2 class="card-title">${esc(s.title)}</h2>
          <div class="lang-grid">
            ${s.items.map((it, i) => `<div class="lang-card" id="card${i}" style="animation-delay:${i * 0.12}s" onclick="tapLang(${i})"><div class="lang-name">${esc(it.lang)}</div><div class="lang-word">${esc(it.word)}</div><div class="audio-tap-badge">${ICON.speaker.replace(/22/g, '15')} Tap</div></div>`).join('')}
          </div>
          <div class="same-meaning">${s.img ? imgTag(s.img, s.meaning) : ''}<span>${esc(s.meaning)}</span></div>
        </div>
      </div>`;
  },

  verse(s) {
    area.innerHTML = `
      <div class="verse-card bouncy">
        ${ICON.heart}
        <div class="verse-text">"${esc(s.verse)}"</div>
        <div class="verse-ref">${esc(s.ref)}</div>
        <p style="font-size:30px;font-weight:700;color:#92400E;max-width:760px;line-height:1.35;">${esc(s.meaning)}</p>
        <button class="btn-dock amber" style="font-size:24px;padding:12px 30px;border-radius:20px;margin-top:6px;" onclick="sayVerse()">${ICON.speaker} Say it with me</button>
      </div>`;
  },

  celebrate(s) {
    area.innerHTML = `
      <div class="celebrate-card">
        ${ICON.trophy}
        <h2>${esc(s.title)}</h2>
        <div class="recap-list">${s.recap.map(r => `<div>${ICON.star}<span>${esc(r)}</span></div>`).join('')}</div>
        <div style="font-size:40px;font-weight:800;color:#92400E;background:#FEF3C7;padding:12px 36px;border-radius:26px;border:4px solid #F59E0B;display:flex;align-items:center;gap:12px;">
          ${ICON.star.replace(/22/g, '36')}<span>My Stars: ${stars}</span>
        </div>
        <div style="display:flex;gap:18px;margin-top:8px;">
          <button class="btn-dock amber" style="font-size:26px;padding:16px 38px;border-radius:22px;" onclick="goToSlide(0)">Play Again</button>
          ${LESSON.nextHref ? `<button class="btn-dock primary" style="font-size:26px;padding:16px 38px;border-radius:22px;" onclick="location.href='${esc(LESSON.nextHref)}'">Next Lesson</button>` : ''}
        </div>
      </div>`;
    sound.cheer();
    if (window.confetti) confetti({ particleCount: 120, spread: 90, origin: { y: 0.6 } });
  }
};

/* =========================================================================
   INTERACTIONS
   ========================================================================= */
function S() { return LESSON.slides[cur]; }
function turnOn() { setPhase(false); }
function pip(i) { const p = document.querySelectorAll('#pips span')[i]; if (p) p.classList.add('on'); }
function speakingCard(id) {
  document.querySelectorAll('.speaking').forEach(c => c.classList.remove('speaking'));
  const el = $(id); if (el) el.classList.add('speaking');
}

function tapCard(i) {
  const s = S(); const it = s.items[i];
  turnOn(); sound.pop(); speakingCard('card' + i);
  Voice.play(it.clip);
  if (!slideState.heard.has(i)) {
    slideState.heard.add(i);
    $('card' + i).classList.add('done');
    pip(i); addStar();
    if (slideState.heard.size === s.items.length) setTimeout(markDone, 600);
  }
}

function tapWord() {
  const s = S();
  turnOn(); Voice.play(s.clip);
  if (!slideState.tapped) { slideState.tapped = true; addStar(); markDone(); }
}

function pickSentence(i) {
  const s = S(); const o = s.options[i];
  turnOn();
  const slot = $('targetSlot');
  slot.textContent = o.word; slot.classList.add('filled');
  document.querySelectorAll('.pic-card').forEach(c => c.classList.remove('done'));
  $('card' + i).classList.add('done');
  Voice.play(o.clip);
  addStar(); markDone();
}

function drawPickRound(withVoice) {
  const s = S(); const r = s.rounds[slideState.round];
  const box = $('pickRound');
  slideState.tries = 0;
  box.innerHTML = `
    <div class="ask-line"><button class="hear-btn" onclick="hearAsk()">${ICON.speaker}</button><span>${esc(r.ask)}</span></div>
    <div class="pic-grid n${r.choices.length}">
      ${r.choices.map((c, i) => `<div class="pic-card ${c.img || c.pose ? '' : 'text-only'}" id="ch${i}" style="animation-delay:${i * 0.1}s" onclick="tapPick(${i})">${itemPic(c)}<div class="pic-word">${esc(c.word)}</div></div>`).join('')}
    </div>
    <div class="feedback-line" id="feedback"></div>`;
  if (withVoice) Voice.play(r.clip);
}
function hearAsk() { const r = S().rounds[slideState.round]; turnOn(); Voice.play(r.clip); }
function tapPick(i) {
  const s = S(); const r = s.rounds[slideState.round]; const c = r.choices[i];
  turnOn();
  if (slideState.locked) return;
  const card = $('ch' + i); const fb = $('feedback');
  if (c.ok) {
    slideState.locked = true;
    card.classList.add('right');
    fb.className = 'feedback-line'; fb.textContent = r.yes || 'Yes! Great job!';
    pip(slideState.round); addStar();
    Voice.play(r.yesClip || fx('good'), {
      onend: () => {
        if (S() !== s) return;
        slideState.locked = false;
        if (slideState.round < s.rounds.length - 1) { slideState.round++; drawPickRound(true); }
        else markDone();
      }
    });
  } else {
    slideState.tries++;
    sound.soft();
    card.classList.remove('wobble'); void card.offsetWidth; card.classList.add('wobble');
    fb.className = 'feedback-line hint'; fb.textContent = r.hint || 'Almost! Try again.';
    Voice.play(r.hintClip || fx('try'));
  }
}

function tapOrder(k) {
  const s = S();
  turnOn();
  const card = $('ord' + k); const fb = $('feedback');
  if (card.classList.contains('done')) return;
  if (k === slideState.next) {
    card.classList.add('done');
    card.insertAdjacentHTML('beforeend', `<div class="order-num">${k + 1}</div>`);
    const slot = $('slot' + k); slot.classList.add('filled'); slot.textContent = `${k + 1}. ${s.items[k].word}`;
    addStar();
    Voice.play(s.items[k].clip);
    slideState.next++;
    fb.className = 'feedback-line'; fb.textContent = '';
    if (slideState.next === s.items.length) {
      fb.textContent = s.yes || 'You put the story in order!';
      setTimeout(() => { if (S() === s) Voice.play(s.yesClip || fx('good')); markDone(); }, 1600);
    }
  } else {
    sound.soft();
    card.classList.remove('wobble'); void card.offsetWidth; card.classList.add('wobble');
    fb.className = 'feedback-line hint';
    fb.textContent = `${s.ask[slideState.next]}`;
    Voice.play(s.askClips[slideState.next]);
  }
}

function drawAct(withVoice) {
  const s = S(); const c = s.cmds[slideState.step];
  const box = $('actBox'); const fb = $('feedback');
  if (fb) { fb.textContent = ''; fb.className = 'feedback-line'; }
  slideState.locked = false;
  box.innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;gap:22px;">
      <div class="act-card" onclick="hearCmd()">
        ${itemPic(c)}
        <div class="act-cmd">${s.simon && c.simon ? '<span class="simon-tag">Simon says...</span><br>' : ''}${esc(c.word)}${c.sub ? `<small>${esc(c.sub)}</small>` : ''}</div>
      </div>
      <div class="big-btn-row">
        ${s.simon
          ? `<button class="big-btn green" onclick="actAnswer(true)">${ICON.check} I did it!</button>
             <button class="big-btn gray" onclick="actAnswer(false)">${ICON.stop} I stayed still!</button>`
          : `<button class="big-btn green" onclick="actAnswer(true)">${ICON.check} I did it!</button>`}
      </div>
    </div>`;
  if (withVoice) Voice.play(c.clip);
}
function hearCmd() { const c = S().cmds[slideState.step]; turnOn(); Voice.play(c.clip); }
function actAnswer(didIt) {
  const s = S(); const c = s.cmds[slideState.step];
  turnOn();
  if (slideState.locked) return;
  slideState.started = true;
  const shouldDo = s.simon ? !!c.simon : true;
  const fb = $('feedback');
  if (didIt === shouldDo) {
    slideState.locked = true;
    pip(slideState.step); addStar();
    fb.className = 'feedback-line';
    fb.textContent = s.simon ? (shouldDo ? 'Yes! Simon said it!' : 'Good listening! You stayed still!') : 'Great moving!';
    Voice.play(s.simon && !shouldDo ? fx('still') : fx('good'), {
      onend: () => {
        if (S() !== s) return;
        if (slideState.step < s.cmds.length - 1) { slideState.step++; drawAct(true); }
        else markDone();
      }
    });
  } else {
    sound.soft();
    fb.className = 'feedback-line hint';
    fb.textContent = shouldDo ? 'Simon said it! Do it!' : 'Oops! Simon did not say it.';
    Voice.play(shouldDo ? fx('doit') : fx('oops'));
  }
}

function tapChant(i) {
  const s = S();
  turnOn();
  document.querySelectorAll('.chant-line').forEach(c => c.classList.remove('now'));
  const el = $('cl' + i); el.classList.add('now');
  Voice.play(s.lines[i].clip, { onend: () => el.classList.remove('now') });
  if (!slideState.heard.has(i)) {
    slideState.heard.add(i); el.classList.add('done'); addStar();
    if (slideState.heard.size === s.lines.length) markDone();
  }
}
function chantAll() {
  const s = S();
  turnOn();
  let i = 0;
  const step = () => {
    if (S() !== s || i >= s.lines.length) { if (S() === s) { addStar(); markDone(); } return; }
    document.querySelectorAll('.chant-line').forEach(c => c.classList.remove('now'));
    const el = $('cl' + i); el.classList.add('now', 'done');
    slideState.heard.add(i);
    const k = i; i++;
    Voice.play(s.lines[k].clip, { onend: step });
  };
  step();
}

function hearExample() { const s = S(); turnOn(); Voice.play(s.example.clip); }
function saidIt(btn) {
  turnOn();
  addStar();
  btn.innerHTML = `${ICON.check} Great talking!`;
  Voice.play(fx('good'));
  markDone();
}

function tapLang(i) {
  const s = S(); const it = s.items[i];
  turnOn(); speakingCard('card' + i);
  Voice.play(it.clip);
  if (!slideState.heard.has(i)) {
    slideState.heard.add(i); $('card' + i).classList.add('done'); addStar();
    if (slideState.heard.size === s.items.length) setTimeout(markDone, 600);
  }
}

function sayVerse() { const s = S(); Voice.play(s.verseClip || s.narration); if (!slideState.v) { slideState.v = 1; addStar(); } }

/* =========================================================================
   NAVIGATION
   ========================================================================= */
function goToSlide(i) { sound.pop(); renderSlide(i); }
function prevSlide() { if (cur > 0) goToSlide(cur - 1); }
function nextSlide() { if (cur < LESSON.slides.length - 1) goToSlide(cur + 1); }
function replayAudio() { sound.pop(); const s = S(); if (s.narration) Voice.play(s.narration, { narration: true }); }
function setPlayPauseUI(paused) {
  $('svgPlayPause').innerHTML = paused ? '<path d="M8 5v14l11-7z"/>' : '<path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>';
  $('txtPlayPause').textContent = paused ? 'Play' : 'Pause';
}
function togglePlayPause() {
  sound.pop();
  if (Voice.mode === 'file') { if (audio.paused) audio.play().catch(() => {}); else audio.pause(); return; }
  if (Voice.mode === 'tts') {
    if (speechSynthesis.paused) { speechSynthesis.resume(); setPlayPauseUI(false); }
    else { speechSynthesis.pause(); setPlayPauseUI(true); }
    return;
  }
  replayAudio();
}
function onSeekChange(v) { if (Voice.mode === 'file' && audio.duration) audio.currentTime = (v / 1000) * audio.duration; }
function toggleAutoAdvance() {
  sound.pop();
  isAutoAdvance = !isAutoAdvance;
  const b = $('btnAutoAdvance');
  b.textContent = isAutoAdvance ? 'Auto: ON' : 'Auto: OFF';
  b.classList.toggle('primary', isAutoAdvance);
}
function toggleMute() { sound.muted = !sound.muted; $('btnSoundMute').style.opacity = sound.muted ? 0.5 : 1; }
function toggleFullscreen() {
  sound.pop();
  if (!document.fullscreenElement) stagewrap.requestFullscreen().catch(() => {});
  else document.exitFullscreen().catch(() => {});
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); nextSlide(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prevSlide(); }
  else if (e.key === ' ') { e.preventDefault(); togglePlayPause(); }
  else if (e.key.toLowerCase() === 'r') { e.preventDefault(); replayAudio(); }
});

/* START: wait for one tap so the browser lets us play sound */
function startLesson() {
  sound.init();
  $('startOverlay').classList.add('gone');
  renderSlide(0);
}
initDots();
$('slideCounterBadge').textContent = `1 / ${LESSON.slides.length}`;
charImg.src = poseSrc(LESSON.slides[0].who);
$('scenicBg').style.backgroundImage = `url('${LESSON.bg}')`;
