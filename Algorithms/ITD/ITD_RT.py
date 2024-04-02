import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import cProfile
import pstats

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo

RATE = 48000  # Sample rate
RECORD_SECONDS = 5
OUTPUT_FILENAME = "stereo_recording.wav"

def signal_detector(signal, thresh=100):
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

pr = cProfile.Profile()
pr.enable()  # Start collecting profiling data
L=[]
R=[]
#offline processing
# frames = b''.join(frames)
for i in range(len(frames)):
    audio_data = np.frombuffer(frames[i], dtype=np.int16)
    left_channel = audio_data[0::2]  # Take every second element starting from 0
    right_channel = audio_data[1::2]  # Take every second element starting from 1
    left_channel_float = left_channel.astype(np.float32)
    right_channel_float = right_channel.astype(np.float32)

    # Normalize the channels to the range [-1, 1] by dividing by the max absolute value
    # This prevents potential overflow issues during correlation
    max_val = max(left_channel_float.max(), right_channel_float.max(), key=abs)
    left_channel_normalized = left_channel_float / max_val
    right_channel_normalized = right_channel_float / max_val
    L.append(left_channel_normalized)
    R.append(right_channel_normalized)
    detected, power = signal_detector(left_channel_normalized)
    print(detected, power)
    # Perform correlation
    corr.append(
        signal.correlate(left_channel_normalized, right_channel_normalized, mode='same') / len(left_channel_normalized)
    )


pr.disable()  # Stop collecting profiling data
ps = pstats.Stats(pr).sort_stats('cumulative')  # Create Stats object
ps.print_stats()  # Print the statistics

#Plotting
r=3
c=1
plt.figure(figsize=(10,4))
plt.subplot(r,c,1)
plt.plot(np.concatenate(L), label="left")

plt.subplot(r,c,2)
plt.plot(np.concatenate(R), label="Right")
plt.title(f"Audio Recording for {RECORD_SECONDS} seconds")
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')

plt.subplot(r,c,3)
plt.plot(corr)
plt.show()


# wf = wave.open(OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(frames)
# wf.close()

# print(f"* Stereo audio saved as {OUTPUT_FILENAME}")