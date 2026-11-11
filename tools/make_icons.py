"""Draw the app icon (a flip-clock card reading 251 under the orange snooze bar) at every size the app needs.

    python3 tools/make_icons.py      # needs Pillow and the DejaVu Sans Condensed Bold font
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = subprocess.check_output(["fc-match", "-f", "%{file}", "DejaVu Sans Condensed:bold"]).decode()
N = 1024
hexrgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def gradient(w, h, top, bot):
    g = Image.new("RGB", (w, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return g

def icon(pad):
    """pad: share of the canvas kept clear around the artwork (Android's maskable icons need more)."""
    img = gradient(N, N, hexrgb("#f6f0e3"), hexrgb("#d6c9ae"))
    inner, oy = N * (1 - 2 * pad), N * pad
    bw, bh = inner * .5, inner * .085
    bx, by = N / 2 - bw / 2, oy + inner * .10
    bar = gradient(int(bw), int(bh), hexrgb("#f0bd62"), hexrgb("#b97d22"))
    m = Image.new("L", bar.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, bar.size[0]-1, bar.size[1]-1], radius=int(bh*.45), fill=255)
    img.paste(bar, (int(bx), int(by)), m)
    fw, fh = inner * .74, inner * .62
    fx, fy = N / 2 - fw / 2, by + bh + inner * .05
    sh = Image.new("L", (N, N), 0)
    ImageDraw.Draw(sh).rounded_rectangle([fx, fy + inner*.02, fx + fw, fy + fh + inner*.02], radius=int(fw*.09), fill=150)
    img.paste((40, 34, 28), (0, 0), sh.filter(ImageFilter.GaussianBlur(N*.02)))
    card = gradient(int(fw), int(fh), hexrgb("#3a3633"), hexrgb("#222020"))
    cm = Image.new("L", card.size, 0); ImageDraw.Draw(cm).rounded_rectangle([0, 0, card.size[0]-1, card.size[1]-1], radius=int(fw*.09), fill=255)
    img.paste(card, (int(fx), int(fy)), cm)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, int(fh * .78))
    tb = d.textbbox((0, 0), "251", font=font)
    layer = Image.new("RGBA", (tb[2]-tb[0]+20, tb[3]-tb[1]+20), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((10 - tb[0], 10 - tb[1]), "251", font=font, fill=hexrgb("#f1ead8") + (255,))
    layer = layer.resize((int(layer.width * .78), layer.height), Image.LANCZOS)
    img.paste(layer, (int(N/2 - layer.width/2), int(fy + fh/2 - layer.height/2)), layer)
    hy = fy + fh / 2
    d.rectangle([fx, hy - N*.004, fx + fw, hy + N*.004], fill=(12, 11, 10))
    for nx in (fx - N*.008, fx + fw - N*.008):
        d.rounded_rectangle([nx, hy - N*.022, nx + N*.016, hy + N*.022], radius=int(N*.006), fill=(70, 64, 58))
    return img

full, mask = icon(.06), icon(.14)
for name, size, src in [("apple-touch-icon.png", 180, full), ("icon-192.png", 192, full), ("icon-512.png", 512, full),
                        ("icon-maskable-512.png", 512, mask), ("favicon.png", 64, full)]:
    src.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name), optimize=True)
print("icons written")
