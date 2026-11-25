"""Baut die Physiologie-App aus den Inhaltsdateien.

Aufruf: python3 tools/build.py [inhalt-ordner] [ausgabe-ordner]
Schreibt vorschau.html (zum Ansehen) und pwa_plain.html (Grundlage für die verschlüsselte Web-App).
"""
import importlib.util, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / 'app'

ABSCHNITT = {'h', 'li', 'tb', 'tc', 'fl', 'br', 'ly', 'm', 'q'}
INHALT_KEYS = ABSCHNITT - {'h', 'q'}
THEMA_KEYS = {'id', 'titel', 'bereich', 'razzia', 'lern', 'kurz'}
SET_KEYS = {'id', 'titel', 'razzia', 'fragen', 'kurz'}
FRAGE_KEYS = {'id', 'nr', 'thema', 'f', 'abb', 'a', 'q', 'korr'}


class InhaltFehler(Exception):
    pass


def _modul(path):
    spec = importlib.util.spec_from_file_location('inhalt_' + path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(src_dir):
    src = Path(src_dir)
    themen = [_modul(p).THEMA for p in sorted(src.glob('thema_*.py'))]
    sets = [_modul(p).FRAGEN for p in sorted(src.glob('fragen_*.py'))]
    return dict(themen=themen, fragensets=sets,
                quellen=_modul(src / 'quellen.py').QUELLEN,
                neu=_modul(src / 'neu.py').NEU)


def _seiten(s):
    if isinstance(s, int):
        return [s]
    nums = [int(x) for x in re.findall(r'\d+', str(s))]
    if not nums:
        raise ValueError(s)
    return nums


def _quellen(q, quellen, wo, err):
    for item in q:
        if not (isinstance(item, (tuple, list)) and len(item) == 2):
            err.append(f'{wo}: Quelle muss (Kürzel, Seite) sein: {item!r}')
            continue
        k, s = item
        if k not in quellen:
            err.append(f'{wo}: unbekannte Quelle {k!r}')
            continue
        try:
            nums = _seiten(s)
        except ValueError:
            err.append(f'{wo}: Seite {s!r} ist keine Zahl')
            continue
        for n in nums:
            if not 1 <= n <= quellen[k]['seiten']:
                err.append(f'{wo}: Seite {n} gibt es in {k} nicht (hat {quellen[k]["seiten"]})')


def _text(x):
    return isinstance(x, str) and x.strip() != ''


def _abschnitte(lst, quellen, wo, err):
    if not isinstance(lst, list) or not lst:
        err.append(f'{wo}: keine Abschnitte')
        return
    for i, a in enumerate(lst):
        w = f'{wo} Abschnitt {i + 1}'
        if not isinstance(a, dict):
            err.append(f'{w}: kein dict')
            continue
        for k in a:
            if k not in ABSCHNITT:
                err.append(f'{w}: unbekannter Schlüssel {k!r}')
        if not INHALT_KEYS & set(a):
            err.append(f'{w}: kein Inhalt')
        if 'h' in a and not _text(a['h']):
            err.append(f'{w}: leere Überschrift')
        if 'li' in a:
            for p in a['li']:
                if isinstance(p, list):
                    if not p or not all(_text(x) for x in p):
                        err.append(f'{w}: leerer Unterpunkt')
                elif not _text(p):
                    err.append(f'{w}: leerer Punkt')
        for tk in ('tb', 'tc'):
            if tk in a:
                t = a[tk]
                if not (isinstance(t, list) and len(t) >= 2):
                    err.append(f'{w}: Tabelle braucht Kopf und Zeilen')
                    continue
                n = len(t[0])
                for r, row in enumerate(t[1:], 2):
                    if len(row) != n:
                        err.append(f'{w}: Tabelle Zeile {r} hat {len(row)} statt {n} Spalten')
        if 'fl' in a:
            s = a['fl'].get('s') if isinstance(a['fl'], dict) else None
            if not s or not all(isinstance(x, list) and 1 <= len(x) <= 3 and _text(x[0]) for x in s):
                err.append(f'{w}: Ablaufkette braucht s=[[Titel, Untertitel?, Pfeiltext?], …]')
        if 'br' in a:
            s = a['br'].get('s') if isinstance(a['br'], dict) else None
            ok = s and all(isinstance(x, list) and len(x) == 3 and _text(x[0])
                           and isinstance(x[1], (int, float)) and x[1] >= 0 for x in s)
            if not ok:
                err.append(f'{w}: Balken brauchen [Label, Zahl ≥ 0, Anzeige]')
        if 'ly' in a:
            s = a['ly'].get('s') if isinstance(a['ly'], dict) else None
            if not s or not all(isinstance(x, list) and 1 <= len(x) <= 2 and _text(x[0]) for x in s):
                err.append(f'{w}: Schichtbild braucht s=[[Name, Notiz?], …]')
        if 'm' in a:
            m = a['m']
            if not (_text(m) or (isinstance(m, list) and m and all(_text(x) for x in m))):
                err.append(f'{w}: leerer Merke-Kasten')
        if 'q' in a:
            _quellen(a['q'], quellen, w, err)


def validate(d):
    err = []
    quellen = d['quellen']
    for k, q in quellen.items():
        if not (_text(q.get('t')) and isinstance(q.get('seiten'), int)):
            err.append(f'Quelle {k}: braucht t und seiten')
    ids = {}

    def seen(i, wo):
        if i in ids:
            err.append(f'{wo}: id {i!r} doppelt (auch in {ids[i]})')
        ids[i] = wo

    themen = set()
    for t in d['themen']:
        wo = f'Thema {t.get("id")}'
        for k in t:
            if k not in THEMA_KEYS:
                err.append(f'{wo}: unbekannter Schlüssel {k!r}')
        for k in ('id', 'titel', 'bereich'):
            if not _text(t.get(k)):
                err.append(f'{wo}: {k} fehlt')
        if not isinstance(t.get('razzia'), int):
            err.append(f'{wo}: razzia muss eine Zahl sein')
        seen(t.get('id'), wo)
        themen.add(t.get('id'))
        _abschnitte(t.get('lern'), quellen, wo, err)
    for s in d['fragensets']:
        wo = f'Fragen {s.get("id")}'
        for k in s:
            if k not in SET_KEYS:
                err.append(f'{wo}: unbekannter Schlüssel {k!r}')
        if not _text(s.get('titel')) or not isinstance(s.get('razzia'), int):
            err.append(f'{wo}: titel/razzia fehlt')
        seen(s.get('id'), wo)
        for f in s.get('fragen') or []:
            fw = f'{wo} Frage {f.get("id")}'
            for k in f:
                if k not in FRAGE_KEYS:
                    err.append(f'{fw}: unbekannter Schlüssel {k!r}')
            seen(f.get('id'), fw)
            if not _text(f.get('f')):
                err.append(f'{fw}: Fragetext fehlt')
            if f.get('thema') not in themen:
                err.append(f'{fw}: Thema {f.get("thema")!r} gibt es nicht')
            _abschnitte(f.get('a'), quellen, fw, err)
            if 'abb' in f:
                _abschnitte(f['abb'], quellen, fw + ' Abbildung', err)
            if 'nr' in f and not _text(f['nr']):
                err.append(f'{fw}: nr muss ein Text sein')
            if not f.get('q'):
                err.append(f'{fw}: keine Quelle')
            else:
                _quellen(f['q'], quellen, fw, err)
            if 'korr' in f and not (isinstance(f['korr'], list) and all(_text(x) for x in f['korr'])):
                err.append(f'{fw}: korr muss eine Liste von Texten sein')
    for n in d['neu']:
        if not (_text(n.get('id')) and _text(n.get('titel')) and n.get('punkte')):
            err.append(f'Neu {n.get("id")}: id/titel/punkte fehlen')
    return err


def _json(d):
    out = dict(themen=d['themen'], fragensets=d['fragensets'], neu=d['neu'],
               quellen={k: dict(t=v['t'], seiten=v['seiten']) for k, v in d['quellen'].items()})
    s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
    return s.replace('<', '\\u003c')


PWA_HEAD = '''<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Physiologie">
'''
PWA_TAIL = ("<script>if('serviceWorker' in navigator&&location.protocol==='https:'){"
            "navigator.serviceWorker.register('sw.js').catch(function(){});}</script>\n")


def build(src_dir, out_dir, app_dir=APP):
    d = load(src_dir)
    err = validate(d)
    if err:
        raise InhaltFehler('\n'.join(err))
    app = Path(app_dir)
    shell = (app / 'shell.html').read_text(encoding='utf-8')
    for ph, f in (('/*CSS*/', 'style.css'), ('/*JS*/', 'app.js')):
        assert shell.count(ph) == 1, ph
        shell = shell.replace(ph, (app / f).read_text(encoding='utf-8'))
    assert shell.count('__DATA__') == 1
    html = shell.replace('__DATA__', _json(d))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'vorschau.html').write_text(html.replace('<!--PWA_HEAD-->', '').replace('<!--PWA_TAIL-->', ''),
                                       encoding='utf-8')
    (out / 'pwa_plain.html').write_text(html.replace('<!--PWA_HEAD-->', PWA_HEAD)
                                        .replace('<!--PWA_TAIL-->', PWA_TAIL), encoding='utf-8')
    return out / 'vorschau.html'


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else ROOT / 'inhalt'
    out = sys.argv[2] if len(sys.argv) > 2 else ROOT / 'build'
    try:
        p = build(src, out)
    except InhaltFehler as e:
        print('Fehler in den Inhalten:\n' + str(e))
        sys.exit(1)
    print('gebaut:', p, round(p.stat().st_size / 1024), 'KB')
