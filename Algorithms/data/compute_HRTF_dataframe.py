import pandas as pd
import numpy as np
from scipy.signal import spectrogram

def compute_spectrogram(data, fs, window_L=4096):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return frequencies, times, Sxx

def compute_LRspectra(L,R,fs=48000):
    L=L/(2**15)
    R=R/(2**15)
    _, _, Sxx_L = compute_spectrogram(L, fs)
    _, _, Sxx_R = compute_spectrogram(R, fs)
    Sxx_L = np.log10(np.mean(Sxx_L, axis=1)) #calc spectrum by average ove time slices
    Sxx_R = np.log10(np.mean(Sxx_R, axis=1))
    maxLR=np.max([np.max(Sxx_L),np.max(Sxx_R)]) #normalize so max of L and R together maps to 0db, preserves relative amplitude
    Sxx_L = Sxx_L - maxLR
    Sxx_R = Sxx_R - maxLR
    return Sxx_L,Sxx_R
def print_df(d,name="DATAFRAME"):
    print(f"\n********** {name} ***********\n"); print(d); d.info(); print("\n")

print("started")
df = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw/hrtf2/raw_whitenoise_narrow_data_az2deg_el2deg_df.pkl")
df1 = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw/hrtf2/raw_whitenoise2_data_az2deg_el2deg_df.pkl")
# df2 = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw/hrtf2/raw_whitenoise_data_az2deg_el2deg_2_df.pkl")
print_df(df)
print_df(df1)

df= pd.concat([df,df1])
# df = df[df['sound_type'] == 'WHITE_NOISE2']

df['HRTF_L'], df['HRTF_R'] = zip(*df.apply(lambda row: compute_LRspectra(row['L'], row['R'], fs=row['sample_rate']), axis=1))
# df1['HRTF_L'], df1['HRTF_R'] = zip(*df1.apply(lambda row: compute_LRspectra(row['L'], row['R'], fs=row['sample_rate']), axis=1))
# df2['HRTF_L'], df2['HRTF_R'] = zip(*df2.apply(lambda row: compute_LRspectra(row['L'], row['R'], fs=row['sample_rate']), axis=1))
df.drop(['L','R'], axis=1, inplace=True)
pd.to_pickle(df, "/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw/hrtf2/HRTF_df2.pkl")
print_df(df)
