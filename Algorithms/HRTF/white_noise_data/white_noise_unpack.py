import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from pickle file
data = []
fn="raw_whitenoise_data_test.pkl"
with open(fn, 'rb') as file:
    while True:
        try:
            data.append(pickle.load(file))
        except EOFError:
            break
print(len(data))
print(data[1][2])

L = [line[0] for line in  data]
R = [line[1] for line in  data]
L_norm = [l/32767 for l in L]
R_norm = [r/32767 for r in R]

az = [line[2][0] for line in  data]
el = [line[2][1] for line in  data]
sample_rate = [line[3] for line in data]

print(sample_rate[1])

df = pd.DataFrame({
    "L": L,  # Wrap arrays in a list to store as array objects in a single dataframe row
    "R": R,
    "L_norm": L_norm,
    "R_norm": R_norm,
    "az": az,
    "el": el,
    "sample_rate": sample_rate
})

print(df)

# def compute_spectrogram(data, fs):
#     frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
#                                           nperseg=4096, noverlap=2048, nfft=4096, scaling='density')
#     return frequencies, times, Sxx

# def plot_spectrogram(t,f,Sxx,title="",xlabel=False,ylabel=False):
#     plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
#     if(ylabel):
#         plt.ylabel('Frequency [Hz]')
#     if(xlabel):
#         plt.xlabel('Time [sec]')
#     plt.title(title)
#     plt.colorbar(label='Intensity [dB]')
#     plt.ylim(0, 22000)  # Limit frequency to human hearing frequency