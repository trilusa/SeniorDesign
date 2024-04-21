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

def print_df(d):
    print(f"\n********** {d['sound_type'].iloc[0]} ***********\n"); print(d); d.info(); print("\n")

# Dictionary of file base names and their corresponding sound types
files_and_types = {
    # 'raw_whitenoise_data_az15deg_el2deg_df': 'WHITE_NOISE',
    # 'raw_whitenoise_data_az15deg_el2deg_start5_df': 'WHITE_NOISE',
    # 'raw_whitenoise_data_az15deg_el2deg_start10_df': 'WHITE_NOISE',
    'raw_primes_data_az15deg_el2deg_df': 'PRIMES',
    # 'raw_primes_data_az15deg_el2deg_start5_df': 'PRIMES',
    # 'raw_primes_data_az15deg_el2deg_start10_df': 'PRIMES',
    # 'raw_birds_data_az15deg_el2deg_start5_df': 'BIRDS',
    # 'raw_birds_data_az15deg_el2deg_start10_df': 'BIRDS',
    'raw_music_data_az15deg_el2deg_df': 'MUSIC',
    'raw_music_data_az15deg_el2deg_start5_df': 'MUSIC',
    'raw_music_data_az15deg_el2deg_start10_df': 'MUSIC',
    'raw_chinesebible_data_az15deg_el2deg_df': 'CHINESE',
    'raw_chinesebible_data_az15deg_el2deg_start5_df': 'CHINESE',
    'raw_chinesebible_data_az15deg_el2deg_start10_df': 'CHINESE',
    'raw_muon_data_az5deg_el5deg_df': 'MUON',
    'raw_cursed_data_az5deg_el5deg_df': 'CURSED',
    'raw_fire_data_az15deg_el2deg_df': 'FIRE',
    'raw_birds_data_az15deg_el2deg_df': 'BIRDS'
}

base_path = "raw/" #run with relative paths from Algorithms/data directory
all_dfs = []

# Loop through the dictionary to process each file
for file_base, sound_type in files_and_types.items():
    file_path = f"{base_path}{file_base}.pkl"
    df = pd.read_pickle(file_path)
    
    # df['sound_type'] = sound_type
    # df = pd.melt(df, id_vars=['az', 'el', 'sound_type', 'sample_rate'], 
    #              value_vars=['L', 'R'], var_name='channel', value_name='signal')
    # #decimate to 48000
    # mask = df['sample_rate'] == 96000  # Create a mask for rows to be decimated
    # df.loc[mask, 'signal'] = df.loc[mask, 'signal'].apply(lambda x: np.array(x)[::2])
    # df.loc[mask, 'sample_rate'] = df.loc[mask, 'sample_rate']//2
    
    print_df(df)
    # df.to_pickle(file_path)
    all_dfs.append(df)

# input()
Ndf=len(all_dfs)
df=pd.concat(all_dfs,ignore_index=True)
# df1 = pd.concat(all_dfs[:Ndf//2], ignore_index=True)
# df2 = pd.concat(all_dfs[Ndf//2:], ignore_index=True)


print(f"\n\n########### All ##############\n\n")
# print(df['signal'].iloc[0].shape)
# print(df1); df1.info()
# df1.to_pickle("raw_recordings1.pkl")
# df2.to_pickle("raw_recordings2.pkl")
df.to_pickle("raw_recordings_no_whitenoise.pkl")
print("DONE")