"""Full Game variant 02 — "163 patients. One doctor." (waiting-room queue, triage board, checklist, mode grid, rank morph).
Video:   python3 fullgame_02.py <out.mp4>          Preview: python3 fullgame_02.py preview <sheet.jpg>
Photos:  python3 fullgame_02.py photos <prefix>    ("The whole game in 4 swipes", 6 slides; add `preview <sheet.jpg>` to also write a sheet)"""
from common import *
import json
from case import bg, card, chip, TRI

CASES = json.load(open(os.path.join(KIT, 'cases.json')))
BYID = {k['id']: k for k in CASES}


def _tri_dot(c, x, y, n, r=30):
    c.drawCircle(x, y, r + 5, P('#ffffff')); c.drawCircle(x, y, r, P(TRI[n])); text(c, str(n), x, y + r * .42, r * 1.2, '#ffffff', 900, 'c')


def s_queue(c, t, hl=('163 patients.', 'One doctor.')):
    bg(c, t); brand_bar(c)
    headline(c, list(hl), 372, 96)
    span = 230 * 6
    for row, (y, sp) in enumerate(((730, 70), (980, -70))):
        for i in range(6):
            K = CASES[(i * 5 + row * 3 + 1) % len(CASES)]
            x = ((i * 230 + t * sp + row * 115) % span) - 150
            face(c, x, y, 98, K['skin'], K['hair'], K['style'], 'pain' if (i + row) % 3 else 'ok', t + i)
            _tri_dot(c, x + 72, y - 72, K['triage'])
    c.drawCircle(540, 1290, 250, P(TEAL, 60, blur=90))
    doctor(c, 540, 1540, .7, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 14, mood='happy')
    k = pop((t - .4) / .4)
    if t > .4: pill(c, 250, 1250, 'WAITING: 163', '#e5484d', '#ffffff', 34, k)
    chip(c, 60, 1440, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)


BOARD = ['joan-harper', 'clive-dunn', 'lucy-grant', 'kai-tanaka']


def s_triage(c, t, hl=('Who do you', 'see first?')):
    bg(c, t); brand_bar(c)
    headline(c, list(hl), 372, 92, a=255 * ease(t / .3))
    active = int(max(0, t - 1.3) / .42) % 4
    for i, cid in enumerate(BOARD):
        K = BYID[cid]; a0 = .15 + i * .22
        if t < a0: continue
        k = ease((t - a0) / .35); y = 590 + i * 215
        c.save(); c.translate((1 - k) * 500, 0)
        card(c, 60, y, 960, 190, 40)
        if t > 1.3 and i == active: rr(c, 60, y, 960, 190, 40, P(TEAL, stroke=10))
        face(c, 160, y + 95, 70, K['skin'], K['hair'], K['style'], 'pain', t + i)
        text(c, f"{K['name']}, {K['age']}", 256, y + 84, 46, INK, 900)
        chip(c, 256, y + 106, K['problem'], '#e2f4f1', TEAL_D, 28)
        lab = f"TRIAGE {K['triage']}"; w = tw(lab, 30) + 44
        rr(c, 990 - w, y + 64, w, 62, 31, P(TRI[K['triage']])); text(c, lab, 990 - w + 22, y + 106, 30, '#ffffff', 900)
        c.restore()
    if t > 1.5: pill(c, 540, 1500, 'Triage 1 to 5. Your call.', '#ffffff', INK, 38, pop((t - 1.5) / .4))


STEPS = [('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat')]


