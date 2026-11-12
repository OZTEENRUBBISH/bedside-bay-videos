"""Render a Startup Legacy ad from a JSON spec.

  python3 ad.py preview <spec.json> <sheet.jpg>   contact sheet of key frames (look at it before rendering)
  python3 ad.py video   <spec.json> <out.mp4>     full video with music, sound effects and AI voiceover
  python3 ad.py photos  <spec.json> <out_dir>     photo set: one 1080x1920 JPG per scene (slide-1.jpg ...)

Spec: {"style": "upbeat|tense|bright", "scenes": [
   {"scene": "broke", "dur": 3.0, "head": ["Line 1", "Line 2"],
    "hud": [stage_from, worth_from, stage_to, worth_to],      # stages 0..4 = Broke..Legacy; omit for no card
    "toasts": [[start, end, "Label", "+$4,200"]], "tags": [[time, "Mansion", x, y]],
    "voice": "One short spoken line."},
   ... last scene {"scene": "cta", "dur": 3.4, "voice": "Startup Legacy. Free on the App Store."}]}
Scene names: see sl.SCENES."""
import sys, os, json, math, skia
from sl import *  # noqa
import sl
from sl2 import SCENES2, LIGHT2
SCENES = dict(SCENES, **SCENES2)

LIGHT = {'office', 'wedding'} | LIGHT2
FPS = 30


def hud_at(sc, t):
    h = sc.get('hud')
    if not h: return None
    s0, w0, s1, w1 = h; d = sc['dur']; k = eio((t - .3) / max(d - .9, .5))
    st = s0 if k < .5 else s1
    return st, lerp(w0, w1, k), lerp(s0 + 1, s1 + 1, k), (1 if w1 != w0 else 0)


def compose(c, sc, t, first=False):
    name = sc['scene']; fn = SCENES[name]
    kw = dict(sc.get('args', {}))
    if name == 'mansion' and 'car_in' in sc: kw['car_in'] = sc['car_in']
    fn(c, t, **kw)
    if name == 'cta':
        brand_top = False
    else:
        col = BG if name in LIGHT else '#ffffff'
        k = 1 if first else ease(t / .35)
        if sc.get('head'): headline(c, sc['head'], 356, 88, col, a=255 * k, dy=(1 - k) * 36, shadow=0 if col == BG else .35)
        for a, b, l, s in sc.get('toasts', []): toast(c, l, s, 540, 560, (t - a) / (b - a))
        for a, l, x, y in sc.get('tags', []): tag(c, l, x, y, clamp((t - a) / .35))
        h = hud_at(sc, t)
        if h: st, wv, pr, bump = h; hud(c, st, wv, pr, bump=bump * abs(math.sin(t * 9)) * .5)
        brand_bar(c)
    if not first and t < .28: c.drawRect(skia.Rect.MakeWH(W, H), P('#ffffff', 200 * (1 - t / .28)))


def soundtrack(spec, wav):
    import sound
    S = spec['scenes']; D = sum(s['dur'] for s in S); starts = []; acc = 0
    for s in S: starts.append(acc); acc += s['dur']
    cues, voice = [], []
    for i, (s, st) in enumerate(zip(S, starts)):
        if i: cues.append((max(st - .25, 0), 'whoosh'))
        for a, b, l, sub in s.get('toasts', []): cues.append((st + a + .05, 'cash' if '$' in sub else 'ding'))
        for a, *_ in s.get('tags', []): cues.append((st + a, 'pop'))
        if s.get('voice'): voice.append((st + (.15 if i == 0 else .3), s['voice'], s['dur'] - (.35 if i == 0 else .5)))
    cta = starts[-1]; cues += [(cta - 1.2, 'riser'), (cta, 'impact')]
    drop = starts[1] if len(starts) > 1 else 0
    rep = sound.build(wav, D, spec.get('style', 'upbeat'), drop=drop, lift=starts[-2] if len(starts) > 2 else None, cta=cta, cues=cues, voice=voice)
    ok = True
    for (vt, vd, txt), (s, st) in zip(rep, [(s, st) for s, st in zip(S, starts) if s.get('voice')]):
        end = vt + vd; lim = st + s['dur']
        flag = 'OK ' if end <= lim + .05 else 'LONG'
        if flag != 'OK ': ok = False
        print(f'  voice {flag} {vt:5.2f}-{end:5.2f} (scene ends {lim:5.2f}): {txt}')
    print('all lines fit' if ok else 'SOME LINES OVERRUN')
    return ok


def main():
    mode, spec_path, out = sys.argv[1:4]
    spec = json.load(open(spec_path)); S = spec['scenes']
    if mode == 'preview':
        frames = []
        for i, s in enumerate(S):
            for t in ((.05, s['dur'] * .7) if i == 0 else (s['dur'] * .7,)):
                surf = new_surface(); compose(surf.getCanvas(), s, t, first=(i == 0)); frames.append(surf)
        contact_sheet(frames, out, cols=min(len(frames), 7))
    elif mode == 'photos':
        os.makedirs(out, exist_ok=True)
        for i, s in enumerate(S):
            surf = new_surface(); compose(surf.getCanvas(), s, s.get('photo_t', s['dur'] * .8), first=True)
            if i == 0 and s.get('swipe', True):
                cc = surf.getCanvas(); w = 300; rr(cc, 720, 1516, w, 76, 38, P(SGOLD)); text(cc, 'Swipe  >', 720 + w / 2, 1568, 40, BG, 900, 'c')
            save_jpg(surf, os.path.join(out, f'slide-{i + 1}.jpg'))
    else:
        os.makedirs(os.path.dirname(out) or '.', exist_ok=True); wav = out[:-4] + '.wav'
        if not soundtrack(spec, wav) and '--force' not in sys.argv:
            sys.exit('voice lines overrun their scenes: shorten them or lengthen the scenes')
        render_video([((lambda c, t, s=s, i=i: compose(c, s, t, first=(i == 0))), s['dur']) for i, s in enumerate(S)], out, wav)
        os.remove(wav)


if __name__ == '__main__':
    main()
