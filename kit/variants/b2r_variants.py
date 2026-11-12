"""Broke to Rich variants (new hooks and scene orders for Dr John Smith's climb).
  rewind — "How did he afford this?" opens on the mansion, rewinds to Day 1, then climbs back.   music: bright
  split  — "Same doctor. Two futures." opens on a split screen, broke intern vs ED Director.     music: upbeat
Video:   python3 b2r_variants.py <rewind|split> <out.mp4>      Preview: python3 b2r_variants.py <name> preview <sheet.jpg>"""
from common import *
import video  # toasts + hud_state of the original model

CHIPS = (('Mansion', 300, 578), ('Supercar', 330, 1044), ('Gold watch', 780, 590))


def chips(c, t=None):
    for n, (l, x, y) in enumerate(CHIPS):
        a0 = .5 + n * .8
        if t is None: pill(c, x, y, l)
        elif t > a0: pill(c, x, y, l, k=pop((t - a0) / .35))


# ---------------------------------------------------------------- rewind
def rw_rich(c, t):
    scenes.rich(c, t + 1.5, car_in=False); chips(c)
    headline(c, ['How did he', 'afford this?'], 356, 92)
    hud(c, 4, 2480000, 5); brand_bar(c)


def _rew_icon(c, x, y, s, col):
    for dx in (0, s * 1.1):
        p = skia.Path(); p.moveTo(x + dx + s, y - s * .7); p.lineTo(x + dx, y); p.lineTo(x + dx + s, y + s * .7); p.close(); c.drawPath(p, P(col))


def rw_poor(c, t):
    scenes.poor(c, t)
    k = clamp(t / .9)
    if k < 1:  # tape-rewind streaks while the bank and rank spin back
        for i in range(14):
            y = (i * 173 + t * 2600) % H
            c.drawRect(skia.Rect.MakeXYWH(0, y, W, 10 + (i % 3) * 8), P('#ffffff', 70 * (1 - k)))
    headline(c, ['Rewind.', 'Day 1. $2,000.'], 356, 92)
    w = 330; rr(c, 60, 590, w, 80, 40, P('#e5484d')); _rew_icon(c, 92, 630, 24, '#ffffff'); text(c, 'REWIND', 162, 646, 42, '#ffffff', 900)
    e = eio(k); rank = [4, 3, 2, 1, 0][min(4, int(e * 5))]
    hud(c, rank, lerp(2480000, 2000, e), lerp(5, 1, e), bump=(1 - k) * abs(math.sin(t * 20)) * .5); brand_bar(c)


def _std(fn, hl, col, idx, tfn=None):
    """One of the original climb scenes with a new headline; idx picks the original HUD/toast track."""
    def f(c, t):
        fn(c, t)
        k = ease(t / .35)
        headline(c, hl, 356, 92, col, a=255 * k, dy=(1 - k) * 36, shadow=0 if col == INK else .35)
        if tfn: tfn(c, t)
        else: video.toasts(c, idx, t)
        r, bank, prog, bump = video.hud_state(idx, t, 1)
        hud(c, r, bank, prog, bump=bump * abs(math.sin(t * 9)) * .5); brand_bar(c)
    return f


REWIND = [(rw_rich, 3.0), (rw_poor, 3.0), (_std(scenes.er, ['Case by case.'], INK, 1), 4.2),
          (_std(scenes.theatre, ['Rank by rank.'], '#ffffff', 2), 3.2),
          (_std(scenes.rich, ['Your turn,', 'doctor.'], '#ffffff', 3, chips), 2.8),
          (cta2('Start with $2,000.', 'Finish as ED Director.'), 3.4)]


def rewind_sound(wav):
    import sound
    cues = [(.1, 'cash'), (2.75, 'whoosh'), (3.0, 'riser'), (3.95, 'impact'), (5.75, 'whoosh'), (6.45, 'ding'), (7.6, 'ding'), (8.9, 'cash'),
            (9.95, 'whoosh'), (10.7, 'ding'), (11.95, 'cash'), (13.15, 'whoosh'), (13.9, 'pop'), (14.7, 'pop'), (15.5, 'pop'), (15.0, 'riser'), (16.2, 'impact')]
    cues += [(3.05 + i * .07, 'tick') for i in range(12)]
    return sound.build(wav, sum(d for _, d in REWIND), 'bright', drop=6.0, lift=10.2, cta=16.2, cues=cues,
        voice=[(0.15, 'How did Doctor John Smith afford this?', 2.7), (3.3, 'Go back to day one. Two thousand dollars.', 2.6),
               (6.3, 'Case by case.', 3.0), (10.4, 'Rank by rank.', 2.7), (13.4, 'Your turn, doctor.', 2.6), (16.5, 'Bedside Bay. Play free.', 2.9)])


