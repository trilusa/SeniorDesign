import pickle
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from pickle file
data = []
fn="raw_whitenoise_data_test.pkl"
with open(fn, 'rb') as file:
    while True:
        try:
            data.append(pickle.load(file))
        except EOFError:
            break
print(len(data))
print(data[1][2])

L = [line[0] for line in  data]
R = [line[1] for line in  data]
L_norm = [l/32767 for l in L]
R_norm = [r/32767 for r in R]

az = [line[2][0] for line in  data]
el = [line[2][1] for line in  data]
sample_rate = [line[3] for line in data]
sound_type = ["WHITE_NOISE" for _ in data]

df = pd.DataFrame({
    "L": L,  # Wrap arrays in a list to store as array objects in a single dataframe row
    "R": R,
    # "L_norm": L_norm,
    # "R_norm": R_norm,
    "az": az,
    "el": el,
    "sound_type": sound_type,
    "sample_rate": sample_rate
})

print(df)
df.to_pickle('white_noise_test_df.pkl')
