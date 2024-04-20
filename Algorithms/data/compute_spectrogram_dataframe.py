import pandas as pd
import numpy as np
from scipy.signal import spectrogram

i=0
def compute_spectrogram(data, fs, window_L=4096):
    data=data/(2**15) #normalize
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=window_L, noverlap=window_L//2, nfft=window_L, scaling='density')
    # global i; print(f"{i} ", end=''); i=i+1
    return Sxx

def print_df(d,name="DATAFRAME"):
    print(f"\n********** {name} ***********\n"); d.info(); print(d); print("\n")

df = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl")
print_df(df)

# df['signal'] = df['signal'].apply(lambda x: x / (2**15))#normalize
num_batches = 10  # You can adjust this number based on your system's memory
batches = np.array_split(df, num_batches)

results = []
for batch in batches:
    batch['spectrogram'] = batch.apply(lambda row: compute_spectrogram(row['signal'], row['sample_rate']), axis=1)
    results.append(batch)
    print_df(batch)  # Optional: to check the output of each batch

# Concatenate all processed batches back into a single DataFrame
df_concatenated = pd.concat(results)
# # df['spectrogram'] = df.apply(lambda row: compute_spectrogram(row['signal'], row['sample_rate']), axis=1)
# pd.to_pickle(df, "spectrograms.pkl")
print_df(df)
