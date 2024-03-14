import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs=48e3
T=1 #seconds
f0=200
f1=20000
t=np.linspace(0, T, int(T * fs), endpoint=False)
f=f0+t*(f1-f0)/T
theta = ((f-f0)/(2*T))*t**2+f0*t
chirp = np.cos(theta)

# Convert the signal to 16-bit integer format
chirp_int16 = np.int16(chirp * 32767)  # 32767 is the max value for int16

# Write the signal to a WAV file
output_file = 'chirp_signal.wav'
wavfile.write(output_file, int(fs), chirp_int16)
output_file


plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(t, f)
plt.title('Instantaneous Frequency of the Chirp Signal')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')

plt.subplot(3, 1, 2)
plt.plot(t, theta)
plt.title('Instantaneous Phase of the Chirp Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 3)
plt.plot(t, chirp)
plt.title('Chirp Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()
