"""Broke to Rich variant 15 — "Dr John Smith's coffee at every rank." The climb told through the cup in front of him:
a vending-machine paper cup, the burnt break-room pot, a takeaway latte with his name spelled wrong, a double espresso
from his own machine, then a gold cup from a personal barista. Each cup slides down the counter; the room and the outfit
upgrade with every rank. The coffee and bank amounts after the $2,000 start are illustrative.
Music: bright.
Video: python3 b2r_15_coffee.py <out.mp4>          Preview: python3 b2r_15_coffee.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

CX, BY = 400, 1150   # where the cup stands on the counter
TY = 1150
FS = 1.2
DX = 836             # the doctor


def _counter(c, top, front, edge=None):
    c.drawRect(skia.Rect.MakeXYWH(0, TY + 6, W, 30), P('#000000', 60, blur=14))
    c.drawRect(skia.Rect.MakeXYWH(0, TY + 26, W, H - TY), P(front))
    rr(c, -20, TY - 10, W + 40, 40, 12, P(top))
    if edge: c.drawRect(skia.Rect.MakeXYWH(0, TY + 26, W, 8), P(edge))


def _steam(c, t, x0, y0, n=3, gap=40, a=150):
    for i in range(n):
        k = (t * .5 + i / n) % 1; sx = x0 + i * gap
        s = skia.Path(); s.moveTo(sx, y0 - k * 90); s.quadTo(sx + 18, y0 - 24 - k * 90, sx, y0 - 48 - k * 90)
        s.quadTo(sx - 18, y0 - 72 - k * 90, sx, y0 - 96 - k * 90)
        c.drawPath(s, P('#ffffff', a * (1 - k), stroke=7))


def _trap(c, wt, wb, y0, y1, p):
    q = skia.Path(); q.moveTo(CX - wt / 2, y0); q.lineTo(CX + wt / 2, y0); q.lineTo(CX + wb / 2, y1); q.lineTo(CX - wb / 2, y1); q.close(); c.drawPath(q, p)


def _shadow(c, w):
    c.drawOval(skia.Rect.MakeXYWH(CX - w / 2, BY - 14, w, 34), P('#000000', 70, blur=10))


def k_vend(c, t):
    _shadow(c, 200)
    _trap(c, 190, 130, BY - 230, BY, P('#efe6d2'))
    _trap(c, 176, 158, BY - 180, BY - 150, P('#a8763e')); _trap(c, 150, 140, BY - 70, BY - 50, P('#a8763e'))
    c.drawOval(skia.Rect.MakeXYWH(CX - 99, BY - 246, 198, 34), P('#d9cfb8')); c.drawOval(skia.Rect.MakeXYWH(CX - 84, BY - 240, 168, 22), P('#6b4a2e'))
    _steam(c, t, CX, BY - 250, 1, 0, 90)
    for i, dx in enumerate((150, 196)):  # the last coins
        c.drawOval(skia.Rect.MakeXYWH(CX + dx - 26, BY - 22 - i * 6, 52, 22), P('#8f9aa5')); c.drawOval(skia.Rect.MakeXYWH(CX + dx - 26, BY - 28 - i * 6, 52, 22), P('#c9d2da'))


def k_mug(c, t):
    px = CX - 196  # glass pot, nearly empty
    c.drawOval(skia.Rect.MakeXYWH(px - 90, BY - 14, 180, 30), P('#000000', 60, blur=10))
    rr(c, px - 84, BY - 200, 168, 200, 56, P('#ffffff', 90))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(px - 84, BY - 200, 168, 200), 56, 56), True)
    c.drawRect(skia.Rect.MakeXYWH(px - 84, BY - 62, 168, 62), P('#2a170d')); c.restore()
    rr(c, px - 84, BY - 200, 168, 200, 56, P('#ffffff', 190, stroke=6)); rr(c, px - 72, BY - 226, 144, 40, 10, P('#1c2530'))
    c.drawArc(skia.Rect.MakeXYWH(px - 150, BY - 180, 110, 130), 90, 180, False, P('#1c2530', stroke=20))
    _shadow(c, 250)
    c.drawArc(skia.Rect.MakeXYWH(CX + 60, BY - 190, 120, 130), 270, 180, False, P('#e8edf1', stroke=30))
    rr(c, CX - 110, BY - 230, 220, 230, 26, P('#f7f9fb'))
    c.drawOval(skia.Rect.MakeXYWH(CX - 110, BY - 246, 220, 34), P('#dfe6ec')); c.drawOval(skia.Rect.MakeXYWH(CX - 96, BY - 241, 192, 24), P('#2a170d'))
    text(c, 'NEED', CX, BY - 124, 50, '#e5484d', 900, 'c'); text(c, 'SLEEP', CX, BY - 70, 50, '#e5484d', 900, 'c')
    dr = skia.Path(); dr.moveTo(CX - 70, BY - 232); dr.quadTo(CX - 62, BY - 190, CX - 72, BY - 168); c.drawPath(dr, P('#4a2c18', stroke=9))  # drip
    _steam(c, t, CX - 30, BY - 256, 2, 50, 110)


def k_latte(c, t):
    _shadow(c, 210)
    _trap(c, 200, 140, BY - 320, BY, P('#ffffff'))
    _trap(c, 187, 162, BY - 250, BY - 110, P('#c79a63'))
    c.save(); c.rotate(-5, CX, BY - 170); text(c, 'JHON?', CX, BY - 154, 56, '#2a1d16', 900, 'c'); c.restore()
    rr(c, CX - 116, BY - 350, 232, 40, 14, P('#3b2a20')); rr(c, CX - 92, BY - 374, 184, 32, 14, P('#4a3528')); rr(c, CX + 20, BY - 372, 46, 12, 6, P('#1c130e'))
    _steam(c, t, CX + 44, BY - 384, 2, 34, 150)


def k_espresso(c, t):
    c.drawOval(skia.Rect.MakeXYWH(CX - 200, BY - 16, 400, 40), P('#000000', 70, blur=10))
    c.drawOval(skia.Rect.MakeXYWH(CX - 190, BY - 36, 380, 56), P('#d9e0e6')); c.drawOval(skia.Rect.MakeXYWH(CX - 176, BY - 34, 352, 44), P('#ffffff'))
    c.drawArc(skia.Rect.MakeXYWH(CX + 56, BY - 150, 90, 90), 270, 180, False, P('#eef2f6', stroke=22))
    cup = skia.Path(); cup.moveTo(CX - 100, BY - 170); cup.lineTo(CX + 100, BY - 170); cup.quadTo(CX + 96, BY - 20, CX, BY - 14); cup.quadTo(CX - 96, BY - 20, CX - 100, BY - 170); cup.close()
    c.drawPath(cup, P('#ffffff')); c.drawOval(skia.Rect.MakeXYWH(CX - 100, BY - 186, 200, 32), P('#e3e9ee')); c.drawOval(skia.Rect.MakeXYWH(CX - 88, BY - 181, 176, 22), P('#b5793c'))
    c.drawOval(skia.Rect.MakeXYWH(CX - 50, BY - 177, 90, 12), P('#d9a565'))
    c.drawLine(CX - 170, BY - 6, CX - 96, BY - 20, P('#c9d2da', stroke=10)); c.drawOval(skia.Rect.MakeXYWH(CX - 190, BY - 14, 40, 20), P('#c9d2da'))  # spoon
    rr(c, CX + 104, BY - 30, 60, 22, 8, P('#c98a3a'))  # biscuit
    _steam(c, t, CX - 34, BY - 196, 3, 34)


def k_gold(c, t):
    c.drawOval(skia.Rect.MakeXYWH(CX - 220, BY - 16, 440, 44), P('#000000', 70, blur=10))
    c.drawOval(skia.Rect.MakeXYWH(CX - 210, BY - 40, 420, 62), P('#c98f1f')); c.drawOval(skia.Rect.MakeXYWH(CX - 196, BY - 38, 392, 50), P(GOLD))
    c.drawArc(skia.Rect.MakeXYWH(CX + 80, BY - 200, 120, 120), 270, 180, False, P('#e0a52c', stroke=26))
    cup = skia.Path(); cup.moveTo(CX - 136, BY - 230); cup.lineTo(CX + 136, BY - 230); cup.quadTo(CX + 130, BY - 24, CX, BY - 16); cup.quadTo(CX - 130, BY - 24, CX - 136, BY - 230); cup.close()
    c.drawPath(cup, grad(CX - 136, 0, CX + 136, 0, ['#ffe9a8', '#f5b83d', '#c98f1f', '#ffd774']))
    c.drawArc(skia.Rect.MakeXYWH(CX - 106, BY - 214, 60, 170), 150, 70, False, P('#ffffff', 190, stroke=10))
    c.drawOval(skia.Rect.MakeXYWH(CX - 136, BY - 250, 272, 40), P('#ffe9a8')); c.drawOval(skia.Rect.MakeXYWH(CX - 122, BY - 244, 244, 28), P('#b5793c'))
    c.save(); c.translate(CX, BY - 230); c.scale(1, .34)  # latte-art heart
    c.drawCircle(-22, -8, 26, P('#fff4dc')); c.drawCircle(22, -8, 26, P('#fff4dc'))
    h = skia.Path(); h.moveTo(-46, 2); h.lineTo(46, 2); h.lineTo(0, 54); h.close(); c.drawPath(h, P('#fff4dc')); c.restore()
    for j in range(6):
        a = j * math.pi / 3 + t * 1.5; sparkle(c, CX + math.cos(a) * 230, BY - 150 + math.sin(a) * 130, 26 * abs(math.sin(t * 3 + j)), 255, '#fff6d8')
    _steam(c, t, CX - 40, BY - 262, 3, 40)


CUPS = [k_vend, k_mug, k_latte, k_espresso, k_gold]


def cup(c, i, t, slide=True):
    dx = (1 - ease(t / .42)) * -640 if slide else 0
    c.save(); c.translate(dx, 0); c.translate(CX, BY); c.scale(FS, FS); c.translate(-CX, -BY); CUPS[i](c, t); c.restore()


def r_corridor(c, t):  # intern: the hospital corridor at night
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#232c38', '#161c24']))
    fl = 200 if (t * 7) % 5 > .5 else 90
    rr(c, 330, 520, 420, 22, 8, P('#eaf6ff', fl)); c.drawCircle(540, 560, 260, P('#bfe3ff', fl * .22, blur=90))
    rr(c, 30, 600, 250, 560, 14, P('#39485a')); rr(c, 48, 620, 150, 330, 8, P('#101821'))
    for r in range(4):
        for k in range(3): rr(c, 60 + k * 46, 636 + r * 78, 34, 54, 8, P(['#e5484d', '#f5b83d', '#17b3a3', '#3a8fd6'][(r + k) % 4], 200))
        c.drawRect(skia.Rect.MakeXYWH(48, 698 + r * 78, 150, 6), P('#39485a'))
    rr(c, 212, 630, 52, 110, 6, P('#101821')); rr(c, 222, 760, 32, 10, 4, P('#0b1017')); c.drawCircle(238, 800, 10, P('#f5b83d'))
    rr(c, 48, 972, 216, 56, 8, P('#ffb629', 230)); text(c, 'COFFEE', 156, 1014, 40, '#3b2a10', 900, 'c')
    rr(c, 70, 1050, 170, 70, 8, P('#0b1017'))
    doctor(c, DX, 1218, 1.0, 'intern', t, la=7, ra=-7, mood='tired')
    _counter(c, '#8a9bab', '#5b6b7a')


def r_break(c, t):  # resident: break room at 3am
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#e3f2f5', '#c6e2e8'])); c.drawRect(skia.Rect.MakeXYWH(0, 880, W, 14), P('#9fd4cf'))
    c.drawCircle(160, 690, 86, P('#ffffff')); c.drawCircle(160, 690, 86, P('#5b7083', stroke=10)); c.drawLine(160, 690, 160, 632, P(INK, stroke=8)); c.drawLine(160, 690, 206, 690, P(INK, stroke=8))
    c.save(); c.rotate(4, 540, 700); rr(c, 440, 600, 220, 150, 6, P('#ffe66b')); text(c, 'WHO FINISHED', 550, 662, 26, '#5b5320', 900, 'c'); text(c, 'THE COFFEE?', 550, 704, 26, '#5b5320', 900, 'c'); c.restore()
    doctor(c, DX, 1218, 1.0, 'resident', t, la=10, ra=-12, mood='tired')
    _counter(c, '#b9c9d4', '#93a7b5')


def r_cafe(c, t):  # registrar: a real coffee shop
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#f9e2b8', '#f0bd8c']))
    rr(c, 50, 560, 330, 330, 14, P('#2f3a34')); rr(c, 50, 560, 330, 330, 14, P('#8a5a3a', stroke=14))
    text(c, 'COFFEE', 215, 640, 50, '#fdf6e3', 900, 'c')
    for i, wd in enumerate((230, 190, 250, 170)):
        c.drawLine(84, 700 + i * 46, 84 + wd, 700 + i * 46, P('#fdf6e3', 170, stroke=8)); c.drawCircle(340, 700 + i * 46, 6, P(GOLD))
    for lx in (540, 700):
        c.drawLine(lx, 480, lx, 590, P('#5a3b24', stroke=6)); sh = skia.Path(); sh.moveTo(lx - 26, 588); sh.lineTo(lx + 26, 588); sh.lineTo(lx + 60, 650); sh.lineTo(lx - 60, 650); sh.close()
        c.drawPath(sh, P('#c0563a')); c.drawCircle(lx, 680, 90, P('#fff3c4', 70, blur=40))
    doctor(c, DX, 1218, 1.0, 'surgeon', t, la=10, ra=-12)
    _counter(c, '#b8743f', '#9a5d30')


def r_office(c, t):  # consultant: his own office, his own machine
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#17463f', '#0b2622']))
    rr(c, 430, 560, 250, 190, 8, P(GOLD)); rr(c, 446, 576, 218, 158, 4, P('#fdf9ee'))
    for i, wd in enumerate((150, 110, 130)): c.drawLine(555 - wd / 2, 616 + i * 30, 555 + wd / 2, 616 + i * 30, P('#9aa7b2', stroke=6))
    c.drawCircle(626, 706, 16, P('#e5484d'))
    rr(c, 36, 760, 250, 400, 22, P('#c9d2da')); rr(c, 36, 760, 250, 96, 22, P('#eef2f6')); rr(c, 60, 1090, 202, 70, 10, P('#8f9aa5'))
    c.drawCircle(98, 808, 22, P('#17b3a3')); c.drawCircle(160, 808, 22, P('#33475b')); c.drawCircle(222, 808, 22, P('#33475b'))
    rr(c, 126, 856, 70, 90, 10, P('#33475b')); rr(c, 146, 946, 30, 40, 6, P('#1c2530'))
    doctor(c, DX, 1218, 1.0, 'consultant', t, la=10, ra=-12, mood='happy')
    _counter(c, '#2b2f36', '#1c2026', '#c9d2da')


def r_mansion(c, t):  # ED Director: marble bar, personal barista
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1130, ['#1b1440', '#5a2a6a', '#f2707a', '#ffc37d']))
    c.drawCircle(540, 980, 230, P('#ffe2a6', 90, blur=70)); c.drawCircle(540, 980, 120, P('#fff0c4'))
    for x in (120, 960):
        rr(c, x - 46, 520, 92, 640, 10, P('#f6efe2')); rr(c, x - 64, 500, 128, 44, 10, P(GOLD)); c.drawRect(skia.Rect.MakeXYWH(x - 16, 544, 8, 610), P('#e3dccb')); c.drawRect(skia.Rect.MakeXYWH(x + 10, 544, 8, 610), P('#e3dccb'))
    bx = 640  # the barista's bell
    b = skia.Path(); b.addArc(skia.Rect.MakeXYWH(bx - 50, TY - 70, 100, 110), 180, 180); b.close(); c.drawPath(b, P(GOLD)); rr(c, bx - 60, TY - 22, 120, 16, 8, P('#c98f1f')); c.drawCircle(bx, TY - 76, 10, P('#ffe9a8'))
    doctor(c, DX, 1218, 1.0, 'director', t, la=10, ra=-150 + math.sin(t * 6) * 12)
    _counter(c, '#fbf7ef', '#e9e2d4', GOLD)


ROOMS = [r_corridor, r_break, r_cafe, r_office, r_mansion]
CUPNAME = ['Vending machine. Lukewarm.', 'Break room pot. Burnt.', 'Takeaway latte. Wrong name.', 'Double espresso. Own machine.', 'Gold cup. Personal barista.']
LIGHT = (1, 2)  # rooms with a light wall: dark headline


def cups_left(c, i, k=1.0):
    """Five little cups under the brand bar: which rank we're on."""
    for j in range(5):
        x = 930 + (j - 2) * 0; y = 0
    c.save(); c.translate(960, 190); c.scale(k, k); c.drawCircle(0, 0, 54, P(GOLD)); text(c, f'{i + 1}', -12, 16, 50, INK, 900, 'c'); text(c, '/5', 22, 16, 30, INK, 900, 'c'); c.restore()


