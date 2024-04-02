import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo

RATE = 48000  # Sample rate
RECORD_SECONDS = 5
OUTPUT_FILENAME = "stereo_recording.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Recording stereo audio...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* Finished recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"* Stereo audio saved as {OUTPUT_FILENAME}")

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
    # max_val = max(left_channel_float.max(), right_channel_float.max(), key=abs)
    left_channel_normalized = left_channel_float / (2**15)
    right_channel_normalized = right_channel_float / (2**15)
    L.append(left_channel_normalized)
    R.append(right_channel_normalized)
L=np.concatenate(L)
R=np.concatenate(R)
r=2
c=1
plt.figure(figsize=(10,4))
plt.subplot(r,c,1)
plt.plot(L, label="L")
plt.plot(R, label="R")
plt.legend()

plt.subplot(r,c,2)

plt.xlabel('Sample Number')
plt.ylabel('Amplitude')


plt.title(f"Audio Recording for {len(R)/RATE} seconds ({len(R)} samples)")
plt.show()