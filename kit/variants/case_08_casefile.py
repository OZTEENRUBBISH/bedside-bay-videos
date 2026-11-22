"""Case variant 08 — "Case file: unsolved." The case arrives as a manila patient file dropped on the desk with a red
UNSOLVED stamp, opens on the patient's statement typed in their own words with the diagnosis line blacked out, then the
four moves as four file dividers, the one-call diagnosis box and the end card. Never reveals the diagnosis. Music: tense.
Video: python3 case_08_casefile.py <case-id> <out.mp4>      Preview: python3 case_08_casefile.py <case-id> preview <sheet.jpg>"""
from common import *
import case
from case import bg, card, chip, TRI, RED

MANILA, MANILA_D, PAPER = '#e9c98a', '#d1a95c', '#fbf7ee'


def stamp(c, cx, cy, label, k, rot=-14, size=84, col=RED):
    """Rubber stamp slamming in. k = 0..1."""
    if k <= 0: return
    s = lerp(2.6, 1, ease(k)); a = 255 * clamp(k * 3)
    w = tw(label, size, 900) + 70; h = size + 50
    c.save(); c.translate(cx, cy); c.rotate(rot); c.scale(s, s)
    rr(c, -w / 2, -h / 2, w, h, 16, P('#ffffff', a * .55))
    rr(c, -w / 2, -h / 2, w, h, 16, P(col, a, stroke=10)); rr(c, -w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 8, P(col, a * .5, stroke=4))
    text(c, label, 0, size * .36, size, col, 900, 'c', a=a); c.restore()


def paperclip(c, x, y):
    p = P('#8a9bab', stroke=7); rr(c, x, y, 34, 96, 17, p); rr(c, x + 8, y + 16, 18, 62, 9, p)


def tri_chip(c, xr, y, K, size=30):
    lab = f"TRIAGE {K['triage']}"; w = tw(lab, size, 900) + 48
    rr(c, xr - w, y, w, size + 28, (size + 28) / 2, P(TRI[K['triage']]))
    text(c, lab, xr - w / 2, y + size + 8, size, INK if K['triage'] == 3 else '#ffffff', 900, 'c')


def k_file(K):
    first, last = K['name'].split()[0], K['name'].split()[-1]; tab = f'{last.upper()}, {first[0]}.'
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Case file:', 'unsolved.', 372, size=116, sub_size=116)
        k = ease(t / .45); x, y, w, h = 110, 660, 860, 700
        c.save(); c.translate(540, 1000 - (1 - k) * 1500); c.rotate(-3 - (1 - k) * 12); c.translate(-540, -1000)
        rr(c, x + 10, y + 18, w, h, 26, P('#000000', 110, blur=28))
        rr(c, x + 40, y - 58, 420, 100, 22, P(MANILA_D)); text(c, tab, x + 70, y - 14, fit(tab, 36, 360), INK, 900)
        rr(c, x + 14, y - 12, w - 28, h, 20, P(PAPER))
        rr(c, x, y, w, h, 26, P(MANILA)); rr(c, x, y, w, h, 26, P(MANILA_D, stroke=5))
        rr(c, x + 50, y + 56, w - 100, 236, 18, P('#ffffff')); rr(c, x + 50, y + 56, w - 100, 236, 18, P('#d5dde5', stroke=3))
        text(c, 'PATIENT FILE  ·  EMERGENCY', x + 84, y + 108, 28, '#8a9bab', 900)
        nm = f"{K['name']}, {K['age']}"; text(c, nm, x + 84, y + 184, fit(nm, 68, w - 170), INK, 900)
        text(c, K['problem'], x + 84, y + 246, 40, '#5b7083', 700); tri_chip(c, x + w - 80, y + 206, K)
        c.save(); c.rotate(-5, x + 230, y + 490)
        rr(c, x + 90, y + 340, 280, 310, 10, P('#000000', 60, blur=10)); rr(c, x + 90, y + 334, 280, 310, 10, P('#ffffff'))
        face(c, x + 230, y + 480, 116, K['skin'], K['hair'], K['style'], 'pain', t); paperclip(c, x + 200, y + 296); c.restore()
        text(c, 'DIAGNOSIS', x + 440, y + 394, 30, '#7a5a10', 900); rr(c, x + 440, y + 412, 350, 56, 8, P(INK))
        for j in range(3): rr(c, x + 440, y + 510 + j * 46, 350 - j * 70, 22, 11, P(MANILA_D))
        stamp(c, x + 590, y + 540, 'UNSOLVED', (t - .9) / .3)
        c.restore()
        if t > 2.1: pill(c, 540, 1470, 'Can you crack it?', GOLD, INK, 52, pop((t - 2.1) / .4))
    return f


