"""Model "Case" — one real Bedside Bay patient as a cliffhanger (never reveals the diagnosis).
Usage: python3 case.py <case-id> <out.mp4> [preview]   (case ids are in cases.json)"""
import sys, os, json, math, skia
from lib import *
import scenes

HERE = os.path.dirname(os.path.abspath(__file__))
RED = '#e5484d'
TRI = {1: '#e5484d', 2: '#f08c2e', 3: '#e0b322', 4: '#3aa76d', 5: '#3a8fd6'}


def bg(c, t):
    c.drawRect(skia.Rect.MakeWH(W, H), grad(0, 0, W * .4, H, ['#0a1a2c', '#0d3540']))
    c.drawCircle(900, 380, 520, P(TEAL, 26, blur=140)); c.drawCircle(120, 1500, 460, P('#3a8fd6', 22, blur=140))
    for i in range(1, 9): c.drawLine(i * 120, 0, i * 120, H, P('#ffffff', 7, stroke=2, cap=False))
    for i in range(1, 16): c.drawLine(0, i * 120, W, i * 120, P('#ffffff', 7, stroke=2, cap=False))
    scenes._ecg(c, 0, W, 1610, t, TEAL, a=70, amp=56, w=5)


def card(c, x, y, w, h, r=44, a=255, col='#ffffff'):
    rr(c, x, y + 12, w, h, r, P('#000000', 90 * a / 255, blur=26)); rr(c, x, y, w, h, r, P(col, a))


def chip(c, x, y, label, bgc, fg, size=30, dot=None):
    w = tw(label, size) + 44 + (30 if dot else 0)
    rr(c, x, y, w, size + 26, (size + 26) / 2, P(bgc))
    if dot: c.drawCircle(x + 30, y + (size + 26) / 2, 9, P(dot))
    text(c, label, x + 22 + (30 if dot else 0), y + size + 6, size, fg, 800)
    return w


