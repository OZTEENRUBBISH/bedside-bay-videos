"""Tiny synth soundtracks. make(path, seconds, style) with style: upbeat | tense | bright."""
import numpy as np, wave
SR = 44100
N = {'D2':73.42,'F2':87.31,'G2':98,'A2':110,'Bb2':116.54,'C3':130.81,'D3':146.83,'E3':164.81,'F3':174.61,'G3':196,'A3':220,'Bb3':233.08,'B3':246.94,'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392,'A4':440,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'G5':783.99}


def make(path, D, style='upbeat', cta=3.4, dings=()):
    n = int(SR * D); out = np.zeros(n)

    def note(f, start, dur, vol=.2, kind='pluck'):
        i0 = int(start * SR); m = min(int(dur * SR), n - i0)
        if m <= 0: return
        tt = np.arange(m) / SR
        if kind == 'pluck': w = (np.sin(2*np.pi*f*tt) + .35*np.sin(4*np.pi*f*tt) + .15*np.sin(6*np.pi*f*tt)) * np.exp(-tt*5)
        elif kind == 'pad': w = (np.sin(2*np.pi*f*tt) + .5*np.sin(2*np.pi*f*1.005*tt)) * np.minimum(tt/.25, 1) * np.clip((dur-tt)/.3, 0, 1)
        elif kind == 'beep': w = np.sin(2*np.pi*f*tt) * np.minimum(tt/.005, 1) * np.exp(-tt*22)
        else: w = np.sin(2*np.pi*(f*np.exp(-tt*28)+45)*tt) * np.exp(-tt*9)
        out[i0:i0+m] += w * vol

    end = D - cta
    if style == 'tense':
        for root, t0 in (('D2', 0), ('Bb2', end/2)):
            note(N[root], t0, end/2, .14, 'pad'); note(N[root]*1.5, t0, end/2, .06, 'pad')
        t = 0.0; gap = .95
        while t < end:  # heartbeat that speeds up
            note(60, t, .25, .42, 'kick'); note(52, t+.18, .25, .3, 'kick'); note(880, t, .2, .05, 'beep')
            t += gap; gap = max(.42, gap*.93)
        arp = ['D4','F4','A4','D5']; t = end*.35; k = 0
        while t < end:
            note(N[arp[k % 4]], t, .4, .09); t += .25; k += 1
    else:
        beat = 60/(124 if style == 'bright' else 120)
        prog = [('C3',['C4','E4','G4','C5']),('G2',['G3','B3','D4','G4']),('A2',['A3','C4','E4','A4']),('F2',['F3','A3','C4','F4'])] if style == 'bright' else \
               [('A2',['A3','C4','E4','A4']),('F2',['F3','A3','C4','F4']),('C3',['C4','E4','G4','C5']),('G2',['G3','B3','D4','G4'])]
        t = 0.0; bar = 0
        while t < end:
            root, arp = prog[bar % 4]; hi = 2.0 if t > end*.66 else 1.0
            note(N[root], t, beat*4, .12, 'pad'); note(N[root]*1.5, t, beat*4, .05, 'pad')
            for k in range(8): note(N[arp[[0,1,2,3,2,1,2,3][k]]]*hi, t+k*beat/2, .5, .14)
            for k in range(4): note(55, t+k*beat, .3, .28 if t > end*.25 else .16, 'kick')
            t += beat*4; bar += 1
    for s in dings: note(N['E5'], s, .5, .10); note(N['G5'], s+.08, .6, .10)
    for f in ('C4','E4','G4','C5','E5'): note(N[f], end, cta, .07, 'pad'); note(N[f], end, 1.5, .10)
    note(55, end, .4, .35, 'kick')
    t = np.arange(n)/SR; out = np.tanh(out*1.3)*.8*np.clip((D-t)/.8, 0, 1)
    w = wave.open(path, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
