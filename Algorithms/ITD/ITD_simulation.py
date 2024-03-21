import numpy as np
import matplotlib.pyplot as plt

N=2**10
fs=96000
ts=1/fs

f0=1000.0
t=np.linspace(0.0,N*ts,N,endpoint=False)
xt=np.sin(f0*2.0*np.pi*t)

xf=np.fft.fft(xt)
f = np.fft.fftfreq(N,ts)


plt.subplot(2, 1, 1) # (rows, columns, panel number)
plt.plot(t, xt)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

plt.subplot(2,1,2)
plt.plot(f,np.abs(xf)/N)
plt.grid()
plt.title('FFT of the signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

print(xf)