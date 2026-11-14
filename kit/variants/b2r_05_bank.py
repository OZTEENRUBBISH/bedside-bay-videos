"""Broke to Rich variant 05 — "Watch this bank balance." The bank balance is the headline: one big balance card on top of
every scene, counting up from the $2,000 start while Dr John Smith climbs. Amounts after $2,000 are illustrative. Music: bright.
Video: python3 b2r_05_bank.py <out.mp4>          Preview: python3 b2r_05_bank.py preview <sheet.jpg>"""
from common import *
import video  # hud_state of the original model (rank / bank / ladder timing)

GREEN = '#1f9d63'


def bank_card(c, bank, rank_i, prog, bump=0.0, y=292):
    """The hero: a wide balance card where the headline normally sits."""
    x, w, h = 60, 960, 290
    rr(c, x, y + 12, w, h, 48, P('#000000', 90, blur=26)); rr(c, x, y, w, h, 48, P('#ffffff'))
    text(c, 'DR JOHN SMITH  ·  BANK BALANCE', x + 44, y + 62, 28, '#5b7083', 800)
    lab = RANKS[rank_i].upper(); cw = tw(lab, 28, 900) + 48; gold = rank_i == 4
    rr(c, x + w - 40 - cw, y + 26, cw, 54, 27, P(GOLD if gold else TEAL)); text(c, lab, x + w - 40 - cw / 2, y + 63, 28, INK if gold else '#ffffff', 900, 'c')
    s = 132 * (1 + .05 * bump)
    text(c, '$' + f'{int(bank):,}', x + 44, y + 190, s, TEAL_D, 900)
    sw = (w - 88 - 4 * 12) / 5
    for i in range(5):
        sx = x + 44 + i * (sw + 12)
        rr(c, sx, y + 222, sw, 16, 8, P('#dfe7ee'))
        f = clamp(prog - i)
        if f > 0: rr(c, sx, y + 222, sw * f, 16, 8, P(GOLD if i == 4 else TEAL))
        text(c, RANKS[i], sx + sw / 2, y + 268, 22, INK if i == rank_i else '#8a9bab', 800, 'c')


def gain(c, label, t, a0, x=770, y=1150):
    """A green '+$' tag that floats up and fades."""
    k = (t - a0) / 1.1
    if not 0 < k < 1: return
    a = 255 * clamp(k * 6) * clamp((1 - k) * 3); w = tw(label, 46, 900) + 56
    c.save(); c.translate(x, y - 150 * ease(k))
    rr(c, -w / 2, -40, w, 80, 40, P('#000000', a * .3, blur=12)); rr(c, -w / 2, -44, w, 80, 40, P(GREEN, a))
    text(c, label, 0, 12, 46, '#ffffff', 900, 'c', a=a); c.restore()


def caption(c, label, t, a0=.25, y=1400):
    if t > a0: pill(c, 540, y, label, '#ffffff', INK, 54, pop((t - a0) / .4))


def b_hook(c, t):
    scenes.poor(c, t)
    bank_card(c, 2000, 0, 1.0); brand_bar(c)
    b = abs(math.sin(t * 5)) * 22
    ar = skia.Path(); ar.moveTo(540, 1150 + b); ar.lineTo(620, 1250 + b); ar.lineTo(460, 1250 + b); ar.close(); c.drawPath(ar, P(GOLD))
    rr(c, 510, 1240 + b, 60, 50, 0, P(GOLD))
    pill(c, 540, 1340 + b, 'WATCH THIS NUMBER', GOLD, INK, 60, .85 + .15 * pop(t / .35))
    caption(c, 'Day 1. Broke intern.', t, .9, 1500)


GAINS = {1: ((.5, '+$4,200'), (1.6, '+$9,500'), (2.9, '+$22,800')), 2: ((.5, '+$85,000'), (1.75, '+$140,000')), 3: ((.3, '+$2,216,000'),)}
CAPS = {1: 'Every case pays.', 2: 'Promotions pay more.', 3: 'ED Director money.'}


def _climb(fn, idx):
    def f(c, t):
        fn(c, t)
        r, bank, prog, bump = video.hud_state(idx, t, 1)
        for a0, lab in GAINS[idx]: gain(c, lab, t, a0, 540 if idx == 3 else 770, 1180 if idx == 3 else 1150)
        bank_card(c, bank, r, prog, bump * abs(math.sin(t * 9))); brand_bar(c)
        caption(c, CAPS[idx], t)
    return f


SC = [(b_hook, 2.6), (_climb(scenes.er, 1), 4.2), (_climb(scenes.theatre, 2), 3.2),
      (_climb(lambda c, t: scenes.rich(c, t, car_in=False), 3), 3.4),
      (cta2('From $2,000 to ED Director.', 'How high can you climb?'), 3.4)]

VOICE = [(0.15, 'Watch this bank balance.', 2.3), (2.9, 'Every case pays.', 3.0), (7.1, 'Promotions pay more.', 2.8),
         (10.3, 'E.D. Director money.', 2.8), (13.7, 'Bedside Bay. Play free.', 2.9)]


def soundtrack(wav):
    import sound
    cues = [(.05, 'pop'), (.9, 'pop'), (2.35, 'whoosh'), (6.55, 'whoosh'), (9.75, 'whoosh'), (12.2, 'riser'), (13.4, 'impact')]
    cues += [(2.6 + a, 'cash') for a, _ in GAINS[1]] + [(6.8 + a, 'cash') for a, _ in GAINS[2]] + [(10.3, 'cash'), (10.0, 'ding')]
    cues += [(10.3 + i * .12, 'tick') for i in range(20)]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=2.6, lift=6.8, cta=13.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.8), (1, 0.9), (1, 2.2), (1, 3.9), (2, 1.0), (2, 2.9), (3, 0.9), (3, 3.2), (4, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
