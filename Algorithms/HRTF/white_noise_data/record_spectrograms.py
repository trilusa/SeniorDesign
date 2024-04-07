import time
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import spectrogram

def compute_spectrogram(data, fs):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=1024, noverlap=512, nfft=1024, scaling='density')
    return frequencies, times, Sxx

def plot_spectrogram(t,f,Sxx,title="",xlabel=False,ylabel=False):
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    if(ylabel):
        plt.ylabel('Frequency [Hz]')
    if(xlabel):
        plt.xlabel('Time [sec]')
    plt.title(title)
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(0, 22000)  # Limit frequency to human hearing frequency

# Parameters
file_name = "/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav"
sample_rate, data = wavfile.read(file_name)
N = len(data)
play_duration =  N / sample_rate
record_duration = play_duration  # Duration in seconds to record, ensure it covers the playback duration
print(f"Wave file playing. N samples = 2**{np.log2(len(data))} samples, duration;{play_duration} sample_rate = {sample_rate}")


# sd.play(data, sample_rate)
recording = sd.rec(int(record_duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16', device=None)
# sd.wait()  # Wait until recording is finished
time.sleep(record_duration)


print(2 ** int(np.log2(len(recording[0]))))
print(recording.shape)
cutoff=17
L = recording[:,0]#[:2 ** int(np.log2(len(recording[0])))]
R = recording[:,1]#[:2 ** int(np.log2(len(recording[1])))]
W = data
print(f"L len;{L.shape}, R len: {R.shape}, Play wave len:{W.shape}")

f, t, Sxx_noise = compute_spectrogram(L,sample_rate)
_, _, Sxx_noise = compute_spectrogram(W,sample_rate)
_, _, Sxx_left = compute_spectrogram(L,sample_rate)
_, _, Sxx_right = compute_spectrogram(R,sample_rate)

np.savez('combined_spectrograms.npz', f=f, t=t,
         Sxx_left=Sxx_left, Sxx_right=Sxx_right, Sxx_noise=Sxx_noise)
plt.figure(figsize=(10, 6))
r=3
c=1
plt.subplot(r,c,1)
plot_spectrogram(t,f, Sxx_noise, 'Spectrogram of White noise',xlabel=False,ylabel=True)
plt.subplot(r,c,2)
plot_spectrogram(t,f,  Sxx_left, 'Spectrogram of Right Channel',xlabel=False,ylabel=True)
plt.subplot(r,c,3)
plot_spectrogram(t,f, Sxx_right, 'Spectrogram of Left Channel', xlabel=True,ylabel=True)
plt.show()
