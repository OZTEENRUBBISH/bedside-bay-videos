"""Broke to Rich variant 10 — "What Dr John Smith eats at every rank." The climb told through his dinner table: instant
noodles on a cardboard box, cold pizza in the break room, a real burger, a steak dinner, then a silver cloche in the mansion.
The table, the room and the outfit upgrade with every rank. The food and bank amounts after the $2,000 start are illustrative.
Music: upbeat.
Video: python3 b2r_10_dinner.py <out.mp4>          Preview: python3 b2r_10_dinner.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

BX, BY = 720, 1154  # where the food sits on the table
TY = 1180           # table top
FS = 1.15           # food scale


def _table(c, top, front, edge=None):
    c.drawRect(skia.Rect.MakeXYWH(0, TY + 6, W, 30), P('#000000', 60, blur=14))
    c.drawRect(skia.Rect.MakeXYWH(0, TY + 26, W, H - TY), P(front))
    rr(c, -20, TY - 14, W + 40, 44, 12, P(top))
    if edge: c.drawRect(skia.Rect.MakeXYWH(0, TY + 26, W, 8), P(edge))


def _plate(c, w=420, col='#ffffff', rim='#d9e0e6'):
    c.drawOval(skia.Rect.MakeXYWH(BX - w / 2, BY - 8, w, 56), P('#000000', 60, blur=10))
    c.drawOval(skia.Rect.MakeXYWH(BX - w / 2, BY - 22, w, 56), P(rim)); c.drawOval(skia.Rect.MakeXYWH(BX - w / 2 + 14, BY - 20, w - 28, 44), P(col))


def _steam(c, t, x0, y0, n=3, gap=40):
    for i in range(n):
        k = (t * .5 + i / n) % 1; sx = x0 + i * gap
        s = skia.Path(); s.moveTo(sx, y0 - k * 90); s.quadTo(sx + 18, y0 - 24 - k * 90, sx, y0 - 48 - k * 90)
        s.quadTo(sx - 18, y0 - 72 - k * 90, sx, y0 - 96 - k * 90)
        c.drawPath(s, P('#ffffff', 150 * (1 - k), stroke=7))


def f_noodles(c, t):
    cup = skia.Path(); cup.moveTo(BX - 110, BY - 210); cup.lineTo(BX + 110, BY - 210); cup.lineTo(BX + 80, BY + 10); cup.lineTo(BX - 80, BY + 10); cup.close()
    c.drawOval(skia.Rect.MakeXYWH(BX - 110, BY - 4, 220, 34), P('#000000', 70, blur=10))
    c.drawPath(cup, P('#f4f1ea')); rr(c, BX - 122, BY - 232, 244, 34, 14, P('#e3ded3'))
    band = skia.Path(); band.moveTo(BX - 102, BY - 150); band.lineTo(BX + 102, BY - 150); band.lineTo(BX + 90, BY - 60); band.lineTo(BX - 90, BY - 60); band.close()
    c.drawPath(band, P('#d64545')); text(c, 'NOODLES', BX, BY - 88, 40, '#ffffff', 900, 'c')
    c.drawLine(BX + 40, BY - 226, BX + 130, BY - 380, P('#c9d2da', stroke=12))  # fork
    for dx in (-14, 0, 14): c.drawLine(BX + 130 + dx, BY - 380, BX + 136 + dx, BY - 420, P('#c9d2da', stroke=6))
    _steam(c, t, BX - 50, BY - 250)


def f_pizza(c, t):
    box = skia.Path(); box.moveTo(BX - 230, BY + 14); box.lineTo(BX + 230, BY + 14); box.lineTo(BX + 200, BY - 40); box.lineTo(BX - 200, BY - 40); box.close()
    c.drawOval(skia.Rect.MakeXYWH(BX - 230, BY, 460, 36), P('#000000', 60, blur=10))
    lid = skia.Path(); lid.moveTo(BX - 200, BY - 40); lid.lineTo(BX + 200, BY - 40); lid.lineTo(BX + 216, BY - 330); lid.lineTo(BX - 216, BY - 330); lid.close()
    c.drawPath(lid, P('#d9b98a')); c.drawPath(lid, P('#b8935f', stroke=6))
    c.drawCircle(BX, BY - 190, 84, P('#c0392b', 60)); text(c, 'PIZZA', BX, BY - 172, 52, '#a3321f', 900, 'c')
    c.drawPath(box, P('#e7cba0')); c.drawPath(box, P('#b8935f', stroke=6))
    sl = skia.Path(); sl.moveTo(BX - 150, BY - 16); sl.lineTo(BX + 130, BY - 34); sl.lineTo(BX + 120, BY + 4); sl.close()
    c.drawPath(sl, P('#f6c453')); c.drawLine(BX + 130, BY - 36, BX + 120, BY + 6, P('#c98a3a', stroke=20))
    for px, py in ((-20, -16), (50, -20), (86, -6)): c.drawOval(skia.Rect.MakeXYWH(BX + px - 16, BY + py - 8, 32, 16), P('#c0392b'))


def f_burger(c, t):
    _plate(c, 440)
    rr(c, BX - 150, BY - 62, 300, 62, 24, P('#d9963f'))
    for i in range(7): c.drawCircle(BX - 144 + i * 48, BY - 70, 28, P('#58b947'))
    rr(c, BX - 164, BY - 124, 328, 52, 24, P('#5b3320'))
    ch = skia.Path(); ch.moveTo(BX - 170, BY - 136); ch.lineTo(BX + 170, BY - 136); ch.lineTo(BX + 120, BY - 104); ch.lineTo(BX + 60, BY - 124); ch.lineTo(BX - 20, BY - 92)
    ch.lineTo(BX - 100, BY - 124); ch.close(); c.drawPath(ch, P('#f6c453'))
    rr(c, BX - 158, BY - 156, 316, 24, 10, P('#d64545'))
    bun = skia.Path(); bun.addArc(skia.Rect.MakeXYWH(BX - 160, BY - 300, 320, 290), 180, 180); bun.close(); c.drawPath(bun, P('#e0a04a'))
    for sx, sy in ((-90, -214), (-30, -252), (40, -236), (96, -200), (-4, -202)):
        c.drawOval(skia.Rect.MakeXYWH(BX + sx - 12, BY + sy - 6, 24, 12), P('#fbe8c2'))
    c.drawLine(BX, BY - 300, BX, BY - 380, P('#c9d2da', stroke=8)); c.drawCircle(BX, BY - 388, 16, P('#d64545'))


def f_steak(c, t):
    _plate(c, 470)
    c.drawOval(skia.Rect.MakeXYWH(BX - 190, BY - 96, 270, 104), P('#f0d9b8')); c.drawOval(skia.Rect.MakeXYWH(BX - 176, BY - 88, 240, 86), P('#7a3b2a'))
    for i in range(4): c.drawLine(BX - 130 + i * 50, BY - 70, BX - 100 + i * 50, BY - 22, P('#4a2015', stroke=9))
    for gx, gy, r in ((110, -30, 34), (150, -52, 30), (176, -22, 28)): c.drawCircle(BX + gx, BY + gy, r, P('#3f9e4a'))
    c.drawCircle(BX + 128, BY - 74, 22, P('#e4572e'))
    _steam(c, t, BX - 110, BY - 110, 3, 54)
    gx = BX + 235  # wine glass
    c.drawLine(gx, BY - 150, gx, BY + 6, P('#e9f1f5', stroke=8)); c.drawOval(skia.Rect.MakeXYWH(gx - 46, BY - 2, 92, 20), P('#e9f1f5'))
    bowl = skia.Path(); bowl.moveTo(gx - 58, BY - 330); bowl.lineTo(gx + 58, BY - 330); bowl.quadTo(gx + 66, BY - 160, gx, BY - 150); bowl.quadTo(gx - 66, BY - 160, gx - 58, BY - 330); bowl.close()
    c.drawPath(bowl, P('#ffffff', 70))
    wine = skia.Path(); wine.moveTo(gx - 58, BY - 250); wine.lineTo(gx + 58, BY - 250); wine.quadTo(gx + 56, BY - 164, gx, BY - 156); wine.quadTo(gx - 56, BY - 164, gx - 58, BY - 250); wine.close()
    c.drawPath(wine, P('#8e1b3a')); c.drawPath(bowl, P('#ffffff', 200, stroke=5))


def f_cloche(c, t):
    _plate(c, 480, '#fff8e4', GOLD)
    lift = ease((t - .9) / .6)
    # the dish under the dome
    rr(c, BX - 70, BY - 60, 140, 60, 14, P('#f6efe2')); rr(c, BX - 52, BY - 104, 104, 50, 12, P('#7a3b2a')); rr(c, BX - 36, BY - 136, 72, 38, 10, P('#3f9e4a'))
    c.drawCircle(BX, BY - 150, 16, P(GOLD))
    if lift > .3:
        for j in range(6):
            a = j * math.pi / 3 + t * 1.5; sparkle(c, BX + math.cos(a) * 190, BY - 120 + math.sin(a) * 110, 26 * abs(math.sin(t * 3 + j)), 255, '#fff6d8')
    c.save(); c.translate(110 * lift, -170 * lift); c.rotate(16 * lift, BX, BY - 120)
    dome = skia.Path(); dome.addArc(skia.Rect.MakeXYWH(BX - 200, BY - 250, 400, 500), 180, 180); dome.close()
    c.drawPath(dome, grad(BX - 200, 0, BX + 200, 0, ['#f4f7fa', '#b9c4ce', '#eef2f6']))
    c.drawArc(skia.Rect.MakeXYWH(BX - 150, BY - 210, 220, 380), 190, 60, False, P('#ffffff', 200, stroke=12))
    rr(c, BX - 214, BY - 14, 428, 28, 14, P('#aab6c1')); c.drawCircle(BX, BY - 268, 26, P(GOLD)); c.drawCircle(BX - 6, BY - 274, 9, P('#ffe9a8'))
    c.restore()


def food(c, fn, t):
    k = pop(t / .35) * FS
    c.save(); c.translate(BX, BY); c.scale(k, k); c.translate(-BX, -BY); fn(c, t); c.restore()


def _candle(c, x, t):
    rr(c, x - 9, TY - 190, 18, 150, 6, P('#fbf6ea')); rr(c, x - 30, TY - 44, 60, 30, 10, P(GOLD)); c.drawCircle(x, TY - 214, 60, P('#ffd98a', 70, blur=30))
    fl = skia.Path(); fl.moveTo(x, TY - 250 - 6 * math.sin(t * 9)); fl.quadTo(x + 18, TY - 206, x, TY - 192); fl.quadTo(x - 18, TY - 206, x, TY - 250 - 6 * math.sin(t * 9)); c.drawPath(fl, P('#ffb347'))


def r_box(c, t):  # intern: bare room, cardboard box for a table
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2a333f', '#1b212a']))
    cr = skia.Path(); cr.moveTo(960, 520); cr.lineTo(930, 600); cr.lineTo(965, 660); cr.lineTo(940, 740); c.drawPath(cr, P('#141a21', stroke=5))
    ang = math.sin(t * 1.7) * 7
    c.save(); c.translate(560, 500); c.rotate(ang); c.drawLine(0, 0, 0, 130, P('#11161c', stroke=6)); rr(c, -14, 126, 28, 26, 5, P('#555f6b'))
    c.drawCircle(0, 176, 150, P('#ffe7a0', 46 + 10 * math.sin(t * 9), blur=60)); c.drawCircle(0, 176, 30, P('#fff0b8')); c.restore()
    c.save(); c.rotate(-5, 130, 640); rr(c, 36, 560, 190, 140, 6, P('#f1ece2')); text(c, 'RENT', 131, 620, 44, '#d64545', 900, 'c'); text(c, 'OVERDUE', 131, 670, 34, '#d64545', 900, 'c'); c.restore()
    doctor(c, 320, 1218, 1.0, 'intern', t, la=7, ra=-7, mood='tired')
    _table(c, '#c79a63', '#b08a5a'); c.drawRect(skia.Rect.MakeXYWH(470, TY + 26, 110, H - TY), P('#d8c39a', 200))
    food(c, f_noodles, t + 1)  # already on the table in the first frame


def r_break(c, t):  # resident: hospital break room
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#e3f2f5', '#c6e2e8'])); c.drawRect(skia.Rect.MakeXYWH(0, 860, W, 14), P('#9fd4cf'))
    c.drawCircle(900, 640, 76, P('#ffffff')); c.drawCircle(900, 640, 76, P('#5b7083', stroke=10)); c.drawLine(900, 640, 900, 596, P(INK, stroke=8)); c.drawLine(900, 640, 934, 640, P(INK, stroke=8))
    rr(c, 60, 560, 200, 240, 10, P('#d7b98a')); rr(c, 78, 580, 74, 90, 4, P('#ffffff')); rr(c, 166, 590, 74, 60, 4, P('#ffe9a8')); rr(c, 90, 690, 120, 80, 4, P('#bfe9e4'))
    doctor(c, 320, 1218, 1.0, 'resident', t, la=10, ra=-12, mood='tired')
    _table(c, '#b9c9d4', '#93a7b5')
    food(c, f_pizza, t)


def r_home(c, t):  # registrar: a proper kitchen table
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#f9e2b8', '#f0bd8c']))
    rr(c, 60, 560, 250, 300, 10, P('#8a5a3a')); rr(c, 76, 576, 218, 268, 6, P('#bfe3f2')); c.drawLine(185, 576, 185, 844, P('#8a5a3a', stroke=10, cap=False))
    c.drawCircle(250, 640, 34, P('#fff3c4'))
    rr(c, 900, 700, 110, 140, 16, P('#c96a3b'));
    for a in (-40, -10, 20, 50):
        lf = skia.Path(); lf.moveTo(955, 700); lf.quadTo(955 + a * 2, 600, 955 + a * 3, 540); c.drawPath(lf, P('#2f9e58', stroke=22))
    doctor(c, 320, 1218, 1.0, 'surgeon', t, la=10, ra=-12)
    _table(c, '#b8743f', '#9a5d30')
    food(c, f_burger, t)


def r_rest(c, t):  # consultant: white tablecloth
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#3a1830', '#1e0f24']))
    for lx in (160, 540, 920):
        c.drawLine(lx, 480, lx, 600, P('#0e0812', stroke=6)); c.drawCircle(lx, 640, 130, P('#ffcf7a', 60, blur=50))
        sh = skia.Path(); sh.moveTo(lx - 30, 596); sh.lineTo(lx + 30, 596); sh.lineTo(lx + 70, 660); sh.lineTo(lx - 70, 660); sh.close(); c.drawPath(sh, P(GOLD))
    doctor(c, 320, 1218, 1.0, 'consultant', t, la=10, ra=-12, mood='happy')
    _table(c, '#fbf6ea', '#ece4d4')
    _candle(c, 462, t)
    food(c, f_steak, t)


def r_mansion(c, t):  # ED Director: private chef
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
    c.drawCircle(800, 900, 210, P('#ffe2a6', 90, blur=70)); c.drawCircle(800, 900, 112, P('#fff0c4'))
    for x in (0, 350, 700, 1050): c.drawRect(skia.Rect.MakeXYWH(x - 14, 480, 28, 600), P('#2a2140'))
    c.drawRect(skia.Rect.MakeXYWH(0, 478, W, 26), P('#2a2140'))
    for dx in (-90, 0, 90):  # chandelier
        c.drawLine(540, 500, 540 + dx, 610, P(GOLD, stroke=6)); c.drawCircle(540 + dx, 630, 60, P('#ffe9a8', 90, blur=26)); c.drawCircle(540 + dx, 630, 18, P('#fff6d8'))
    doctor(c, 320, 1218, 1.0, 'director', t, la=10, ra=-150 + math.sin(t * 6) * 12)
    _table(c, '#f6f1e6', '#e6dfd0', GOLD)
    _candle(c, 462, t); _candle(c, 1040, t + 1)
    food(c, f_cloche, t)


ROOMS = [r_box, r_break, r_home, r_rest, r_mansion]
DISH = ['Instant noodles. Again.', 'Cold pizza at 3am.', 'A real burger.', 'Steak dinner.', 'Private chef.']
LIGHT = (1, 2)  # rooms with a light wall: dark headline


def tag(c, i, k=1.0):
    c.save(); c.translate(960, 190); c.scale(k, k); c.drawCircle(0, 0, 50, P(GOLD)); text(c, f'{i + 1}/5', 0, 15, 38, INK, 900, 'c'); c.restore()


def e_hook(c, t):
    r_box(c, t)
    title2(c, 'What Dr John Smith eats', 'at every rank.', 356, size=92, sub_size=92)
    hud(c, 0, 2000, 1); brand_bar(c)
    if t > 1.5: tag(c, 0, pop((t - 1.5) / .35))


def _course(i):
    def f(c, t):
        ROOMS[i](c, t)
        k = ease(t / .3); dark = i in LIGHT
        title2(c, RANKS[i], DISH[i], 356, INK if dark else '#ffffff', TEAL_D if dark else GOLD, dy=(1 - k) * -30, a=255 * k, shadow=0 if dark else .35, size=108, sub_size=80)
        up = clamp((t - .35) / .5)
        hud(c, i, lerp(BANK[i - 1], BANK[i], eio((t - .35) / 1.2)), i + up, bump=math.sin(up * math.pi)); brand_bar(c)
        if t > .25: tag(c, i, pop((t - .25) / .35))
    return f


SC = [(e_hook, 3.0)] + [(_course(i), 2.6 if i < 4 else 3.2) for i in range(1, 5)] + [(cta2('Start on instant noodles.', 'Climb to ED Director.'), 3.4)]

VOICE = [(0.15, 'What Doctor John Smith eats, at every rank.', 2.7), (3.2, 'Resident. Cold pizza.', 2.2), (5.8, 'Registrar. A real burger.', 2.2),
         (8.4, 'Consultant. Steak dinner.', 2.2), (11.0, 'E.D. Director. Private chef.', 2.8), (14.5, 'Start on noodles. Bedside Bay. Play free.', 3.2)]


def soundtrack(wav):
    import sound
    st = [3.0, 5.6, 8.2, 10.8]
    cues = [(.05, 'pop'), (1.5, 'pop')] + [(s - .25, 'whoosh') for s in st] + [(s + .25, 'pop') for s in st]
    cues += [(s + .4, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + .6, 'cash') for s in st]
    cues += [(11.7, 'ding'), (12.9, 'riser'), (14.0, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.0, lift=10.8, cta=14.0, cues=cues, voice=VOICE)


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
