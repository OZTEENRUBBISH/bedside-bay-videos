"""Broke to Rich variant 18 — "Dr John Smith's phone at every rank." The climb told through the phone in his hand:
a cracked hand-me-down on 3% with "Storage full", the same phone taped up and buzzing with 47 missed pages, a decent
phone whose calendar is all shifts, a new phone with a dinner reservation confirmed, then a gold phone that his
assistant answers. The phone is held up big in the foreground; the room and the outfit upgrade with every rank
(locker room, night corridor, on-call office, a day off outdoors, a private jet).
The phones, the settings and the bank amounts after the $2,000 start are illustrative.
Music: upbeat.
Video: python3 b2r_18_phone.py <out.mp4>          Preview: python3 b2r_18_phone.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK, OUT

PX, PY = 690, 862    # centre of the phone
PW, PH = 350, 640
DX, FOOT = 236, 1218  # the doctor
SLEEVE = ['#8fbdb6', '#17a394', '#2f8f9d', '#ffffff', '#25303d']
RED, GREEN = '#e5484d', '#1f9d63'


# ---------------------------------------------------------------- the phone
def _hand_back(c, i):
    rr(c, -92, PH / 2 - 4, 184, 230, 40, P(SLEEVE[i]))
    if i == 3: rr(c, -92, PH / 2 - 4, 184, 230, 40, P('#c9d2da', stroke=4))
    if i == 4: rr(c, -92, PH / 2 - 4, 184, 34, 10, P('#ffffff')); rr(c, -98, PH / 2 + 34, 196, 30, 8, P(GOLD))
    rr(c, -PW / 2 - 20, 96, PW + 40, 256, 70, P(SKIN_D))


def _hand_front(c):
    c.save(); c.rotate(-14, -PW / 2, 180); rr(c, -PW / 2 - 34, 96, 76, 176, 38, P(SKIN)); rr(c, -PW / 2 - 12, 108, 36, 30, 14, P('#f8dcc4')); c.restore()
    for k in range(3): rr(c, PW / 2 - 30, 84 + k * 78, 62, 64, 30, P(SKIN)); rr(c, PW / 2 - 30, 84 + k * 78, 62, 64, 30, P(SKIN_D, 120, stroke=3))


def _body(c, col, r, edge=None, screen=None):
    rr(c, -PW / 2 + 8, -PH / 2 + 14, PW, PH, r, P('#000000', 90, blur=22))
    rr(c, -PW / 2, -PH / 2, PW, PH, r, col if isinstance(col, skia.Paint) else P(col))
    if edge: rr(c, -PW / 2 + 3, -PH / 2 + 3, PW - 6, PH - 6, r - 3, P(edge, stroke=6))
    x, y, w, h, sr = screen
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), sr, sr), True)


OLD = (-PW / 2 + 24, -PH / 2 + 74, PW - 48, PH - 164, 10)    # thick bezels, home button
NEW = (-PW / 2 + 13, -PH / 2 + 13, PW - 26, PH - 26, 38)     # edge to edge


def _battery(c, x, y, frac, col, label, fg='#ffffff'):
    rr(c, x, y, 48, 24, 6, P(fg, stroke=3)); rr(c, x + 50, y + 7, 5, 10, 2, P(fg)); rr(c, x + 4, y + 4, max(5, 40 * frac), 16, 3, P(col))
    text(c, label, x - 10, y + 22, 26, col if frac < .2 else fg, 900, 'r')


def _crack(c):
    x, y, w, h, _ = OLD
    for pts in (((x + w, y + 30), (x + w - 70, y + 110), (x + w - 96, y + 190), (x + 60, y + 330), (x, y + 372)),
                ((x + w - 96, y + 190), (x + w - 40, y + 290), (x + w, y + 330)), ((x + w - 70, y + 110), (x + w - 170, y + 96), (x + w - 230, y)),
                ((x + 60, y + 330), (x + 96, y + 420), (x + 70, y + h))):
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, P('#000000', 90, stroke=7)); c.drawPath(p, P('#ffffff', 215, stroke=3))


def _old_shell(c, t):
    _body(c, '#7f8a96', 44, '#646e79', OLD)
    x, y, w, h, _ = OLD
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P('#18222e'))
    return x, y, w, h


def _old_end(c):
    c.restore()
    rr(c, -44, -PH / 2 + 34, 88, 12, 6, P('#4d5661')); c.drawCircle(0, PH / 2 - 46, 28, P('#646e79')); c.drawCircle(0, PH / 2 - 46, 28, P('#4d5661', stroke=4))
    for sx, sy, ln in ((-140, -280, 30), (120, 286, 36), (-150, 240, 22)): c.drawLine(sx, sy, sx + ln, sy + 8, P('#aab3bd', 170, stroke=4))


def p_intern(c, t):
    x, y, w, h = _old_shell(c, t)
    text(c, '5:02', x + 16, y + 44, 28, '#c9d2da', 800); _battery(c, x + w - 72, y + 20, .06 if (t * 2) % 1 < .6 else 0, RED, '3%')
    text(c, '3%', x + w / 2, y + 200, 150, RED, 900, 'c'); text(c, 'BATTERY', x + w / 2, y + 240, 28, '#8a9bab', 900, 'c')
    rr(c, x + 14, y + 280, w - 28, 92, 18, P('#fff3d6')); c.drawCircle(x + 54, y + 326, 24, P(GOLD)); text(c, '!', x + 54, y + 340, 40, INK, 900, 'c')
    text(c, 'Storage full', x + 88, y + 322, 31, INK, 900); text(c, 'Delete something.', x + 88, y + 354, 21, '#5b7083', 700)
    rr(c, x + 14, y + 384, w - 28, 80, 18, P('#2a3644')); text(c, 'Charger: also broken', x + w / 2, y + 433, 24, '#c9d2da', 800, 'c')
    _crack(c); _old_end(c)


def p_resident(c, t):
    x, y, w, h = _old_shell(c, t)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 258), P(RED))
    text(c, '47', x + w / 2, y + 170, 176, '#ffffff', 900, 'c'); text(c, 'MISSED PAGES', x + w / 2, y + 226, 36, '#ffffff', 900, 'c')
    for k, lab in enumerate(('Page from the ER', 'Page from the ER', 'Another page. ER.')):
        yy = y + 274 + k * 70; rr(c, x + 12, yy, w - 24, 60, 14, P('#2a3644')); c.drawCircle(x + 42, yy + 30, 11, P(RED))
        text(c, lab, x + 64, yy + 39, 25, '#ffffff', 800)
    _crack(c); _old_end(c)
    for (tx, ty, ang, tw_) in ((-PW / 2 + 60, -PH / 2 + 30, -38, 230), (PW / 2 - 70, PH / 2 - 60, -32, 220)):   # tape holding it together
        c.save(); c.translate(tx, ty); c.rotate(ang); rr(c, -tw_ / 2, -27, tw_, 54, 4, P('#e9d8a6', 235))
        for j in range(5): c.drawLine(-tw_ / 2 + 20 + j * tw_ / 5, -27, -tw_ / 2 + 20 + j * tw_ / 5, 27, P('#cdb97f', 150, stroke=2, cap=False))
        c.restore()


def p_registrar(c, t):
    _body(c, '#1c2530', 46, '#3a4756', NEW)
    x, y, w, h, _ = NEW
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P('#f4f7fa')); c.drawRect(skia.Rect.MakeXYWH(x, y, w, 150), P(TEAL_D))
    text(c, '9:41', x + 28, y + 46, 24, '#ffffff', 800); _battery(c, x + w - 84, y + 24, .62, '#ffffff', '')
    text(c, 'This month', x + w / 2, y + 116, 46, '#ffffff', 900, 'c')
    for k, d in enumerate('MTWTF'): text(c, d, x + 20 + 30 + k * 59, y + 184, 24, '#5b7083', 900, 'c')
    lit = int(max(0, t - .45) / .05)
    for r in range(5):
        for k in range(5):
            cx, cy = x + 20 + k * 59, y + 198 + r * 74; n = r * 5 + k; off = n == 18
            if n > lit: rr(c, cx, cy, 53, 66, 10, P('#e3e9ee')); continue
            rr(c, cx, cy, 53, 66, 10, P(GOLD if off else TEAL))
            text(c, 'OFF?' if off else 'SHIFT', cx + 26.5, cy + 41, 15, INK if off else '#ffffff', 900, 'c')
    rr(c, x + 20, y + 574, w - 40, 30, 15, P('#e3e9ee'))
    c.restore(); rr(c, -46, -PH / 2 + 24, 92, 22, 11, P('#1c2530'))


def p_consultant(c, t):
    _body(c, '#e3e9ef', 50, '#b9c4ce', NEW)
    x, y, w, h, _ = NEW
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), grad(x, y, x + w, y + h, ['#17b3a3', '#2b6cb0', '#3b2f7d']))
    c.drawCircle(x + w * .8, y + h * .82, 150, P('#ffffff', 26)); c.drawCircle(x + w * .1, y + h * .6, 110, P('#ffffff', 20))
    text(c, '7:30', x + 28, y + 46, 24, '#ffffff', 800); _battery(c, x + w - 84, y + 24, 1, '#58d68d', '')
    text(c, '7:30', x + w / 2, y + 190, 112, '#ffffff', 900, 'c'); text(c, 'Friday. Not on call.', x + w / 2, y + 236, 26, '#dff1f4', 800, 'c')
    k = pop((t - .45) / .4)
    if t > .45:
        c.save(); c.translate(x + w / 2, y + 380); c.scale(k, k)
        rr(c, -w / 2 + 12, -86 + 8, w - 24, 236, 26, P('#000000', 70, blur=14)); rr(c, -w / 2 + 12, -86, w - 24, 236, 26, P('#ffffff'))
        c.drawCircle(0, -30, 40, P(GREEN)); check(c, 0, -28, 18, '#ffffff', 8)
        text(c, 'Dinner reservation', 0, 54, 28, INK, 900, 'c'); text(c, 'CONFIRMED', 0, 96, 40, GREEN, 900, 'c'); text(c, 'Table for two, 8:00', 0, 132, 24, '#5b7083', 700, 'c')
        c.restore()
    rr(c, -60, y + h - 22, 120, 8, 4, P('#ffffff', 200))
    c.restore(); rr(c, -46, -PH / 2 + 24, 92, 22, 11, P('#101418'))


def p_director(c, t):
    _body(c, grad(-PW / 2, -PH / 2, PW / 2, PH / 2, ['#ffe9a8', '#f5b83d', '#c98a1e', '#ffd774']), 50, '#fff4cf', NEW)
    x, y, w, h, _ = NEW
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), grad(0, y, 0, y + h, ['#12263f', '#0b1626']))
    text(c, 'INCOMING CALL', x + w / 2, y + 96, 26, '#8fb0c9', 900, 'c')
    ring = (t * 1.3) % 1
    c.drawCircle(x + w / 2, y + 232, 92 + 46 * ring, P(GREEN, 110 * (1 - ring), stroke=8))
    face(c, x + w / 2, y + 232, 88, '#e9b995', '#2a1d16', 'bob', 'ok', t, gown=False)
    text(c, 'Dr Smith’s', x + w / 2, y + 392, 50, '#ffffff', 900, 'c'); text(c, 'office', x + w / 2, y + 444, 50, '#ffffff', 900, 'c')
    rr(c, x + 24, y + 474, w - 48, 52, 26, P(GREEN)); text(c, 'Assistant answered', x + w / 2, y + 509, 24, '#ffffff', 900, 'c')
    text(c, '00:' + f'{int(max(0, t - .4) * 3) + 1:02d}', x + w / 2, y + 574, 30, '#8fb0c9', 800, 'c')
    c.restore(); rr(c, -46, -PH / 2 + 24, 92, 22, 11, P('#101418'))
    for j in range(6):
        a = j * math.pi / 3 + t * 1.2; sparkle(c, math.cos(a) * 236, math.sin(a) * 372 - 20, 26 * abs(math.sin(t * 3 + j)), 255, '#fff6d8')


PHONES = [p_intern, p_resident, p_registrar, p_consultant, p_director]


def phone(c, i, t, enter=True):
    k = ease(t / .4) if enter else 1
    buzz = math.sin(t * 58) * 7 * (1 if (t * 1.6) % 1 < .62 else 0) if i == 1 else 0
    c.save(); c.translate(PX + buzz, PY + (1 - k) * 760); c.rotate((1 - k) * 10 + (buzz * .25 if i == 1 else math.sin(t * 2.1) * 1.2))
    _hand_back(c, i); PHONES[i](c, t); _hand_front(c); c.restore()
    if i == 1 and k > .9:   # buzz lines
        for sgn in (-1, 1):
            for j in range(2):
                r = 236 + j * 34; a = 150 if (t * 1.6) % 1 < .62 else 40
                c.drawArc(skia.Rect.MakeXYWH(PX - r, PY - 330 - r * .0, 2 * r, 300), -28 if sgn > 0 else 152, 56, False, P(GOLD, a, stroke=10))


# ---------------------------------------------------------------- rooms
def _floor(c, col, line=None, y=1150):
    c.drawRect(skia.Rect.MakeXYWH(0, y, W, H - y), P(col))
    if line: c.drawRect(skia.Rect.MakeXYWH(0, y, W, 14), P(line))


def r_lockers(c, t):   # intern: staff locker room
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#232b36', '#171d25']))
    fl = 200 if (t * 3.1) % 1 > .12 else 110
    rr(c, 40, 534, 420, 20, 8, P('#dfe9f2', fl)); c.drawOval(skia.Rect.MakeXYWH(-100, 480, 700, 240), P('#bcd3e6', fl * .16, blur=70))
    for k in range(7):
        x = k * 156 - 6
        rr(c, x, 590, 148, 566, 6, P('#3d4b5a')); rr(c, x + 8, 598, 132, 550, 4, P('#465667'))
        for j in range(4): c.drawLine(x + 34, 640 + j * 20, x + 114, 640 + j * 20, P('#2f3b47', stroke=6))
        rr(c, x + 110, 860, 14, 54, 5, P('#232b36'))
    c.save(); c.rotate(-4, 72, 770); rr(c, 14, 742, 122, 52, 4, P('#e9d8a6')); text(c, 'INTERN', 75, 780, 28, INK, 900, 'c'); c.restore()
    c.save(); c.rotate(3, 390, 790); rr(c, 334, 742, 112, 100, 4, P('#f1ece2')); text(c, 'RENT', 390, 786, 32, RED, 900, 'c'); text(c, 'DUE', 390, 822, 32, RED, 900, 'c'); c.restore()
    _floor(c, '#20262e', '#2f3b47')
    rr(c, 30, 1108, 420, 30, 8, P('#6b4a2e')); c.drawRect(skia.Rect.MakeXYWH(60, 1138, 18, 70), P('#3a2a1c')); c.drawRect(skia.Rect.MakeXYWH(402, 1138, 18, 70), P('#3a2a1c'))


def r_corridor(c, t):  # resident: the corridor on a night shift
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#eaf4fb', '#cfe3f0']))
    c.drawRect(skia.Rect.MakeXYWH(0, 930, W, 220), P('#b7d3e6')); c.drawRect(skia.Rect.MakeXYWH(0, 918, W, 14), P('#8fb5cf'))
    for dx in (20, 760):
        rr(c, dx, 590, 300, 566, 8, P('#8fb5cf')); rr(c, dx + 12, 602, 132, 554, 4, P('#d9e8f2')); rr(c, dx + 156, 602, 132, 554, 4, P('#d9e8f2'))
        for wx in (dx + 78, dx + 222): c.drawCircle(wx, 720, 44, P('#3a5f7d')); c.drawCircle(wx, 720, 44, P('#8fb5cf', stroke=8)); c.drawCircle(wx - 12, 708, 10, P('#ffffff', 90))
    rr(c, 120, 510, 190, 76, 12, P('#e5484d')); text(c, 'ER', 190, 566, 54, '#ffffff', 900, 'c')
    ar = skia.Path(); ar.moveTo(240, 548); ar.lineTo(286, 548); ar.moveTo(270, 532); ar.lineTo(288, 548); ar.lineTo(270, 564); c.drawPath(ar, P('#ffffff', stroke=8))
    _floor(c, '#c3d5e0', '#a9c2d2'); c.drawRect(skia.Rect.MakeXYWH(0, 1196, W, 22), P(TEAL, 170))


def r_office(c, t):    # registrar: the on-call office
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#2c5c50', '#1e4239']))
    c.drawRect(skia.Rect.MakeXYWH(0, 960, W, 190), P('#1a382f')); c.drawRect(skia.Rect.MakeXYWH(0, 950, W, 12), P('#3b7566'))
    rr(c, 40, 560, 230, 170, 8, P('#c79a63')); rr(c, 56, 576, 198, 138, 4, P('#fbf6ea'))
    for j, wl in enumerate((120, 150, 96)): rr(c, 155 - wl / 2, 604 + j * 26, wl, 10, 5, P('#b9c4ce'))
    c.drawCircle(214, 690, 16, P(GOLD)); c.drawCircle(214, 690, 8, P('#ffe9a8'))
    rr(c, 950, 990, 110, 160, 16, P('#c96a3b'))
    for a in (-22, -4, 14, 34):
        lf = skia.Path(); lf.moveTo(1005, 990); lf.quadTo(1005 + a * 2, 880, 1005 + a * 3, 800); c.drawPath(lf, P('#58b947', stroke=22))
    _floor(c, '#6b4a2e', '#8a5a3a')


def r_dayoff(c, t):    # consultant: an evening off, outdoors
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1150, ['#1f5fae', '#4f9fe0', '#bfe3f7']))
    c.drawCircle(150, 640, 150, P('#fff6d8', 70, blur=50)); c.drawCircle(150, 640, 70, P('#fff3c4'))
    for cx, cy, s in ((430 + math.sin(t * .4) * 12, 600, 1.0), (980 + math.sin(t * .3 + 1) * 10, 720, .8)):
        for dx, dy, r in ((-60, 10, 44), (0, -14, 60), (64, 10, 46), (0, 26, 50)): c.drawCircle(cx + dx * s, cy + dy * s, r * s, P('#ffffff', 235))
    h1 = skia.Path(); h1.moveTo(0, 1000); h1.quadTo(260, 860, 560, 980); h1.quadTo(820, 880, W, 960); h1.lineTo(W, 1160); h1.lineTo(0, 1160); h1.close(); c.drawPath(h1, P('#4fae6a'))
    h2 = skia.Path(); h2.moveTo(0, 1070); h2.quadTo(360, 980, 700, 1080); h2.quadTo(900, 1040, W, 1070); h2.lineTo(W, 1160); h2.lineTo(0, 1160); h2.close(); c.drawPath(h2, P('#3c9459'))
    _floor(c, '#d9c9a8', '#efe3c8')
    for x in range(0, W + 1, 120): c.drawLine(x, 1040, x, 1150, P('#ffffff', stroke=10, cap=False))
    rr(c, -10, 1026, W + 20, 20, 8, P('#ffffff'))


def r_jet(c, t):       # ED Director: a private jet (illustrative)
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 1200, ['#fbf4e4', '#f1e4c8']))
    c.drawRect(skia.Rect.MakeXYWH(0, 500, W, 10), P(GOLD)); c.drawRect(skia.Rect.MakeXYWH(0, 990, W, 10), P(GOLD))
    c.drawRect(skia.Rect.MakeXYWH(0, 1000, W, 150), P('#e6d6b4'))
    for k in range(4):
        x = 36 + k * 270
        rr(c, x - 12, 588, 204, 296, 96, P('#d9c9a8')); rr(c, x, 600, 180, 272, 86, P('#7cc4f2'))
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, 600, 180, 272), 86, 86), True)
        c.drawRect(skia.Rect.MakeXYWH(x, 600, 180, 272), grad(0, 600, 0, 872, ['#3f8fe0', '#bfe3f7']))
        for j in range(3):
            cx = x + ((t * 60 + j * 150 + k * 70) % 420) - 120; cy = 690 + j * 62
            c.drawOval(skia.Rect.MakeXYWH(cx, cy, 150, 44), P('#ffffff', 235)); c.drawCircle(cx + 60, cy + 6, 34, P('#ffffff', 235))
        c.restore(); rr(c, x, 600, 180, 272, 86, P('#ffffff', 150, stroke=6))
    _floor(c, '#8a5a3a', GOLD)
    rr(c, -40, 900, 250, 330, 60, P('#f6efe2')); rr(c, -40, 900, 250, 330, 60, P('#d9c9a8', stroke=6)); rr(c, -30, 1060, 290, 80, 34, P('#efe3c8'))  # leather seat


ROOMS = [r_lockers, r_corridor, r_office, r_dayoff, r_jet]
LINE = ['', '47 missed pages.', 'The calendar is all shifts.', 'Dinner reservation: confirmed.', 'His assistant answers it.']
LIGHT = (1, 4)  # rooms with a light wall: dark headline


def tag(c, i, k=1.0):
    c.save(); c.translate(960, 190); c.scale(k, k); c.drawCircle(0, 0, 50, P(GOLD)); text(c, f'{i + 1}/5', 0, 15, 38, INK, 900, 'c'); c.restore()


def doc(c, i, t):
    ra = -150 + math.sin(t * 6) * 12 if i == 4 else (-34 + math.sin(t * 5) * 6 if i == 3 else -10)
    doctor(c, DX, FOOT, 1.0, OUT[i], t, la=8, ra=ra, mood='tired' if i < 2 else ('happy' if i == 3 else 'ok'))


def e_hook(c, t):
    r_lockers(c, t); doc(c, 0, t)
    phone(c, 0, t + 1, enter=False)   # already in his hand in the first frame
    title2(c, 'Dr John Smith’s phone', 'at every rank.', 356, size=92, sub_size=92)
    hud(c, 0, 2000, 1); brand_bar(c)
    if t > 1.5: tag(c, 0, pop((t - 1.5) / .35))


def _rank(i):
    def f(c, t):
        ROOMS[i](c, t); doc(c, i, t); phone(c, i, t)
        if i == 4 and t > 1.0:   # the assistant picks up
            k = pop((t - 1.0) / .35); c.save(); c.translate(250, 560); c.scale(k, k)
            rr(c, -206, -46 + 6, 412, 92, 46, P('#000000', 60, blur=12)); rr(c, -206, -46, 412, 92, 46, P(INK))
            tl = skia.Path(); tl.moveTo(180, -10); tl.lineTo(246, 30); tl.lineTo(170, 30); tl.close(); c.drawPath(tl, P(INK))
            text(c, '“Dr Smith’s office.”', 0, 14, 38, '#ffffff', 900, 'c'); c.restore()
        k = ease(t / .3); dark = i in LIGHT
        title2(c, RANKS[i], LINE[i], 356, INK if dark else '#ffffff', TEAL_D if dark else GOLD, dy=(1 - k) * -30, a=255 * k, shadow=0 if dark else .35, size=108, sub_size=76)
        up = clamp((t - .35) / .5)
        hud(c, i, lerp(BANK[i - 1], BANK[i], eio((t - .35) / 1.2)), i + up, bump=math.sin(up * math.pi)); brand_bar(c)
        if t > .25: tag(c, i, pop((t - .25) / .35))
    return f


SC = [(e_hook, 3.0)] + [(_rank(i), 2.7 if i < 4 else 3.3) for i in range(1, 5)] + [(cta2('Start on 3% battery.', 'Climb to ED Director.'), 3.8)]

VOICE = [(0.15, 'Doctor John Smith’s phone, at every rank.', 2.7), (3.2, 'Resident. Forty-seven missed pages.', 2.4), (5.9, 'Registrar. A calendar full of shifts.', 2.4),
         (8.5, 'Consultant. Dinner reservation confirmed.', 2.4), (11.3, 'E.D. Director. His assistant answers it.', 3.0), (14.6, 'Start on three percent. Bedside Bay. Play free.', 3.3)]


def soundtrack(wav):
    import sound
    st = [3.0, 5.7, 8.4, 11.1]
    cues = [(.05, 'pop'), (.5, 'beep'), (1.5, 'pop')] + [(s - .25, 'whoosh') for s in st] + [(s + .25, 'pop') for s in st]
    cues += [(s + .45, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + .7, 'cash') for s in st]
    cues += [(3.5, 'beep'), (4.1, 'beep'), (4.7, 'beep'), (9.0, 'ding'), (12.1, 'ding'), (13.2, 'riser'), (14.4, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.0, lift=11.1, cta=14.4, cues=cues, voice=VOICE)


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
        if len(sys.argv) > 3:
            for n, (i, t) in enumerate(pts): save_jpg(frame(compose(i), t), f'{sys.argv[3]}-{n}.jpg')
    elif sys.argv[1] == 'phonemes':
        import sound
        for _, l, _ in VOICE: print(l, '->', sound.phonemes(l))
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
