#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from functools import reduce
from scipy.signal import spectrogram

# Transform each DataFrame
def transform_df(df, sound_type):
    df = df[['az', 'el', 'L', 'R']].copy()
    df.rename(columns={'L': f'{sound_type}_L', 'R': f'{sound_type}_R'}, inplace=True)
    return df

def compute_spectrogram(data, fs, window_L=4096):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return frequencies, times, Sxx

def compute_spectrum(x,fs):
    _, _, Sxx = compute_spectrogram(x, fs)
    X = np.mean(Sxx, axis=1)
    return X

#white noise df load
df_whitenoise = pd.read_pickle( "/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_whitenoise_data_az15deg_el2deg_df.pkl")
print(type(df_whitenoise['L']))
df_whitenoise['L'] = [(l*(2**15)).astype(np.int16) for l in df_whitenoise['L']] #unnormalize
df_whitenoise['R'] = [(r*(2**15)).astype(np.int16) for r in df_whitenoise['R']]
df_whitenoise['sound_type'] = 'WHITE_NOISE' #add sound type
df_whitenoise = pd.melt(df_whitenoise, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print(df_whitenoise.head()); df_whitenoise.info()



#primes load df
df_primes = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_primes_data_az15deg_el2deg_df.pkl")
df_primes['sound_type'] = "PRIMES"
df_primes = pd.melt(df_primes, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print(df_primes.head()); df_primes.info()

#load birds
df_birds = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_birds_data_az15deg_el2deg_df.pkl")
df_birds['sound_type'] = "BIRDS"
df_birds = pd.melt(df_birds, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print(df_birds.head()); df_birds.info()

#load fire
df_fire = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_fire_data_az15deg_el2deg_df.pkl")
df_fire['sound_type'] = "FIRE"
df_fire = pd.melt(df_fire, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print(df_fire.head()); df_fire.info()

df_music = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_music_data_az15deg_el2deg_df.pkl")
df_music['sound_type'] = "MUSIC"
df_music = pd.melt(df_music, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
print(df_music.head()); df_music.info()

# df_chinese = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_fire_data_az15deg_el2deg_df.pkl")
# df_chinese['sound_type'] = "CHINESE"
# df_chinese = pd.melt(df_chinese, id_vars=['az', 'el', 'sound_type', 'sample_rate'], value_vars=['L', 'R'], var_name='channel', value_name='signal')
# print(df_chinese.head()); df_chinese.info()

# df_whitenoise = transform_df(df_whitenoise, 'whitenoise')
# df_primes = transform_df(df_primes, 'primes')
# df_birds = transform_df(df_birds, 'birds')
# df_fire = transform_df(df_fire, 'fire')
# df_music = transform_df(df_music, 'music')

# #compute hrtf from white noise
# fs = 96000  
# def apply_spectrum(row, column_name):
#     return compute_spectrum(row[column_name], fs)
# # Applying the function and creating the new DataFrame
# df_HRTF = df_whitenoise[['az', 'el']].copy()
# df_HRTF['HRTF_L'] = df_whitenoise.apply(lambda row: apply_spectrum(row, 'whitenoise_L'), axis=1)
# df_HRTF['HRTF_R'] = df_whitenoise.apply(lambda row: apply_spectrum(row, 'whitenoise_R'), axis=1)
# print(df_HRTF.head()); df_HRTF.info()
# df_HRTF.to_pickle("HRTF.pkl")
print(f"\n\n--------------\n\n")
# # Combine DataFrames horizontally based on 'az' and 'el'
dfs = [df_whitenoise, df_primes, df_birds, df_fire, df_music]
df = pd.concat(dfs, ignore_index=True)
# df = reduce(lambda left, right: pd.merge(left, right, on=['az', 'el'], how='outer'), dfs)
df.to_pickle("raw_recordings.pkl")
print(df.head()); df.info()

# # Melt the DataFrame to go from wide to long format
# tidy_df = df.melt(id_vars=['az', 'el'], var_name='variable', value_name='signal')

# Split the 'variable' column into 'source' and 'channel'
# tidy_df[['source', 'channel']] = tidy_df['variable'].str.split('_', expand=True)

# # Drop the original 'variable' column as it's no longer needed
# tidy_df.drop('variable', axis=1, inplace=True)

# # Add a constant column for sample rate
# tidy_df['sample_rate'] = 96000

# # Reorder columns to match your specified order, if needed
# tidy_df = tidy_df[['signal', 'channel', 'source', 'az', 'el', 'sample_rate']]