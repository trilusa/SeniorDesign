#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from functools import reduce
from scipy.signal import spectrogram
import time

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

t0 = time.time()
#white noise df load, unnormalize
df_whitenoise = pd.read_pickle( "/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_whitenoise_data_az15deg_el2deg_df.pkl")
print(type(df_whitenoise['L']))
# df_whitenoise['L'] = (df_whitenoise['L'] * 2**15).astype(np.int16)
df_whitenoise['L'] = [(l*(2**15)).astype(np.int16) for l in df_whitenoise['L']]
df_whitenoise['R'] = [(r*(2**15)).astype(np.int16) for r in df_whitenoise['R']]

# df_whitenoise['R'] = (df_whitenoise['R'] * 2**15).astype(np.int16)
df_whitenoise['sound_type'] = 'WHITE_NOISE' #add sound type
df_whitenoise.head(); df_whitenoise.info()
print(f"Load time WHITE_NOISE: {time.time()-t0} ")
#primes load df
t0=time.time()
df_primes = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_primes_data_az15deg_el2deg_df.pkl")
df_primes.head(); df_primes.info()
print(f"Load time PRIMES: {time.time()-t0} ")

#load birds
t0=time.time()
df_birds = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_birds_data_az15deg_el2deg_df.pkl")
df_birds['sound_type'] = "BIRDS"
print(df_birds.head()); df_birds.info()
print(f"Load time Birds: {time.time()-t0} ")

#load fire
# df_fire = pd.read_pickle("")


t0=time.time()
df_whitenoise = transform_df(df_whitenoise, 'whitenoise')
df_primes = transform_df(df_primes, 'primes')
df_birds = transform_df(df_birds, 'birds')
# df_fire = transform_df(df_fire, 'fire')

#compute hrtf from white noise
fs = 96000  
def apply_spectrum(row, column_name):
    return compute_spectrum(row[column_name], fs)
# Applying the function and creating the new DataFrame
df_HRTF = df_whitenoise[['az', 'el']].copy()
df_HRTF['HRTF_L'] = df_whitenoise.apply(lambda row: apply_spectrum(row, 'whitenoise_L'), axis=1)
df_HRTF['HRTF_R'] = df_whitenoise.apply(lambda row: apply_spectrum(row, 'whitenoise_R'), axis=1)
print(df_HRTF.head()); df_HRTF.info()
df_HRTF.to_pickle("HRTF.pkl")

# Combine DataFrames horizontally based on 'az' and 'el'
dfs = [df_whitenoise, df_primes, df_birds]
df_final = reduce(lambda left, right: pd.merge(left, right, on=['az', 'el'], how='outer'), dfs)
df_final.to_pickle("raw_recordings.pkl")
df_final.head(); df_final.info()
print(f"Load time final df: {time.time()-t0} ")

# Save the final DataFrame as a pickle file
df_az100 = df_final[df_final['az'] == 100]
print(df_az100.head()); df_az100.info()



#load DF into workspace


# matrix = np.vstack(df['L'].values)