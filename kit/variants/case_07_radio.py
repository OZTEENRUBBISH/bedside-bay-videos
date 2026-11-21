"""Case variant 07 — "Dr Smith, come in." The case arrives as a call on a handheld two-way radio (pulsing waveform, caption
strip), the patient's own words run as live captions under the portrait, the four moves are four radio channels to pick
from, then the one-call diagnosis box and the end card. Never reveals the diagnosis. Music: upbeat.
Video: python3 case_07_radio.py <case-id> <out.mp4>      Preview: python3 case_07_radio.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

BAY = 4
GREEN = '#3ee08a'


def radio(c, cx, cy, t, talking=True):
    """Illustrated handheld radio, about 280 x 640 including the antenna."""
    c.save(); c.translate(cx + (math.sin(t * 40) * 3 if talking else 0), cy); c.rotate(-8)
    rr(c, -120, -200 + 16, 250, 440, 40, P('#000000', 100, blur=26))
    rr(c, 50, -330, 34, 150, 14, P('#1a222b')); c.drawCircle(67, -334, 20, P('#1a222b'))  # antenna
    rr(c, -80, -236, 70, 50, 12, P('#3a4756')); rr(c, -72, -250, 54, 22, 8, P('#55657a'))  # knob
    rr(c, -134, -90, 22, 130, 10, P(GOLD if talking else '#55657a'))  # push-to-talk
    rr(c, -120, -200, 240, 440, 40, P('#25303d')); rr(c, -120, -200, 240, 440, 40, P('#3a4756', stroke=6))
    rr(c, -90, -168, 180, 110, 16, P('#0b1218')); text(c, f'BAY {BAY}', 0, -112, 44, GREEN, 900, 'c')
    text(c, 'ER  ·  CH 1', 0, -76, 22, GREEN, 800, 'c', a=180)
    for i in range(6): rr(c, -80, -20 + i * 34, 160, 14, 7, P('#131b23'))  # speaker grille
    c.drawCircle(84, 204, 12, P(RED, 255 if (t * 3) % 1 < .6 else 90))
    c.restore()


def wave(c, cx, cy, t, n=31, w=14, gap=10, amp=70, col=GREEN, a=255):
    for i in range(n):
        d = abs(i - n // 2) / (n / 2)
        h = 10 + amp * (1 - d * .7) * abs(math.sin(t * 9 + i * .9) * math.sin(t * 5.3 + i * .37))
        x = cx + (i - n // 2) * (w + gap)
        rr(c, x - w / 2, cy - h, w, 2 * h, w / 2, P(col, a))


def k_radio(K):
    tri = TRI[K['triage']]; msg = f'Patient for you in bay {BAY}.'
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Dr Smith,', 'come in.', 372, size=116, sub_size=116);
        c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 516, W, 400))
        for j in range(3):  # signal arcs either side of the antenna
            k = (t * 1.1 + j / 3) % 1; r = 70 + k * 110
            for s in (-1, 1):
                c.drawArc(skia.Rect.MakeXYWH(596 - r, 640 - r, 2 * r, 2 * r), -90 + s * 55 - 26, 52, False, P(GREEN, 220 * (1 - k), stroke=12))
        c.restore()
        radio(c, 540, 920, t)
        wave(c, 540, 1240, t)
        # caption strip
        rr(c, 60, 1330, 960, 130, 30, P('#000000', 215)); rr(c, 84, 1356, 150, 78, 20, P(GREEN)); text(c, 'RADIO', 159, 1409, 36, '#0b1218', 900, 'c')
        typed = msg[:int(clamp((t - .4) / 1.4) * len(msg))]
        text(c, typed, 262, 1414, fit(msg, 54, 730, 800), '#ffffff', 800)
        if t > 2.2:
            lab = f"{K['name']}, {K['age']}  ·  {K['problem']}  ·  Triage {K['triage']}"; s = fit(lab, 40, 800, 800); w = tw(lab, s) + 74
            c.save(); c.translate(540, 1530); k = pop((t - 2.2) / .4); c.scale(k, k)
            chip(c, -w / 2, -(s + 26) / 2, lab, '#ffffff', INK, s, dot=tri); c.restore()
    return f


def k_subs(K, dur):
    q = K['quote']; tri = TRI[K['triage']]
    def f(c, t):
        bg(c, t); brand_bar(c)
        k0 = ease(t / .3)
        text(c, f'BAY {BAY}', 540, 388, 60, GOLD, 900, 'c', a=255 * k0, shadow=.35)
        for j in range(2):
            ring = (t * .9 + j * .5) % 1
            c.drawCircle(540, 660, 220 + ring * 110, P(tri, 170 * (1 - ring), stroke=10))
        face(c, 540, 660, 220 * pop(t / .4), K['skin'], K['hair'], K['style'], 'pain', t)
        pill(c, 540, 930, f"{K['name']}, {K['age']}", '#ffffff', INK, 54, k0)
        pill(c, 540, 1020, f"{K['problem']}  ·  Triage {K['triage']}", tri, INK if K['triage'] == 3 else '#ffffff', 38, k0)
        # live captions box
        size = 66; lines = wrap(q, size, 800, 860)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 800, 860)
        lh = size * 1.22; bh = 96 + len(lines) * lh; y0 = 1090
        rr(c, 60, y0, 960, bh, 34, P('#000000', 215 * k0))
        c.drawCircle(104, y0 + 46, 11, P(RED, 255 if (t * 2) % 1 < .6 else 80)); text(c, 'LIVE CAPTIONS', 128, y0 + 57, 30, '#bfe9e4', 900, a=255 * k0)
        c.save(); c.translate(900, y0 + 46); wave(c, 0, 0, t, n=9, w=8, gap=6, amp=22); c.restore()
        n = len(q.split()); cur = int(clamp((t - .8) / (dur - 2.4)) * n + .999) if t > .8 else 0
        wi = 0
        for i, ln in enumerate(lines):
            x = 110
            for w in ln.split():
                if wi < cur: text(c, w, x, y0 + 84 + size * .78 + i * lh, size, GOLD if wi == cur - 1 and cur < n else '#ffffff', 800)
                x += tw(w + ' ', size, 800); wi += 1
        if t > dur - 1.2: pill(c, 540, min(y0 + bh + 80, 1540), 'What’s your first move?', GOLD, INK, 50, pop((t - dur + 1.2) / .4))
    return f


CH = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Act before it gets worse')]


def k_channels(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Four moves.', 'Your call.', 372, size=104, sub_size=104, a=255 * ease(t / .3))
        active = int(max(0, t - 1.4) / .5) % 4 if t > 1.4 else -1
        for i, (ic, lab, sub) in enumerate(CH):
            k = ease((t - .2 - i * .2) / .35)
            if k <= 0: continue
            on = i == active; y = 560 + i * 196
            c.save(); c.translate((1 - k) * (-900 if i % 2 == 0 else 900), 0); c.translate(540, y + 84); s = 1.03 if on else 1.0; c.scale(s, s); c.translate(-540, -(y + 84))
            card(c, 60, y, 960, 168, 40)
            if on: rr(c, 60, y, 960, 168, 40, P(GOLD, stroke=10))
            rr(c, 84, y + 24, 150, 120, 24, P('#0b1218')); text(c, 'CH', 159, y + 68, 30, GREEN, 900, 'c', a=170); text(c, str(i + 1), 159, y + 126, 62, GREEN, 900, 'c')
            c.drawCircle(318, y + 84, 54, P(TEAL if on else TEAL_D)); icon(c, ic, 318, y + 84, 66)
            text(c, lab, 398, y + 80, 58, INK, 900); text(c, sub, 398, y + 126, 32, '#5b7083', 700)
            for b in range(4):  # signal bars
                h = 22 + b * 18; lit = on and b <= int((t * 8) % 5)
                rr(c, 884 + b * 28, y + 128 - h, 18, h, 6, P(GREEN if lit else '#cfd9e2'))
            c.restore()
        first = K['name'].split()[0]
        if t > 2.0:
            lab = f'{first} is still waiting'; w = tw(lab, 40) + 74
            c.save(); c.translate(540, 1410); k = pop((t - 2.0) / .4); c.scale(k, k)
            chip(c, -w / 2, -33, lab, '#ffffff', INK, 40, dot=TRI[K['triage']]); c.restore()
    return f


D0, D_Q, D2 = 3.3, 5.4, 3.6


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(k_radio(K), D0), (k_subs(K, D_Q), D_Q), (k_channels(K), D2), (SC[2][0], 3.5), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]
    num = ['one', 'two', 'three', 'four', 'five', 'six'][BAY - 1]
    a, b, c_ = D0, D0 + D_Q, D0 + D_Q + D2
    return [(0.15, f'Doctor Smith, come in. Patient in bay {num}.', D0 - .35), (a + .2, f"{first}, {K['age']}. {K['quote']}", D_Q - .4),
            (b + .2, 'Four moves. Your call.', D2 - .5), (c_ + .2, 'One call. Get it right.', 3.0), (c_ + 3.7, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    n = len(K['quote'].split()); a, b, c_ = D0, D0 + D_Q, D0 + D_Q + D2; e = c_ + 3.5
    cues = [(.05, 'beep'), (.35, 'beep')] + [(.45 + i * .17, 'tick') for i in range(8)] + [(2.2, 'pop'), (a - .25, 'whoosh')]
    cues += [(a + .05, 'beep')] + [(a + .8 + i * (D_Q - 2.4) / n, 'tick') for i in range(n)] + [(b - 1.2, 'ding'), (b - .25, 'whoosh')]
    cues += [(b + .2 + i * .2, 'pop') for i in range(4)] + [(b + 1.4 + i * .5, 'tick') for i in range(4)] + [(b + 2.0, 'pop')]
    cues += [(c_ - .25, 'whoosh'), (c_ + 1.7, 'ding'), (c_ + 2.1, 'beep'), (e - 1.2, 'riser'), (e, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=a, lift=c_, cta=e, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.4), (0, 3.0), (1, 0.6), (1, 2.6), (1, 5.0), (2, 1.0), (2, 2.9), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 5)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
