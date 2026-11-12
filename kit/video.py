"""Bedside Bay ad 001 — 'Broke intern to ED Director'. Usage: video.py preview | render"""
import sys, os, subprocess, math, skia
from lib import *
import scenes

FPS = 30
# (fn, seconds, headline lines, headline colour)
SC = [
    (scenes.poor, 3.0, ['Day 1.', 'Broke intern.']),
    (scenes.er, 4.2, ['Solve real', 'ER cases.'], INK),
    (scenes.theatre, 3.2, ['Take on the', 'big surgeries.']),
    (scenes.rich, 4.2, ['Live like an', 'ED Director.']),
    (scenes.cta, 3.4, None),
]


def hud_state(i, t, d):
    k = t / d
    if i == 0: return 0, 2000, 1.0, 0
    if i == 1:
        bank = lerp(2000, 38500, eio((t - .5) / 3.2)); r = 0 if t < 1.55 else (1 if t < 3.0 else 2)
        return r, bank, lerp(1, 3, eio((t - .4) / 3.2)), 1
    if i == 2:
        bank = lerp(38500, 264000, eio((t - .3) / 2.5)); r = 2 if t < 1.7 else 3
        return r, bank, lerp(3, 4, eio((t - .3) / 2.4)), 1
    if i == 3:
        return 4, lerp(264000, 2480000, eio((t - .2) / 3.0)), lerp(4, 5, eio(t / 1.2)), 1
    return 4, 2480000, 5, 0


def toasts(c, i, t):
    if i == 1:
        for (a, b, l, s) in ((.45, 1.45, 'Case solved', '+$4,200'), (1.6, 2.7, 'Promoted: Resident', '+$9,500'),
                             (2.9, 4.1, 'Promoted: Registrar', '+$22,800')):
            toast(c, l, s, 450, 556, (t - a) / (b - a))
    if i == 2:
        toast(c, 'Surgery complete', '+$85,000', 540, 540, (t - .5) / 1.1)
        toast(c, 'Promoted: Consultant', '+$140,000', 540, 540, (t - 1.75) / 1.3, GOLD)
    if i == 3:
        for (a, l, x, y) in ((.5, 'Mansion', 300, 578), (1.3, 'Supercar', 330, 1044), (2.1, 'Gold watch', 780, 590)):
            k = pop((t - a) / .35)
            if t > a:
                w = tw(l, 36) + 60
                c.save(); c.translate(x, y); c.scale(k, k)
                rr(c, -w / 2, -34, w, 68, 34, P('#000000', 70, blur=12)); rr(c, -w / 2, -38, w, 68, 34, P(GOLD))
                text(c, l, 0, 8, 36, INK, 900, 'c'); c.restore()


def compose(c, i, t):
    fn, d, hl = SC[i][:3]
    col = SC[i][3] if len(SC[i]) > 3 else '#ffffff'
    fn(c, t)
    k = 1 if i == 0 else ease(t / .35)
    if hl:
        headline(c, hl, 356, 92, col, a=255 * k, dy=(1 - k) * 36, shadow=0 if col == INK else .35)
        toasts(c, i, t)
        r, bank, prog, bump = hud_state(i, t, d)
        hud(c, r, bank, prog, bump=bump * abs(math.sin(t * 9)) * .5)
        brand_bar(c)
    if i > 0 and t < .28:
        c.drawRect(skia.Rect.MakeWH(W, H), P('#ffffff', 200 * (1 - t / .28)))


def frame(i, t):
    s = new_surface(); compose(s.getCanvas(), i, t); return s


def preview():
    os.makedirs('prev', exist_ok=True)
    for n, (i, t) in enumerate([(0, 0.0), (0, 1.8), (1, 1.1), (1, 3.4), (2, 2.3), (3, 2.6), (4, 2.5)]):
        frame(i, t).makeImageSnapshot().save(f'prev/p{n}.png', skia.kPNG)
    # contact sheet
    from PIL import Image
    ims = [Image.open(f'prev/p{n}.png').resize((432, 768)) for n in range(7)]
    sh = Image.new('RGB', (432 * 4, 768 * 2), '#222')
    for n, im in enumerate(ims): sh.paste(im, ((n % 4) * 432, (n // 4) * 768))
    sh.save('prev/sheet.jpg', quality=85)


def render():
    os.makedirs('out', exist_ok=True)
    parts = []
    for i, sc in enumerate(SC):
        d = sc[1]
        tmp, fin = f'out/tmp_s{i}.mp4', f'out/s{i}.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast',
                              '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        s = new_surface(); c = s.getCanvas()
        for f in range(int(round(d * FPS))):
            compose(c, i, f / FPS); p.stdin.write(to_rgba(s))
        p.stdin.close()
        assert p.wait() == 0
        os.rename(tmp, fin); parts.append(fin); print('scene', i, 'done', flush=True)
    open('out/list.txt', 'w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in parts))
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'out/list.txt', '-c', 'copy', 'out/silent.mp4'])


if __name__ == '__main__':
    preview() if sys.argv[1] == 'preview' else render()
