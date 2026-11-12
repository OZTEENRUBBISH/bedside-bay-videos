"""Photo set 001 — five illustrated slides of the career climb."""
import os, skia
from lib import *
import scenes
os.makedirs('out', exist_ok=True)
S = [
    (lambda c: scenes.poor(c, 1.8), ['Broke intern', 'to ED Director'], '#ffffff', (0, 2000, 1)),
    (lambda c: scenes.er(c, 2.2, 'resident'), ['Solve cases.', 'Get promoted.'], INK, (1, 18400, 2)),
    (lambda c: scenes.theatre(c, 2.3), ['Unlock the', 'big surgeries.'], '#ffffff', (3, 264000, 4)),
    (lambda c: scenes.rich(c, 2.6, car_in=False), ['Then live like', 'an ED Director.'], '#ffffff', (4, 2480000, 5)),
    (lambda c: scenes.cta(c, 2.5), None, None, None),
]
for i, (fn, hl, col, h) in enumerate(S):
    s = new_surface(); c = s.getCanvas(); fn(c)
    if hl:
        headline(c, hl, 356, 92, col, shadow=0 if col == INK else .35)
        hud(c, *h); brand_bar(c)
        if i == 0:
            w = 300; rr(c, 720, 1516, w, 76, 38, P(GOLD)); text(c, 'Swipe  >', 720 + w / 2, 1568, 40, INK, 900, 'c')
        if i == 3:
            for l, x, y in (('Mansion', 300, 578), ('Supercar', 330, 1044), ('Gold watch', 780, 590)):
                ww = tw(l, 36) + 60; rr(c, x - ww / 2, y - 38, ww, 68, 34, P(GOLD)); text(c, l, x, y + 8, 36, INK, 900, 'c')
    s.makeImageSnapshot().save(f'out/tmp{i}.png', skia.kPNG)
    from PIL import Image
    Image.open(f'out/tmp{i}.png').convert('RGB').save(f'out/photo001_{i+1}.jpg', quality=92); os.remove(f'out/tmp{i}.png')
from PIL import Image
sh = Image.new('RGB', (324 * 5, 576))
for i in range(5): sh.paste(Image.open(f'out/photo001_{i+1}.jpg').resize((324, 576)), (i * 324, 0))
sh.save('prev/csheet.jpg', quality=85)
