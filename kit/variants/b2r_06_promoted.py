"""Broke to Rich variant 06 — "4 promotions from broke." Every cut is a promotion: a PROMOTED stamp slams down, and Dr John
Smith's staff ID badge (rank, bank, promotion stars) upgrades. Bank amounts after the $2,000 start are illustrative. Music: upbeat.
Video: python3 b2r_06_promoted.py <out.mp4>          Preview: python3 b2r_06_promoted.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import OUT, BANK
from b2r_ranks_photos import _consult

RED = '#e5484d'


def star(c, cx, cy, r, col):
    p = skia.Path()
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rad = r if i % 2 == 0 else r * .45
        (p.lineTo if i else p.moveTo)(cx + math.cos(a) * rad, cy + math.sin(a) * rad)
    p.close(); c.drawPath(p, P(col))


def badge(c, rank_i, t, bank, new=0.0, y=1262):
    """Staff ID card: photo, name, rank, bank and one star per promotion. new = 0..1 pop of the newest star."""
    x, w, h = 60, 960, 256; top = rank_i == 4
    rr(c, x, y + 12, w, h, 44, P('#000000', 90, blur=24)); rr(c, x, y, w, h, 44, P('#ffffff'))
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 44, 44), True)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, 60), P(GOLD if top else TEAL)); c.restore()
    rr(c, 490, y - 24, 100, 44, 14, P('#5b7083')); rr(c, 516, y - 10, 48, 14, 7, P('#ffffff'))
    text(c, 'BEDSIDE BAY  ·  STAFF ID', x + 40, y + 42, 26, INK if top else '#ffffff', 900)
    cx, cy = x + 124, y + 156
    clip = skia.Path(); clip.addCircle(cx, cy, 76); c.save(); c.clipPath(clip, doAntiAlias=True)
    c.drawRect(skia.Rect.MakeXYWH(cx - 80, cy - 80, 160, 160), P('#dff1f4'))
    doctor(c, cx, cy + 262, .5, OUT[rank_i], 0.5, la=10, ra=-10, mood='tired' if rank_i == 0 else 'happy'); c.restore()
    c.drawCircle(cx, cy, 76, P(GOLD if top else TEAL, stroke=8))
    text(c, 'Dr John Smith', x + 226, y + 118, 40, '#5b7083', 800)
    text(c, RANKS[rank_i], x + 226, y + 182, 62, INK, 900)
    text(c, 'BANK', x + w - 40, y + 112, 24, '#5b7083', 800, 'r')
    text(c, '$' + f'{int(bank):,}', x + w - 40, y + 172, 52, TEAL_D, 900, 'r')
    text(c, 'PROMOTIONS', x + 226, y + 230, 22, '#5b7083', 800)
    for i in range(4):
        on = i < rank_i; r = 19 * (pop(new) if (on and i == rank_i - 1) else 1)
        star(c, x + 420 + i * 52, y + 222, r, GOLD if on else '#dfe7ee')


def stamp(c, t, n, rank_i, a0=.12):
    """PROMOTED stamp slamming in where the headline normally sits, then the new rank under it."""
    if t < a0: return
    k = clamp((t - a0) / .2); s = lerp(2.6, 1, ease(k)); a = 255 * clamp(k * 3); top = rank_i == 4
    sh = math.sin((t - a0) * 70) * 7 * clamp(1 - (t - a0 - .2) / .3) if t > a0 + .2 else 0
    c.save(); c.translate(540 + sh, 444); c.rotate(-5); c.scale(s, s)
    col = INK if top else RED
    rr(c, -400, -80, 800, 184, 28, P('#000000', a * .35, blur=20))
    rr(c, -400, -92, 800, 184, 28, P(GOLD if top else '#ffffff', a)); rr(c, -400, -92, 800, 184, 28, P(col, a, stroke=14))
    rr(c, -374, -66, 748, 132, 16, P(col, a, stroke=5))
    text(c, 'PROMOTED', 0, 44, fit('PROMOTED', 124, 700), col, 900, 'c', a=a); c.restore()
    if a0 + .2 < t < a0 + .75:
        kk = (t - a0 - .2) / .55
        for j in range(8):
            ang = j * math.pi / 4 + .3; sparkle(c, 540 + math.cos(ang) * (420 + 120 * kk), 444 + math.sin(ang) * (130 + 90 * kk), 26, 255 * (1 - kk), GOLD)
    if t > a0 + .4:
        pill(c, 540, 610, f'{n} of 4  ·  {RANKS[rank_i]}', INK, '#ffffff', 54, pop((t - a0 - .4) / .35))


def p_hook(c, t):
    scenes.poor(c, t)
    title2(c, '4 promotions', 'from broke.', 356, size=108, sub_size=96)
    badge(c, 0, t, 2000); brand_bar(c)
    if t > .9: pill(c, 250, 980, 'Day 1', GOLD, INK, 48, pop((t - .9) / .35))


def _promo(fn, i):
    def f(c, t):
        fn(c, t)
        bank = lerp(BANK[i - 1], BANK[i], eio((t - .35) / 1.3))
        stamp(c, t, i, i)
        badge(c, i if t > .3 else i - 1, t, bank, (t - .3) / .4); brand_bar(c)
    return f


SC = [(p_hook, 2.6), (_promo(lambda c, t: scenes.er(c, t, 'resident'), 1), 2.8), (_promo(scenes.theatre, 2), 2.8),
      (_promo(_consult, 3), 2.8), (_promo(lambda c, t: scenes.rich(c, t, car_in=False), 4), 3.4),
      (cta2('4 promotions to the top.', 'How fast can you climb?'), 3.4)]

VOICE = [(0.15, 'Four promotions from broke.', 2.3), (2.95, 'Promoted. Resident.', 2.3), (5.75, 'Promoted. Registrar.', 2.3),
         (8.55, 'Promoted. Consultant.', 2.3), (11.35, 'Promoted. E.D. Director.', 2.8), (14.7, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    starts = [2.6, 5.4, 8.2, 11.0]
    cues = [(.05, 'pop'), (.9, 'pop')] + [(s - .25, 'whoosh') for s in starts] + [(s + .3, 'impact') for s in starts]
    cues += [(s + .55, f'step:{i + 1}') for i, s in enumerate(starts)] + [(s + .7, 'cash') for s in starts]
    cues += [(11.9 + i * .1, 'tick') for i in range(10)] + [(13.2, 'riser'), (14.4, 'impact'), (14.45, 'ding')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=2.6, lift=11.0, cta=14.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .14)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.8), (1, 0.25), (1, 2.2), (2, 0.5), (2, 2.4), (3, 2.2), (4, 0.6), (4, 3.0), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
