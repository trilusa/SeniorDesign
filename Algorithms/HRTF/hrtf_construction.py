import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, freqz

# Set parameters
fft_len = 4096
np.random.seed(0)

# Generate Gaussian white noise
white_noise = np.random.normal(0, 1, (fft_len,58))
impulse = np.array([1]+[0]*4095)
# Design a low-pass filter - Butterworth in this example
order = 6
cutoff_frequency = 0.25  # Cutoff frequency as a fraction of the Nyquist rate
b, a = butter(order, cutoff_frequency, btype='low', analog=False)

# Apply the filter to the white noise
filtered_noise = filtfilt(b, a, white_noise)
filtered_noise=np.mean(filtered_noise,axis=1)
filtered_impulse = filtfilt(b, a, impulse)
# Compute the FFT of the filtered noise
filtered_noise_fft = np.fft.fft(filtered_noise, n=fft_len)

filtered_impulse_fft = np.fft.fft(filtered_impulse, n=fft_len)
# Calculate the magnitude response of the filtered noise
filtered_noise_magnitude = np.abs(filtered_noise_fft)
filtered_impulse_magnitude = np.abs(filtered_impulse_fft)

# Compute the IFFT to estimate the impulse response
estimated_noise_impulse_response = np.fft.ifft(filtered_noise_fft).real
estimated_impulse_impulse_response = np.fft.ifft(filtered_impulse_fft).real

# # # Use the estimated impulse response to calculate its FFT magnitude response
# impulse_response_fft = np.fft.fft(estimated_noise_impulse_response, n=fft_len)
# impulse_response_magnitude = np.abs(impulse_response_fft)

# Plotting
plt.figure(figsize=(14, 10))

# Plot filtered noise spectrum
plt.subplot(3, 1, 1)
plt.plot(filtered_noise_magnitude[:fft_len//2],label="noise")
plt.plot(filtered_impulse_magnitude[:fft_len//2],label="pulse")
plt.title('Magnitude Response of Filtered Noise and Pulse')
plt.ylabel('Magnitude')
plt.legend()
# Plot estimated impulse response
plt.subplot(3, 1, 2)
plt.plot(estimated_noise_impulse_response,label="noise")
plt.plot(estimated_impulse_impulse_response,label="pulse")

plt.title('Estimated Impulse Response')
plt.ylabel('Amplitude')
plt.legend()

# # Plot magnitude response from estimated impulse response
# plt.subplot(3, 1, 3)
# plt.plot(impulse_response_magnitude[:fft_len//2])
# plt.title('Magnitude Response from Estimated Impulse Response')
# plt.xlabel('Frequency Bin')
# plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()