def k_statement(K, dur):
    q = K['quote']
    def f(c, t):
        bg(c, t); brand_bar(c); k0 = ease(t / .3)
        text(c, 'PATIENT STATEMENT', 540, 396, 66, GOLD, 900, 'c', a=255 * k0, shadow=.35)
        x, y, w, h = 70, 480, 940, 1000
        rr(c, x - 18, y + 18, w + 36, h, 26, P(MANILA_D)); rr(c, x, y + 12, w, h, 14, P('#000000', 70, blur=18)); rr(c, x, y, w, h, 14, P(PAPER))
        face(c, x + 160, y + 160, 104 * pop(t / .4), K['skin'], K['hair'], K['style'], 'pain', t); paperclip(c, x + 60, y - 30)
        nm = f"{K['name']}, {K['age']}"; text(c, nm, x + 296, y + 144, fit(nm, 60, 590), INK, 900)
        xx = x + 296 + chip(c, x + 296, y + 174, K['problem'], '#e2f4f1', TEAL_D, 30) + 14
        chip(c, xx, y + 174, f"Triage {K['triage']}", TRI[K['triage']], INK if K['triage'] == 3 else '#ffffff', 30)
        c.drawLine(x + 50, y + 300, x + w - 50, y + 300, P('#d9d2c2', stroke=3))
        text(c, 'IN THEIR OWN WORDS', x + 50, y + 354, 28, '#8a9bab', 900)
        size = 62; lines = wrap(q, size, 700, w - 110)
        while len(lines) > 4: size -= 4; lines = wrap(q, size, 700, w - 110)
        lh = size * 1.42; n = int(len(q) * clamp((t - .7) / (dur - 2.9))); shown = 0
        for i, ln in enumerate(lines):
            by = y + 446 + i * lh
            c.drawLine(x + 50, by + 20, x + w - 50, by + 20, P('#e4dccb', stroke=3))
            part = ln[:max(0, n - shown)]; shown += len(ln) + 1
            if part:
                wv = text(c, part, x + 54, by, size, INK, 700)
                if len(part) < len(ln) and (t * 3) % 1 < .6: rr(c, x + 60 + wv, by - size * .8, 6, size, 3, P(TEAL))
        dy_ = y + h - 140
        text(c, 'DIAGNOSIS:', x + 50, dy_ + 46, 44, '#7a5a10', 900); rr(c, x + 330, dy_, w - 380, 64, 8, P(INK))
        stamp(c, x + w - 250, dy_ - 30, 'UNSOLVED', (t - (dur - 1.5)) / .3, rot=-8, size=60)
    return f


TABS = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Make the call')]


