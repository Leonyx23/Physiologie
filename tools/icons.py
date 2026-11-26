"""Erzeugt die App-Icons (türkises Feld mit EKG-Linie). Aufruf: python3 tools/icons.py"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


def icon(size):
    s = 4  # Supersampling für glatte Kanten
    n = size * s
    im = Image.new('RGBA', (n, n), (14, 106, 115, 255))
    d = ImageDraw.Draw(im)
    pts = [(0.10, 0.55), (0.32, 0.55), (0.40, 0.33), (0.52, 0.76), (0.62, 0.42), (0.70, 0.55), (0.90, 0.55)]
    d.line([(x * n, y * n) for x, y in pts], fill=(255, 255, 255, 255), width=int(0.075 * n), joint='curve')
    r = int(0.0375 * n)
    for x, y in (pts[0], pts[-1]):
        d.ellipse([x * n - r, y * n - r, x * n + r, y * n + r], fill=(255, 255, 255, 255))
    return im.resize((size, size), Image.LANCZOS)


if __name__ == '__main__':
    for sz in (180, 192, 512):
        icon(sz).save(ROOT / f'icon-{sz}.png')
        print('icon', sz)