# ---------------------------------------------------------------- split screen
def sp_split(c, t):
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, 540, H)); c.translate(-290, 0); scenes.poor(c, t); c.restore()
    c.save(); c.clipRect(skia.Rect.MakeXYWH(540, 0, 540, H)); c.translate(-95, 0); scenes.rich(c, t + 1.5, car_in=False)
    # the scene is only 1080 wide: extend sky, hill, lawn and driveway to cover the shifted strip
    c.drawRect(skia.Rect.MakeXYWH(1080, 0, 100, 1130), grad(0, 0, 0, 1130, ['#272b73', '#8a4a94', '#f2707a', '#ffc37d']))
    c.drawRect(skia.Rect.MakeXYWH(1080, 1060, 100, 80), P('#5b3f86', 200))
    c.drawRect(skia.Rect.MakeXYWH(1080, 1120, 100, H - 1120), grad(0, 1120, 0, 1500, ['#2e9f6b', '#1c7a50']))
    d = skia.Path(); d.moveTo(1080, 1390.6); d.lineTo(1180, 1445.3); d.lineTo(1180, 1500); d.lineTo(1080, 1500); d.close(); c.drawPath(d, P('#c9cdd3'))
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(534, 570, 12, H - 570), P('#ffffff'))
    headline(c, ['Same doctor.', 'Two futures.'], 356, 92)
    k1, k2 = pop((t - .15) / .35), pop((t - .45) / .35)
    pill(c, 270, 610, 'DAY 1', '#ffffff', INK, 40, k1 if t > .15 else 0)
    pill(c, 810, 610, 'ED DIRECTOR', GOLD, INK, 40, k2 if t > .45 else 0)
    c.drawCircle(540, 900, 64, P('#000000', 80, blur=14)); c.drawCircle(540, 896, 60, P('#ffffff')); text(c, 'VS', 540, 914, 50, INK, 900, 'c')
    for x, lab, val, col in ((60, 'BANK', '$2,000', '#d64545'), (500, 'BANK', '$2,480,000', TEAL_D)):
        rr(c, x, 1300, 420, 170, 40, P('#000000', 70, blur=22)); rr(c, x, 1290, 420, 170, 40, P('#ffffff'))
        text(c, lab, x + 36, 1346, 26, '#5b7083', 800); text(c, val, x + 36, 1426, 62, col, 900)
    brand_bar(c)


def sp_poor(c, t):
    scenes.poor(c, t)
    k = ease(t / .35)
    headline(c, ['It starts with', '$2,000.'], 356, 92, a=255 * k, dy=(1 - k) * 36)
    hud(c, 0, 2000, 1.0); brand_bar(c)


SPLIT = [(sp_split, 3.2), (sp_poor, 2.6), (_std(scenes.er, ['Solve cases.', 'Get paid.'], INK, 1), 4.2),
         (_std(scenes.theatre, ['Get promoted.', 'Get paid more.'], '#ffffff', 2), 3.2),
         (_std(scenes.rich, ['Which future', 'do you want?'], '#ffffff', 3, chips), 2.8),
         (cta2('Broke intern or ED Director?', 'Your career. Your call.'), 3.2)]


def split_sound(wav):
    import sound
    cues = [(.15, 'pop'), (.45, 'pop'), (.7, 'riser'), (2.2, 'cash'), (2.95, 'whoosh'), (3.3, 'beep'), (5.55, 'whoosh'), (6.25, 'ding'), (7.4, 'ding'),
            (8.7, 'cash'), (9.75, 'whoosh'), (10.5, 'ding'), (11.75, 'cash'), (12.95, 'whoosh'), (13.7, 'pop'), (14.5, 'pop'), (15.3, 'pop'),
            (14.8, 'riser'), (16.0, 'impact')]
    return sound.build(wav, sum(d for _, d in SPLIT), 'upbeat', drop=5.8, lift=12.6, cta=16.0, cues=cues,
        voice=[(0.15, 'Same doctor. Two futures.', 2.8), (3.4, 'It starts with two thousand dollars.', 2.2),
               (6.1, 'Solve cases. Get paid.', 3.2), (10.2, 'Get promoted. Get paid more.', 2.8),
               (13.2, 'Which future do you want?', 2.5), (16.3, 'Bedside Bay. Play free.', 2.7)])


V = {'rewind': (REWIND, rewind_sound), 'split': (SPLIT, split_sound)}


def compose(SC, i):
    fn = SC[i][0]
    def f(c, t):
        fn(c, t)
        if i > 0: flash(c, t)
    return f


if __name__ == '__main__':
    SC, snd = V[sys.argv[1]]
    if sys.argv[2] == 'preview':
        pts = [(0, 0.0), (0, 2.4), (1, 0.4), (1, 2.4), (2, 1.1), (2, 3.4), (3, 2.3), (4, 2.6), (5, 2.5)]
        contact_sheet([frame(compose(SC, i), t) for i, t in pts], sys.argv[3], 5)
    else:
        out = sys.argv[2]; wav = out[:-4] + '.wav'
        for r in snd(wav): print(r)
        render_video([(compose(SC, i), d) for i, (_, d) in enumerate(SC)], out, wav); os.remove(wav)