def k_tabs(K):
    first = K['name'].split()[0]
    def f(c, t):
        bg(c, t); brand_bar(c)
        title2(c, 'Four moves', 'to crack it.', 372, size=108, sub_size=108, a=255 * ease(t / .3))
        active = int(max(0, t - 1.5) / .5) % 4 if t > 1.5 else -1
        for i, (ic, lab, sub) in enumerate(TABS):
            k = ease((t - .2 - i * .22) / .4)
            if k <= 0: continue
            y = 600 + i * 200; on = i == active; tx = 90 + i * 222
            c.save(); c.translate(0, (1 - k) * 1000)
            rr(c, tx, y - 46, 200, 80, 18, P(GOLD if on else MANILA_D)); text(c, f'STEP {i + 1}', tx + 100, y - 10, 28, INK, 900, 'c')
            rr(c, 60, y + 10, 960, 168, 22, P('#000000', 90, blur=20)); rr(c, 60, y, 960, 168, 22, P(MANILA)); rr(c, 76, y + 14, 928, 140, 14, P(PAPER))
            if on: rr(c, 60, y, 960, 168, 22, P(GOLD, stroke=10))
            c.drawCircle(170, y + 84, 54, P(TEAL if on else TEAL_D)); icon(c, ic, 170, y + 84, 66)
            text(c, lab, 254, y + 84, 58, INK, 900); text(c, sub, 254, y + 128, 32, '#5b7083', 700)
            text(c, f'0{i + 1}', 968, y + 106, 60, MANILA_D, 900, 'r'); c.restore()
        if t > 2.0:
            lab = f'{first}’s file is still open'; w = tw(lab, 40) + 74
            c.save(); c.translate(540, 1450); k = pop((t - 2.0) / .4); c.scale(k, k)
            chip(c, -w / 2, -33, lab, '#ffffff', INK, 40, dot=TRI[K['triage']]); c.restore()
    return f


D0, D_Q, D2 = 3.2, 5.6, 3.5


def build(case_id):
    K, SC = case.build(case_id)
    return K, [(k_file(K), D0), (k_statement(K, D_Q), D_Q), (k_tabs(K), D2), (SC[2][0], 3.5), (SC[3][0], 3.6)]


def script(K):
    first = K['name'].split()[0]; a, b, c_ = D0, D0 + D_Q, D0 + D_Q + D2
    return [(0.15, 'Case file. Unsolved.', D0 - .35), (a + .2, f"{first}, {K['age']}. {K['quote']}", D_Q - .4),
            (b + .2, 'Four moves to crack it.', D2 - .5), (c_ + .2, 'One call. Get it right.', 3.0), (c_ + 3.7, f'{first} is waiting. Bedside Bay. Play free.', 3.1)]


def soundtrack(K, SC, wav):
    import sound
    a, b, c_ = D0, D0 + D_Q, D0 + D_Q + D2; e = c_ + 3.5; n = 22
    cues = [(.05, 'whoosh'), (.42, 'pop'), (.9, 'impact'), (2.1, 'ding'), (a - .25, 'whoosh')]
    cues += [(a + .7 + i * (D_Q - 2.9) / n, 'tick') for i in range(n)] + [(b - 1.5, 'impact'), (b - .25, 'whoosh')]
    cues += [(b + .2 + i * .22, 'pop') for i in range(4)] + [(b + 1.5 + i * .5, 'tick') for i in range(4)] + [(b + 2.0, 'pop')]
    cues += [(c_ - .25, 'whoosh'), (c_ + 1.7, 'ding'), (c_ + 2.1, 'beep'), (e - 1.2, 'riser'), (e, 'impact')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=a, lift=c_, cta=e, cues=cues, voice=script(K))


if __name__ == '__main__':
    K, SC = build(sys.argv[1])
    def comp(i):
        def f(c, t):
            SC[i][0](c, t)
            if i > 0: flash(c, t)
        return f
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 0.7), (0, 1.3), (0, 3.0), (1, 0.6), (1, 2.4), (1, 5.4), (2, 1.0), (2, 3.2), (3, 3.2), (4, 3.0)]
        contact_sheet([frame(comp(i), t) for i, t in pts], sys.argv[3], 6)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in soundtrack(K, SC, wav): print(r)
        render_video([(comp(i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