def s_intro(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        pulse = .5 + .5 * math.sin(t * 7)
        lab = f"INCOMING  ·  TRIAGE {K['triage']}"; w = tw(lab, 34) + 96
        rr(c, (W - w) / 2, 300, w, 70, 35, P(TRI[K['triage']])); c.drawCircle((W - w) / 2 + 40, 335, 10 + 4 * pulse, P('#ffffff', 255 - 90 * pulse))
        text(c, lab, (W - w) / 2 + 66, 347, 34, '#ffffff', 900)
        headline(c, ['Your next patient'], 478, 84)
        k = ease(t / .45); dy = (1 - k) * 160
        c.save(); c.translate(0, dy)
        card(c, 60, 560, 960, 640)
        face(c, 210, 720, 112, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, f"{K['name']}, {K['age']}", 350, 706, 56, INK, 900)
        x = 350 + chip(c, 350, 736, K['problem'], '#e2f4f1', TEAL_D, 30) + 14
        chip(c, x, 736, K['level'], '#eef2f6', '#5b7083', 30)
        c.drawLine(110, 868, 970, 868, P('#e4eaf0', stroke=3))
        text(c, '“', 104, 1004, 150, TEAL, 900)
        q = K['quote']; n = int(len(q) * clamp((t - .55) / 1.9)); lines = wrap(q, 50, 700, 780)
        shown = 0
        for i, ln in enumerate(lines):
            part = ln[:max(0, n - shown)]; shown += len(ln) + 1
            if part: text(c, part, 190, 960 + i * 66, 50, INK, 700)
        c.restore()
    return f


TILES = [('talk', 'Talk', 'Take the history'), ('examine', 'Examine', 'Find the signs'), ('tests', 'Tests', 'Order what matters'), ('treat', 'Treat', 'Act before it gets worse')]


def s_move(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['Your move, doctor.'], 372, 84, a=255 * ease(t / .3))
        card(c, 60, 450, 960, 150, 40)
        face(c, 150, 525, 56, K['skin'], K['hair'], K['style'], 'pain', t)
        text(c, K['name'], 230, 516, 40, INK, 900); text(c, K['problem'], 230, 562, 30, '#5b7083', 700)
        secs = int(t * 9); text(c, f"{secs // 60:02d}:{secs % 60:02d}", 980, 548, 60, RED, 900, 'r'); text(c, 'ON THE CLOCK', 980, 492, 22, '#5b7083', 800, 'r')
        active = int(max(0, t - 1.7) / .5) % 4
        for i, (ic, lab, sub) in enumerate(TILES):
            k = pop((t - .25 - i * .32) / .4)
            if t < .25 + i * .32: continue
            x = 60 + (i % 2) * 490; y = 640 + (i // 2) * 300
            c.save(); c.translate(x + 235, y + 135); c.scale(k, k); c.translate(-235, -135)
            on = t > 1.7 and i == active
            card(c, 0, 0, 470, 270, 40, col='#ffffff')
            if on: rr(c, 0, 0, 470, 270, 40, P(TEAL, stroke=10))
            c.drawCircle(90, 96, 58, P(TEAL if on else TEAL_D)); icon(c, ic, 90, 96, 70)
            text(c, lab, 172, 112, 54, INK, 900); text(c, sub, 40, 214, 31, '#5b7083', 700)
            c.restore()
        doctor(c, 900, 1560, .5, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 12, mood='happy')
        chip(c, 60, 1290, 'DR JOHN SMITH  ·  ON SHIFT', '#ffffff', INK, 28, dot=TEAL)
    return f


def s_call(K):
    def f(c, t):
        bg(c, t); brand_bar(c)
        headline(c, ['One call.', 'Get it right.'], 352, 88, a=255 * ease(t / .3))
        k = ease((t - .15) / .4)
        c.save(); c.translate(0, (1 - k) * 120)
        card(c, 60, 560, 960, 520)
        first = K['name'].split()[0]
        text(c, f"What's wrong with {first}?", 110, 646, 48, INK, 900)
        rr(c, 110, 684, 860, 104, 26, P('#f3f6f9')); rr(c, 110, 684, 860, 104, 26, P('#cfd9e2', stroke=4))
        typed = 'Diagnosis'[:int(clamp((t - .6) / .7) * 9)]
        wv = text(c, typed, 144, 752, 44, '#8a9bab', 700)
        if (t * 2.4) % 1 < .55: rr(c, 150 + wv, 708, 5, 56, 2, P(TEAL))
        for i in range(3):
            a = 255 * ease((t - 1.0 - i * .22) / .3); y = 816 + i * 82
            rr(c, 110, y, 860, 66, 20, P('#eef2f6', a)); rr(c, 134, y + 21, 300 + i * 90, 24, 12, P('#c3cfda', a))
            c.drawCircle(940, y + 33, 14, P('#c3cfda', a))
        c.restore()
        if t > 1.7:
            k2 = pop((t - 1.7) / .4); c.save(); c.translate(60, 1130); c.scale(k2, k2)
            chip(c, 0, 0, 'Right call: reputation up', '#1f9d63', '#ffffff', 34); c.restore()
        if t > 2.1:
            k2 = pop((t - 2.1) / .4); c.save(); c.translate(60, 1222); c.scale(k2, k2)
            chip(c, 0, 0, "Wrong call: it's on you", RED, '#ffffff', 34); c.restore()
        doctor(c, 870, 1560, .56, 'resident', t, la=10, ra=-12, mood='tired')
        chip(c, 60, 1330, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)
    return f


def s_cta(K):
    def f(c, t):
        bg(c, t)
        first = K['name'].split()[0]
        k = pop(t / .45); ring = (t * .8) % 1
        c.drawCircle(540, 520, 170 + ring * 110, P(TEAL, 150 * (1 - ring), stroke=8))
        c.save(); c.translate(540, 520); c.scale(k, k); face(c, 0, 0, 170, K['skin'], K['hair'], K['style'], 'pain', t); c.restore()
        a = 255 * ease((t - .2) / .4)
        text(c, f'{first} is waiting.', 540, 830, 96, '#ffffff', 900, 'c', a=a, shadow=.35)
        text(c, '163 patients. Beginner to Hard.', 540, 910, 46, '#bfe9e4', 700, 'c', a=a)
        if t > .6:
            b = pop((t - .6) / .5) * (1 + .03 * math.sin(t * 6))
            c.save(); c.translate(540, 1060); c.scale(b, b)
            rr(c, -330, -56, 660, 132, 66, P('#000000', 80, blur=20)); rr(c, -330, -66, 660, 132, 66, P(TEAL))
            text(c, 'Take the case free', 0, 22, 60, '#ffffff', 900, 'c'); c.restore()
        a2 = 255 * ease((t - .9) / .4)
        logo(c, 262, 1196, 76); text(c, 'bedsidebay.com', 360, 1252, 56, '#ffffff', 800, a=a2)
    return f


def build(case_id):
    K = next(k for k in json.load(open(os.path.join(HERE, 'cases.json'))) if k['id'] == case_id)
    return K, [(s_intro(K), 3.6), (s_move(K), 3.9), (s_call(K), 3.8), (s_cta(K), 3.5)]


def soundtrack(K, SC, wav):
    import sound
    first = K['name'].split()[0]; age = K['age'] if K['age'].isdigit() else ''
    import re
    q1 = re.split(r'(?<=[.!?])\s+', K['quote'])[0]  # first sentence only, so the line fits the scene
    intro = f"{first}{', ' + age if age else ''}. {q1}"
    cues = [(.05, 'beep')] + [(.6 + i * .09, 'tick') for i in range(20)] + [(3.35, 'whoosh'), (7.25, 'whoosh'), (11.05, 'riser'), (11.3, 'impact')]
    cues += [(3.85 + i * .32, 'pop') for i in range(4)] + [(9.2, 'ding'), (9.6, 'beep')]
    return sound.build(wav, sum(d for _, d in SC), 'tense', drop=3.6, lift=7.5, cta=11.3, cues=cues,
        voice=[(0.2, intro, 3.3), (3.8, 'Your move, doctor.', 3.0), (7.7, 'One call. Get it right.', 3.2), (11.6, f'{first} is waiting. Play free.', 3.0)])


if __name__ == '__main__':
    K, SC = build(sys.argv[1]); out = sys.argv[2]
    if len(sys.argv) > 3:
        fr = []
        for i, t in ((0, 0.0), (0, 3.0), (1, 2.6), (2, 3.2), (3, 2.8)):
            s = new_surface(); SC[i][0](s.getCanvas(), t); fr.append(s)
        contact_sheet(fr, out, 5)
    else:
        wav = out[:-4] + '.wav'; soundtrack(K, SC, wav)
        render_video(SC, out, wav); os.remove(wav)
