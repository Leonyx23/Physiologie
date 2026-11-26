"""Klickt die App im Browser durch (Playwright, Chromium)."""
import sys
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402

FIX = ROOT / 'tests' / 'fixtures' / 'inhalt'
SIZES = [(360, 740, 'light'), (430, 900, 'dark'), (1100, 800, 'light')]


@pytest.fixture(scope='module')
def url(tmp_path_factory):
    out = tmp_path_factory.mktemp('app')
    return build.build(FIX, out).as_uri()


@pytest.fixture(scope='module')
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


def new_page(browser, w=430, h=900, scheme='light', broken_storage=False):
    ctx = browser.new_context(viewport=dict(width=w, height=h), color_scheme=scheme)
    if broken_storage:
        ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blockiert')}})")
    pg = ctx.new_page()
    pg.errors = []
    pg.on('pageerror', lambda e: pg.errors.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and pg.errors.append(m.text))
    return pg


def go(pg, url, hash_):
    pg.goto(url + hash_)
    pg.wait_for_selector('#app main')


def no_overflow(pg):
    assert pg.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Seite scrollt waagerecht'


@pytest.mark.parametrize('w,h,scheme', SIZES)
def test_alle_reiter(browser, url, w, h, scheme):
    pg = new_page(browser, w, h, scheme)
    go(pg, url, '')
    for tab in ['lernen', 'razzia', 'abfragen', 'suche', 'neu']:
        pg.click(f'nav.tabs a[data-tab="{tab}"]')
        pg.wait_for_selector(f'main[data-view="{tab}"]')
        no_overflow(pg)
    assert pg.errors == []


@pytest.mark.parametrize('w,h,scheme', SIZES)
def test_lernseite(browser, url, w, h, scheme):
    pg = new_page(browser, w, h, scheme)
    go(pg, url, '#/lernen')
    assert pg.inner_text('section.abteilung h2') == 'Stoffwechsel'
    assert not any('Razzia' in h for h in pg.locator('main h2').all_inner_texts())
    assert pg.locator('section.abteilung').count() == 1  # leere Abteilung wird nicht gezeigt
    pg.click('.thema-link[data-thema="energie"]')
    pg.wait_for_selector('main[data-view="thema"]')
    assert pg.inner_text('main h1') == 'Energiestoffwechsel'
    assert 'Stoffwechsel' in pg.inner_text('main .meta')
    for sel in ['.abschnitt', '.fl', '.fl.loop', '.br', '.ly', '.merke', 'table', 'b']:
        assert pg.locator(sel).count() > 0, sel
    assert 'Test </script> bleibt Text.' in pg.inner_text('.merke')
    assert 'Testskript A, S. 2' in pg.inner_text('main')
    no_overflow(pg)
    pg.click('.thema-fragen a')
    pg.wait_for_selector('main[data-view="set"] .frage')
    assert pg.errors == []


