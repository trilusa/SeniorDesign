import numpy as np
import wave

# Constants
sample_rate = 96000  # 96 kHz
duration = 20
# duration = 2**20 / sample_rate  # Calculate duration to get exactly 2^19 samples
num_samples = int(duration * sample_rate)

# Generate white noise using a Gaussian distribution
white_noise = np.random.normal(0, 1, num_samples)

# Normalize the white noise to the maximum 16-bit integer range
normalized_noise = np.int16(white_noise / np.max(np.abs(white_noise)) * 32767)

# Set up parameters for the WAV file
file_name = "/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav"
num_channels = 1
sampwidth = 2  # 2 bytes per sample (16 bits per sample)

# Create a WAV file
with wave.open(file_name, 'w') as wav_file:
    wav_file.setparams((num_channels, sampwidth, sample_rate, num_samples, 'NONE', 'not compressed'))
    wav_file.writeframes(normalized_noise.tobytes())

print(f"Generated white noise WAV file with {num_samples} samples at {sample_rate} Hz ({duration}s)")
