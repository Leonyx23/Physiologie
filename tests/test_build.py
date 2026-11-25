import copy, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402

FIX = ROOT / 'tests' / 'fixtures' / 'inhalt'


def data():
    return copy.deepcopy(build.load(FIX))


def test_load_finds_everything():
    d = data()
    assert [t['id'] for t in d['themen']] == ['energie']
    assert [s['id'] for s in d['fragensets']] == ['test']
    assert set(d['quellen']) == {'A', 'B'}
    assert d['neu'][0]['id'] == '2026-11-26-start'


def test_validate_ok():
    assert build.validate(data()) == []


def test_unknown_key():
    d = data()
    d['themen'][0]['lern'].append(dict(h='x', zz=1))
    errs = build.validate(d)
    assert any('zz' in e for e in errs)


def test_bad_source_key():
    d = data()
    d['fragensets'][0]['fragen'][0]['q'] = [('X', 1)]
    assert any("'X'" in e for e in build.validate(d))


def test_source_page_out_of_range():
    d = data()
    d['fragensets'][0]['fragen'][0]['q'] = [('B', 4)]
    assert any('Seite 4' in e for e in build.validate(d))


def test_page_range_string_ok_and_checked():
    d = data()
    d['fragensets'][0]['fragen'][0]['q'] = [('A', '2–4')]
    assert build.validate(d) == []
    d['fragensets'][0]['fragen'][0]['q'] = [('A', '9–11')]
    assert any('Seite' in e for e in build.validate(d))


def test_dup_id():
    d = data()
    d['fragensets'][0]['fragen'][1]['id'] = 't1'
    assert any('t1' in e and 'doppelt' in e for e in build.validate(d))


def test_table_width():
    d = data()
    d['themen'][0]['lern'][1]['tb'].append(['nur eins'])
    assert any('Tabelle' in e for e in build.validate(d))


def test_frage_without_source():
    d = data()
    d['fragensets'][0]['fragen'][0]['q'] = []
    assert any('Quelle' in e for e in build.validate(d))


def test_frage_unknown_thema():
    d = data()
    d['fragensets'][0]['fragen'][0]['thema'] = 'gibtsnicht'
    assert any('gibtsnicht' in e for e in build.validate(d))


def test_bar_value_must_be_number():
    d = data()
    d['themen'][0]['lern'][5]['br']['s'][0][1] = 'viel'
    assert any('Balken' in e for e in build.validate(d))


def test_abb_checked_like_sections():
    d = data()
    d['fragensets'][0]['fragen'][2]['abb'] = [dict(h='x', yy=1)]
    assert any('yy' in e for e in build.validate(d))


def test_nr_must_be_text():
    d = data()
    d['fragensets'][0]['fragen'][2]['nr'] = ''
    assert any('nr' in e for e in build.validate(d))


def test_build_embeds_json(tmp_path):
    out = build.build(FIX, tmp_path)
    html = (tmp_path / 'vorschau.html').read_text(encoding='utf-8')
    assert out == tmp_path / 'vorschau.html'
    assert html.lower().startswith('<!doctype html>')
    m = re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S)
    assert m, 'Datenblock fehlt'
    assert '</script>' not in m.group(1)
    payload = json.loads(m.group(1))
    assert payload['themen'][0]['titel'] == 'Energiestoffwechsel'
    assert 'Test </script> bleibt Text.' in json.dumps(payload, ensure_ascii=False)
    pwa = (tmp_path / 'pwa_plain.html').read_text(encoding='utf-8')
    assert 'manifest.webmanifest' in pwa and "serviceWorker" in pwa


def test_build_refuses_invalid(tmp_path):
    bad = tmp_path / 'inhalt'
    bad.mkdir()
    for f in FIX.iterdir():
        if f.suffix == '.py':
            (bad / f.name).write_text(f.read_text(encoding='utf-8'), encoding='utf-8')
    (bad / 'fragen_test.py').write_text(
        (FIX / 'fragen_test.py').read_text(encoding='utf-8').replace("q=[('A', 3)]", "q=[]"), encoding='utf-8')
    try:
        build.build(bad, tmp_path / 'out')
    except build.InhaltFehler as e:
        assert 'Quelle' in str(e)
    else:
        raise AssertionError('ungültige Inhalte wurden gebaut')
