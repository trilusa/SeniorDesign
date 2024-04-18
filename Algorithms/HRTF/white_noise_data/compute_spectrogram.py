import time
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import spectrogram
import threading
# import pickle
import pandas as pd

df = pd.read_pickle('white_noise_df.pkl')

def compute_spectrogram(data, fs):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=4096, noverlap=2048, nfft=4096, scaling='density')
    return frequencies, times, Sxx

def plot_spectrogram(f,t,Sxx,title="",xlabel=False,ylabel=False):
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    if(ylabel):
        plt.ylabel('Frequency [Hz]')
    if(xlabel):
        plt.xlabel('Time [sec]')
    plt.title(title)
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(0, 22000)  # Limit frequency to human hearing frequency

i=200
L = df.at[i, 'L']
L_norm = L/(2**15)
R = df.at[i, 'R']
R_norm = R/(2**15)
az=df.at[i,'az']
el=df.at[i,'el']
sample_rate = df.at[i,'sample_rate']
_,_,SxxL = compute_spectrogram(L_norm, sample_rate)
f,t,SxxR = compute_spectrogram(R_norm, sample_rate)
HRTF_L = np.mean(SxxL,axis=1)
HRTF_R= np.mean(SxxR,axis=1)


r=2; c=3
plt.subplot(r,c,(1,2))
plot_spectrogram(f,t,SxxL,title=f"Test Spectrogram for az={az}°, el={el}°")
plt.subplot(r,c,(4,5))
plot_spectrogram(f,t,SxxR,xlabel=True, ylabel=True)

plt.subplot(r,c,3)
plt.plot(HRTF_L,f)
plt.ylim((0,22000))
plt.subplot(r,c,6)
plt.plot(HRTF_R,f)
plt.ylim((0,22000))
plt.show()