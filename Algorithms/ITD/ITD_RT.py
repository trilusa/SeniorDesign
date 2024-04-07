import pyaudio
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

CHUNK = 2048
FORMAT = pyaudio.paInt16
max_val = 2**15 #max value of paInt16
CHANNELS = 2  # Stereo
RATE = 96000  # Sample rate
RECORD_SECONDS = 6
frames = []
L=[]
R=[]
corr = []
samp_delay_estimates_per_frame = []

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

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

#Begine offline processing
#read, de-interleave, cast to float, normalize, and concatenate to 1D signal for Left and Right
for i in range(int(RATE / CHUNK * 1),len(frames)):
    audio_data = np.frombuffer(frames[i], dtype=np.int16)
    left_channel = audio_data[0::2]  # Take every second element starting from 0
    right_channel = audio_data[1::2]  # Take every second element starting from 1
    left_channel_float = left_channel.astype(np.float32)
    right_channel_float = right_channel.astype(np.float32)
    left_channel_normalized = left_channel_float / max_val
    right_channel_normalized = right_channel_float / max_val
    L.append(left_channel_normalized)
    R.append(right_channel_normalized)
L = np.concatenate(L)
R = np.concatenate(R)

#compute correlation and spectrog (Left and Right channels) for overlapping segments
segment_length = CHUNK
overlap = CHUNK/2
step = segment_length - overlap
num_segments = int(np.ceil((len(L) - overlap) / step))
spectrogramL = np.zeros((int(segment_length / 2 + 1), num_segments))
spectrogramR = np.zeros((int(segment_length / 2 + 1), num_segments))
for i in range(num_segments):
    #read segment
    start = int(i * step)
    end = int(start + segment_length)
    segmentL = L[start:end]
    segmentR = R[start:end]
    
    # only run if there is significant signal power
    detected, power = signal_detector(segmentL, thresh=.00)
    if(detected):
        # zero pad if necessary
        if len(segmentL) < segment_length:
            segmentL  = np.pad(segmentL, (0, segment_length - len(segmentL)), 'constant')
        if len(segmentR) < segment_length:
            segmentR  = np.pad(segmentR, (0, segment_length - len(segmentR)), 'constant')
        
        #apply hamming window
        windowed_segmentL = segmentL * np.hamming(segment_length)
        windowed_segmentR = segmentR * np.hamming(segment_length)

        #compute and construct the spectrogram
        fft_resultL = np.fft.rfft(windowed_segmentL)
        fft_resultR = np.fft.rfft(windowed_segmentR)
        power_spectrumL = np.abs(fft_resultL) ** 2
        power_spectrumR = np.abs(fft_resultR) ** 2
        spectrogramL[:, i] = power_spectrumL
        spectrogramR[:, i] = power_spectrumR

        #compute the correlation of the two signals
        frame_corr = signal.correlate(segmentL, segmentR, mode='same') / len(segmentL)
        corr.append(frame_corr)
        
        #use argmax to estimate the relative delay in this sampple
        samp_delay_estimates_per_frame.append(np.argmax(frame_corr)-CHUNK/2)

        # corr_freq = np.multiply(np.conjugate(fft_resultL), fft_resultR)
        # corr[:,i] = np.fft.ifft(corr_freq)

#construct the freq and time axist for spectrograms
freqs = np.fft.rfftfreq(segment_length, 1/RATE)
times = np.arange(num_segments) * step / RATE

# corr_mean = np.mean(corr,axis=0)
#filter outliers
samp_delay_estimates_per_frame_filtered = [x for x in samp_delay_estimates_per_frame if np.abs(x) < 80]
samp_delay_est = np.mean(samp_delay_estimates_per_frame_filtered)
sec_delay_est = samp_delay_est / RATE
meter_delay_est = sec_delay_est * 343.0 #assume speed of sound
cm_delay_est = meter_delay_est*100

print(f"Delay estimes per frame:\n{samp_delay_estimates_per_frame}")
print(f"Estimated Delay: {samp_delay_est}samples, {sec_delay_est*1e6}us, {cm_delay_est}cm, {num_segments} segments")

#Plotting
r=6
c=1
plt.figure(figsize=(16,12))
plt.subplot(r,c,1)
xlim=len(L)
plt.plot(L[:xlim], label="left")
plt.plot(R[:xlim], label="Right")
plt.legend(loc='right')
plt.title(f"Audio Recording for {len(R)/RATE} seconds ({len(R)} samples).")
plt.xlabel('Sample Number')
plt.ylabel('Amplitude')

#plot all correlations
plt.subplot(r,c,2)
for i in range(0,len(corr)):
    plt.plot(range(-CHUNK//2, CHUNK//2),corr[i])

plt.subplot(r,c,3)
plt.title(f"Correlation. sample delay estimate={samp_delay_est} samples, distance = {cm_delay_est}cm")
# plt.plot(range(-CHUNK//2, CHUNK//2),corr_mean)
plt.hist(samp_delay_estimates_per_frame, bins=CHUNK, range=(-80,80))

plt.subplot(r,c,4)
plt.pcolormesh(times, freqs, 10 * np.log10(spectrogramL), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram Left')
plt.colorbar(label='Intensity [AU]')

plt.subplot(r,c,5)
plt.pcolormesh(times, freqs, 10 * np.log10(spectrogramR), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram Right')
plt.colorbar(label='Intensity [AU]')

plt.show()



# wf = wave.open(OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(frames)
# wf.close()

# print(f"* Stereo audio saved as {OUTPUT_FILENAME}")