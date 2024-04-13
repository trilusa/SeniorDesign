import pickle
import matplotlib.pyplot as plt
import numpy as np

# Load data from pickle file
data = []
with open('hrtf_data10.pkl', 'rb') as file:
    while True:
        try:
            data.append(pickle.load(file))
        except EOFError:
            break

# Sort data by angles
data_sorted = sorted(data, key=lambda x: x[2])
angles = np.array([item[2] for item in data_sorted])

# Ensure all entries have the same size
if len(set(np.array(item[0]).shape for item in data_sorted)) != 1:
    raise ValueError("HRTFs have varying sizes, please check your data!")

hrtf_left = np.array([item[0] for item in data_sorted])
hrtf_right = np.array([item[1] for item in data_sorted])

# Constants
sample_rate = 96000  # Hz
nyquist_freq = sample_rate / 2
n_fft = hrtf_left.shape[1]  # Total number of FFT points
print(n_fft)
# Calculate the index for the Nyquist frequency (half of the sample rate)
nyquist_index = n_fft // 2

# Generate frequency bins up to the Nyquist frequency
frequencies = np.linspace(0, nyquist_freq, nyquist_index)

# Truncate HRTF data to include only frequencies up to the Nyquist frequency
hrtf_left = hrtf_left[:, :nyquist_index]
hrtf_right = hrtf_right[:, :nyquist_index]

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Heatmap for HRTF Left
cax_left = axs[0].imshow(10*np.log10(hrtf_left), aspect='auto', origin='lower', interpolation='none',
                         extent=[frequencies[0], frequencies[-1], angles.min(), angles.max()])
axs[0].set_title('HRTF Left')
axs[0].set_xlabel('Frequency (Hz)')
axs[0].set_ylabel('Elevation Angle (degrees)')
fig.colorbar(cax_left, ax=axs[0], orientation='vertical').set_label('Magnitude (dB)')

# Heatmap for HRTF Right
cax_right = axs[1].imshow(10*np.log10(hrtf_right), aspect='auto', origin='lower', interpolation='none',
                          extent=[frequencies[0], frequencies[-1], angles.min(), angles.max()])
axs[1].set_title('HRTF Right')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Elevation Angle (degrees)')
fig.colorbar(cax_right, ax=axs[1], orientation='vertical').set_label('Magnitude (dB)')

plt.tight_layout()
plt.show()
