"""Case variant 02 — quote-first quiz: the patient's own words open the ad, then "What do you do first?" (A-D), the one-call
diagnosis box and the end card. Never reveals the diagnosis.
Video: python3 case_02.py <case-id> <out.mp4>      Preview: python3 case_02.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED


def q_hook(K):
    first = K['name'].split()[0]
    def f(c, t):
        bg(c, t); brand_bar(c)
        pulse = .5 + .5 * math.sin(t * 7)
        lab = f"JUST WALKED IN  ·  TRIAGE {K['triage']}"; w = tw(lab, 34) + 96
        rr(c, (W - w) / 2, 300, w, 70, 35, P(TRI[K['triage']])); c.drawCircle((W - w) / 2 + 40, 335, 10 + 4 * pulse, P('#ffffff', 255 - 90 * pulse))
        text(c, lab, (W - w) / 2 + 66, 347, 34, '#ffffff', 900)
        ring = (t * .9) % 1
        c.drawCircle(540, 640, 205 + ring * 90, P(TRI[K['triage']], 170 * (1 - ring), stroke=8))
        c.drawCircle(540, 640, 250, P(TEAL, 70, blur=80))
        face(c, 540, 640, 200, K['skin'], K['hair'], K['style'], 'pain', t)
        q = '“' + K['quote'] + '”'; size = 74; lines = wrap(q, size, 900, 940)
        if len(lines) > 3: size = 60; lines = wrap(q, size, 900, 940)
        n = int(len(q) * clamp((t - .1) / 2.2)); shown = 0; y = 980
        for i, ln in enumerate(lines):
            part = ln[:max(0, n - shown)]; shown += len(ln) + 1
            if part: text(c, part, 540 - tw(ln, size, 900) / 2, y + i * size * 1.15, size, '#ffffff', 900, shadow=.35)
        y += len(lines) * size * 1.15 + 10
        text(c, f"{K['name']}, {K['age']}", 540, y, 50, '#bfe9e4', 800, 'c', a=255 * ease((t - .1) / .4))
        if t > 3.4: pill(c, 540, 1480, "You're the doctor. Now what?", '#ffffff', INK, 40, pop((t - 3.4) / .4))
    return f


OPTS = [('A', 'talk', 'Talk', 'Ask what happened'), ('B', 'examine', 'Examine', 'Look for the signs'),
        ('C', 'tests', 'Tests', 'Order what matters'), ('D', 'treat', 'Treat', 'Act right now')]


def q_choice(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['What do you', 'do first?'], 356, 92, a=255 * ease(t / .3))
        card(c, 60, 520, 960, 130, 40)
        face(c, 140, 585, 48, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, K['name'], 210, 578, 38, INK, 900); text(c, K['problem'], 210, 620, 28, '#5b7083', 700)
        secs = int(t * 9); text(c, f"{secs // 60:02d}:{secs % 60:02d}", 980, 608, 56, RED, 900, 'r'); text(c, 'ON THE CLOCK', 980, 556, 20, '#5b7083', 800, 'r')
        active = int(max(0, t - 1.7) / .5) % 4
        for i, (L, ic, lab, sub) in enumerate(OPTS):
            a0 = .25 + i * .3
            if t < a0: continue
            k = ease((t - a0) / .35); y = 690 + i * 172; on = t > 1.7 and i == active
            c.save(); c.translate((1 - k) * (-500 if i % 2 else 500), 0)
            card(c, 60, y, 960, 150, 40)
            if on: rr(c, 60, y, 960, 150, 40, P(GOLD, stroke=10))
            c.drawCircle(140, y + 75, 46, P(GOLD if on else '#eef2f6')); text(c, L, 140, y + 94, 54, INK, 900, 'c')
            c.drawCircle(262, y + 75, 46, P(TEAL if on else TEAL_D)); icon(c, ic, 262, y + 75, 56)
            text(c, lab, 334, y + 72, 50, INK, 900); text(c, sub, 334, y + 116, 30, '#5b7083', 700)
            c.restore()
        chip(c, 60, 1400, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
    return f


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(q_hook(K), 5.0), (q_choice(K), 4.0), (SC[2][0], 3.8), (SC[3][0], 3.8)]


def script(K):
    first = K['name'].split()[0]
    return [(0.2, f"{first}, {K['age']}. {K['quote']}", 4.6), (5.2, 'What do you do first?', 3.0),
            (9.2, 'One call. Get it right.', 3.2), (13.0, f'{first} is waiting. Bedside Bay. Play free.', 3.3)]


def soundtrack(K, SC, wav):
    import sound
    cues = [(.05, 'beep'), (.55, 'beep')] + [(.2 + i * .12, 'tick') for i in range(18)] + [(3.4, 'pop'), (4.75, 'whoosh'), (8.75, 'whoosh'), (12.55, 'riser'), (12.8, 'impact')]
    cues += [(5.25 + i * .3, 'pop') for i in range(4)] + [(6.7 + i * .5, 'tick') for i in range(4)] + [(10.7, 'ding'), (11.1, 'beep')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=5.0, lift=9.0, cta=12.8, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.2), (0, 3.8), (1, 1.2), (1, 3.4), (2, 3.2), (3, 3.2)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 4)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
