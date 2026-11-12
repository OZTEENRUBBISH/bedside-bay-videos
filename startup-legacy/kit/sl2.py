"""Style 2 for Startup Legacy ads: the money side. Clean finance-app dashboards (marketing spend, customers,
unit economics, profit and loss), job offers from headhunters, and owning a sports club.
All team names below are the game's own invented clubs; no real brands."""
import math, skia
from sl import *  # noqa

INK = BG
MUTED = '#5b6472'
RED = '#e5484d'


def ui_bg(c, t, top='#eef3f8', bot='#dfe8f1'):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, [top, bot]))
    for i in range(7):  # faint grid
        c.drawLine(0, 520 + i * 160, W, 520 + i * 160, P('#ffffff', 90, stroke=2))


def card(c, x, y, w, h, r=36, col='#ffffff', a=255):
    rr(c, x, y + 10, w, h, r, P('#000000', 34 * a / 255, blur=22)); rr(c, x, y, w, h, r, P(col, a))


def num(c, s, x, y, size, col=INK, align='l', a=255):
    return text(c, s, x, y, size, col, 900, align, a=a)


def countup(v0, v1, t, t0=0.2, d=2.2):
    return lerp(v0, v1, eio((t - t0) / d))


def mini_founder(c, cx, cy, s, t, outfit='suit'):
    """Head-and-shoulders founder in a round badge."""
    c.save(); clip = skia.Path(); clip.addCircle(cx, cy, s); c.clipPath(clip, doAntiAlias=True)
    c.drawCircle(cx, cy, s, P(GREEN))
    founder(c, cx, cy + s * 2.55, s / 210, outfit, t, la=6, ra=-6, mood='happy')
    c.restore(); c.drawCircle(cx, cy, s, P('#ffffff', stroke=6))


