import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import time

def compute_spectrogram(data, fs):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=4096, noverlap=2048, nfft=4096, scaling='density')
    return frequencies, times, Sxx

def compute_HRTF(x,fs):
    _, _, Sxx = compute_spectrogram(x, fs)
    HRTF = np.mean(Sxx, axis=1)
    return HRTF

def apply_HRTF_parallel(x,fs):
    with ProcessPoolExecutor() as executor:
        HRTF = list(executor.map(compute_HRTF,x,[fs]*len(x)))
    return HRTF

print("Script Started")
t0=time.time()
fn='/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_primes_data_az15deg_el2deg_df'
df = pd.read_pickle(fn+'.pkl')
df.info(); print(df)
print(f"\n{fn} loaded into df in {time.time()-t0} sec\n")

print(df['az'])
az_slice=100
filtered_df = df.loc[df['az'] == az_slice]
filtered_df.info()
sample_rate = 96000
L=filtered_df['L']
R=filtered_df['R']


#comment if already normalized
L_lst =[l/(2**15) for l in L]
R_lst =[r/(2**15) for r in R]


t0=time.time()
print(f"Computation started at {t0}")
# HRTF_L_lst = apply_HRTF_parallel(L, sample_rate)
# HRTF_R_lst = apply_HRTF_parallel(R, sample_rate)
HRTF_L_lst = []
HRTF_R_lst = []
for l in L_lst:
    HRTF_L_lst.append(compute_HRTF(l,sample_rate))
for r in R_lst:
    HRTF_R_lst.append(compute_HRTF(r,sample_rate))

elapsed = time.time()-t0
print(f"Computation Finished, executed in {elapsed} sec ({elapsed/len(HRTF_L_lst)}) per HRTF)")
print(HRTF_L_lst)
filtered_df['HRTF_L'] = HRTF_L_lst
filtered_df['HRTF_R'] = HRTF_R_lst
filtered_df.to_pickle(fn+'_az90deg'+ '.pkl')

f,_,_ = compute_spectrogram(np.zeros_like(L.iloc[0]), sample_rate) #just to get freq axis

# Example arrays and variables (you should already have these)
# HRTF_R_lst, HRTF_L_lst, f, filtered_df

HRTF_L_arr = np.stack(HRTF_L_lst, axis=0)
print(HRTF_L_arr.size)
print(type(HRTF_L_arr))
HRTF_R_arr = np.stack(HRTF_R_lst, axis=0)
max_f_idx = 1000

r = 1; c = 2
fig, axs = plt.subplots(r, c, figsize=(12, 6))
# plt.title(f"Left and Right HRTFs for azimuth={az_slice}°")
# Color map plot for HRTF_L_lst on the top-left subplot (index 0, 0)
axs[0, 0].imshow(10 * np.log10(HRTF_L_arr[:,:max_f_idx]), aspect='auto', origin='lower', interpolation='none',
                  extent=[f[0], f[max_f_idx - 1], filtered_df['el'].min(), filtered_df['el'].max()])
axs[0, 0].set_title(f"Left HRTF (azimuth={az_slice}°0)")
axs[0, 0].xlabel("f [Hz]")
axs[0, 0].ylabel("elevation [ ° ]")

# Color map plot for HRTF_R_lst on the top-right subplot (index 0, 1)
axs[0, 1].imshow(10 * np.log10(HRTF_R_arr[:,:max_f_idx]), aspect='auto', origin='lower', interpolation='none',
                  extent=[f[0], f[max_f_idx - 1], filtered_df['el'].min(), filtered_df['el'].max()])
axs[0, 1].set_title("Right HRTF")
# Line plots for HRTF_L_lst on the bottom-left subplot (index 1, 0)
# for i, v in enumerate(HRTF_L_lst):
#     vdb = 10 * np.log10(v)
#     axs[1, 0].plot(f, vdb, label=f"{filtered_df['el'].iloc[i]} deg")
# axs[1, 0].set_title("HRTF L")
# axs[1, 0].set_xlim((0, 22000))
# # axs[1, 0].legend()

# # Line plots for HRTF_R_lst on the bottom-right subplot (index 1, 1)
# for i, v in enumerate(HRTF_R_lst):
#     vdb = 10 * np.log10(v)
#     axs[1, 1].plot(f, vdb, label=f"{filtered_df['el'].iloc[i]} deg")
# axs[1, 1].set_xlim((0, 22000))
# axs[1, 1].set_title("HRTF R")
# # axs[1, 1].legend()

# plt.tight_layout()
# plt.show()


# r=2; c=2
# fig, axs = plt.subplots(r, c, figsize=(12, 6))

# plt.imshow(10*np.log10(HRTF_R_lst), aspect='auto', origin='lower', interpolation='none',
#                          extent=[f[0], f[-1], filtered_df['el'].min(), filtered_df['el'].max()])
# plt.subplot(r,c,3)
# for i,v in enumerate(HRTF_L_lst):
#     vdb=10*np.log10(v)
#     plt.plot(f,vdb,label=f"{filtered_df['el'].iloc[i]} deg")
    
# plt.title("L")
# plt.xlim((0,22000))
# plt.legend()
# plt.subplot(r,c,4)
# for i,v in enumerate(HRTF_R_lst):
#     vdb=10*np.log10(v)
#     plt.plot(f,vdb,label=f"{filtered_df['el'].iloc[i]} deg")
# plt.xlim((0,22000))
# plt.title("R")
# plt.legend()

# plt.show()
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