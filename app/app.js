(function () {
'use strict';
var D = JSON.parse(document.getElementById('data').textContent);
var app = document.getElementById('app');

/* ---------- Speicher (geht auch ohne localStorage) ---------- */
var mem = {};
var store = {
  get: function (k, d) {
    try { var v = localStorage.getItem('physiologie.' + k); if (v != null) return JSON.parse(v); } catch (e) { if (k in mem) return mem[k]; }
    return k in mem ? mem[k] : d;
  },
  set: function (k, v) {
    mem[k] = v;
    try { localStorage.setItem('physiologie.' + k, JSON.stringify(v)); } catch (e) {}
  }
};

/* ---------- Daten aufbereiten ---------- */
var THEMA = {}, SET = {}, FRAGE = {};
D.themen.forEach(function (t) { THEMA[t.id] = t; t.fragen = []; });
D.fragensets.forEach(function (s) {
  SET[s.id] = s;
  s.fragen.forEach(function (f, i) { f.set = s.id; f.nr = f.nr || String(i + 1); FRAGE[f.id] = f; if (THEMA[f.thema]) THEMA[f.thema].fragen.push(f); });
});

/* ---------- DOM-Helfer ---------- */
function el(tag, attrs) {
  var n = document.createElement(tag);
  if (attrs) for (var k in attrs) {
    var v = attrs[k];
    if (v == null || v === false) continue;
    if (k === 'text') n.textContent = v;
    else if (k === 'on') for (var ev in v) n.addEventListener(ev, v[ev]);
    else n.setAttribute(k, v === true ? '' : v);
  }
  for (var i = 2; i < arguments.length; i++) add(n, arguments[i]);
  return n;
}
function add(n, c) {
  if (c == null || c === false) return;
  if (Array.isArray(c)) c.forEach(function (x) { add(n, x); });
  else n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
}
/* **fett** -> <b>, alles andere bleibt Text */
function rich(s) {
  var f = document.createDocumentFragment(), parts = String(s).split(/\*\*(.+?)\*\*/);
  parts.forEach(function (p, i) { if (p) f.appendChild(i % 2 ? el('b', { text: p }) : document.createTextNode(p)); });
  return f;
}
function plural(n, a, b) { return n + ' ' + (n === 1 ? a : b); }

/* ---------- Lernformat ---------- */
function quelle(q) {
  return el('p', { class: 'quelle' }, 'Quelle: ' + q.map(function (x) {
    var s = D.quellen[x[0]];
    return (s ? s.t : x[0]) + ', S. ' + x[1];
  }).join('; '));
}
function liste(items) {
  return el('ul', null, items.map(function (p) {
    if (Array.isArray(p)) return el('li', null, rich(p[0]), el('ul', null, p.slice(1).map(function (u) { return el('li', null, rich(u)); })));
    return el('li', null, rich(p));
  }));
}
function tabelle(t, breit) {
  var head = t[0];
  return el('div', { class: 'tbl-wrap' + (breit ? ' breit' : '') },
    el('table', null,
      el('thead', null, el('tr', null, head.map(function (h) { return el('th', null, rich(h)); }))),
      el('tbody', null, t.slice(1).map(function (r) {
        return el('tr', null, r.map(function (c, i) { return el('td', { 'data-label': head[i] }, rich(c)); }));
      }))));
}
function kette(fl) {
  var s = fl.s, chips = s.every(function (x) { return !x[1]; });
  var box = el('div', { class: 'fl' + (fl.loop ? ' loop' : '') + (chips ? ' chips' : '') });
  s.forEach(function (x, i) {
    if (i) box.appendChild(el('div', { class: 'fl-a', 'aria-hidden': 'true' }, s[i - 1][2] ? el('span', { text: s[i - 1][2] }) : null));
    box.appendChild(el('div', { class: 'fl-s' }, el('div', { class: 'fl-t' }, rich(x[0])), x[1] ? el('div', { class: 'fl-u' }, rich(x[1])) : null));
  });
  if (fl.loop) box.appendChild(el('div', { class: 'fl-loop', text: '↺ wieder von vorn: ' + s[0][0].replace(/\*\*/g, '') }));
  return el('figure', null, box, fl.c ? el('figcaption', null, rich(fl.c)) : null);
}
function balken(br) {
  var max = Math.max.apply(null, br.s.map(function (x) { return x[1]; })) || 1;
  return el('figure', null, el('div', { class: 'br' }, br.s.map(function (x) {
    return el('div', { class: 'br-r' },
      el('div', { class: 'br-l' }, rich(x[0])),
      el('div', { class: 'br-t' }, el('div', { class: 'br-f', style: 'width:' + Math.max(2, x[1] / max * 100).toFixed(1) + '%' })),
      el('div', { class: 'br-v' }, rich(x[2])));
  })), br.c ? el('figcaption', null, rich(br.c)) : null);
}
function schichten(ly) {
  return el('figure', null, el('div', { class: 'ly' },
    ly.top ? el('div', { class: 'ly-e', text: ly.top }) : null,
    ly.s.map(function (x, i) {
      return el('div', { class: 'ly-s', style: '--i:' + i + ';--n:' + ly.s.length },
        el('span', { class: 'ly-n' }, rich(x[0])), x[1] ? el('span', { class: 'ly-x' }, rich(x[1])) : null);
    }),
    ly.bot ? el('div', { class: 'ly-e', text: ly.bot }) : null), ly.c ? el('figcaption', null, rich(ly.c)) : null);
}
function merke(m) {
  return el('div', { class: 'merke' }, el('div', { class: 'merke-k', text: 'Merke' }),
    Array.isArray(m) ? liste(m) : el('p', null, rich(m)));
}
function abschnitt(a, tag) {
  var box = el('section', { class: 'abschnitt' });
  if (a.h) box.appendChild(el(tag || 'h2', null, rich(a.h)));
  if (a.li) box.appendChild(liste(a.li));
  if (a.tb) box.appendChild(tabelle(a.tb, true));
  if (a.tc) box.appendChild(tabelle(a.tc, false));
  if (a.fl) box.appendChild(kette(a.fl));
  if (a.br) box.appendChild(balken(a.br));
  if (a.ly) box.appendChild(schichten(a.ly));
  if (a.m) box.appendChild(merke(a.m));
  if (a.q) box.appendChild(quelle(a.q));
  return box;
}
function abbildung(f, wieBei) {
  if (!f.abb) return null;
  var inhalt = f.abb.map(function (a) { return abschnitt(a, 'h3'); });
  if (wieBei) return el('details', { class: 'frage-abb' }, el('summary', { text: 'Abbildung wie bei ' + wieBei + ' – antippen zum Zeigen' }), inhalt);
  return el('div', { class: 'frage-abb' }, inhalt);
}
function antwort(f) {
  return el('div', { class: 'antwort' },
    f.a.map(function (a) { return abschnitt(a, 'h3'); }),
    f.korr ? el('div', { class: 'korr' }, el('div', { class: 'korr-k', text: '✎ Korrigiert und ergänzt' }), liste(f.korr)) : null,
    quelle(f.q));
}

/* ---------- Ansichten ---------- */
var TABS = [['lernen', 'Lernen'], ['fragen', 'Fragen'], ['abfragen', 'Abfragen'], ['suche', 'Suche'], ['neu', 'Neu']];
function shell(tab, view, inhalt) {
  var neuNeu = D.neu.length && store.get('neu') !== D.neu[0].id;
  app.textContent = '';
  app.appendChild(el('header', { class: 'top' },
    el('div', { class: 'brand' }, el('span', { class: 'logo', 'aria-hidden': 'true' }), 'Physiologie'),
    el('nav', { class: 'tabs' }, TABS.map(function (t) {
      return el('a', { href: '#/' + t[0], 'data-tab': t[0], 'aria-current': t[0] === tab ? 'page' : null },
        t[1], t[0] === 'neu' && neuNeu ? el('span', { class: 'dot', 'aria-label': 'neu' }) : null);
    }))));
  var main = el('main', { 'data-view': view }, inhalt);
  app.appendChild(main);
  return main;
}
function zurueck(href, text) { return el('a', { class: 'zurueck', href: href, text: '← ' + text }); }

function razzien(list) {
  var r = {};
  list.forEach(function (x) { (r[x.razzia] = r[x.razzia] || []).push(x); });
  return Object.keys(r).sort(function (a, b) { return a - b; }).map(function (k) { return [k, r[k]]; });
}

function vLernen() {
  shell('lernen', 'lernen', [
    el('h1', { text: 'Lernen' }),
    D.themen.length ? razzien(D.themen).map(function (g) {
      return el('section', { class: 'gruppe' }, el('h2', { text: g[0] + '. Razzia' }),
        el('div', { class: 'karten' }, g[1].map(function (t) {
          return el('a', { class: 'karte-l thema-link', href: '#/lernen/' + t.id, 'data-thema': t.id },
            el('span', { class: 'k-t', text: t.titel }),
            el('span', { class: 'k-m', text: t.bereich + (t.fragen.length ? ' · ' + plural(t.fragen.length, 'Frage', 'Fragen') : '') }),
            t.kurz ? el('span', { class: 'k-k', text: t.kurz }) : null);
        })));
    }) : el('p', { class: 'leer', text: 'Noch keine Themen.' })
  ]);
}

function vThema(t) {
  var secs = t.lern.map(function (a) { return abschnitt(a); });
  var heads = t.lern.map(function (a, i) { return [a.h, secs[i]]; }).filter(function (x) { return x[0]; });
  shell('lernen', 'thema', [
    zurueck('#/lernen', 'Alle Themen'),
    el('h1', { text: t.titel }),
    el('p', { class: 'meta', text: t.bereich + ' · ' + t.razzia + '. Razzia' }),
    heads.length > 2 ? el('nav', { class: 'inhalt', 'aria-label': 'Inhalt' }, heads.map(function (x) {
      return el('button', { type: 'button', on: { click: function () { x[1].scrollIntoView({ behavior: 'smooth', block: 'start' }); } } },
        x[0].replace(/\*\*/g, ''));
    })) : null,
    secs,
    t.fragen.length ? el('div', { class: 'thema-fragen' },
      el('a', { href: '#/fragen/thema/' + t.id, text: 'Fragen zu diesem Thema (' + t.fragen.length + ') →' })) : null
  ]);
}

function fragenListe(fragen, offenId) {
  var stand = store.get('stand', {}), vorAbb = null, vorNr = null;
  return el('div', { class: 'fragen' }, fragen.map(function (f) {
    var abbKey = f.abb ? JSON.stringify(f.abb) : null, wieBei = abbKey && abbKey === vorAbb ? vorNr : null;
    if (abbKey && !wieBei) { vorAbb = abbKey; vorNr = f.nr; }
    if (!abbKey) vorAbb = null;
    var s = stand[f.id], th = THEMA[f.thema];
    var box = el('div', { class: 'frage' + (f.id === offenId ? ' offen' : ''), 'data-id': f.id });
    box.appendChild(el('button', { type: 'button', class: 'frage-f', 'aria-expanded': f.id === offenId ? 'true' : 'false',
      on: { click: function () { var o = box.classList.toggle('offen'); this.setAttribute('aria-expanded', o); alleText(); } } },
      el('span', { class: 'nr', text: f.nr }), el('span', { class: 'ft' }, rich(f.f)),
      s ? el('span', { class: 'st' + (s.ok ? ' ok' : ''), title: s.ok ? 'schon gewusst' : 'noch üben', text: s.ok ? '✓' : '•' }) : null));
    var ab = abbildung(f, wieBei);
    if (ab) box.appendChild(ab);
    box.appendChild(el('div', { class: 'frage-meta' },
      th ? el('a', { class: 'zum-thema', href: '#/lernen/' + th.id, text: th.titel }) : null,
      f.korr ? el('span', { class: 'korr-tag', text: '✎ korrigiert' }) : null));
    box.appendChild(antwort(f));
    return box;
  }));
}
function alleText() {
  var b = document.getElementById('alle');
  if (!b) return;
  var zu = document.querySelectorAll('.frage:not(.offen)').length;
  b.textContent = zu ? 'Alle aufdecken' : 'Alle verdecken';
}
function alleKnopf() {
  return el('button', { type: 'button', id: 'alle', class: 'knopf leise', on: { click: function () {
    var zu = document.querySelectorAll('.frage:not(.offen)').length > 0;
    document.querySelectorAll('.frage').forEach(function (f) { f.classList.toggle('offen', zu); f.querySelector('.frage-f').setAttribute('aria-expanded', zu); });
    alleText();
  } } }, 'Alle aufdecken');
}

function vFragen() {
  var stand = store.get('stand', {});
  function gewusst(list) { return list.filter(function (f) { return stand[f.id] && stand[f.id].ok; }).length; }
  shell('fragen', 'fragen', [
    el('h1', { text: 'Fragen' }),
    D.fragensets.length ? el('section', { class: 'gruppe' }, el('h2', { text: 'Fragensammlungen' }),
      el('div', { class: 'karten' }, D.fragensets.map(function (s) {
        return el('a', { class: 'karte-l set-link', href: '#/fragen/' + s.id, 'data-set': s.id },
          el('span', { class: 'k-t', text: s.titel }),
          el('span', { class: 'k-m', text: plural(s.fragen.length, 'Frage', 'Fragen') + ' · ' + gewusst(s.fragen) + ' gewusst' }),
          s.kurz ? el('span', { class: 'k-k', text: s.kurz }) : null);
      }))) : el('p', { class: 'leer', text: 'Noch keine Fragen.' }),
    el('section', { class: 'gruppe' }, el('h2', { text: 'Nach Thema' }),
      el('div', { class: 'karten' }, D.themen.filter(function (t) { return t.fragen.length; }).map(function (t) {
        return el('a', { class: 'karte-l', href: '#/fragen/thema/' + t.id },
          el('span', { class: 'k-t', text: t.titel }),
          el('span', { class: 'k-m', text: plural(t.fragen.length, 'Frage', 'Fragen') + ' · ' + gewusst(t.fragen) + ' gewusst' }));
      })))
  ]);
}

function vSet(titel, sub, fragen, offenId, back) {
  shell('fragen', 'set', [
    zurueck(back || '#/fragen', 'Alle Fragen'),
    el('h1', { text: titel }),
    el('p', { class: 'meta', text: sub }),
    el('div', { class: 'leiste' }, el('span', { class: 'hinweis', text: 'Frage antippen zum Aufdecken' }), alleKnopf()),
    fragenListe(fragen, offenId)
  ]);
  alleText();
  if (offenId) {
    var n = document.querySelector('.frage[data-id="' + offenId + '"]');
    if (n) setTimeout(function () { n.scrollIntoView({ block: 'start' }); }, 0);
  }
}

/* ---------- Abfragen ---------- */
var Q = null; /* laufende Abfrage */
function mischen(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
var wahl = null;
function vAbfragen() {
  if (Q && !Q.fertig) return vKarte();
  if (!wahl) { wahl = {}; D.themen.forEach(function (t) { if (t.fragen.length) wahl[t.id] = true; }); }
  var nurUnsicher = { v: false };
  var themen = D.themen.filter(function (t) { return t.fragen.length; });
  shell('abfragen', 'abfragen', [
    el('h1', { text: 'Abfragen' }),
    el('p', { class: 'meta', text: 'Wähle die Themen. Die Fragen kommen gemischt. Was du nicht wusstest, kommt am Ende noch einmal.' }),
    themen.length ? razzien(themen).map(function (g) {
      return el('fieldset', { class: 'wahl' }, el('legend', { text: g[0] + '. Razzia' }), g[1].map(function (t) {
        return el('label', null, el('input', { type: 'checkbox', checked: !!wahl[t.id], on: { change: function () { wahl[t.id] = this.checked; } } }),
          el('span', { text: t.titel }), el('span', { class: 'anz', text: t.fragen.length }));
      }));
    }) : null,
    el('label', { class: 'opt' }, el('input', { type: 'checkbox', on: { change: function () { nurUnsicher.v = this.checked; } } }),
      el('span', { text: 'Nur Fragen, die ich noch nicht gewusst habe' })),
    el('div', { class: 'meldung' }),
    el('button', { type: 'button', id: 'start', class: 'knopf', text: 'Los geht’s', on: { click: function () {
      var stand = store.get('stand', {});
      var fr = [];
      themen.forEach(function (t) { if (wahl[t.id]) fr = fr.concat(t.fragen); });
      if (nurUnsicher.v) fr = fr.filter(function (f) { return !(stand[f.id] && stand[f.id].ok); });
      if (!fr.length) {
        var m = document.querySelector('.meldung');
        m.textContent = '';
        m.appendChild(el('p', { class: 'leer', text: nurUnsicher.v ? 'In dieser Auswahl hast du schon alles gewusst.' : 'Bitte mindestens ein Thema wählen.' }));
        return;
      }
      starte(fr);
    } } })
  ]);
}
function starte(fr) {
  Q = { reihe: mischen(fr.slice()), n: fr.length, erst: {}, gewusst: 0, fertig: false };
  vKarte();
}
function vKarte() {
  if (!Q.reihe.length) { Q.fertig = true; return vEnde(); }
  var f = Q.reihe[0], th = THEMA[f.thema];
  var done = Q.n - new Set(Q.reihe.map(function (x) { return x.id; })).size;
  var ant = antwort(f), knoepfe;
  function bewerte(ok) {
    var stand = store.get('stand', {}), s = stand[f.id] || { ok: 0, nochmal: 0 };
    if (ok) s.ok++; else s.nochmal++;
    s.t = Date.now();
    stand[f.id] = s;
    store.set('stand', stand);
    if (!(f.id in Q.erst)) { Q.erst[f.id] = ok; if (ok) Q.gewusst++; }
    Q.reihe.shift();
    if (!ok) Q.reihe.push(f);
    vKarte();
    window.scrollTo(0, 0);
  }
  knoepfe = el('div', { class: 'k-knoepfe', hidden: true },
    el('button', { type: 'button', id: 'nochmal', class: 'knopf leise', text: 'Nochmal', on: { click: function () { bewerte(false); } } }),
    el('button', { type: 'button', id: 'gewusst', class: 'knopf', text: 'Gewusst', on: { click: function () { bewerte(true); } } }));
  var zeigen = el('button', { type: 'button', id: 'zeigen', class: 'knopf', text: 'Antwort zeigen', on: { click: function () {
    karte.classList.add('offen'); zeigen.hidden = true; knoepfe.hidden = false;
  } } });
  var karte = el('div', { class: 'karte' },
    el('div', { class: 'k-meta' }, el('span', { text: done + ' von ' + Q.n + ' geschafft' }), th ? el('span', { text: th.titel }) : null),
    el('div', { class: 'k-frage' }, rich(f.f)), abbildung(f), ant);
  shell('abfragen', 'karte', [
    el('div', { class: 'fortschritt' }, el('div', { style: 'width:' + (done / Q.n * 100).toFixed(1) + '%' })),
    karte, zeigen, knoepfe,
    el('button', { type: 'button', class: 'link', text: 'Abfrage beenden', on: { click: function () { Q = null; vAbfragen(); } } })
  ]);
}
function vEnde() {
  var falsch = Object.keys(Q.erst).filter(function (id) { return !Q.erst[id]; }).map(function (id) { return FRAGE[id]; });
  shell('abfragen', 'ende', [
    el('div', { class: 'ende' },
      el('h1', { text: 'Geschafft!' }),
      el('p', { class: 'gross', text: Q.gewusst + ' von ' + Q.n + ' beim ersten Mal gewusst' }),
      falsch.length ? el('div', null, el('h2', { text: 'Diese solltest du noch üben' }),
        el('ul', null, falsch.map(function (f) { return el('li', null, el('a', { href: '#/fragen/' + f.set + '/' + f.id }, rich(f.f))); }))) : null,
      el('div', { class: 'leiste' },
        falsch.length ? el('button', { type: 'button', class: 'knopf', text: 'Die ' + falsch.length + ' üben', on: { click: function () { starte(falsch); } } }) : null,
        el('button', { type: 'button', class: 'knopf leise', text: 'Neue Abfrage', on: { click: function () { Q = null; vAbfragen(); } } })))
  ]);
}

/* ---------- Suche ---------- */
function norm1(c) {
  var l = c.toLowerCase();
  if (l === 'ß') return 'ss';
  return l.normalize('NFD').replace(/[̀-ͯ]/g, '');
}
function normMap(s) { var out = '', map = []; for (var i = 0; i < s.length; i++) { var n = norm1(s[i]); for (var j = 0; j < n.length; j++) { out += n[j]; map.push(i); } } return { s: out, map: map }; }
function woerter(q) { return normMap(q).s.split(/[^a-z0-9]+/).filter(Boolean); }
function textVon(a) {
  var t = [];
  (function walk(x) { if (typeof x === 'string') t.push(x.replace(/\*\*/g, '')); else if (Array.isArray(x)) x.forEach(walk); else if (x && typeof x === 'object') for (var k in x) if (k !== 'q' && k !== 'loop') walk(x[k]); })(a);
  return t.join(' · ');
}
var INDEX = null;
function index() {
  if (INDEX) return INDEX;
  INDEX = [];
  D.themen.forEach(function (t) { var txt = t.titel + ' · ' + textVon(t.lern); INDEX.push({ art: 'Lernseite', titel: t.titel, href: '#/lernen/' + t.id, txt: txt, n: normMap(txt) }); });
  D.fragensets.forEach(function (s) { s.fragen.forEach(function (f) {
    var txt = f.f + ' · ' + textVon(f.abb || []) + ' · ' + textVon(f.a); INDEX.push({ art: s.titel + ', Frage ' + f.nr, titel: f.f.replace(/\*\*/g, ''), href: '#/fragen/' + s.id + '/' + f.id, txt: txt, n: normMap(txt) });
  }); });
  return INDEX;
}
var suchText = '';
function vSuche() {
  var res = el('div', { class: 'ergebnis' });
  var inp = el('input', { id: 'q', type: 'search', placeholder: 'z. B. Glykolyse, Laktat, Herzzeitvolumen', autocomplete: 'off', value: suchText });
  var tm;
  inp.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(function () { suchText = inp.value; zeige(); }, 120); });
  function zeige() {
    res.textContent = '';
    var w = woerter(suchText);
    if (!suchText.trim()) { res.appendChild(el('p', { class: 'hinweis', text: 'Durchsucht alle Lernseiten, Fragen und Antworten.' })); return; }
    if (!w.length) { res.appendChild(el('p', { class: 'leer', text: 'Bitte ein Wort mit Buchstaben oder Zahlen eingeben.' })); return; }
    var hits = index().filter(function (e) { return w.every(function (x) { return e.n.s.indexOf(x) >= 0; }); });
    if (!hits.length) { res.appendChild(el('p', { class: 'leer', text: 'Nichts gefunden.' })); return; }
    res.appendChild(el('p', { class: 'hinweis', text: plural(hits.length, 'Treffer', 'Treffer') }));
    hits.slice(0, 80).forEach(function (e) {
      var p = e.n.s.indexOf(w[0]), a = e.n.map[p], b = e.n.map[p + w[0].length - 1] + 1;
      var s0 = Math.max(0, a - 60), s1 = Math.min(e.txt.length, b + 80);
      res.appendChild(el('a', { class: 'treffer', href: e.href },
        el('span', { class: 'k-m', text: e.art }), el('span', { class: 'k-t', text: e.titel }),
        el('span', { class: 'snip' }, (s0 ? '…' : '') + e.txt.slice(s0, a), el('mark', { text: e.txt.slice(a, b) }), e.txt.slice(b, s1) + (s1 < e.txt.length ? '…' : ''))));
    });
  }
  shell('suche', 'suche', [el('h1', { text: 'Suche' }), inp, res]);
  zeige();
  inp.focus();
}

/* ---------- Neu ---------- */
function vNeu() {
  if (D.neu.length) store.set('neu', D.neu[0].id);
  shell('neu', 'neu', [el('h1', { text: 'Neu' }), D.neu.map(function (n) {
    return el('article', { class: 'neu-eintrag' }, el('p', { class: 'meta', text: n.datum }), el('h2', { text: n.titel }), liste(n.punkte));
  })]);
}

/* ---------- Router ---------- */
function route() {
  var h = location.hash.replace(/^#\/?/, '').split('/').map(decodeURIComponent);
  var top = h[0] || 'lernen';
  if (top !== 'abfragen' && Q && Q.fertig) Q = null;
  if (top === 'lernen' && !h[1]) return vLernen();
  if (top === 'lernen' && THEMA[h[1]]) return vThema(THEMA[h[1]]);
  if (top === 'fragen' && !h[1]) return vFragen();
  if (top === 'fragen' && h[1] === 'thema' && THEMA[h[2]]) {
    var t = THEMA[h[2]];
    return vSet(t.titel, 'Fragen aus allen Sammlungen zu diesem Thema', t.fragen, null, '#/fragen');
  }
  if (top === 'fragen' && SET[h[1]]) {
    var s = SET[h[1]];
    return vSet(s.titel, s.razzia + '. Razzia · ' + plural(s.fragen.length, 'Frage', 'Fragen'), s.fragen, FRAGE[h[2]] ? h[2] : null);
  }
  if (top === 'abfragen') return vAbfragen();
  if (top === 'suche') return vSuche();
  if (top === 'neu') return vNeu();
  location.replace('#/lernen');
}
window.addEventListener('hashchange', function () { route(); if (!/^#\/fragen\/[^/]+\/./.test(location.hash)) window.scrollTo(0, 0); });
route();
})();