# ---------------------------------------------------------------- marketing spend -> customers
def marketing(c, t):
    ui_bg(c, t)
    k = eio((t - .2) / 2.4)
    spend = lerp(500, 20000, k); cust = lerp(40, 1860, eio((t - .5) / 2.4))
    card(c, 60, 500, 960, 250)
    text(c, 'MONTHLY MARKETING SPEND', 100, 560, 28, MUTED, 800)
    num(c, money(spend) + '/mo', 100, 650, 84, INK)
    rr(c, 100, 690, 880, 18, 9, P('#e1e5ea')); rr(c, 100, 690, 880 * (.05 + .95 * k), 18, 9, P(GREEN))
    c.drawCircle(100 + 880 * (.05 + .95 * k), 699, 26, P('#ffffff')); c.drawCircle(100 + 880 * (.05 + .95 * k), 699, 26, P(GREEN, stroke=6))
    # customers card + growing dots
    card(c, 60, 790, 460, 330)
    text(c, 'CUSTOMERS', 100, 850, 28, MUTED, 800); num(c, f'{int(cust):,}', 100, 940, 76, GREEN_D)
    n = int(lerp(3, 40, eio((t - .5) / 2.4)))
    for i in range(n):
        cx, cy = 110 + (i % 10) * 40, 990 + (i // 10) * 34; pk = clamp((t - .5 - i * .05) * 4)
        c.drawCircle(cx, cy, 13 * pop(pk), P(GREEN if i % 7 else SGOLD))
    # revenue card + sparkline
    card(c, 560, 790, 460, 330)
    text(c, 'REVENUE', 600, 850, 28, MUTED, 800); num(c, money(cust * 49) + '/mo', 600, 930, 58, INK)
    pth = skia.Path(); pts = 24
    for i in range(pts):
        u = i / (pts - 1)
        if u > clamp((t - .3) / 2.4): break
        y = 1080 - (u ** 1.6) * 110 - math.sin(i * 1.3) * 6
        (pth.lineTo if i else pth.moveTo)(600 + u * 380, y)
    c.drawPath(pth, P(GREEN, stroke=8))


# ---------------------------------------------------------------- unit economics
def unit_econ(c, t):
    ui_bg(c, t, '#0f1720', '#16212d')
    for i in range(7): c.drawLine(0, 520 + i * 160, W, 520 + i * 160, P('#ffffff', 10, stroke=2))
    rows = [('Cost per customer', '$38', '#ffffff'), ('Lifetime value', '$412', '#3ee08a'), ('Payback', '2.4 months', '#ffffff')]
    for i, (lab, val, col) in enumerate(rows):
        k = ease((t - .2 - i * .35) / .5); y = 500 + i * 150
        rr(c, 60 + (1 - k) * 200, y, 960, 124, 30, P('#1d2a38', 255 * k))
        text(c, lab, 100 + (1 - k) * 200, y + 76, 42, '#c9d5e3', 700, a=255 * k)
        num(c, val, 980 + (1 - k) * 200, y + 80, 56, col, 'r', a=255 * k)
    k = pop(clamp((t - 1.5) / .5))
    if k > 0:
        c.save(); c.translate(540, 1000); c.scale(k, k)
        rr(c, -330, -70, 660, 140, 70, P('#3ee08a')); num(c, 'LTV : CAC  =  10.8x', 0, 20, 56, '#0f1720', 'c'); c.restore()
    if t > 2.0:
        a = 255 * ease((t - 2.0) / .4); text(c, 'Every $1 of ads brings back $10.80', 540, 1130, 40, '#9fb2c2', 700, 'c', a=a)


# ---------------------------------------------------------------- profit and loss
def pnl(c, t):
    ui_bg(c, t)
    card(c, 60, 480, 960, 700)
    text(c, 'THIS MONTH', 100, 545, 28, MUTED, 800); text(c, 'Profit & loss', 100, 610, 54, INK, 900)
    rows = [('Revenue', 91400, GREEN_D), ('Cost of goods', -18300, RED), ('Wages + super', -24600, RED), ('Rent', -6200, RED),
            ('Marketing', -12000, RED), ('Tax', -7600, RED)]
    for i, (lab, v, col) in enumerate(rows):
        k = ease((t - .2 - i * .22) / .35); y = 660 + i * 66
        text(c, lab, 100, y + 30, 38, INK, 700, a=255 * k)
        s = ('+' if v > 0 else '-') + money(abs(v)); num(c, s, 980, y + 32, 40, col, 'r', a=255 * k)
        c.drawLine(100, y + 54, 980, y + 54, P('#e8ecf0', 255 * k, stroke=2))
    k = pop(clamp((t - 1.8) / .45))
    if k > 0:
        c.save(); c.translate(540, 1130); c.scale(k, k)
        rr(c, -440, -50, 880, 100, 50, P(GREEN)); text(c, 'Profit', -400, 18, 44, '#ffffff', 900); num(c, '+$22,700', 400, 20, 52, '#ffffff', 'r'); c.restore()


# ---------------------------------------------------------------- price vs demand
def pricing(c, t):
    ui_bg(c, t)
    card(c, 60, 480, 960, 700)
    text(c, 'PRICE TEST', 100, 545, 28, MUTED, 800)
    k = .5 + .45 * math.sin((t - .3) * 1.6)  # slider sweeps
    price = lerp(19, 99, k); demand = 2600 * math.exp(-2.4 * k); revenue = price * demand
    num(c, f'${price:.0f}', 100, 640, 80, INK); text(c, 'per customer', 330, 636, 36, MUTED, 700)
    rr(c, 100, 680, 880, 16, 8, P('#e1e5ea')); c.drawCircle(100 + 880 * k, 688, 26, P('#ffffff')); c.drawCircle(100 + 880 * k, 688, 26, P(GREEN, stroke=6))
    # revenue curve
    pth = skia.Path()
    for i in range(61):
        u = i / 60; r = lerp(19, 99, u) * 2600 * math.exp(-2.4 * u); y = 1100 - r / 52000 * 300
        (pth.lineTo if i else pth.moveTo)(100 + u * 880, y)
    c.drawPath(pth, P(GREEN, stroke=8))
    best = 1 / 2.4 * 1.0; c.drawLine(100 + 880 * .43, 760, 100 + 880 * .43, 1110, P(SGOLD, stroke=4))
    text(c, 'sweet spot', 100 + 880 * .43 + 14, 790, 30, '#b88a2c', 800)
    y = 1100 - revenue / 52000 * 300; c.drawCircle(100 + 880 * k, y, 18, P(INK))
    text(c, f'{int(demand):,} customers', 100, 1160, 36, MUTED, 700); num(c, money(revenue) + '/mo', 980, 1160, 40, GREEN_D, 'r')


# ---------------------------------------------------------------- job offers
def offer(c, t, title='Chief Executive Officer', pay='$48,500 / month', who='Executive search firm', tag_='HEADHUNTER'):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#1a2433', '#0e141d']))
    c.drawCircle(540, 820, 460, P(GREEN, 40, blur=140))
    # phone
    k = ease(t / .5); y0 = 480 + (1 - k) * 300
    rr(c, 230, y0, 620, 760, 70, P('#05070a')); rr(c, 246, y0 + 16, 588, 728, 58, P('#f4f6f9'))
    rr(c, 470, y0 + 30, 140, 30, 15, P('#05070a'))
    mini_founder(c, 540, y0 + 170, 78, t)
    text(c, tag_, 540, y0 + 300, 28, GREEN_D, 900, 'c')
    text(c, 'Job offer', 540, y0 + 366, 56, INK, 900, 'c')
    lines = wrap(title, 46, 800, 520)
    for i, l in enumerate(lines): text(c, l, 540, y0 + 430 + i * 52, 46, INK, 800, 'c')
    yy = y0 + 430 + len(lines) * 52
    num(c, pay, 540, yy + 34, 50, GREEN_D, 'c')
    text(c, who, 540, yy + 82, 30, MUTED, 700, 'c')
    # buttons + tap
    tap = clamp((t - 1.6) / .3)
    bs = 1 - .08 * math.sin(tap * math.pi)
    c.save(); c.translate(400, y0 + 660); c.scale(bs, bs); rr(c, -120, -44, 240, 88, 44, P(GREEN)); text(c, 'Accept', 0, 14, 40, '#ffffff', 900, 'c'); c.restore()
    rr(c, 560, y0 + 616, 240, 88, 44, P('#e1e5ea')); text(c, 'Decline', 680, y0 + 674, 40, MUTED, 800, 'c')
    if t > 1.2:
        fx, fy = lerp(560, 410, ease((t - 1.2) / .4)), lerp(y0 + 900, y0 + 676, ease((t - 1.2) / .4))
        c.drawCircle(fx, fy, 34, P(SKIN)); rr(c, fx - 16, fy, 32, 120, 16, P(SKIN))
        if t > 1.6: c.drawCircle(400, y0 + 660, 40 + 120 * clamp((t - 1.6) / .5), P('#ffffff', 160 * (1 - clamp((t - 1.6) / .5)), stroke=8))
    if t > 1.9:
        for i in range(24):
            kk = clamp((t - 1.9) / 1.6); a = i * 2 * math.pi / 24; r = 120 + 420 * kk
            c.save(); c.rotate(t * 300 + i * 30, 540 + math.cos(a) * r, 860 + math.sin(a) * r + 300 * kk * kk)
            rr(c, 540 + math.cos(a) * r - 9, 860 + math.sin(a) * r + 300 * kk * kk - 6, 18, 12, 2, P([SGOLD, GREEN, '#ffffff', '#74c0fc'][i % 4], 255 * (1 - kk))); c.restore()


def offer_ladder(c, t):
    """Stack of offers climbing from first job to CEO."""
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#eef3f8', '#dfe8f1']))
    offers = [('Junior Analyst', '$3,900/mo', '#8a94a3'), ('Account Manager', '$7,200/mo', '#5b6472'),
              ('Operations Director', '$16,500/mo', GREEN_D), ('CEO', '$48,500/mo', '#b88a2c')]
    for i, (role, pay, col) in enumerate(offers):
        k = 1.0 if i == 0 else ease((t - i * .45) / .45)
        if k <= 0: continue
        y = 1080 - i * 150 - (1 - k) * 60
        card(c, 100 + i * 20, y, 880 - i * 40, 128, 34, '#ffffff' if i < 3 else '#fff7e0', 255 * k)
        rr(c, 130 + i * 20, y + 34, 60, 60, 18, P(col, 255 * k)); check(c, 160 + i * 20, y + 66, 16, '#ffffff', 7)
        text(c, role, 220 + i * 20, y + 60, 40, INK, 900, a=255 * k); text(c, 'Offer accepted', 220 + i * 20, y + 100, 26, MUTED, 700, a=255 * k)
        num(c, pay, 950 - i * 20, y + 80, 40, col, 'r', a=255 * k)
    if t > 2.0: sparkle(c, 940, 600, 34 * abs(math.sin(t * 4)), 255, SGOLD)


# ---------------------------------------------------------------- sports club
CLUB = ('Ashkettle Rovers', '#C8102E', '#FFFFFF')


def stadium(c, t, score=(2, 1), opp='Brammerholt'):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, 900, ['#060b16', '#14233d']))
    for lx in (120, 960):  # floodlights
        c.drawLine(lx, 540, lx, 820, P('#3a4556', stroke=10)); rr(c, lx - 60, 500, 120, 50, 8, P('#e9f2ff'))
        cone = skia.Path(); cone.moveTo(lx - 60, 550); cone.lineTo(lx + 60, 550); cone.lineTo(540 + (lx - 540) * .1 + 260, 1150); cone.lineTo(540 + (lx - 540) * .1 - 260, 1150); cone.close()
        c.drawPath(cone, P('#e9f2ff', 22))
    # stands with crowd
    st = skia.Path(); st.moveTo(0, 760); st.lineTo(W, 760); st.lineTo(W, 940); st.lineTo(0, 940); st.close(); c.drawPath(st, P('#1d2a40'))
    for i in range(260):
        x = (i * 37) % W; y = 775 + (i * 53 % 150); jump = abs(math.sin(t * 9 + i)) * 6 if t > 1.4 else 0
        c.drawCircle(x, y - jump, 7, P([CLUB[1], CLUB[2], '#f4d35e', '#94a3b8'][i % 4], 230))
    # pitch
    c.drawRect(skia.Rect.MakeXYWH(0, 940, W, 260), grad(0, 940, 0, 1200, ['#2f9e44', '#237a35']))
    for i in range(6): c.drawRect(skia.Rect.MakeXYWH(i * 180, 940, 90, 260), P('#ffffff', 14))
    c.drawLine(540, 940, 540, 1200, P('#ffffff', 160, stroke=5)); c.drawCircle(540, 1070, 80, P('#ffffff', 160, stroke=5))
    # ball flying into the net
    k = clamp((t - .4) / 1.0)
    if k < 1:
        bx, by = lerp(380, 960, k), 1120 - math.sin(k * math.pi) * 180
        c.drawCircle(bx, by, 18, P('#ffffff')); c.drawCircle(bx, by, 8, P('#111111'))
    rr(c, 930, 1000, 120, 120, 6, P('#ffffff', 60)); c.drawRect(skia.Rect.MakeXYWH(930, 1000, 120, 120), P('#ffffff', stroke=5))
    # scoreboard
    s0 = score[0] if t > 1.4 else score[0] - 1
    card(c, 160, 500, 760, 200, 30, '#0b1220')
    rr(c, 190, 530, 30, 140, 10, P(CLUB[1]))
    text(c, CLUB[0].split()[0].upper(), 250, 590, 40, '#ffffff', 900); text(c, opp.upper(), 250, 660, 40, '#9fb2c2', 900)
    k2 = pop(clamp((t - 1.4) / .4)) if t > 1.4 else 1
    c.save(); c.translate(860, 578); c.scale(k2, k2); num(c, str(s0), 0, 14, 60, SGOLD, 'c'); c.restore()
    num(c, str(score[1]), 860, 664, 60, '#ffffff', 'c')


