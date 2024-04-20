import pandas as pd
import numpy as np
from scipy.signal import spectrogram

def compute_spectrogram(data, fs, window_L=4096):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return frequencies, times, Sxx

def compute_spectrum(x,fs=96000):
    x=x/(2**15)
    _, _, Sxx = compute_spectrogram(x, fs)
    X = np.mean(Sxx, axis=1)
    return X

def print_df(d,name="DATAFRAME"):
    print(f"\n********** {name} ***********\n"); print(d); d.info(); print("\n")

df = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl")
df = df[df['sound_type'] == 'WHITE_NOISE']
df['spectrum'] = df.apply(lambda row: compute_spectrum(row['signal'],fs=96000), axis=1)
df['sound_type']='HRTF'
df.drop('signal', axis=1, inplace=True)
pd.to_pickle(df, "HRTF_df.pkl")
print_df(df)