def e_hook(c, t):
    r_corridor(c, t); cup(c, 0, t + 1, slide=False)
    title2(c, 'Dr John Smith’s coffee', 'at every rank.', 356, size=92, sub_size=92)
    hud(c, 0, 2000, 1); brand_bar(c)
    if t > 1.5: cups_left(c, 0, pop((t - 1.5) / .35))


def _rank(i):
    def f(c, t):
        ROOMS[i](c, t); cup(c, i, t)
        k = ease(t / .3); dark = i in LIGHT
        title2(c, RANKS[i], CUPNAME[i], 356, INK if dark else '#ffffff', TEAL_D if dark else GOLD, dy=(1 - k) * -30, a=255 * k, shadow=0 if dark else .35, size=108, sub_size=74)
        up = clamp((t - .35) / .5)
        hud(c, i, lerp(BANK[i - 1], BANK[i], eio((t - .35) / 1.2)), i + up, bump=math.sin(up * math.pi)); brand_bar(c)
        if t > .25: cups_left(c, i, pop((t - .25) / .35))
    return f


SC = [(e_hook, 3.0)] + [(_rank(i), 2.7 if i < 4 else 3.3) for i in range(1, 5)] + [(cta2('Start on vending-machine coffee.', 'Climb to ED Director.'), 3.4)]

VOICE = [(0.15, "Doctor John Smith's coffee, at every rank.", 2.7), (3.2, 'Resident. Burnt break room coffee.', 2.3), (5.9, 'Registrar. A takeaway latte.', 2.3),
         (8.6, 'Consultant. Double espresso.', 2.3), (11.3, 'E.D. Director. Personal barista.', 2.9), (14.55, 'Start at the bottom. Bedside Bay. Play free.', 3.0)]


def soundtrack(wav):
    import sound
    st = [3.0, 5.7, 8.4, 11.1]
    cues = [(.05, 'pop'), (1.5, 'pop')] + [(s - .2, 'whoosh') for s in st] + [(s + .4, 'tick') for s in st] + [(s + .25, 'pop') for s in st]
    cues += [(s + .45, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + .7, 'cash') for s in st]
    cues += [(12.0, 'ding'), (13.3, 'riser'), (14.4, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=3.0, lift=11.1, cta=14.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .12)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.15), (1, 2.3), (2, 2.3), (3, 2.3), (4, 0.6), (4, 3.0), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