def test_fragen_aufdecken(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/razzia')
    pg.wait_for_selector('main[data-view="razzia"]')
    pg.click('.set-link[data-set="test"]')
    pg.wait_for_selector('.frage[data-id="t1"]')
    assert not pg.is_visible('.frage[data-id="t1"] .antwort')
    pg.click('.frage[data-id="t1"] .frage-f')
    assert pg.is_visible('.frage[data-id="t1"] .antwort')
    assert 'Quelle: Testskript A, S. 3' in pg.inner_text('.frage[data-id="t1"]')
    assert pg.is_visible('.frage[data-id="t3"] .frage-abb')
    assert pg.inner_text('.frage[data-id="t3"] .nr') == 'III.6a'
    assert pg.locator('.frage[data-id="t4"] details.frage-abb:not([open])').count() == 1
    assert 'wie bei III.6a' in pg.inner_text('.frage[data-id="t4"] details.frage-abb summary')
    pg.click('#alle')
    assert pg.locator('.frage .antwort:visible').count() == 4
    assert 'korrigiert' in pg.inner_text('.frage[data-id="t2"] .korr').lower()
    pg.click('#alle')
    assert pg.locator('.frage .antwort:visible').count() == 0
    pg.click('.frage[data-id="t1"] .zum-thema')
    pg.wait_for_selector('main[data-view="thema"]')
    assert pg.errors == []


def test_abfragen_durchlauf(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/abfragen')
    pg.click('#start')
    seen, abb = 0, 0
    while pg.locator('.ende').count() == 0:
        pg.wait_for_selector('.karte .k-frage')
        if pg.locator('.karte .frage-abb').count():
            assert pg.is_visible('.karte .frage-abb')
            abb += 1
        pg.click('#zeigen')
        assert pg.is_visible('.karte .antwort')
        pg.click('#nochmal' if seen == 0 else '#gewusst')
        seen += 1
        assert seen < 10
    assert seen == 5  # 4 Fragen + 1 Wiederholung
    assert abb >= 1
    stand = pg.evaluate("JSON.parse(localStorage.getItem('physiologie.stand'))")
    assert set(stand) == {'t1', 't2', 't3', 't4'}
    assert pg.errors == []


def test_abfragen_nach_sammlung(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/abfragen')
    assert pg.inner_text('fieldset.wahl legend') == 'Testrazzia'
    assert pg.errors == []


def test_abfragen_leer(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/abfragen')
    for box in pg.locator('.wahl input:checked').all():
        box.uncheck()
    pg.click('#start')
    assert pg.locator('.leer').count() == 1
    assert pg.errors == []


@pytest.mark.parametrize('q,want', [('atp', True), ('Säure', True), ('saure', True), ('(', False),
                                    ('glykolyse', True), ('xyzxyz', False)])
def test_suche(browser, url, q, want):
    pg = new_page(browser)
    go(pg, url, '#/suche')
    pg.fill('#q', q)
    pg.wait_for_timeout(250)
    assert (pg.locator('.treffer').count() > 0) == want, q
    if not want:
        assert pg.locator('.leer').count() == 1
    assert pg.errors == []


def test_neu_punkt(browser, url):
    pg = new_page(browser)
    go(pg, url, '')
    assert pg.locator('nav.tabs a[data-tab="neu"] .dot').count() == 1
    pg.click('nav.tabs a[data-tab="neu"]')
    pg.wait_for_selector('.neu-eintrag')
    assert pg.locator('nav.tabs a[data-tab="neu"] .dot').count() == 0
    pg.reload()
    pg.wait_for_selector('#app main')
    assert pg.locator('nav.tabs a[data-tab="neu"] .dot').count() == 0


def test_falscher_link(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/lernen/gibtsnicht')
    pg.wait_for_selector('main[data-view="lernen"]')
    go(pg, url, '#/quatsch')
    pg.wait_for_selector('main[data-view="lernen"]')
    assert pg.errors == []


def test_ohne_speicher(browser, url):
    pg = new_page(browser, broken_storage=True)
    go(pg, url, '#/abfragen')
    pg.click('#start')
    pg.click('#zeigen')
    pg.click('#gewusst')
    pg.click('nav.tabs a[data-tab="neu"]')
    pg.wait_for_selector('.neu-eintrag')
    assert pg.errors == []


@pytest.mark.parametrize('scheme,textfarbe', [('light', 'rgb(22, 24, 29)'), ('dark', 'rgb(236, 238, 242)')])
def test_bild_auf_lernseite(browser, url, scheme, textfarbe):
    pg = new_page(browser, 360, 740, scheme)
    go(pg, url, '#/lernen/energie')
    fig = pg.locator('figure.bild')
    assert fig.count() == 1
    svg = fig.locator('svg')
    assert svg.get_attribute('role') == 'img'
    assert 'Probebild' in svg.get_attribute('aria-label') and '**' not in svg.get_attribute('aria-label')
    assert fig.locator('figcaption b').inner_text() == 'Kasten'
    assert pg.evaluate("getComputedStyle(document.querySelector('figure.bild text')).fill") == textfarbe
    rect = pg.evaluate("getComputedStyle(document.querySelector('figure.bild rect')).fill")
    assert rect not in ('rgb(0, 0, 0)', textfarbe)
    assert pg.evaluate("document.querySelector('figure.bild marker').id") == 'probe-p'
    # Bild steht direkt unter der Überschrift, vor dem Text
    assert pg.evaluate("document.querySelector('figure.bild').nextElementSibling.tagName") == 'UL'
    assert svg.bounding_box()['width'] <= 360
    no_overflow(pg)
    assert pg.errors == []


def test_suche_findet_bildunterschrift(browser, url):
    pg = new_page(browser)
    go(pg, url, '#/suche')
    pg.fill('#q', 'Probebild')
    pg.wait_for_selector('.treffer')
    assert 'Probebild' in pg.locator('.treffer').first.inner_text()
