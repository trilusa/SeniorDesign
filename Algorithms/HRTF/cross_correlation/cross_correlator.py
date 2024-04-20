import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import spectrogram

fs=96000
window_L=4096

def softmax(z):
    exp_z = np.exp(z - np.max(z))
    return exp_z / np.sum(exp_z)

def compute_spectrogram(data, fs=fs, window_L=window_L):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    return frequencies, times, Sxx

def apply_spectrogram(row, column_name):
    f,t,Sxx = compute_spectrogram(row[column_name], fs=fs)
    return Sxx

df_hrtf = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/HRTF.pkl")
df_hrtf = df_hrtf[df_hrtf['az'] == 100]
# print(df_hrtf.head()); df_hrtf.info()

hrtf_L_arr = np.stack(df_hrtf['HRTF_L']) 
# print(hrtf_L_arr.shape)

df = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl")
df = df[df['az'] == 100] #pick out only straight ahe
# print(df.head()); df.info()



#normalize all raw signals

signal_choices = ['whitenoise', 'primes', 'birds', 'fire', 'music']
# for sig in signal_choices:
#     df[sig+'_L'] = df.apply(lambda row: [r / (2 ** 15) for r in row[sig+'_L']], axis=1)
#     df[sig+'_R'] = df.apply(lambda row: [r / (2 ** 15) for r in row[sig+'_R']], axis=1)

df['whitenoise_L'] = [l/(2**15) for l in df['whitenoise_L']] 
df['whitenoise_R'] = [l/(2**15) for l in df['whitenoise_R']] 
df['primes_L'] = [l/(2**15) for l in df['primes_L']] 
df['primes_R'] = [l/(2**15) for l in df['primes_R']] 
df['birds_L'] = [l/(2**15) for l in df['birds_L']] 
df['birds_R'] = [l/(2**15) for l in df['birds_R']] 
df['fire_L'] = [l/(2**15) for l in df['fire_L']] 
df['fire_R'] = [l/(2**15) for l in df['fire_R']] 
df['music_L'] = [l/(2**15) for l in df['music_L']] 
df['music_R'] = [l/(2**15) for l in df['music_R']] 
print(df.head()); df.info()


# take spectrogram of all
signal_columns = ['whitenoise_L', 'whitenoise_R', 'primes_L', 'primes_R', 'birds_L', 'birds_R']#], 'fire_L', 'fire_R']
for sig in signal_choices:
    df[sig+'_L'] = df.apply(lambda row: apply_spectrogram(row, sig+'_L'), axis=1)
    df[sig+'_R'] = df.apply(lambda row: apply_spectrogram(row, sig+'_R'), axis=1)

print("done with data preprociing")
# print(df.head()); df.info()
# print(df['whitenoise_L'].iloc[0])
# print(df['whitenoise_L'].iloc[0].shape[1])
# print(type(df['whitenoise_L']))

num_pos = 51

f=np.linspace(0,fs/2,window_L//2)
el=np.array([e for e in df['el']])
tidx = [t for t in range(0,df['whitenoise_L'].iloc[0].shape[1])]
n_time_slices=10
num_iters=1000
el_truth=np.zeros(num_iters)
similarity = np.zeros((num_iters,n_time_slices,num_pos))
for i in range(0,num_iters):
    rand_signal_str = np.random.choice(signal_choices)
    rand_az_idx = 100
    rand_el_idx = np.random.randint(num_pos)
    el_truth[i]=df_hrtf['el'].iloc[rand_el_idx]
    random_time_indices = np.random.choice(tidx)
    rand_windows_L = df[rand_signal_str+'_L'].iloc[rand_el_idx][:,random_time_indices]
    rand_windows_R = df[rand_signal_str+'_R'].iloc[rand_el_idx][:,random_time_indices]
    for el_idx in range(0,num_pos):
        hrtf_L = df_hrtf['HRTF_L'].iloc[el_idx]
        hrtf_R = df_hrtf['HRTF_R'].iloc[el_idx]
        for t in range(0,n_time_slices):
        # print(f"lengths HRTF: {len(hrtf_R)} and {len(hrtf_R)}\nlengths of time slice spectrum: {len(rand_window_R)} and {len(rand_window_R)} ")
            x_L = hrtf_L*rand_windows_R[t]
            x_R = hrtf_R*rand_windows_L[t]
            similarity[i,t,el_idx] = np.linalg.norm(x_L - x_R)
        # similarity[i,el_idx] = softmax(np.linalg.norm(x_L - x_R))
similarity=softmax(np.mean(similarity,axis=1)) #average accross time slices axis

print(similarity)
print(softmax(np.array([1,2,3])).sum())
print(np.sum(similarity,axis=1))
err=np.zeros(num_iters)
plt.subplot(2,1,1)
for i in range(num_iters):
    max_idx = np.argmax(similarity[i,:])
    err[i]=(el[max_idx]-el_truth[i])
    # plt.plot(el,similarity[i,:], label=el_truth[i])
    # plt.plox1t([el_truth[i], el_truth[i]], [similarity[i,:].min(), similarity[i,:].max()])
    # plt.scatter(el[max_idx],similarity[i,max_idx])
# plt.title(f"Similarirty for random slice data: Signal={rand_signal_str}\n angle=({rand_az_idx},{rand_el_idx})\n time idx = {rand_time_idx}")
# plt.legend()
bias=50
# err[err < -100] += 150
plt.subplot(2,1,2)
plt.hist(err,bins=25)
plt.xlabel("elevation error (degrees)")

plt.show()


    # row_for_rand_ang = df.sample(n=1)
    # rand_signal_str = np.random.choice(signal_choices)
    # spec_L = row_for_rand_ang[rand_signal_str+'_L']
    # spec_R = row_for_rand_ang[rand_signal_str+'_R']
    # rand_time_idx = np.random.randint(0, spec_L.shape[1])
    # frame_L = spec_L[:,rand_time_idx] # Get the random 2049-length vector



# hrtf_matrix = np.random.rand(51, 2049)  # Simulated HRTF data (51 rows, 2049 columns)
# spectrogram_matrix = np.random.rand(2049, 233)  # Simulated spectrogram data (2049 rows, 233 columns)

# # Reshape HRTF matrix for broadcasting
# hrtf_matrix_reshaped = hrtf_matrix[:, np.newaxis, :]  # Shape (51, 1, 2049)

# # Broadcast and multiply
# result = hrtf_matrix_reshaped * spectrogram_matrix  # Result shape (51, 233, 2049)