def club_dash(c, t):
    ui_bg(c, t)
    card(c, 60, 480, 960, 330)
    rr(c, 100, 520, 90, 110, 18, P(CLUB[1])); rr(c, 118, 540, 54, 70, 10, P(CLUB[2])); rr(c, 132, 554, 26, 42, 6, P(CLUB[1]))
    text(c, CLUB[0], 220, 572, 50, INK, 900); text(c, 'Football club · you own it', 220, 616, 30, MUTED, 700)
    bars = [('Tickets', 186000), ('Sponsors', 112000), ('Merch', 41000), ('TV rights', 60000)]
    for i, (lab, v) in enumerate(bars):
        k = eio((t - .3 - i * .2) / .8); x = 120 + i * 220; h = v / 186000 * 90 * k
        rr(c, x, 760 - h, 120, h, 14, P(GREEN if i else SGOLD)); text(c, lab, x + 60, 796, 26, MUTED, 800, 'c')
        if k > .9: text(c, money(v * k), x + 60, 752 - h, 26, INK, 900, 'c')
    # league table
    card(c, 60, 850, 960, 330)
    text(c, 'LEAGUE TABLE', 100, 908, 28, MUTED, 800)
    pos = int(round(lerp(7, 1, eio((t - .4) / 2.0))))
    teams = ['Brammerholt Bulldogs', 'Sandrevale Strikers', 'Esterbrae Tempest', 'Cedrimoor Lumberjacks', 'Glenvarra Sparks', 'Port Vessary']
    order = teams[:pos - 1] + [CLUB[0]] + teams[pos - 1:]
    for i, nm in enumerate(order[:4]):
        y = 960 + i * 54; me = nm == CLUB[0]
        if me: rr(c, 84, y - 38, 912, 52, 14, P('#fff4cf'))
        text(c, f'{i + 1}.  {nm}', 110, y, 34, INK if me else MUTED, 900 if me else 700)
    if pos > 4: text(c, f'{pos}.  {CLUB[0]}', 110, 960 + 4 * 54 - 10, 34, INK, 900)