def s_play(c, t, hl=('Talk. Examine.', 'Tests. Treat.')):
    scenes.er(c, t + 2, 'resident'); brand_bar(c)
    headline(c, list(hl), 356, 92, INK, shadow=0)
    card(c, 60, 1262, 880, 330, 44)
    for i, (ic, lab) in enumerate(STEPS):
        x = 60 + (i % 2) * 440; y = 1262 + (i // 2) * 165; a0 = .3 + i * .55
        c.drawCircle(x + 84, y + 82, 50, P(TEAL if t >= a0 else '#c3cfda')); icon(c, ic, x + 84, y + 82, 60)
        text(c, lab, x + 152, y + 100, 48, INK if t >= a0 else '#8a9bab', 900)
        if t >= a0:
            k = pop((t - a0) / .35); c.save(); c.translate(x + 392, y + 82); c.scale(k, k)
            c.drawCircle(0, 0, 26, P('#1f9d63')); check(c, 0, 2, 12, '#ffffff', 6); c.restore()


MODES = [('career', 'Career'), ('shift', 'Quick shift'), ('practice', 'Case practice'), ('firstaid', 'First aid')]


def s_modes(c, t, hl=('Four modes.', 'Pick yours.')):
    bg(c, t); brand_bar(c)
    headline(c, list(hl), 372, 92, a=255 * ease(t / .3))
    active = int(max(0, t - 1.5) / .4) % 4
    for i, (ic, lab) in enumerate(MODES):
        a0 = .2 + i * .28
        if t < a0: continue
        k = pop((t - a0) / .4); x = 60 + (i % 2) * 455; y = 600 + (i // 2) * 430
        c.save(); c.translate(x + 215, y + 200); c.scale(k, k); c.translate(-215, -200)
        card(c, 0, 0, 430, 400, 44)
        if t > 1.5 and i == active: rr(c, 0, 0, 430, 400, 44, P(GOLD, stroke=10))
        c.drawCircle(215, 150, 96, P(TEAL if i != 3 else '#e5484d')); icon(c, ic, 215, 150, 116)
        text(c, lab, 215, 332, 50, INK, 900, 'c'); c.restore()


OUT = ['intern', 'resident', 'surgeon', 'consultant', 'director']
BANK = [2000, 18400, 38500, 264000, 2480000]  # illustrative after the $2,000 start


def s_ladder(c, t, hl=('Intern to', 'ED Director.')):
    bg(c, t); brand_bar(c)
    headline(c, list(hl), 372, 92, a=255 * ease(t / .3))
    step = .58; i = min(4, int(t / step)); lt = t - i * step
    c.drawCircle(540, 900, 300, P(GOLD if i == 4 else TEAL, 70, blur=100))
    doctor(c, 540, 1236, 1.0, OUT[i], t, la=10, ra=-150 + math.sin(t * 6) * 12 if i == 4 else -12, mood='tired' if i == 0 else 'happy')
    if i > 0 and lt < .45:
        k = lt / .45
        c.drawCircle(540, 900, 120 + 320 * k, P('#ffffff', 190 * (1 - k), blur=30))
        for j in range(6):
            a = j * math.pi / 3 + t; sparkle(c, 540 + math.cos(a) * (170 + 120 * k), 900 + math.sin(a) * (190 + 120 * k), 22, 255 * (1 - k), GOLD)
    bank = BANK[i] if i == 0 else lerp(BANK[i - 1], BANK[i], eio(lt / .4))
    hud(c, i, bank, i + ease(lt / .4), bump=abs(math.sin(t * 9)) * .5 if lt < .4 and i else 0)


SC = [(s_queue, 2.8), (s_triage, 3.0), (s_play, 3.2), (s_modes, 3.0), (s_ladder, 3.4),
      (cta2('163 patients are waiting.', 'Start your first shift.'), 3.4)]


def compose(i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t)
    return f


def soundtrack(wav):
    import sound
    st = [0, 2.8, 5.8, 9.0, 12.0, 15.4]
    cues = [(.4, 'pop'), (2.55, 'whoosh'), (5.55, 'whoosh'), (8.75, 'whoosh'), (11.75, 'whoosh'), (14.2, 'riser'), (15.4, 'impact')]
    cues += [(2.95 + i * .22, 'pop') for i in range(4)] + [(4.1 + i * .42, 'tick') for i in range(4)]
    cues += [(6.1 + i * .55, 'ding') for i in range(4)] + [(9.2 + i * .28, 'pop') for i in range(4)]
    cues += [(12.0 + i * .58, f'step:{i}') for i in range(5)] + [(14.32, 'cash')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=2.8, lift=9.0, cta=15.4, cues=cues,
        voice=[(0.15, 'A hundred and sixty-three patients. One doctor.', 2.6), (3.0, 'Who do you see first?', 2.6),
               (6.0, 'Talk. Examine. Test. Treat.', 3.0), (9.2, 'Four modes. Pick yours.', 2.7),
               (12.2, 'Climb from intern to E.D. Director.', 3.1), (15.7, 'Bedside Bay. Play free.', 2.9)])


# ---------------------------------------------------------------- photo set: "The whole game in 4 swipes"
def p_hook(c, t=1.0):
    bg(c, t); brand_bar(c)
    headline(c, ['New here?', 'The whole game', 'in 4 swipes.'], 372, 88)
    c.drawCircle(540, 1090, 330, P(TEAL, 60, blur=90))
    doctor(c, 540, 1440, 1.0, 'resident', t, la=10, ra=-150, mood='happy')
    chip(c, 60, 1470, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)
    swipe(c, 640, 1462)


def _num(c, n):
    c.drawCircle(930, 196, 50, P(GOLD)); text(c, f'{n}/4', 930, 212, 40, INK, 900, 'c')


def photos():
    def s(fn, t, hl, n):
        def f(c): fn(c, t, hl); _num(c, n)
        return f
    return [lambda c: p_hook(c),
            s(s_queue, 1.5, ('Treat', '163 patients.'), 1),
            s(s_play, 3.0, ('Talk. Examine.', 'Tests. Treat.'), 2),
            s(s_ladder, 3.3, ('Climb', 'five ranks.'), 3),
            s(s_modes, 1.45, ('Pick from', 'four modes.'), 4),
            lambda c: cta2('163 patients are waiting.', 'Start as an intern.')(c, 2.5)]


if __name__ == '__main__':
    if sys.argv[1] == 'preview':
        pts = [(0, 0.0), (0, 1.8), (1, 2.4), (2, 1.2), (2, 3.0), (3, 2.6), (4, 0.4), (4, 1.4), (4, 3.2), (5, 2.5)]
        contact_sheet([frame(compose(i), t) for i, t in pts], sys.argv[2], 5)
    elif sys.argv[1] == 'photos':
        fr = save_slides(photos(), sys.argv[2])
        if len(sys.argv) > 4: contact_sheet(fr, sys.argv[4], 6)
    else:
        out = sys.argv[1]; wav = out[:-4] + '.wav'
        for r in soundtrack(wav): print(r)
        render_video([(compose(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
