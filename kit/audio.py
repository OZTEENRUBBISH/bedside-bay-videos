import numpy as np, wave
sr=44100; D=18.0; n=int(sr*D); t=np.arange(n)/sr; out=np.zeros(n)
def note(f,start,dur,vol=.2,kind='pluck'):
    i0=int(start*sr); m=int(dur*sr); 
    if i0>=n: return
    m=min(m,n-i0); tt=np.arange(m)/sr
    if kind=='pluck': w=(np.sin(2*np.pi*f*tt)+.35*np.sin(4*np.pi*f*tt)+.15*np.sin(6*np.pi*f*tt))*np.exp(-tt*5)
    elif kind=='pad': w=(np.sin(2*np.pi*f*tt)+.5*np.sin(2*np.pi*f*1.005*tt))*np.minimum(tt/.25,1)*np.minimum((dur-tt)/.3,1)
    elif kind=='beep': w=np.sin(2*np.pi*f*tt)*np.minimum(tt/.005,1)*np.exp(-tt*22)
    elif kind=='kick': w=np.sin(2*np.pi*(f*np.exp(-tt*28)+45)*tt)*np.exp(-tt*9)
    out[i0:i0+m]+=w*vol
N={'A2':110,'C3':130.81,'D3':146.83,'E3':164.81,'F2':87.31,'F3':174.61,'G2':98,'G3':196,'A3':220,'B3':246.94,'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392,'A4':440,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'G5':783.99}
beat=60/120
# scene 0 (0-3s): sparse, minor, slow monitor beeps
note(N['A2'],0,3.0,.10,'pad'); note(N['E3'],0,3.0,.06,'pad')
for b in (0.2,1.2,2.2): note(880,b,.3,.07,'beep')
# scenes 1-3 (3-14.6s): driving arpeggio that climbs
prog=[('A2',['A3','C4','E4','A4']),('F2',['F3','A3','C4','F4']),('C3',['C4','E4','G4','C5']),('G2',['G3','B3','D4','G4'])]
tcur=3.0; bar=0
while tcur<14.6:
    root,arp=prog[bar%4]; lift=1.0 if tcur<7.2 else (1.0 if tcur<10.4 else 2.0)
    note(N[root],tcur,beat*4,.12,'pad'); note(N[root]*1.5,tcur,beat*4,.05,'pad')
    for k in range(8):
        note(N[arp[[0,1,2,3,2,1,2,3][k]]]*lift,tcur+k*beat/2,.5,.13 if tcur<10.4 else .16)
    for k in range(4):
        note(55,tcur+k*beat,.3,.32 if tcur>=7.2 else .22,'kick')
    tcur+=beat*4; bar+=1
# reward dings on toasts / promotions
for s in (3.5,4.65,5.95,7.75,9.0,10.9,11.7,12.5):
    note(N['E5'],s,.5,.10); note(N['G5'],s+.08,.6,.10)
# CTA (14.6-18): resolved major chord
for f in ('C4','E4','G4','C5','E5'): note(N[f],14.6,3.2,.07,'pad'); note(N[f],14.6,1.5,.10)
note(55,14.6,.4,.35,'kick')
fade=np.minimum(1,(D-t)/.8); out=np.tanh(out*1.3)*.8*np.clip(fade,0,1)
w=wave.open('out/music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close()
