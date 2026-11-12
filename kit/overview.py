"""Model "Full Game" — the whole of Bedside Bay in one video.
Usage: python3 overview.py <out.mp4> [preview]"""
import sys, os, json, math, skia
from lib import *
import scenes
from case import bg, card, chip

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = json.load(open(os.path.join(HERE, 'cases.json')))


def s_hook(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['Run your own', 'emergency room.'], 372, 96)
    c.drawCircle(540, 1000, 330, P(TEAL, 60, blur=90))
    doctor(c, 540, 1330, 1.05, 'resident', t, la=10, ra=-150 + math.sin(t * 6) * 14, mood='happy')
    k = pop((t - .5) / .4)
    if t > .5:
        c.save(); c.translate(540, 1410); c.scale(k, k)
        w = tw('The emergency medicine career game', 34) + 60
        rr(c, -w / 2, -36, w, 72, 36, P('#ffffff')); text(c, 'The emergency medicine career game', 0, 12, 34, INK, 800, 'c'); c.restore()


def s_patients(c, t):
    bg(c, t); brand_bar(c)
    n = int(lerp(0, 163, eio(t / 1.6)))
    text(c, str(n), 540, 470, 210, '#ffffff', 900, 'c', shadow=.35)
    text(c, 'patients to treat', 540, 560, 60, '#bfe9e4', 800, 'c')
    for i in range(12):
        K = CASES[(i * 5) % len(CASES)]; col, row = i % 4, i // 4
        k = pop((t - .3 - i * .09) / .35)
        if t < .3 + i * .09: continue
        cx, cy = 165 + col * 250, 730 + row * 240
        c.save(); c.translate(cx, cy); c.scale(k, k); face(c, 0, 0, 96, K['skin'], K['hair'], K['style'], 'pain' if i % 3 else 'ok', t + i); c.restore()
    a = 255 * ease((t - 1.6) / .4)
    w = tw('From sprained ankles to resuscitation', 38) + 64
    rr(c, (W - w) / 2, 1392, w, 80, 40, P('#ffffff', a)); text(c, 'From sprained ankles to resuscitation', 540, 1446, 38, INK, 800, 'c', a=a)


def s_play(c, t):
    scenes.er(c, t + 2, 'resident'); brand_bar(c)
    words = ['Talk.', 'Examine.', 'Test.', 'Treat.']
    n = min(4, int(t / .55) + 1)
    headline(c, [' '.join(words[:min(n, 2)]), ' '.join(words[2:n]) if n > 2 else ''], 356, 92, INK, shadow=0)
    for i, (ic, lab) in enumerate((('talk', 'Talk'), ('examine', 'Examine'), ('tests', 'Tests'), ('treat', 'Treat'))):
        if t < i * .55: continue
        k = pop((t - i * .55) / .35); x = 60 + i * 222
        c.save(); c.translate(x + 100, 1370); c.scale(k, k)
        rr(c, -100, -98, 200, 200, 40, P('#000000', 60, blur=16)); rr(c, -100, -108, 200, 200, 40, P('#ffffff'))
        c.drawCircle(0, -34, 48, P(TEAL)); icon(c, ic, 0, -34, 58); text(c, lab, 0, 62, 34, INK, 900, 'c'); c.restore()


def s_ladder(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['Climb five ranks.'], 380, 92, a=255 * ease(t / .3))
    outs = ['intern', 'resident', 'surgeon', 'consultant', 'director']
    for i in range(5):
        x = 40 + i * 200; top = 1300 - i * 120
        if t < .2 + i * .42: continue
        k = ease((t - .2 - i * .42) / .35)
        rr(c, x, top + (1 - k) * 80, 200, 1500 - top, 16, grad(0, top, 0, 1500, ['#1cb5a3' if i < 4 else GOLD, '#0e7f76' if i < 4 else '#c98d1f'], 255 * k))
        text(c, RANKS[i], x + 100, top + 60, 27, '#ffffff' if i < 4 else INK, 900, 'c', a=255 * k)
        c.save(); c.translate(0, (1 - pop((t - .3 - i * .42) / .35)) * -200)
        doctor(c, x + 100, top + 4, .36, outs[i], t + i, mood='tired' if i == 0 else 'happy', ra=-150 if i == 4 else -12); c.restore()
    a = 255 * ease((t - 2.4) / .4)
    text(c, 'Bigger rank. Harder cases. Better pay.', 540, 480, 42, '#bfe9e4', 700, 'c', a=a)
    chip(c, 60, 560, 'DR JOHN SMITH', '#ffffff', INK, 28, dot=TEAL)


MODES = [('career', 'Career', 'Intern to ED Director'), ('shift', 'Quick shift', 'One shift, pick a specialty'),
         ('practice', 'Case practice', '163 patients, one at a time'), ('firstaid', 'First aid', 'Emergencies for everyone')]


def s_modes(c, t):
    bg(c, t); brand_bar(c)
    headline(c, ['Four ways to play.'], 380, 92, a=255 * ease(t / .3))
    for i, (ic, lab, sub) in enumerate(MODES):
        if t < .2 + i * .3: continue
        k = pop((t - .2 - i * .3) / .4); y = 480 + i * 236
        c.save(); c.translate(540, y + 105); c.scale(k, k); c.translate(-480, -105)
        card(c, 0, 0, 960, 210, 44)
        c.drawCircle(110, 105, 68, P(TEAL if i != 3 else '#e5484d')); icon(c, ic, 110, 105, 82)
        text(c, lab, 214, 98, 58, INK, 900); text(c, sub, 214, 152, 34, '#5b7083', 700); c.restore()


SC = [(s_hook, 2.8), (s_patients, 3.2), (s_play, 3.4), (s_ladder, 3.6), (s_modes, 3.2), (scenes.cta, 3.4)]

def soundtrack(wav):
    import sound
    cues = [(2.55, 'whoosh'), (5.75, 'whoosh'), (9.15, 'whoosh'), (12.75, 'whoosh'), (15.0, 'riser'), (16.2, 'impact')]
    cues += [(3.1 + i * .09, 'pop') for i in range(12)] + [(6.0 + i * .55, 'pop') for i in range(4)]
    cues += [(9.6 + i * .42, f'step:{i}') for i in range(5)] + [(13.2 + i * .3, 'pop') for i in range(4)]
    return sound.build(wav, sum(d for _, d in SC), 'bright', drop=0.0, lift=9.4, cta=16.2, cues=cues,
        voice=[(0.15, 'Run your own emergency room.', 2.5), (3.0, 'One hundred and sixty-three patients to treat.', 3.0), (6.2, 'Talk. Examine. Test. Treat.', 3.0),
               (9.6, 'Climb five ranks, from intern to E.D. Director.', 3.3), (13.2, 'Four ways to play.', 2.8), (16.5, 'Bedside Bay. Play free.', 2.9)])


if __name__ == '__main__':
    out = sys.argv[1]
    if len(sys.argv) > 2:
        fr = []
        for i, t in ((0, 0.0), (0, 2.0), (1, 2.6), (2, 2.8), (3, 3.2), (4, 2.8)):
            s = new_surface(); SC[i][0](s.getCanvas(), t); fr.append(s)
        contact_sheet(fr, out, 6)
    else:
        wav = out[:-4] + '.wav'; soundtrack(wav)
        render_video(SC, out, wav); os.remove(wav)
