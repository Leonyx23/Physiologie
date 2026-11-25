"""Prüft die echten Inhalte (nur wenn inhalt/ vorhanden ist): Laden, Prüfen, jede Seite im Browser."""
import sys
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
INHALT = ROOT / 'inhalt'
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402

pytestmark = pytest.mark.skipif(not INHALT.exists(), reason='inhalt/ fehlt (nur verschlüsselt im Repo)')


def test_inhalt_gueltig():
    assert build.validate(build.load(INHALT)) == []


def test_jede_frage_hat_thema_mit_lernseite():
    d = build.load(INHALT)
    themen = {t['id'] for t in d['themen']}
    for s in d['fragensets']:
        for f in s['fragen']:
            assert f['thema'] in themen


@pytest.mark.parametrize('w,scheme', [(360, 'light'), (1100, 'dark')])
def test_alle_seiten_im_browser(tmp_path, w, scheme):
    url = build.build(INHALT, tmp_path).as_uri()
    d = build.load(INHALT)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport=dict(width=w, height=800), color_scheme=scheme)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        hashes = ['#/lernen', '#/fragen', '#/abfragen', '#/suche', '#/neu']
        hashes += ['#/lernen/' + t['id'] for t in d['themen']]
        hashes += ['#/fragen/' + s['id'] for s in d['fragensets']]
        for h in hashes:
            pg.goto(url + h)
            pg.wait_for_selector('#app main')
            if pg.locator('#alle').count():
                pg.click('#alle')
            wide = pg.evaluate('document.documentElement.scrollWidth - window.innerWidth')
            assert wide <= 0, f'{h} scrollt waagerecht um {wide}px'
        b.close()
    assert errs == []
