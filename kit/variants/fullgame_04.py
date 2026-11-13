"""Full Game variant 04 — "4 ways to play doctor." The whole game told mode by mode (numbered 1-4): Career, Quick shift,
Case practice, First aid. Music: bright.
Video: python3 fullgame_04.py <out.mp4>          Preview: python3 fullgame_04.py preview <sheet.jpg>"""
from common import *
import fullgame_02 as f2
from case import bg, card, chip, TRI, RED

f2.BOARD = ['victor-petrov', 'zoe-martin', 'bob-harris', 'ben-taylor']  # a different queue from variant 02
MODES = [('career', 'Career', 220, 760), ('shift', 'Quick shift', 870, 740), ('practice', 'Case practice', 220, 1180), ('firstaid', 'First aid', 860, 1180)]


def m_hook(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['4 ways to', 'play doctor.'], 372, 100)
    c.drawCircle(540, 1020, 300, P(TEAL, 60, blur=90))
    doctor(c, 540, 1330, .92, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')
    for i, (ic, lab, x, y) in enumerate(MODES):
        a0 = .15 + i * .3
        if t < a0: continue
        k = pop((t - a0) / .4); y += math.sin(t * 2.2 + i) * 8
        c.save(); c.translate(x, y); c.scale(k, k)
        c.drawCircle(0, 8, 100, P('#000000', 80, blur=18)); c.drawCircle(0, 0, 100, P('#ffffff'))
        c.drawCircle(0, 0, 84, P(RED if ic == 'firstaid' else TEAL)); icon(c, ic, 0, 0, 100)
        c.drawCircle(-74, -74, 34, P(GOLD)); text(c, str(i + 1), -74, -58, 44, INK, 900, 'c')
        c.restore()
        pill(c, x, y + 140, lab, '#ffffff', INK, 34, k)
    chip(c, 60, 1440, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)


def _m(fn, top, sub, col='#ffffff', top_col=GOLD):
    def f(c, t):
        fn(c, t, ()); k = ease(t / .3)
        title2(c, top, sub, 356, col, top_col, a=255 * k, dy=(1 - k) * 30, shadow=0 if col == INK else .35)
    return f


def m_firstaid(c, t):
    bg(c, t); brand_bar(c); k = ease(t / .3)
    title2(c, '4. First aid', 'When seconds count.', 356, a=255 * k, dy=(1 - k) * 30)
    for j in range(3):
        ring = (t * .7 + j / 3) % 1
        c.drawCircle(360, 900, 150 + ring * 190, P(RED, 150 * (1 - ring), stroke=8))
    s = pop(t / .45) * (1 + .04 * math.sin(t * 7))
    c.save(); c.translate(360, 900); c.scale(s, s)
    c.drawCircle(0, 10, 160, P('#000000', 80, blur=22)); c.drawCircle(0, 0, 160, P('#ffffff')); c.drawCircle(0, 0, 136, P(RED)); icon(c, 'firstaid', 0, 0, 170)
    c.restore()
    doctor(c, 790, 1330, .92, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')
    if t > .7: pill(c, 360, 1210, 'MODE 4 OF 4', '#ffffff', INK, 36, pop((t - .7) / .4))
    chip(c, 60, 1440, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)


SC = [(m_hook, 2.8), (_m(f2.s_ladder, '1. Career', 'Intern to ED Director.'), 3.4),
      (_m(f2.s_triage, '2. Quick shift', 'Who do you see first?'), 3.0),
      (_m(f2.s_play, '3. Case practice', 'Talk. Examine. Tests. Treat.', INK, TEAL_D), 3.2),
      (m_firstaid, 2.6), (cta2('163 patients. Four modes.', 'Pick one and start.'), 3.4)]


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t)
    return f


VOICE = [(0.15, 'Four ways to play doctor.', 2.5), (3.0, 'One. Career. Intern to E.D. Director.', 3.1),
         (6.4, 'Two. Quick shift. Who do you see first?', 2.7), (9.4, 'Three. Case practice. Talk, examine, test, treat.', 2.9),
         (12.6, 'Four. First aid.', 2.3), (15.3, 'Bedside Bay. Play free.', 2.8)]


def soundtrack(wav):
    import sound
    cues = [(.15 + i * .3, 'pop') for i in range(4)] + [(2.55, 'whoosh'), (5.95, 'whoosh'), (8.95, 'whoosh'), (12.15, 'whoosh'), (13.8, 'riser'), (15.0, 'impact')]
    cues += [(2.8 + i * .58, f'step:{i}') for i in range(5)] + [(5.2, 'cash')]
    cues += [(6.35 + i * .22, 'pop') for i in range(4)] + [(7.5 + i * .42, 'tick') for i in range(3)]
    cues += [(9.5 + i * .55, 'ding') for i in range(4)] + [(12.45, 'beep'), (12.85, 'beep'), (13.1, 'pop')]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=2.8, lift=9.2, cta=15.0, cues=cues, voice=VOICE)


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 2.2), (1, 0.4), (1, 3.2), (2, 2.4), (3, 0.5), (3, 3.0), (4, 0.3), (4, 2.2), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
