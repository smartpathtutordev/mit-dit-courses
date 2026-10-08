/**
 * Age-6 player. Teacher Sage speaks only from prebuilt clips.
 * Next = the next short line. She steps aside when a story picture needs the space.
 */
(function () {
  const ROOT = window.ROOT_PATH || "../../../../../";
  const BASE = window.LESSON_BASE || "../";
  const $ = (id) => document.getElementById(id);

  function esc(s) {
    return String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  function fileUrl(rel) {
    if (!rel) return "";
    if (/^https?:|^data:/.test(rel)) return rel;
    if (rel.startsWith("POSES/")) return ROOT + rel;
    const media = String(rel).replace(/^.*\/(media\/)/, "media/");
    if (media.startsWith("media/")) return BASE + media;
    return BASE + rel.replace(/^\.\//, "");
  }

  const CLIP_ALIAS = {
    "hi-sage": ["hello", "hello-talk"],
    "today": ["today-talk", "hello-talk", "now-intro-talk"],
    "now-you": ["now-me", "now-me-talk", "now-intro", "now-intro-talk"],
    "now-family-kid": ["now-family", "now-family-talk"],
    "now-story": ["now-intro", "now-intro-talk", "now-draw"],
    "yes": ["check-why0", "check", "check-talk"],
    "look-again": ["describe-try", "check"],
    "tap-right": ["check-talk", "check", "tap-right"],
    "tap-family": ["family-words-talk", "family-words", "tap-family"],
    "tap-word": ["family-words-talk", "tap-word"],
    "tap-one": ["name-try-talk", "tap-one"],
    "verse-kid": ["verse-talk", "verse"],
    "verse-talk": ["verse"]
  };

  function clipUrls(clip, extra) {
    if (!clip && !(extra || []).length) return [];
    const names = [];
    const add = (n) => {
      const s = String(n || "").replace(/\.(mp3|wav)$/i, "");
      if (s && names.indexOf(s) < 0) names.push(s);
    };
    add(clip);
    (extra || []).forEach(add);
    (CLIP_ALIAS[String(clip || "")] || []).forEach(add);
    names.slice().forEach((n) => {
      add(n + "-talk");
      add(n + "-kid");
    });
    const urls = [];
    names.forEach((name) => {
      urls.push(BASE + "speech/" + name + ".mp3");
      urls.push(BASE + "speech/" + name + ".wav");
      urls.push(ROOT + "KID-PLAYER/speech/" + name + ".mp3");
      urls.push(ROOT + "KID-PLAYER/speech/" + name + ".wav");
    });
    return urls;
  }

  class Voice {
    constructor() {
      this.audio = null;
      this.gen = 0;
    }
    stop() {
      this.gen++;
      if (this.audio) {
        try { this.audio.pause(); this.audio.src = ""; } catch (e) {}
        this.audio = null;
      }
    }
    playUrls(urls, done, onMeta) {
      const list = (urls || []).filter(Boolean);
      if (!list.length) { if (done) setTimeout(done, 200); return; }
      this.stop();
      const g = this.gen;
      const tryAt = (n) => {
        if (g !== this.gen) return;
        if (n >= list.length) { if (done) setTimeout(() => done(false), 200); return; }
        const a = new Audio();
        let settled = false;
        const fail = () => {
          if (settled || g !== this.gen) return;
          settled = true;
          tryAt(n + 1);
        };
        a.onerror = fail;
        a.onended = () => { if (g === this.gen && done) setTimeout(() => done(true), 200); };
        a.onloadedmetadata = () => {
          if (settled || g !== this.gen) return;
          if (!(a.duration > 0.15)) return fail();
          settled = true;
          this.audio = a;
          if (onMeta) onMeta(a.duration);
          a.play().catch(() => fail());
        };
        setTimeout(fail, 4000);
        a.src = list[n];
      };
      tryAt(0);
    }
    speakClip(clip, done, onMeta, extra) {
      this.playUrls(clipUrls(clip, extra), done, onMeta);
    }
  }

  let PAGES = [];
  const voice = new Voice();
  let i = 0, stars = 0, qi = 0, orderAt = 0;

  function page() { return PAGES[i] || {}; }

  function look(mode, cue) {
    document.body.dataset.look = mode;
    const kid = document.querySelector(".kid");
    if (kid) kid.classList.toggle("is-story", mode === "story" || page().fit === "contain" || page().type === "beat");
    if ($("cue")) {
      $("cue").dataset.look = mode;
      $("cue").textContent = cue;
    }
  }

  function num(v) {
    if (v == null || v === "") return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  }

  function setArt(p) {
    const scene = $("scene");
    if (scene) {
      const bg = fileUrl(p.bg);
      scene.style.backgroundImage = bg ? "url('" + bg.replace(/'/g, "\\'") + "')" : "";
      const fit = p.fit === "contain" || p.type === "beat" || p.type === "story" || p.type === "song";
      const bx = num(p.bgX);
      const by = num(p.bgY);
      scene.classList.toggle("is-fit", fit);
      scene.classList.toggle("is-stand", !fit && (p.stand || "stand") === "stand" && p.hideFace !== true && bx == null);
      scene.classList.toggle("is-placed", bx != null || by != null);
      if (bx != null) scene.style.setProperty("--bg-x", bx + "%");
      else scene.style.removeProperty("--bg-x");
      if (by != null) scene.style.setProperty("--bg-y", by + "%");
      else scene.style.removeProperty("--bg-y");
      if (bx != null || by != null) {
        scene.style.backgroundPosition = (bx != null ? bx : 50) + "% " + (by != null ? by : 42) + "%";
      } else {
        scene.style.backgroundPosition = "";
      }
    }
    const face = $("face");
    if (!face) return;
    const stand = p.hideFace ? "off" : (p.stand || "stand");
    const fx = num(p.faceX);
    const fy = num(p.faceY);
    const fh = num(p.faceH);
    const custom = stand !== "off" && (fx != null || fy != null || fh != null);
    face.className = "sage " + (custom ? "custom" : stand);
    face.style.removeProperty("--face-x");
    face.style.removeProperty("--face-y");
    face.style.removeProperty("--face-h");
    if (custom) {
      if (fx != null) face.style.setProperty("--face-x", fx + "%");
      if (fy != null) face.style.setProperty("--face-y", fy + "%");
      if (fh != null) face.style.setProperty("--face-h", fh + "%");
    }
    if (stand !== "off") {
      face.alt = "Teacher Sage";
      face.src = ROOT + "POSES/TALA/" + (p.pose || "talking.png");
    }
  }

  function taps(p) {
    return /^(words|check|pick|pair|order|pack|steps)$/.test(p.type);
  }

  function echo(text) {
    let el = document.querySelector(".echo");
    if (!el && $("work")) {
      el = document.createElement("p");
      el.className = "hint echo";
      $("work").insertBefore(el, $("work").firstChild);
    }
    if (el) el.textContent = text || "";
  }

  function paint() {
    const p = page();
    const w = $("work");
    if (!w) return;
    w.innerHTML = "";
    if (p.type === "hello" || p.type === "bridge" || p.type === "beat" || p.type === "story") {
      w.innerHTML = "<p class=\"word\">" + esc(p.talk || p.line || p.say || "") + "</p>"
        + (p.hint ? "<p class=\"hint\">" + esc(p.hint) + "</p>" : "");
      return;
    }
    if (p.type === "teach" && (p.word || p.mean || p.model || p.hint)) {
      w.innerHTML = (p.word ? "<p class=\"word\">" + esc(p.word) + "</p>" : "")
        + (p.mean ? "<p class=\"hint\">" + esc(p.mean) + "</p>" : "")
        + (p.model ? "<p class=\"hint\">" + esc(p.model) + "</p>" : "")
        + (p.hint ? "<p class=\"hint\">" + esc(p.hint) + "</p>" : "");
      return;
    }
    if (p.type === "verse" && (p.line || p.talk)) {
      w.innerHTML = "<p class=\"hint\">" + esc(p.line || p.talk) + "</p>";
      return;
    }
    if (p.type === "say" && (p.lines || []).length) {
      w.innerHTML = (p.lines || []).map((l) => "<p class=\"hint\">" + esc(l) + "</p>").join("");
      return;
    }
    if (p.type === "steps") {
      const steps = p.steps || [];
      w.innerHTML = "<p class=\"hint echo\"></p><div class=\"row\">" + steps.map((s, n) =>
        "<button type=\"button\" class=\"chip\" data-i=\"" + n + "\">" + esc((s.n || (n + 1)) + ". " + (s.t || s.l || "")) + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".chip").forEach((b) => {
        b.onclick = () => {
          const s = steps[+b.dataset.i] || {};
          b.classList.add("yes");
          echo(s.l || s.t || "");
          look("sage", "Listen");
          voice.speakClip(s.clip, null, null, [p.srcId, p.id]);
          stars++; if ($("stars")) $("stars").textContent = stars;
        };
      });
      return;
    }
    if (p.type === "words" || p.type === "pick") {
      const defs = (p.defs && p.defs.length) ? p.defs : (p.chips || []).map((c) => ({ w: c, clip: "" }));
      w.innerHTML = "<p class=\"hint echo\"></p><div class=\"row\">" + defs.map((d, n) =>
        "<button type=\"button\" class=\"chip\" data-i=\"" + n + "\">" + esc(d.w || d) + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".chip").forEach((b) => {
        b.onclick = () => {
          const d = defs[+b.dataset.i] || {};
          b.classList.add("yes");
          echo(d.m || d.w || "");
          if (d.bg) {
            const next = Object.assign({}, p, { bg: d.bg, fit: d.fit, hideFace: d.hideFace, stand: d.hideFace ? "off" : (d.stand || p.stand), pose: d.pose || p.pose });
            setArt(next);
          }
          look("sage", "Listen");
          voice.speakClip(d.clip, () => look("tap", "Now tap"), null, [p.srcId, p.id]);
          stars++; if ($("stars")) $("stars").textContent = stars;
        };
      });
      return;
    }
    if (p.type === "pair") {
      const chips = p.chips || [];
      w.innerHTML = "<p class=\"hint echo\">" + esc(p.ask || "") + "</p><div class=\"row\">" + chips.map((c, n) =>
        "<button type=\"button\" class=\"chip\" data-i=\"" + n + "\">" + esc(c) + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".chip").forEach((b) => {
        b.onclick = () => {
          w.querySelectorAll(".chip").forEach((x) => x.classList.remove("yes"));
          b.classList.add("yes");
          echo(String(chips[+b.dataset.i] || ""));
          stars++; if ($("stars")) $("stars").textContent = stars;
        };
      });
      return;
    }
    if (p.type === "order") {
      const steps = p.steps || [];
      w.innerHTML = "<p class=\"hint echo\"></p><div class=\"row\">" + steps.map((s, n) =>
        "<button type=\"button\" class=\"chip\" data-i=\"" + n + "\">" + esc((s.n || (n + 1)) + ". " + (s.t || "")) + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".chip").forEach((b) => {
        b.onclick = () => {
          const n = +b.dataset.i;
          const s = steps[n] || {};
          if (n === orderAt) {
            b.classList.add("yes");
            echo(s.l || s.t || "");
            voice.speakClip(s.clip, null, null, [p.srcId, p.id]);
            orderAt++;
            stars++; if ($("stars")) $("stars").textContent = stars;
          } else {
            b.classList.add("no");
            voice.speakClip("look-again", null, null, ["describe-try", "check"]);
            setTimeout(() => b.classList.remove("no"), 400);
          }
        };
      });
      return;
    }
    if (p.type === "pack") {
      const items = p.items || [];
      w.innerHTML = "<p class=\"hint echo\"></p><div class=\"row\">" + items.map((d, n) =>
        "<button type=\"button\" class=\"chip\" data-i=\"" + n + "\">" + esc(d.w || "") + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".chip").forEach((b) => {
        b.onclick = () => {
          const d = items[+b.dataset.i] || {};
          echo(d.s || d.w || "");
          voice.speakClip(d.clip, null, null, [p.srcId, p.id]);
          if (d.ok) {
            b.classList.add("yes");
            stars++; if ($("stars")) $("stars").textContent = stars;
          } else {
            b.classList.add("no");
            setTimeout(() => b.classList.remove("no"), 400);
          }
        };
      });
      return;
    }
    if (p.type === "check") {
      const item = (p.items || [])[qi];
      if (!item) { next(); return; }
      w.innerHTML = "<p class=\"word echo\">" + esc(item.q || "Tap one.") + "</p><div class=\"row\">" + (item.choices || []).map((c) =>
        "<button type=\"button\" class=\"chip q\">" + esc(c) + "</button>"
      ).join("") + "</div>";
      w.querySelectorAll(".q").forEach((b) => {
        b.onclick = () => {
          const ok = b.textContent.toLowerCase() === String(item.a || "").toLowerCase();
          if (ok) {
            b.classList.add("yes");
            echo(item.why || "Yes.");
            voice.speakClip(item.whyClip || "yes", null, null, ["check-why0", "check"]);
            stars++; if ($("stars")) $("stars").textContent = stars;
            qi++;
            setTimeout(() => {
              if (qi < (p.items || []).length) paint();
              else look("picture", "Look at the picture");
            }, 700);
          } else {
            b.classList.add("no");
            voice.speakClip("look-again", null, null, ["describe-try", "check"]);
            setTimeout(() => b.classList.remove("no"), 400);
          }
        };
      });
    }
  }

  function cueFor(p) {
    if (taps(p)) return ["tap", "Now tap"];
    if (p.type === "beat" || p.type === "story" || p.fit === "contain") return ["story", "Look at the picture"];
    return ["picture", "Look at the picture"];
  }

  function go(n) {
    if (!PAGES.length) return;
    i = Math.max(0, Math.min(PAGES.length - 1, n));
    qi = 0;
    orderAt = 0;
    const p = page();
    setArt(p);
    if ($("prev")) $("prev").classList.toggle("off", i === 0);
    const dots = $("dots");
    if (dots) {
      dots.innerHTML = Array.from({ length: PAGES.length }, (_, k) => "<i class=\"" + (k === i ? "on" : "") + "\"></i>").join("");
    }
    look("sage", "Listen");
    paint();
    if (p.type === "check") look("tap", "Now tap");
    voice.speakClip(p.clip || p.id, (ok) => {
      if (page() !== p) return;
      const c = cueFor(p);
      look(c[0], c[1]);
      if (ok && !taps(p)) setTimeout(() => { if (page() === p) next(); }, 600);
    }, null, [p.srcId, p.id]);
  }

  function next() {
    if (!PAGES.length) {
      if ($("talk")) $("talk").textContent = "Open this lesson from the Easy hub.";
      return;
    }
    voice.stop();
    if (i >= PAGES.length - 1) {
      if ($("done")) $("done").classList.add("show");
      return;
    }
    go(i + 1);
  }

  function prev() {
    voice.stop();
    if (i > 0) go(i - 1);
  }

  window.KidGo = {
    next: next,
    prev: prev,
    go: go,
    speak: () => {
      look("sage", "Listen");
      voice.speakClip(page().clip || page().id, null, null, [page().srcId, page().id]);
    }
  };

  function bind() {
    if ($("prev")) $("prev").onclick = prev;
    if ($("speak")) $("speak").onclick = () => window.KidGo.speak();
    if ($("next")) $("next").onclick = next;
    if ($("again")) $("again").onclick = () => {
      if ($("done")) $("done").classList.remove("show");
      stars = 0; if ($("stars")) $("stars").textContent = 0;
      go(0);
    };
  }

  function start(pages) {
    PAGES = (pages || []).map((p) => Object.assign({}, p));
    bind();
    if (!PAGES.length) {
      if ($("talk")) $("talk").textContent = "This lesson has no pages yet.";
      if ($("cue")) $("cue").textContent = "Open from the Easy hub";
      return;
    }
    go(0);
  }

  bind();
  start(window.LESSON_PAGES || []);
})();