def club_money(c, t):
    """Club finance sliders: ticket price, wage bill, star signing."""
    ui_bg(c, t, '#101a2b', '#0b1220')
    rows = [('Ticket price', '$25', '$32', .42, .55), ('Wage bill', '$180k', '$260k', .4, .7), ('Coach', 'Good', 'Elite', .5, 1.0)]
    for i, (lab, a0, a1, k0, k1) in enumerate(rows):
        y = 500 + i * 190; k = ease((t - .3 - i * .4) / .6); v = lerp(k0, k1, k)
        rr(c, 60, y, 960, 160, 32, P('#1b2840'))
        text(c, lab, 100, y + 62, 40, '#c9d5e3', 800); num(c, a1 if k > .5 else a0, 980, y + 64, 48, '#3ee08a', 'r')
        rr(c, 100, y + 104, 880, 14, 7, P('#2c3b56')); rr(c, 100, y + 104, 880 * v, 14, 7, P('#3ee08a'))
        c.drawCircle(100 + 880 * v, y + 111, 22, P('#ffffff'))
    k = pop(clamp((t - 1.7) / .45))
    if k > 0:
        c.save(); c.translate(540, 1110); c.scale(k, k)
        rr(c, -360, -60, 720, 120, 60, P(SGOLD)); num(c, 'Star signing: +6 rating', 0, 18, 48, INK, 'c'); c.restore()


