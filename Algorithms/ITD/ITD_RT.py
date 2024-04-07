import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import cProfile
import pstats

CHUNK = 2**11
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo

RATE = 96000  # Sample rate
RECORD_SECONDS = 6
OUTPUT_FILENAME = "stereo_recording.wav"

def signal_detector(signal, thresh=1):
    pwr = np.mean(np.square(signal))
    return pwr > thresh, pwr


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Recording stereo audio...")

frames = []
corr = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* Finished recording")

stream.stop_stream()
stream.close()
p.terminate()

# pr = cProfile.Profile()
# pr.enable()  # Start collecting profiling data
L=[]
R=[]
#offline processing
# frames = b''.join(frames)
for i in range(int(RATE / CHUNK * 1),len(frames)):
    audio_data = np.frombuffer(frames[i], dtype=np.int16)
    left_channel = audio_data[0::2]  # Take every second element starting from 0
    right_channel = audio_data[1::2]  # Take every second element starting from 1
    left_channel_float = left_channel.astype(np.float32)
    right_channel_float = right_channel.astype(np.float32)

    # Normalize the channels to the range [-1, 1] by dividing by the max absolute value
    # This prevents potential overflow issues during correlation
    max_val = 2**15
    left_channel_normalized = left_channel_float / max_val
    right_channel_normalized = right_channel_float / max_val
    L.append(left_channel_normalized)
    R.append(right_channel_normalized)
    detected, power = signal_detector(left_channel_normalized, thresh=.01)
    if(detected):
        print(detected, power)
        L.append(left_channel_normalized)
        R.append(right_channel_normalized)
        corr.append(
            signal.correlate(left_channel_normalized, right_channel_normalized, mode='same') / len(left_channel_normalized)
        )
L = np.concatenate(L)
R = np.concatenate(R)

segment_length = CHUNK
overlap = CHUNK/2
step = segment_length - overlap
num_segments = int(np.ceil((len(L) - overlap) / step))
spectrogram = np.zeros((int(segment_length / 2 + 1), num_segments))

for i in range(num_segments):
    start = int(i * step)
    end = int(start + segment_length)
    segment = L[start:end]
    if len(segment) < segment_length:
        segment  = np.pad(segment, (0, segment_length - len(segment)), 'constant')
    windowed_segment = segment * np.hamming(segment_length)
    fft_result = np.fft.rfft(windowed_segment)
    power_spectrum = np.abs(fft_result) ** 2
    spectrogram[:, i] = power_spectrum
freqs = np.fft.rfftfreq(segment_length, 1/RATE)
times = np.arange(num_segments) * step / RATE

    # Perform correlation
    
# print(len(corr))
corr_mean = np.mean(corr,axis=0)
samp_delay_est = np.argmax(corr_mean)-CHUNK/2
sec_delay_est = samp_delay_est / RATE
meter_delay_est = sec_delay_est * 343.0 #assume speed of sound
cm_delay_est = meter_delay_est*100
print(len(corr), corr_mean)
print(f"{samp_delay_est}samples, {sec_delay_est*1e6}us, {cm_delay_est}cm")


# pr.disable()  # Stop collecting profiling data
# ps = pstats.Stats(pr).sort_stats('cumulative')  # Create Stats object
# ps.print_stats()  # Print the statistics

#Plotting
r=4
c=1
plt.figure(figsize=(16,12))
plt.subplot(r,c,1)
plt.plot(L, label="left")
plt.plot(R, label="Right")
plt.legend(loc='right')
# plt.subplot(r,c,2)
plt.title(f"Audio Recording for {len(R)/RATE} seconds ({len(R)} samples)")
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')

plt.subplot(r,c,2)
for i in range(0,len(corr)):
    plt.plot(range(-CHUNK//2, CHUNK//2),corr[i])

plt.subplot(r,c,3)
plt.title(f"Correlation. sample delay estimate={samp_delay_est} samples, distance = {cm_delay_est}cm")
plt.plot(range(-CHUNK//2, CHUNK//2),corr_mean)

plt.subplot(r,c,4)
plt.pcolormesh(times, freqs, 10 * np.log10(spectrogram), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram')
plt.colorbar(label='Intensity [AU]')
plt.show()

# wf = wave.open(OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(frames)
# wf.close()

# print(f"* Stereo audio saved as {OUTPUT_FILENAME}")