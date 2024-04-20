import pandas as pd
import numpy as np
import wave
import os

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

# Function to save a signal to a WAV file
def save_wave(filename, signal, sample_rate):
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(np.array(signal, dtype=np.int16).tobytes())  # Convert the signal to bytes

df = pd.read_pickle("/Users/adrian/Documents/Senior Design/SeniorDesign/Algorithms/data/raw_recordings.pkl")

# Iterate over each row in the dataframe
for index, row in df.iterrows():
    output_dir = f"wav/{row['sound_type']}"
    ensure_dir(output_dir)
    filename = f"{output_dir}/az{row['az']}_el{row['el']}_{row['sound_type']}_fs{row['sample_rate']}_{row['channel']}.wav"
    save_wave(filename, row['signal'], row['sample_rate'])
