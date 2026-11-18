"""Case variant 05 — "Who's behind curtain 3?" A bay curtain slides open on the patient, the patient's own words light up
word by word, the four moves are dealt as a fanned hand of cards ("Play your first move."), then the one-call diagnosis box
and the end card. Never reveals the diagnosis. Music: upbeat.
Video: python3 case_05_curtain.py <case-id> <out.mp4>      Preview: python3 case_05_curtain.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

DX, DY, DW, DH = 110, 660, 860, 840  # the bay
BED = 3


def k_hook(K):
    tri = TRI[K['triage']]
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Who’s behind', f'curtain {BED}?'], 372, 104)
        o = eio((t - 1.0) / .8)  # curtain: 0 shut, 1 open
        c.save(); c.clipRect(skia.Rect.MakeXYWH(DX, DY, DW, DH))
        c.drawRect(skia.Rect.MakeXYWH(DX, DY, DW, DH), grad(0, DY, 0, DY + DH, ['#e3f2f5', '#c6e2e8']))
        c.drawRect(skia.Rect.MakeXYWH(DX, DY + DH - 170, DW, 170), P('#aecbd4'))
        rr(c, DX + 150, DY + 560, 560, 60, 20, P('#ffffff')); rr(c, DX + 130, DY + 610, 600, 40, 12, P('#93a7b5'))  # bed
        for j in range(2):
            ring = (t * .9 + j * .5) % 1
            c.drawCircle(540, DY + 360, 250 + ring * 130, P(tri, 170 * (1 - ring), stroke=10))
        face(c, 540, DY + 360, 200 + 40 * o, K['skin'], K['hair'], K['style'], 'pain', t)
        # curtain, gathered to the left as it opens
        n = 12; fw = DW * (1 - .88 * o) / n
        for i in range(n):
            x = DX + i * fw + math.sin(t * 3 + i * .8) * 4 * (1 - o)
            c.drawRect(skia.Rect.MakeXYWH(x, DY + 26, fw + 2, DH - 70 + (10 if i % 2 else 0)), grad(x, 0, x + fw, 0, ['#35a39a', '#2b8f87'] if i % 2 == 0 else ['#2b8f87', '#1f766f']))
        if o < 1:
            a = 255 * (1 - o)
            c.drawCircle(540 - 300 * o, DY + 400, 150, P('#ffffff', a * .9)); text(c, '?', 540 - 300 * o, DY + 470, 200, TEAL_D, 900, 'c', a=a)
        c.restore()
        rr(c, DX - 20, DY, DW + 40, 26, 13, P('#8ea2b1'))  # rail + hooks
        for i in range(n + 1): c.drawCircle(DX + i * DW * (1 - .88 * o) / n, DY + 30, 9, P('#5b7083'))
        rr(c, DX - 10, DY, 20, DH, 8, P('#8ea2b1')); rr(c, DX + DW - 10, DY, 20, DH, 8, P('#8ea2b1'))
        rr(c, 830, DY - 76, 170, 64, 14, P('#ffffff')); text(c, f'BED {BED}', 915, DY - 32, 38, INK, 900, 'c')
        if t > 1.9: pill(c, 540, DY + DH - 190, f"{K['name']}, {K['age']}", '#ffffff', INK, 58, pop((t - 1.9) / .4))
        if t > 2.3: pill(c, 540, DY + DH - 80, f"{K['problem']}  ·  Triage {K['triage']}", tri, '#ffffff', 42, pop((t - 2.3) / .4))
    return f


def k_words(K, dur):
    q = K['quote']
    def f(c, t):
        bg(c, t); brand_bar(c)
        k0 = ease(t / .3)
        face(c, 540, 440, 130 * k0, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}  ·  Bed {BED}", 540, 650, 46, '#bfe9e4', 800, 'c', a=255 * k0)
        size = 96; lines = wrap(q, size, 900, 960)
        while len(lines) > 5: size -= 4; lines = wrap(q, size, 900, 960)
        words = q.split(); n = len(words)
        cur = int(clamp((t - 1.2) / (dur - 2.4)) * n) if t > 1.2 else -1  # index of the word being said
        if t > dur - 1.2: cur = n
        wi = 0; y = 800
        for i, ln in enumerate(lines):
            x = 540 - tw(ln, size, 900) / 2
            for w in ln.split():
                col, a = ('#ffffff', 255) if wi < cur else ((GOLD, 255) if wi == cur else ('#ffffff', 70))
                text(c, w, x, y + i * size * 1.16, size, col, 900, a=a, shadow=.35 if wi <= cur else 0)
                x += tw(w + ' ', size, 900); wi += 1
        yb = y + len(lines) * size * 1.16 + 40
        if t > dur - 1.1: pill(c, 540, max(yb, 1400), 'What would you ask first?', GOLD, INK, 50, pop((t - dur + 1.1) / .4))
    return f


CARDS = [('talk', 'Talk', 'Get the story'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make it count')]


def k_cards(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Play your', 'first move.'], 372, 100, a=255 * ease(t / .3))
        active = int(max(0, t - 1.5) / .5) % 4 if t > 1.5 else -1
        order = [i for i in range(4) if i != active] + ([active] if active >= 0 else [])
        for i in order:
            ic, lab, sub = CARDS[i]
            k = ease((t - .2 - i * .18) / .4)
            if k <= 0: continue
            ang = (-18.75 + i * 12.5) * k; on = i == active
            c.save(); c.translate(540, 2110); c.rotate(ang); c.translate(0, -1100 - (80 if on else 0) + (1 - k) * 500)
            rr(c, -114, -200, 228, 420, 30, P('#000000', 90, blur=22)); rr(c, -114, -210, 228, 420, 30, P('#ffffff'))
            rr(c, -114, -210, 228, 420, 30, P(GOLD if on else '#c3cfda', stroke=10 if on else 4))
            text(c, str(i + 1), -86, -152, 42, '#8a9bab', 900)
            c.drawCircle(0, -60, 74, P(TEAL if on else TEAL_D)); icon(c, ic, 0, -60, 88)
            text(c, lab, 0, 92, fit(lab, 52, 196), INK, 900, 'c')
            for j, ln in enumerate(wrap(sub, 28, 700, 196)): text(c, ln, 0, 136 + j * 34, 28, '#5b7083', 700, 'c')
            c.restore()
        first = K['name'].split()[0]
        if t > 2.0:
            lab = f'{first} is still waiting'; w = tw(lab, 40) + 74
            c.save(); c.translate(540, 1420); k = pop((t - 2.0) / .4); c.scale(k, k)
            chip(c, -w / 2, -33, lab, '#ffffff', INK, 40, dot=TRI[K['triage']]); c.restore()
    return f


D_Q = 5.2


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(k_hook(K), 3.4), (k_words(K, D_Q), D_Q), (k_cards(K), 3.8), (SC[2][0], 3.6), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]
    num = ['one', 'two', 'three', 'four', 'five', 'six'][BED - 1]
    return [(0.15, f"Who's behind curtain {num}?", 2.9), (3.6, f"{first}, {K['age']}. {K['quote']}", 4.8), (8.8, 'Play your first move.', 3.0),
            (12.6, 'One call. Get it right.', 3.0), (16.2, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    n = len(K['quote'].split())
    cues = [(.05, 'pop'), (.5, 'tick'), (.75, 'tick'), (1.0, 'whoosh'), (1.75, 'ding'), (1.9, 'pop'), (2.3, 'pop'), (3.15, 'whoosh')]
    cues += [(3.4 + 1.2 + i * (D_Q - 2.4) / n, 'tick') for i in range(n)] + [(7.5, 'ding'), (8.35, 'whoosh')]
    cues += [(8.8 + i * .18, 'pop') for i in range(4)] + [(10.1 + i * .5, 'tick') for i in range(4)] + [(10.6, 'pop')]
    cues += [(12.15, 'whoosh'), (14.1, 'ding'), (14.5, 'beep'), (14.8, 'riser'), (16.0, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'upbeat', drop=3.4, lift=12.4, cta=16.0, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 1.4), (0, 3.0), (1, 0.6), (1, 2.6), (1, 4.8), (2, 1.0), (2, 2.8), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 5)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
