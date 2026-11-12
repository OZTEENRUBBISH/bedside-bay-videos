"""Soundtracks for Bedside Bay ads: music bed + sound effects + AI voiceover (Kokoro, open model).

build(path, D, style, drop, lift, cta, cues, voice)
  style: 'upbeat' | 'tense' | 'bright'
  drop/lift/cta: seconds where drums come in, where the track lifts, where the end card starts
  cues:  [(time, kind)] kind in whoosh|pop|ding|cash|tick|beep|riser|impact|step:<n>
  voice: [(time, text, max_seconds)] spoken lines; music ducks under them
"""
import os, subprocess, wave
import numpy as np
from scipy import signal

SR = 44100
VOICE = 'am_michael'
TTS_DIR = os.path.expanduser('~/.cache/bedside-tts')
TTS_URL = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/'
_k = None
rng = np.random.default_rng(7)
NOTE = {'D2': 73.42, 'F2': 87.31, 'G2': 98.0, 'A2': 110.0, 'Bb2': 116.54, 'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61,
        'G3': 196.0, 'A3': 220.0, 'Bb3': 233.08, 'B3': 246.94, 'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.0,
        'A4': 440.0, 'B4': 493.88, 'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.0, 'C6': 1046.5}


def _t(d): return np.arange(int(d * SR)) / SR
def _f(x, kind, fc):
    return signal.sosfilt(signal.butter(2, np.array(fc) / (SR / 2), kind, output='sos'), x)
def _saw(f, tt, k=10): return sum(np.sin(2 * np.pi * f * h * tt) / h for h in range(1, k + 1)) * .55


def kick():
    tt = _t(.36); ph = 2 * np.pi * np.cumsum(45 + 110 * np.exp(-tt * 38)) / SR
    return np.sin(ph) * np.exp(-tt * 11) + .25 * _f(rng.standard_normal(len(tt)), 'high', 3000) * np.exp(-tt * 300)
def clap():
    tt = _t(.22); e = sum(np.exp(-np.maximum(tt - d, 0) * 60) * (tt >= d) for d in (0, .012, .026)) / 2
    return _f(rng.standard_normal(len(tt)), 'band', [900, 4200]) * e
def hat(op=False):
    tt = _t(.3 if op else .06); return _f(rng.standard_normal(len(tt)), 'high', 7500) * np.exp(-tt * (16 if op else 90)) * .6
def bass(f, d):
    tt = _t(d); return _f(_saw(f, tt, 8), 'low', 420) * np.minimum(tt / .01, 1) * np.exp(-tt * 3.5)
def pluck(f, d=.45):
    tt = _t(d); return _f(_saw(f, tt, 6) + _saw(f * 1.006, tt, 6), 'low', 2600) * np.exp(-tt * 7) * np.minimum(tt / .004, 1) * .5
def pad(fs, d):
    tt = _t(d); w = sum(_saw(f * dt, tt, 6) for f in fs for dt in (.996, 1.004))
    return _f(w, 'low', 1100) * np.minimum(tt / .35, 1) * np.clip((d - tt) / .4, 0, 1) / len(fs) * .6
def bell(f, d=1.3):
    tt = _t(d); return sum(a * np.sin(2 * np.pi * f * m * tt) * np.exp(-tt * dc) for m, a, dc in ((1, 1, 4), (2.76, .5, 7), (5.4, .25, 11), (8.93, .12, 16))) * .5
def pop():
    tt = _t(.09); ph = 2 * np.pi * np.cumsum(380 + 700 * tt / .09) / SR; return np.sin(ph) * np.exp(-tt * 34) * np.minimum(tt / .003, 1)
def tick():
    tt = _t(.03); return _f(rng.standard_normal(len(tt)), 'high', 3500) * np.exp(-tt * 220) * .5
def beep():
    tt = _t(.16); return np.sin(2 * np.pi * 880 * tt) * np.minimum(tt / .004, 1) * np.clip((.16 - tt) / .03, 0, 1) * .5
def cash():
    w = np.zeros(int(1.2 * SR)); a, b = bell(2093, 1.0), bell(2637, 1.0); w[:len(a)] += a; i = int(.075 * SR); w[i:i + len(b)] += b[:len(w) - i]
    tt = _t(.25); s = _f(rng.standard_normal(len(tt)), 'high', 6000) * np.exp(-tt * 20) * .25; w[:len(s)] += s; return w
def whoosh(d=.55):
    n = int(d * SR); x = rng.standard_normal(n); y = np.zeros(n); u = np.linspace(0, 1, n); a = .02 + .5 * np.sin(np.pi * u) ** 2; p = 0.0
    for i in range(n): p += a[i] * (x[i] - p); y[i] = p
    return _f(y, 'high', 300) * np.sin(np.pi * u) ** 2 * 1.4
def riser(d=1.2):
    tt = _t(d); u = tt / d; ph = 2 * np.pi * np.cumsum(220 * 2 ** (u * 2.6)) / SR
    return (_f(rng.standard_normal(len(tt)), 'high', 2500) * .5 + np.sin(ph) * .35) * u ** 2
def impact():
    tt = _t(1.4); ph = 2 * np.pi * np.cumsum(34 + 60 * np.exp(-tt * 14)) / SR
    return np.sin(ph) * np.exp(-tt * 3.2) * 1.2 + _f(rng.standard_normal(len(tt)), 'low', 1800) * np.exp(-tt * 9) * .6
def heart():
    w = np.zeros(int(.5 * SR)); k = kick() * .9; w[:len(k)] += k; i = int(.19 * SR); w[i:i + len(k)] += k[:len(w) - i] * .65; return _f(w, 'low', 160) * 1.6


class Mix:
    def __init__(s, D): s.n = int(D * SR); s.b = np.zeros(s.n)
    def add(s, w, t, v=1.0):
        i = int(t * SR)
        if 0 <= i < s.n: m = min(len(w), s.n - i); s.b[i:i + m] += w[:m] * v


def music(D, style, drop, lift, cta):
    m = Mix(D); bpm = {'upbeat': 120, 'tense': 100, 'bright': 124}[style]; beat = 60 / bpm
    if style == 'bright': prog = [('C3', 'C4 E4 G4 C5'), ('G2', 'G3 B3 D4 G4'), ('A2', 'A3 C4 E4 A4'), ('F2', 'F3 A3 C4 F4')]
    elif style == 'tense': prog = [('D2', 'D4 F4 A4 D5'), ('Bb2', 'Bb3 D4 F4 Bb3'), ('F2', 'F3 A3 C4 F4'), ('A2', 'A3 C4 E4 A4')]
    else: prog = [('A2', 'A3 C4 E4 A4'), ('F2', 'F3 A3 C4 F4'), ('C3', 'C4 E4 G4 C5'), ('G2', 'G3 B3 D4 G4')]
    t = 0.0; bar = 0
    while t < cta:
        root, arp = prog[bar % 4]; arp = [NOTE[x] for x in arp.split()]; on = t >= drop - 1e-6; hi = t >= lift - 1e-6
        m.add(pad([NOTE[root] * 2, arp[1], arp[2]], min(beat * 4 + .3, cta - t + .3)), t, .5 if on else .7)
        if style == 'tense':
            for k in range(4): m.add(heart(), t + k * beat, .55 if on else .4)
            if on:
                for k in range(16): m.add(tick(), t + k * beat / 4, .35 if k % 4 else .6)
                for k in range(8): m.add(pluck(arp[[0, 2, 1, 3, 0, 2, 3, 1][k]] * (2 if hi else 1)), t + k * beat / 2, .28)
                for k in (0, 2.5): m.add(bass(NOTE[root], beat * 1.4), t + k * beat, .7)
        elif on:
            for k in range(4):
                m.add(kick(), t + k * beat, .9)
                if k % 2: m.add(clap(), t + k * beat, .5)
            for k in range(8):
                m.add(hat(hi and k % 2 == 1), t + k * beat / 2, .32); m.add(bass(NOTE[root], beat / 2), t + k * beat / 2, .55)
                m.add(pluck(arp[[0, 1, 2, 3, 2, 1, 2, 3][k]] * (2 if hi else 1)), t + k * beat / 2, .36)
        else:
            for k in (0, 2): m.add(pluck(arp[k]), t + k * beat, .3)
        t += beat * 4; bar += 1
    m.b[int(cta * SR):] *= np.linspace(1, 0, max(1, m.n - int(cta * SR))) ** 2
    end = ['C4', 'E4', 'G4', 'C5'] if style != 'tense' else ['D4', 'F4', 'A4', 'D5']
    m.add(pad([NOTE[x] for x in end], D - cta + .2), cta, 1.0)
    for i, x in enumerate(end): m.add(bell(NOTE[x] * 2, 2.2), cta + i * .06, .22)
    return m.b


def _kokoro():
    global _k
    if _k is None:
        os.makedirs(TTS_DIR, exist_ok=True)
        for f in ('kokoro-v1.0.onnx', 'voices-v1.0.bin'):
            p = os.path.join(TTS_DIR, f)
            if not os.path.exists(p) or os.path.getsize(p) < 1e6:
                subprocess.check_call(['curl', '-sSL', '-o', p, TTS_URL + f])
        from kokoro_onnx import Kokoro
        _k = Kokoro(os.path.join(TTS_DIR, 'kokoro-v1.0.onnx'), os.path.join(TTS_DIR, 'voices-v1.0.bin'))
    return _k


def say(text, max_s=None, speed=1.0):
    """Speak one line; returns 44.1k mono. Speeds up (to 1.3x at most) if it would overrun max_s."""
    def synth(sp):
        s, sr = _kokoro().create(text, voice=VOICE, speed=sp, lang='en-us'); s = np.asarray(s, dtype=np.float64)
        idx = np.where(np.abs(s) > .01)[0]; s = s[max(0, idx[0] - 400):idx[-1] + 2400] if len(idx) else s
        return signal.resample_poly(s, 147, 80)
    w = synth(speed)
    if max_s and len(w) / SR > max_s: w = synth(min(1.3, speed * len(w) / SR / max_s * 1.03))
    w = _f(w, 'high', 85); w = w / (np.abs(w).max() + 1e-9)
    return np.tanh(w * 1.6) / np.tanh(1.6)


def build(path, D, style='upbeat', drop=0.0, lift=None, cta=None, cues=(), voice=()):
    cta = D - 3.4 if cta is None else cta; lift = cta * .66 if lift is None else lift
    mus = music(D, style, drop, lift, cta); mus = mus / (np.abs(mus).max() + 1e-9) * .5
    fx = Mix(D)
    for t, kind in cues:
        if kind.startswith('step:'): fx.add(bell(NOTE[['C5', 'D5', 'E5', 'G5', 'C6'][int(kind[5:])]], .9), t, .45)
        else:
            w, v = {'whoosh': (whoosh, .5), 'pop': (pop, .5), 'ding': (lambda: bell(1318.5, 1.0), .4), 'cash': (cash, .42), 'tick': (tick, .5),
                    'beep': (beep, .35), 'riser': (riser, .45), 'impact': (impact, .7)}[kind]
            fx.add(w(), t, v)
    vo = Mix(D); report = []
    free = 0.0
    for t, text, mx in voice:
        w = say(text, mx); t = max(t, free); vo.add(w, t, .95); free = t + len(w) / SR + .12  # never overlap two lines
        report.append((round(t, 2), round(len(w) / SR, 2), text))
    env = _f(np.abs(vo.b), 'low', 6); env = np.clip(env / .12, 0, 1)
    out = mus * (1 - .62 * env) + fx.b * (1 - .3 * env) + vo.b
    tt = np.arange(len(out)) / SR; out = np.tanh(out * 1.15) * .95 * np.clip((D - tt) / .5, 0, 1)
    w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    return report
