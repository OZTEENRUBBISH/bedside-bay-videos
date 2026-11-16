"""Broke to Rich variant 07 — "Same doctor. Mattress or mansion?" Modelled on the split-screen hook of variant 03 (best
engagement in the first weekly review), with new content: the slanted split stays on screen and pans item against item
(noodles vs supercar, rent notice vs gold watch) over a "tale of the tape" card, then the divider slides away while the rank
ladder climbs from Intern to ED Director. Bank amounts after the $2,000 start are illustrative. Music: bright.
Video: python3 b2r_07_versus.py <out.mp4>          Preview: python3 b2r_07_versus.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK

RED = '#d64545'
SLANT = 60


def view(c, kind, t, clip, cx, cy, zoom, sx, sy):
    """Draw the poor or rich scene inside the clip path so scene point (cx, cy) lands on screen point (sx, sy) at this zoom.
    The scene's own sky/wall and ground are extended so any pan or zoom stays covered."""
    c.save(); c.clipPath(clip, doAntiAlias=True)
    c.translate(sx, sy); c.scale(zoom, zoom); c.translate(-cx, -cy)
    big = lambda y0, y1: skia.Rect.MakeLTRB(-4000, y0, 5080, y1)
    if kind == 'poor':
        c.drawRect(big(-4000, 1150), grad(0, 0, 0, 1200, ['#2a333f', '#1b212a'])); c.drawRect(big(1150, 6000), P('#2e2620'))
        c.save(); c.clipRect(skia.Rect.MakeWH(W, H)); scenes.poor(c, t); c.restore()
    else:
        c.drawRect(big(-4000, 1130), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
        c.drawRect(big(1120, 6000), grad(0, 1120, 0, 1500, ['#2e9f6b', '#1c7a50']))
        c.save(); c.clipRect(skia.Rect.MakeWH(W, H)); scenes.rich(c, t + 1.5, car_in=False); c.restore()
    c.restore()


def _poly(pts):
    p = skia.Path()
    for i, (x, y) in enumerate(pts): (p.lineTo if i else p.moveTo)(x, y)
    p.close(); return p


def halves(c, T, d, L, R, rs=None):
    """Slanted split at centre x = d. L / R = (cx, cy, zoom) of the poor / rich view; rs = screen anchor of the rich view."""
    if d > -SLANT:
        view(c, 'poor', T, _poly([(-10, 0), (d + SLANT, 0), (d - SLANT, H), (-10, H)]), *L, d / 2, 930)
    rs = rs or ((d + W) / 2, 930)
    view(c, 'rich', T, _poly([(d + SLANT, 0), (W + 10, 0), (W + 10, H), (d - SLANT, H)]), *R, *rs)
    sh = skia.GradientShader.MakeLinear(points=[skia.Point(0, 0), skia.Point(0, 700)], colors=[C('#0b1624'), C('#0b1624'), C('#0b1624', 0)],
                                        positions=[0, .6, 1])
    p = skia.Paint(AntiAlias=True); p.setShader(sh); c.drawRect(skia.Rect.MakeWH(W, 700), p)  # keeps the headline clear of the scenery
    if d > -SLANT:
        x = lambda y: d + SLANT - 2 * SLANT * y / H
        c.drawLine(x(596), 596, x(H), H, P('#ffffff', stroke=12, cap=False))


def tape(c, row, k=1.0, y=1290):
    """Tale-of-the-tape card: broke side against rich side with a VS badge in the middle."""
    ll, lv, rl, rv = row
    c.save(); c.translate(540, y + 100); c.scale(k, k); c.translate(-540, -(y + 100))
    rr(c, 60, y + 12, 960, 200, 44, P('#000000', 90, blur=24)); rr(c, 60, y, 960, 200, 44, P('#ffffff'))
    text(c, ll, 100, y + 62, 26, '#5b7083', 800); text(c, lv, 100, y + 146, fit(lv, 62, 360), RED, 900)
    text(c, rl, 980, y + 62, 26, '#5b7083', 800, 'r'); text(c, rv, 980, y + 146, fit(rv, 62, 360), TEAL_D, 900, 'r')
    c.drawCircle(540, y + 100, 58, P(INK)); text(c, 'VS', 540, y + 117, 46, '#ffffff', 900, 'c')
    c.restore()


def labels(c, d, t=9.0):
    if d > 300: pill(c, d / 2, 640, 'DAY 1', '#ffffff', INK, 40, pop((t - .15) / .35) if t > .15 else 0)
    pill(c, (d + W) / 2, 640, 'ED DIRECTOR', GOLD, INK, 40, pop((t - .45) / .35) if t > .45 else 0)


VIEWS = [((437, 900, .8), (535, 940, .7)),          # the whole room against the whole driveway
         ((918, 1120, 2.4), (321, 1190, 1.15)),     # instant noodles against the supercar
         ((905, 700, 1.9), (880, 800, 1.6))]        # rent notice against the gold watch
ROWS = [('BANK', '$2,000', 'BANK', '$2,480,000'), ('DINNER', 'Noodles', 'DRIVEWAY', 'Supercar'),
        ('ON THE WALL', 'Rent overdue', 'ON THE WRIST', 'Gold watch')]
HL = [('Same doctor.', 'Mattress or mansion?'), ('Noodles', 'or a supercar?'), ('Rent overdue', 'or a gold watch?')]
DUR = [3.0, 2.6, 2.6, 3.6, 3.4]
START = [sum(DUR[:i]) for i in range(5)]


def _mix(a, b, k): return tuple(lerp(x, y, k) for x, y in zip(a, b))


def beat(i):
    def f(c, t):
        k = eio(t / .45) if i else 1
        L = _mix(VIEWS[i - 1][0], VIEWS[i][0], k) if i else VIEWS[0][0]
        R = _mix(VIEWS[i - 1][1], VIEWS[i][1], k) if i else VIEWS[0][1]
        halves(c, START[i] + t, 540, L, R)
        labels(c, 540, t if i == 0 else 9.0)
        a = ease(t / .3) if i else 1
        title2(c, HL[i][0], HL[i][1], 356, a=255 * a, dy=(1 - a) * 30, size=104, sub_size=84)
        tape(c, ROWS[i], pop((t - (.9 if i == 0 else .3)) / .4) if t > (.9 if i == 0 else .3) else 0)
        brand_bar(c)
    return f


def climb_state(t):
    p = lerp(1, 5, eio((t - .3) / 2.3)); x = p - 1; j = min(3, int(x))
    return min(4, max(0, math.ceil(p - 1e-6) - 1)), lerp(BANK[j], BANK[j + 1], x - j), p


def climb(c, t):
    e = eio((t - .2) / 1.3); d = lerp(540, -80, e)
    halves(c, START[3] + t, d, VIEWS[2][0], _mix(VIEWS[2][1], (540, 960, 1.0), e), (lerp(810, 540, e), lerp(930, 960, e)))
    labels(c, d)
    a = ease(t / .3)
    title2(c, 'One career', 'between them.', 356, a=255 * a, dy=(1 - a) * 30, size=104, sub_size=84)
    r, bank, p = climb_state(t)
    hud(c, r, bank, p, bump=abs(math.sin(t * 9)) * .5 if p < 5 else 0); brand_bar(c)


SC = [(beat(0), DUR[0]), (beat(1), DUR[1]), (beat(2), DUR[2]), (climb, DUR[3]),
      (cta2('Start on the mattress.', 'Climb to the mansion.'), DUR[4])]

VOICE = [(0.15, 'Same doctor. Mattress, or mansion?', 2.7), (3.2, 'Noodles, or a supercar?', 2.3), (5.8, 'Rent overdue, or a gold watch?', 2.3),
         (8.4, 'One career between them. Climb it.', 3.2), (12.1, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.15, 'pop'), (.45, 'pop'), (.9, 'cash'), (2.9, 'whoosh'), (3.3, 'pop'), (5.5, 'whoosh'), (5.9, 'pop'), (8.15, 'whoosh')]
    cues += [(s, f'step:{i + 1}') for i, s in enumerate((9.25, 9.65, 10.05, 10.8))] + [(10.85, 'cash'), (10.6, 'riser'), (11.8, 'impact'), (11.85, 'ding')]
    return sound.build(wav, sum(DUR), 'bright', drop=3.0, lift=8.2, cta=11.8, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i == 4: flash(c, t)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.2), (1, 2.0), (2, 2.0), (3, 0.6), (3, 1.2), (3, 3.2), (4, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
