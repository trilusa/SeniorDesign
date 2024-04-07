import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

# Load the WAV file
file_name = "/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav"
sample_rate, data = wavfile.read(file_name)

# Ensure the data is in the correct format (might need to convert if stereo)
if data.ndim > 1:
    data = data[:, 0]  # Take the first channel if stereo

# Compute the spectrogram
frequencies, times, Sxx = spectrogram(data, fs=sample_rate, window='hamming',
                                      nperseg=1024, noverlap=512, nfft=1024, scaling='density')

# Plot the spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(times, frequencies, 10 * np.log10(Sxx), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram of White Noise')
plt.colorbar(label='Intensity [dB]')
plt.ylim(0, sample_rate / 2)  # Limit frequency to Nyquist frequency
plt.show()
