import pandas as pd
import numpy as np
from scipy.signal import spectrogram

def compute_spectrogram(data, fs, window_L=4096):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return frequencies, times, Sxx

def compute_spectrum(x,fs):
    _, _, Sxx = compute_spectrogram(x, fs)
    X = np.mean(Sxx, axis=1)
    return X

# def split_audio(row,T=1.0):
#     # Calculate the number of samples per 1-second audio
#     fs = row['sample_rate']
#     N=int(T*fs)
#     new_rows = []
#     num_segs = len(row['signal'])/N
#     for i in range(int(num_segs)):
#         start_idx = i * N
#         end_idx = start_idx + N
#         new_row = row.copy()
#         new_row['signal'] = row['signal'][start_idx:end_idx]
#         new_rows.append(new_row)
#     return pd.DataFrame(new_rows)

def print_df(d):
    print(f"\n********** {d['sound_type'].iloc[0]} ***********\n"); print(d); d.info(); print("\n")

#white noise df load
df_whitenoise = pd.read_pickle( "/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_whitenoise_data_az15deg_el2deg_df.pkl")
df_whitenoise['L'] = [(l*(2**15)).astype(np.int16) for l in df_whitenoise['L']] #unnormalize
df_whitenoise['R'] = [(r*(2**15)).astype(np.int16) for r in df_whitenoise['R']]
df_whitenoise['sound_type'] = 'WHITE_NOISE' #add sound type
df_whitenoise = pd.melt(df_whitenoise, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_whitenoise)

#primes load df
df_primes = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_primes_data_az15deg_el2deg_df.pkl")
df_primes['sound_type'] = "PRIMES"
df_primes = pd.melt(df_primes, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_primes)

#load birds
df_birds = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_birds_data_az15deg_el2deg_df.pkl")
df_birds['sound_type'] = "BIRDS"
df_birds = pd.melt(df_birds, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_birds)

#load fire
df_fire = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_fire_data_az15deg_el2deg_df.pkl")
df_fire['sound_type'] = "FIRE"
df_fire = pd.melt(df_fire, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_fire)

df_music = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_music_data_az15deg_el2deg_df.pkl")
df_music['sound_type'] = "MUSIC"
df_music = pd.melt(df_music, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_music)

df_chinese = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_chinesebible_data_az15deg_el2deg_df.pkl")
df_chinese['sound_type'] = "CHINESE"
df_chinese = pd.melt(df_chinese, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print_df(df_chinese)

dfs = [df_whitenoise, df_primes, df_birds, df_fire, df_music]
df = pd.concat(dfs, ignore_index=True)

print(f"\n\n########### All ##############\n\n")
# df = pd.concat(df.apply(split_audio, axis=1).tolist(), ignore_index=True)
print(df); df.info()
df.to_pickle("raw_recordings.pkl")