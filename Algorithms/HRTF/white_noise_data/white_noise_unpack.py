import pickle
import numpy as np
import pandas as pd
import time

# Load data from pickle file
t0=time.time()
print(t0)
data = []
fn= "raw_whitenoise_data_az15deg_el2deg"
fn_in=fn+".pkl"
with open(fn_in, 'rb') as file:
    while True:
        try:
            data.append(pickle.load(file))
        except EOFError:
            break
print(len(data))
print(data[1][2])

L = [np.array(line[0])/(2**15) for line in  data]
R = [np.array(line[1])/(2**15) for line in  data]

# R = [line[1] for line in  data]
print(len(L))
# L_norm = np.array(L)/(2**15)
# R_norm = np.array(R)/(2**15)
# print(len(L_norm))

az = [line[2][0] for line in  data]
el = [line[2][1] for line in  data]
sample_rate = [line[3] for line in data]
# sound_type = ["WHITE_NOISE" for _ in data]

df = pd.DataFrame({
    "L": L,
    "R": R,
    "az": az,
    "el": el,
    # "sound_type": sound_type,
    "sample_rate": sample_rate
})

print(df)
df.info()
print(f"Elapsed: {time.time()-t0} sec")
df.to_pickle(fn+"_df.pkl")
