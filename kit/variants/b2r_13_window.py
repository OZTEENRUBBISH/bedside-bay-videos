"""Broke to Rich variant 13 — "The view from his window at every rank." One window, five views: a brick wall for the
Intern, the hospital parking lot at night, city rooftops, a sunset skyline, then the ED Director's own driveway. The window
frame, the wall and Dr John Smith's outfit upgrade with every rank while the career card climbs. The views and the bank
amounts after the $2,000 start are illustrative. Music: bright.
Video: python3 b2r_13_window.py <out.mp4>          Preview: python3 b2r_13_window.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

WX, WY, WW, WH = 70, 540, 620, 640  # the window opening


def v_brick(c, t):
    c.drawRect(skia.Rect.MakeWH(WW, WH), P('#7a3f33'))
    for r in range(11):
        y = r * 60
        c.drawLine(0, y, WW, y, P('#5a2c24', stroke=6, cap=False))
        for x in range(-60 if r % 2 else 0, WW, 120): c.drawLine(x, y, x, y + 60, P('#5a2c24', stroke=6, cap=False))
    c.drawRect(skia.Rect.MakeXYWH(500, 0, 34, WH), P('#3d4650')); rr(c, 492, 300, 50, 22, 4, P('#2c343c'))  # drainpipe
    on = (t * 1.3 + .5) % 1 > .18 and (t * 7.1 + .5) % 1 > .12  # flickering sign
    a = 255 if on else 70
    rr(c, 60, 150, 380, 150, 16, P('#1b1418')); rr(c, 60, 150, 380, 150, 16, P('#ff5d8f', a, stroke=8))
    if on: c.drawRect(skia.Rect.MakeXYWH(40, 130, 420, 190), P('#ff5d8f', 50, blur=40))
    text(c, 'OPEN', 250, 252, 96, '#ff8fb1', 900, 'c', a=a)
    c.drawRect(skia.Rect.MakeWH(WW, WH), P('#0a0d14', 70))


def _car(c, x, y, col, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -70, -34, 140, 40, 12, P(col)); rr(c, -40, -64, 84, 40, 14, P(col)); rr(c, -32, -58, 68, 24, 8, P('#1c2530'))
    c.drawCircle(-40, 6, 16, P('#14181d')); c.drawCircle(40, 6, 16, P('#14181d')); c.restore()


def v_parking(c, t):
    c.drawRect(skia.Rect.MakeWH(WW, WH), grad(0, 0, 0, 380, ['#0c1430', '#27365e']))
    c.drawCircle(480, 110, 44, P('#e8edf5')); c.drawCircle(498, 98, 38, P('#0f1936'))
    for i, (sx, sy) in enumerate(((60, 60), (180, 130), (300, 50), (380, 180), (560, 230), (110, 220))):
        c.drawCircle(sx, sy, 3, P('#ffffff', 150 + 100 * math.sin(t * 3 + i)))
    c.drawRect(skia.Rect.MakeXYWH(0, 330, WW, WH - 330), P('#2b3038'))
    for row, y in enumerate((420, 540)):
        for i in range(6):
            x = 30 + i * 110; c.drawLine(x, y - 70, x, y + 24, P('#e9edf1', 130, stroke=5, cap=False))
    for x, y, col in ((85, 420, '#4f6f8f'), (305, 420, '#8f4f4f'), (525, 420, '#5d7f5a'), (195, 540, '#c9b458'), (415, 540, '#6a5d8f')):
        _car(c, x, y, col)
    for lx in (140, 470):  # lamp posts
        c.drawLine(lx, 330, lx, 170, P('#8ea2b1', stroke=8, cap=False)); rr(c, lx - 34, 160, 68, 16, 8, P('#8ea2b1'))
        cone = skia.Path(); cone.moveTo(lx - 26, 176); cone.lineTo(lx + 26, 176); cone.lineTo(lx + 120, 600); cone.lineTo(lx - 120, 600); cone.close()
        c.drawPath(cone, P('#ffe9a8', 34)); c.drawCircle(lx, 180, 30, P('#ffe9a8', 150, blur=14))
    rr(c, 340, 214, 84, 84, 14, P('#2b6cb0')); text(c, 'P', 382, 282, 70, '#ffffff', 900, 'c'); c.drawLine(382, 298, 382, 334, P('#8ea2b1', stroke=8, cap=False))


def v_roofs(c, t):
    c.drawRect(skia.Rect.MakeWH(WW, WH), grad(0, 0, 0, WH, ['#6fc3f2', '#cfeefb']))
    c.drawCircle(500, 120, 60, P('#fff3c4'))
    for i, (cy, sp) in enumerate(((110, 22), (220, 14))):
        x = (t * sp + i * 330) % (WW + 300) - 200
        for dx, r in ((0, 38), (46, 50), (100, 36)): c.drawCircle(x + dx, cy, r, P('#ffffff', 235))
    for x, y, w, col in ((0, 400, 170, '#c97a5a'), (150, 330, 150, '#a85f48'), (290, 440, 180, '#d08f6a'), (450, 360, 190, '#b56a50')):
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, WH - y), P(col)); c.drawRect(skia.Rect.MakeXYWH(x - 6, y - 14, w + 12, 18), P('#7c4636'))
        for j in range(2):
            for k in range(int(w // 60)):
                rr(c, x + 16 + k * 58, y + 40 + j * 100, 30, 52, 4, P('#fbe9c8', 220))
    rr(c, 190, 262, 60, 60, 8, P('#6f5a4a')); c.drawLine(196, 322, 196, 334, P('#4b3a2e', stroke=6)); c.drawLine(244, 322, 244, 334, P('#4b3a2e', stroke=6))  # water tank
    c.drawLine(530, 360, 530, 250, P('#4b3a2e', stroke=5));
    for k in range(3): c.drawLine(506, 262 + k * 22, 554, 262 + k * 22, P('#4b3a2e', stroke=4))
    for i in range(3):  # birds
        bx = (t * 60 + i * 150) % (WW + 100) - 50; by = 190 + i * 26 + math.sin(t * 5 + i) * 6
        b = skia.Path(); b.moveTo(bx - 16, by - 8); b.quadTo(bx - 6, by - 12, bx, by); b.quadTo(bx + 6, by - 12, bx + 16, by - 8); c.drawPath(b, P('#33475b', stroke=5))


def v_skyline(c, t):
    c.drawRect(skia.Rect.MakeWH(WW, WH), grad(0, 0, 0, WH, ['#3b2a6b', '#c2527d', '#ff9d5c', '#ffd27a']))
    c.drawCircle(310, 470, 170, P('#ffe2a6', 90, blur=50)); c.drawCircle(310, 470, 90, P('#fff0c4'))
    for x, w, h, col in ((0, 90, 300, '#2a1f4a'), (80, 110, 420, '#211a3d'), (180, 80, 250, '#2a1f4a'), (250, 70, 180, '#352759'), (330, 110, 360, '#211a3d'),
                         (430, 90, 470, '#1b1533'), (510, 110, 310, '#2a1f4a')):
        c.drawRect(skia.Rect.MakeXYWH(x, WH - h, w, h), P(col))
        for j in range(int(h // 46)):
            for k in range(int(w // 30)):
                if (x + j * 7 + k * 13) % 5 < 3:
                    a = 200 + 55 * math.sin(t * 2 + j + k + x)
                    rr(c, x + 10 + k * 28, WH - h + 18 + j * 46, 14, 22, 2, P('#ffd98a', a))
    c.drawLine(475, WH - 470, 475, WH - 560, P('#1b1533', stroke=6)); c.drawCircle(475, WH - 564, 7, P('#ff5d5d', 160 + 95 * math.sin(t * 6)))


def v_estate(c, t):
    c.drawRect(skia.Rect.MakeWH(WW, WH), grad(0, 0, 0, 380, ['#3a8fd6', '#9fd8f5', '#ffe9c0']))
    c.drawCircle(120, 110, 54, P('#fff6d8')); c.drawCircle(120, 110, 100, P('#fff0c4', 70, blur=30))
    hill = skia.Path(); hill.moveTo(0, 330); hill.quadTo(180, 250, 380, 320); hill.quadTo(520, 280, WW, 320); hill.lineTo(WW, 400); hill.lineTo(0, 400); hill.close()
    c.drawPath(hill, P('#3f8f6a'))
    c.drawRect(skia.Rect.MakeXYWH(0, 350, WW, WH - 350), grad(0, 350, 0, WH, ['#3fb87a', '#1f8a55']))
    for hx in range(0, WW, 62): c.drawCircle(hx + 30, 356, 34, P('#1c7a50'))  # hedge
    drv = skia.Path(); drv.moveTo(250, 380); drv.lineTo(400, 380); drv.lineTo(WW + 60, WH); drv.lineTo(40, WH); drv.close(); c.drawPath(drv, P('#d5d8dd'))
    # fountain
    c.drawOval(skia.Rect.MakeXYWH(40, 440, 200, 60), P('#e9edf1')); c.drawOval(skia.Rect.MakeXYWH(54, 446, 172, 42), P('#6fc3f2'))
    rr(c, 130, 400, 20, 60, 6, P('#e9edf1'))
    for s in (-1, 1):
        for j in range(4):
            k = (t * 1.2 + j / 4) % 1; c.drawCircle(140 + s * k * 60, 400 - math.sin(k * math.pi) * 50 + k * 60, 6, P('#dff4ff', 255 * (1 - k * .5)))
    # palm
    tr = skia.Path(); tr.moveTo(560, 400); tr.quadTo(540, 280, 572, 180); c.drawPath(tr, P('#7a5636', stroke=18))
    for ang in (-150, -110, -60, -20, 30, 200):
        a = math.radians(ang + math.sin(t * 1.5 + ang) * 3); f = skia.Path(); f.moveTo(572, 180)
        f.quadTo(572 + math.cos(a) * 60, 180 + math.sin(a) * 60 - 34, 572 + math.cos(a) * 130, 180 + math.sin(a) * 100 + 14); c.drawPath(f, P('#1f8f57', stroke=16))
    # supercar gliding up the drive
    x = lerp(760, 380, ease((t - .3) / 1.0)); y = 560
    c.drawOval(skia.Rect.MakeXYWH(x - 150, y + 16, 300, 30), P('#000000', 70, blur=8))
    body = skia.Path(); body.moveTo(x - 150, y + 20); body.lineTo(x - 152, y - 6); body.quadTo(x - 110, y - 34, x - 50, y - 40)
    body.quadTo(x - 14, y - 82, 46 + x, y - 82); body.quadTo(x + 96, y - 80, x + 120, y - 44); body.quadTo(x + 156, y - 36, x + 158, y - 6); body.lineTo(x + 158, y + 20); body.close()
    c.drawPath(body, grad(0, y - 82, 0, y + 20, ['#ff4d4d', '#c01f2e']))
    win = skia.Path(); win.moveTo(x - 36, y - 40); win.quadTo(x - 8, y - 70, x + 42, y - 70); win.quadTo(x + 82, y - 68, x + 100, y - 42); win.close(); c.drawPath(win, P('#1c2530'))
    rr(c, x - 150, y - 12, 26, 12, 6, P('#fff3b0'))
    for wx in (x - 86, x + 94): c.drawCircle(wx, y + 20, 32, P('#14181d')); c.drawCircle(wx, y + 20, 18, P('#cfd6dd'))
    sparkle(c, x + 10, y - 60, 22 * abs(math.sin(t * 3)), 255)


VIEWS = [v_brick, v_parking, v_roofs, v_skyline, v_estate]
WALL = [['#2a333f', '#1b212a'], ['#e3f2f5', '#c6e2e8'], ['#f9e2b8', '#f0bd8c'], ['#34264f', '#1e1630'], ['#f6efe2', '#e6d9c0']]
FLOOR = ['#2e2620', '#aecbd4', '#9a5d30', '#2a1f3a', '#c9a878']
FRAME = ['#59626e', '#ffffff', '#8a5a3a', '#f4f1ea', GOLD]
CAP = ['A brick wall.', 'The hospital parking lot.', 'City rooftops.', 'The skyline at sunset.', 'His own driveway.']
LIGHT = (1, 2, 4)  # light walls: dark headline


def room(i, c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1220, WALL[i]))
    c.drawRect(skia.Rect.MakeXYWH(0, 1216, W, H - 1216), P(FLOOR[i])); c.drawRect(skia.Rect.MakeXYWH(0, 1204, W, 16), P('#000000', 50))
    if i == 0:
        cr = skia.Path(); cr.moveTo(980, 560); cr.lineTo(950, 640); cr.lineTo(985, 700); cr.lineTo(960, 780); c.drawPath(cr, P('#141a21', stroke=5))
        c.drawOval(skia.Rect.MakeXYWH(720, 980, 300, 160), P('#141a21', 130, blur=26))
    if i == 4:
        for x in (720, 1010): c.drawRect(skia.Rect.MakeXYWH(x, 500, 16, 704), P('#e2d2ae'))
    # window: shadow, view, frame, sill
    f = FRAME[i]; b = 26
    rr(c, WX - b, WY - b + 12, WW + 2 * b, WH + 2 * b, 14, P('#000000', 90, blur=22)); rr(c, WX - b, WY - b, WW + 2 * b, WH + 2 * b, 14, P(f))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(WX, WY, WW, WH)); c.translate(WX, WY); VIEWS[i](c, t)
    gl = skia.Path(); gl.moveTo(60, 0); gl.lineTo(200, 0); gl.lineTo(-40, WH); gl.lineTo(-180, WH); gl.close(); c.drawPath(gl, P('#ffffff', 22))
    c.restore()
    if i < 4:
        c.drawRect(skia.Rect.MakeXYWH(WX + WW / 2 - 9, WY, 18, WH), P(f)); c.drawRect(skia.Rect.MakeXYWH(WX, WY + WH * .5 - 9, WW, 18), P(f))
    if i == 0:  # taped crack
        cr = skia.Path(); cr.moveTo(WX + 40, WY + 420); cr.lineTo(WX + 130, WY + 500); cr.lineTo(WX + 110, WY + 560); cr.lineTo(WX + 200, WY + 620); c.drawPath(cr, P('#dfe7ee', 200, stroke=4))
        c.save(); c.rotate(38, WX + 120, WY + 500); rr(c, WX + 60, WY + 482, 120, 36, 4, P('#d8c39a', 230)); c.restore()
    rr(c, WX - b - 20, WY + WH + b - 6, WW + 2 * b + 40, 34, 10, P(f)); rr(c, WX - b - 20, WY + WH + b + 22, WW + 2 * b + 40, 10, 5, P('#000000', 50))
    if i == 2:  # plant on the sill
        rr(c, WX + 500, WY + WH - 60, 80, 84, 12, P('#c96a3b'))
        for a in (-40, -10, 20, 50):
            lf = skia.Path(); lf.moveTo(WX + 540, WY + WH - 60); lf.quadTo(WX + 540 + a * 1.4, WY + WH - 130, WX + 540 + a * 2.2, WY + WH - 180); c.drawPath(lf, P('#2f9e58', stroke=18))
    if i >= 3:  # curtains
        col = ['#7c2f4f', '#5e2140'] if i == 3 else ['#fff6e2', '#ecd9ae']
        for sx in (WX - b - 30, WX + WW + b - 60):
            for k in range(3): rr(c, sx + k * 30, WY - b - 8, 34, WH + 88, 14, P(col[k % 2]))
        rr(c, WX - b - 50, WY - b - 24, WW + 2 * b + 100, 22, 11, P(GOLD if i == 4 else '#c9b458'))
    mood = 'tired' if i < 2 else ('happy' if i == 3 else 'ok')
    ra = -150 + math.sin(t * 6) * 12 if i == 4 else -12
    doctor(c, 884, 1236, .92, OUT[i], t, la=10 if i else 7, ra=ra, mood=mood, flip=i < 4)


def tag(c, i, k=1.0):
    c.save(); c.translate(960, 190); c.scale(k, k); c.drawCircle(0, 0, 50, P(GOLD)); text(c, f'{i + 1}/5', 0, 15, 38, INK, 900, 'c'); c.restore()


def e_hook(c, t):
    room(0, c, t)
    title2(c, 'The view from his window', 'at every rank.', 356, size=92, sub_size=92)
    hud(c, 0, 2000, 1); brand_bar(c)
    if t > 1.2: pill(c, WX + WW / 2, WY + WH - 70, 'Intern: a brick wall.', '#ffffff', INK, 40, pop((t - 1.2) / .35))
    if t > 1.5: tag(c, 0, pop((t - 1.5) / .35))


def _rank(i):
    def f(c, t):
        room(i, c, t)
        k = ease(t / .3); dark = i in LIGHT
        title2(c, RANKS[i], CAP[i], 356, INK if dark else '#ffffff', TEAL_D if dark else GOLD, dy=(1 - k) * -30, a=255 * k, shadow=0 if dark else .35, size=108, sub_size=80)
        up = clamp((t - .35) / .5)
        hud(c, i, lerp(BANK[i - 1], BANK[i], eio((t - .35) / 1.2)), i + up, bump=math.sin(up * math.pi)); brand_bar(c)
        if t > .25: tag(c, i, pop((t - .25) / .35))
    return f


SC = [(e_hook, 3.0)] + [(_rank(i), 2.6 if i < 4 else 3.2) for i in range(1, 5)] + [(cta2('Start with a brick wall.', 'Climb to ED Director.'), 3.4)]

VOICE = [(0.15, "The view from his window, at every rank.", 2.7), (3.2, 'Resident. The parking lot.', 2.2), (5.8, 'Registrar. City rooftops.', 2.2),
         (8.4, 'Consultant. The skyline.', 2.2), (11.0, 'E.D. Director. His own driveway.', 2.8), (14.5, 'Earn the view. Bedside Bay. Play free.', 3.2)]


def soundtrack(wav):
    import sound
    st = [3.0, 5.6, 8.2, 10.8]
    cues = [(.05, 'pop'), (1.2, 'pop'), (1.5, 'tick')] + [(s - .25, 'whoosh') for s in st] + [(s + .25, 'pop') for s in st]
    cues += [(s + .4, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + .7, 'cash') for s in st]
    cues += [(11.9, 'ding'), (12.9, 'riser'), (14.0, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=3.0, lift=10.8, cta=14.0, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .14)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.2), (1, 2.2), (2, 2.2), (3, 2.2), (4, 0.5), (4, 2.8), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
