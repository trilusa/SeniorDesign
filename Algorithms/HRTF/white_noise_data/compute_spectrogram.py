import time
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import spectrogram
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import time

def compute_spectrogram(data, fs):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=4096, noverlap=2048, nfft=4096, scaling='density')
    return frequencies, times, Sxx

def compute_HRTF(L,R,fs):
    _, _, SxxL = compute_spectrogram(L, fs)
    _, _, SxxR = compute_spectrogram(R, fs)
    HRTF_L = np.mean(SxxL, axis=1)
    HRTF_R = np.mean(SxxR, axis=1)
    return HRTF_L, HRTF_R

def apply_HRTF_parallel(L,R,fs):
    with ProcessPoolExecutor() as executor:
        HRTF_L,HRTF_R = list(executor.map(compute_HRTF, L,R,[fs]*len(L)))
    return HRTF_L,HRTF_R



print("Script Started")
t0=time.time()
fn='raw_whitenoise_data_az15deg_el2deg_df.pkl'
df = pd.read_pickle(fn)
df.info(); print(df)
print(f"\n{fn} loaded into df in {time.time()-t0} sec\n")

print(df.loc[df['az'] == 10])

filtered_df = df.loc[df['az'] == 10]
filtered_df.info()
sample_rate = 96000
L=filtered_df['L']
R=filtered_df['R']

t0=time.time()
print(f"Computation started at {t0}")
HRTF_L,HRTF_R = apply_HRTF_parallel(L,R, sample_rate)
elapsed = time.time()-t0
print(f"Computation Finished, executed in {elapsed} sec ({elapsed/len(L)}) per HRTF)")
print(HRTF_L)


# def plot_spectrogram(f,t,Sxx,title="",xlabel=False,ylabel=False):
#     plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
#     if(ylabel):
#         plt.ylabel('Frequency [Hz]')
#     if(xlabel):
#         plt.xlabel('Time [sec]')
#     plt.title(title)
#     plt.colorbar(label='Intensity [dB]')
#     plt.ylim(0, 22000)  # Limit frequency to human hearing frequency

# def apply_spectrogram_parallel(data, fs):
#     with ProcessPoolExecutor() as executor:
#         results = list(executor.map(compute_spectrogram, data, [fs]*len(data)))
#     return results

# def process_row(i, row):
#     L_norm = row['L'] / (2**15)
#     R_norm = row['R'] / (2**15)
#     _, _, SxxL = compute_spectrogram(L_norm, row['sample_rate'])
#     _, _, SxxR = compute_spectrogram(R_norm, row['sample_rate'])
#     HRTF_L = np.mean(SxxL, axis=1)
#     HRTF_R = np.mean(SxxR, axis=1)
#     return i, HRTF_L, HRTF_R

# df['HRTF_L'] = None
# df['HRTF_R'] = None
# for i, HRTF_L, HRTF_R in results:
#     df.at[i, 'HRTF_L'] = HRTF_L
#     df.at[i, 'HRTF_R'] = HRTF_R

# for i, row in df.iterrows():
#     L = df.at[i, 'L']
#     L_norm = L/(2**15)
#     R = df.at[i, 'R']
#     R_norm = R/(2**15)
#     az=df.at[i,'az']
#     el=df.at[i,'el']
#     sample_rate = df.at[i,'sample_rate']
#     _,_,SxxL = compute_spectrogram(L_norm, sample_rate)
#     f,t,SxxR = compute_spectrogram(R_norm, sample_rate)
#     HRTF_L = np.mean(SxxL,axis=1)
#     HRTF_R= np.mean(SxxR,axis=1)
#     df.at[i, 'HRTF_L'] = HRTF_L
#     df.at[i, 'HRTF_R'] = HRTF_R
# for i in range(len(df)):
#     L = df.at[i, 'L']
#     L_norm = L/(2**15)
#     R = df.at[i, 'R']
#     R_norm = R/(2**15)
#     az=df.at[i,'az']
#     el=df.at[i,'el']
#     sample_rate = df.at[i,'sample_rate']
#     _,_,SxxL = compute_spectrogram(L_norm, sample_rate)
#     f,t,SxxR = compute_spectrogram(R_norm, sample_rate)
#     HRTF_L = np.mean(SxxL,axis=1)
#     HRTF_R= np.mean(SxxR,axis=1)
#     df['HRTF_L'][i] = HRTF_L
#     df['HRTF_R'][i] = HRTF_R

# print(df)
# df.to_pickle(fn)

# r=2; c=3
# plt.subplot(r,c,(1,2))
# plot_spectrogram(f,t,SxxL,title=f"Test Spectrogram for az={az}°, el={el}°")
# plt.subplot(r,c,(4,5))
# plot_spectrogram(f,t,SxxR,xlabel=True, ylabel=True)

# plt.subplot(r,c,3)
# plt.plot(HRTF_L,f)
# plt.ylim((0,22000))
# plt.subplot(r,c,6)
# plt.plot(HRTF_R,f)
# plt.ylim((0,22000))
# plt.show()