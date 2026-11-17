"""Broke to Rich variant 09 — "Mom keeps texting Dr John Smith." The climb told as a text thread drawn over each scene: Mom
asks, John's reply shows the new rank (noodles, promoted, in surgery, consultant, "whose car is that?"). Bank amounts after
the $2,000 start are illustrative. Music: bright.
Video: python3 b2r_09_mom_texts.py <out.mp4>          Preview: python3 b2r_09_mom_texts.py preview <sheet.jpg>"""
from common import *
from fullgame_02 import BANK
from b2r_ranks_photos import _consult

THREAD = [('Are you eating properly?', 'Noodles. Again.'), ('How’s the new job?', 'Promoted. Resident now.'),
          ('Call me back!', 'Can’t. In surgery.'), ('Still at work?', 'Made Consultant, Mom.'),
          ('WHOSE CAR IS THAT?', 'Mine. ED Director now.')]


def _bub(c, x, y, w, col, k, right):
    ax = x + w if right else x
    c.save(); c.translate(ax, y + 104); c.scale(k, k); c.translate(-ax, -(y + 104))
    rr(c, x, y + 8, w, 104, 46, P('#000000', 90, blur=16)); rr(c, x, y, w, 104, 46, P(col))
    tail = skia.Path()
    if right: tail.moveTo(x + w - 54, y + 96); tail.lineTo(x + w + 6, y + 118); tail.lineTo(x + w - 18, y + 70)
    else: tail.moveTo(x + 54, y + 96); tail.lineTo(x - 6, y + 118); tail.lineTo(x + 18, y + 70)
    tail.close(); c.drawPath(tail, P(col))


def chat(c, t, mom, john, am=.15, aj=1.15, y=286):
    """Mom's text (left, white, with her avatar) then John's reply (right, teal) in the headline area."""
    if t >= am:
        k = pop((t - am) / .3); s = fit(mom, 46, 720, 800); w = tw(mom, s, 800) + 64
        c.drawCircle(104, y + 56, 52, P('#000000', 70, blur=10))
        face(c, 104, y + 52, 50, '#f0c29b', '#b9bcc2', 'bob', 'ok', t, gown=False)
        rr(c, 62, y + 92, 84, 34, 17, P(INK)); text(c, 'MOM', 104, y + 117, 22, '#ffffff', 900, 'c')
        _bub(c, 176, y, w, '#ffffff', k, False); text(c, mom, 176 + 32, y + 52 + s * .36, s, INK, 800); c.restore()
    if am + .5 <= t < aj:  # typing dots
        _bub(c, 1020 - 170, y + 128, 170, TEAL, 1, True)
        for i in range(3):
            c.drawCircle(1020 - 125 + i * 40, y + 180 - 8 * max(0, math.sin((t - am) * 12 - i * .9)), 11, P('#ffffff'))
        c.restore()
    if t >= aj:
        k = pop((t - aj) / .3); s = fit(john, 46, 760, 800); w = tw(john, s, 800) + 64
        _bub(c, 1020 - w, y + 128, w, TEAL, k, True); text(c, john, 1020 - w + 32, y + 180 + s * .36, s, '#ffffff', 800); c.restore()


def m_hook(c, t):
    scenes.poor(c, t)
    a = 255 * clamp((1.55 - t) / .2)
    if a > 0: title2(c, 'Mom keeps texting', 'Dr John Smith.', 356, a=a, size=100, sub_size=92)
    chat(c, t, *THREAD[0], am=1.6, aj=2.6)
    hud(c, 0, 2000, 1); brand_bar(c)
    if t > .5: pill(c, 250, 980, 'Broke intern', GOLD, INK, 44, pop((t - .5) / .35))


def _step(fn, i):
    def f(c, t):
        fn(c, t)
        chat(c, t, *THREAD[i])
        up = t >= 1.15
        bank = lerp(BANK[i - 1], BANK[i], eio((t - 1.15) / 1.0))
        hud(c, i if up else i - 1, bank, i + clamp((t - 1.15) / .5), bump=math.sin(clamp((t - 1.15) / .5) * math.pi)); brand_bar(c)
        if 1.15 < t < 1.8:
            k = (t - 1.15) / .65
            for j in range(6):
                a = j * math.pi / 3 + t; sparkle(c, 250 + math.cos(a) * (120 + 90 * k), 1384 + math.sin(a) * (90 + 60 * k), 22, 255 * (1 - k), GOLD)
    return f


SC = [(m_hook, 3.7), (_step(lambda c, t: scenes.er(c, t, 'resident'), 1), 2.8), (_step(scenes.theatre, 2), 2.8),
      (_step(_consult, 3), 2.8), (_step(lambda c, t: scenes.rich(c, t, car_in=True), 4), 3.3),
      (cta2('Start as a broke intern.', 'Make Mom proud.'), 3.4)]

VOICE = [(0.15, 'Mom keeps texting Doctor John Smith.', 2.6), (4.1, 'Promoted. Resident now.', 2.2), (6.9, 'Can’t talk. In surgery.', 2.2),
         (9.7, 'Made consultant, Mom.', 2.2), (12.5, 'Whose car is that? Mine.', 2.7), (15.7, 'Make Mom proud. Bedside Bay. Play free.', 3.0)]


def soundtrack(wav):
    import sound
    st = [3.7, 6.5, 9.3, 12.1]
    cues = [(.05, 'pop'), (.5, 'pop'), (1.6, 'ding'), (2.6, 'pop')] + [(s - .25, 'whoosh') for s in st] + [(s + .15, 'ding') for s in st]
    cues += [(s + 1.15, 'pop') for s in st] + [(s + 1.3, f'step:{i + 1}') for i, s in enumerate(st)] + [(s + 1.45, 'cash') for s in st]
    cues += [(14.2, 'riser'), (15.4, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=3.7, lift=12.1, cta=15.4, cues=cues, voice=VOICE)


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t, .14)
    return f


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.2), (0, 3.4), (1, 0.4), (1, 0.9), (1, 2.5), (2, 2.5), (3, 2.5), (4, 0.6), (4, 3.0)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
