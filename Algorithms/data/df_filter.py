import pandas as pd
import numpy as np
import time

t0=time.time()
fn="/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl"
df = pd.read_pickle(fn)
df=df.query('sound_type!="WHITE_NOISE"')
print(df)
df.info()
print(time.time()-t0)

# # Define the range for az and el according to your specifications
# az_range = range(10, 191, 5)  # Starts at 10, ends at 190, steps of 5
# el_range = range(50, 151, 10)  # Starts at 50, ends at 150, steps of 10
# labels = [(az-10-90,el-90) for az in az_range for el in el_range]
# label_dict = {label: index for index, label in enumerate(labels)}

# print(labels,len(labels))
# # Filter the DataFrame
# df = df[df['az'].isin(az_range) & df['el'].isin(el_range)]
# df['az'] = df['az']-10-90
# df['el'] = df['el']-90
# # df=df.drop(columns=['sound_type'])
# df['label_tuple'] = list(zip(df['az'], df['el']))
# df['label'] = df['label_tuple'].map(label_dict) # Map the 'label_tuple' to its corresponding index

# Display the filtered DataFrame
print(df)
# df.to_json("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings_filtered_for_training.json")
# df.to_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings_filtered_for_training.pkl")
