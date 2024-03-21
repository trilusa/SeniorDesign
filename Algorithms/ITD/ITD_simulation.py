import numpy as np
import matplotlib.pyplot as plt

N=2**10
N_frames=5
fs=96000
ts=1/fs

f0=6000.0
t=np.linspace(0,N*ts,N,endpoint=False)
t=np.tile(np.linspace(-N*ts/2,N*ts/2,N,endpoint=False), N_frames)
print(len(t))
xt=np.sin(f0*2.0*np.pi*t)
xt=np.sinc(f0*t)


xf=np.fft.fft(xt)#[:1+N//2]
#f = np.fft.fftfreq(N,ts)[:1+N//2]
f=np.linspace(-fs/2,fs/2,N*N_frames)

plt.subplot(3, 1, 1) # (rows, columns, panel number)
plt.plot(xt)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

plt.subplot(3,1,2)
plt.plot(f,np.abs(xf)/N)
plt.grid()
plt.title('Magnitude')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.subplot(3,1,3)
plt.plot(f,np.angle(xf))
plt.grid()
plt.title('Phase')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Rad')
plt.show()

print(xf)