def trophy(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, 0, H, ['#0b1a33', '#1c3f73']))
    for i in range(40):
        kk = (t * .4 + i * .043) % 1; x = (i * 131 + 31) % 1040 + 20
        c.save(); c.rotate(t * 220 + i * 37, x, 480 + kk * 760); rr(c, x - 9, 480 + kk * 760 - 6, 18, 12, 2, P([SGOLD, CLUB[1], '#ffffff'][i % 3], 230)); c.restore()
    k = pop(clamp(t / .6)); c.save(); c.translate(540, 800); c.scale(k, k)
    c.drawCircle(0, -20, 260, P(SGOLD, 50, blur=80))
    cup = skia.Path(); cup.moveTo(-150, -200); cup.lineTo(150, -200); cup.quadTo(150, 20, 0, 60); cup.quadTo(-150, 20, -150, -200); cup.close()
    c.drawPath(cup, grad(0, -200, 0, 60, ['#ffe08a', '#d9a43a']))
    c.drawArc(skia.Rect.MakeXYWH(-230, -170, 120, 140), 90, 180, False, P('#d9a43a', stroke=22))
    c.drawArc(skia.Rect.MakeXYWH(110, -170, 120, 140), 270, 180, False, P('#d9a43a', stroke=22))
    rr(c, -24, 60, 48, 90, 8, P('#d9a43a')); rr(c, -110, 150, 220, 60, 12, P('#b88a2c')); rr(c, -150, 210, 300, 50, 12, P('#7a5a1c'))
    text(c, 'CHAMPIONS', 0, 244, 34, '#fff4cf', 900, 'c'); sparkle(c, 90, -160, 30 * abs(math.sin(t * 4)), 255, '#ffffff'); c.restore()
    founder(c, 210, 1236, .7, 'mogul', t, la=10, ra=-160 + math.sin(t * 6) * 10)


SCENES2 = {'marketing': marketing, 'unit': unit_econ, 'pnl': pnl, 'pricing': pricing, 'offer': offer, 'ladder': offer_ladder,
           'stadium': stadium, 'club': club_dash, 'clubmoney': club_money, 'trophy': trophy}
LIGHT2 = {'marketing', 'pnl', 'pricing', 'ladder', 'club'}
