"""Baut die App und legt sie als index.html ins Repository (für GitHub Pages).
Aufruf: python3 tools/publish.py  – danach prüfen, committen, pushen (nur mit OK der Nutzerin)."""
import shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import build  # noqa: E402

if __name__ == '__main__':
    build.build(ROOT / 'inhalt', ROOT / 'build')
    shutil.copyfile(ROOT / 'build' / 'pwa_plain.html', ROOT / 'index.html')
    print('index.html', round((ROOT / 'index.html').stat().st_size / 1024), 'KB')
