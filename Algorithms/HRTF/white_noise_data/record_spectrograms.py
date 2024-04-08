import time
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import spectrogram
import serial
import threading


def compute_spectrogram(data, fs):
    frequencies, times, Sxx = spectrogram(data, fs=fs, window='hamming',
                                          nperseg=1024, noverlap=512, nfft=1024, scaling='density')
    return frequencies, times, Sxx

def plot_spectrogram(t,f,Sxx,title="",xlabel=False,ylabel=False):
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    if(ylabel):
        plt.ylabel('Frequency [Hz]')
    if(xlabel):
        plt.xlabel('Time [sec]')
    plt.title(title)
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(0, 22000)  # Limit frequency to human hearing frequency

def send_angle_thread(ser, angle):
    print("sending angles")
    angles_str = ','.join(str(a) for a in angle)
    print(angles_str)
    ser.write((angles_str + '\n').encode())
    ser.flush()
    print("angles_sent")
    time.sleep(2)
    
def record_thread(record_duration, sample_rate, output_buf):
    recording = sd.rec(int(record_duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    print("recording started")
    time.sleep(record_duration+.5)
    output_buf.append(recording)
    print("Recording written to buffer")

def play_thread(data,sample_rate):
    print("Wav file is playing")
    sd.play(data, sample_rate)
    sd.wait()  # Wait until recording is finished
    print("Wave file finished")

print("Script Began")
# Connect to arduino
ser = serial.Serial('/dev/ttyACM2', 9600)  # Change '/dev/ttyACM0' to your Arduino's port
ser.flush()
time.sleep(1)

# Parameters
file_name = "/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav"
wav_sample_rate, wav_signal = wavfile.read(file_name)

sample_rate = 96000
dead_time = 1.5 #amount of time to cuttof the front 
dead_samples = int(dead_time * sample_rate)
record_duration = 2.5+dead_time
N = record_duration * sample_rate

print(f"N samples={N} (2**{np.log2(N)}) samples\n duration={record_duration}\n sample_rate={sample_rate}")


#shared variables
angle=(90,85)
shared_recording = []


arduino = threading.Thread(target=send_angle_thread, args=(ser,angle))
record = threading.Thread(target=record_thread, args=(record_duration,sample_rate, shared_recording))
play = threading.Thread(target=play_thread,args=(wav_signal,wav_sample_rate))

play.start()
arduino.start()
record.start()

# Wait for recording and send angle threads to complete
arduino.join()
record.join()
play.join()

recording = shared_recording[0] if shared_recording else None

if recording is None:
    raise TypeError

print(type(recording), recording[:,0].shape) 
#cuttoff the first ~1.36 second (2^17 samples), this is a work around
 
L = recording[dead_samples:,0]
R = recording[dead_samples:,1]

print(f"L len;{L.shape}, R len: {R.shape}")

f, t, Sxx_left = compute_spectrogram(L,sample_rate)
f, t, Sxx_right = compute_spectrogram(R,sample_rate)

HRTF_left = np.mean(Sxx_left,axis=1)
HRTF_right= np.mean(Sxx_right,axis=1)


print(f"Sxx shape={Sxx_left.shape}\tHRTF shape={HRTF_left.shape}")
# np.savez('combined_spectrograms.npz', f=f, t=t,
#          Sxx_left=Sxx_left, Sxx_right=Sxx_right, Sxx_noise=Sxx_noise)

plt.figure(figsize=(10, 6))
r=3
c=2
plt.subplot(r,c,1)
plot_spectrogram(t,f,Sxx_left, f'Spectrogram of Right Channel, (az={angle[0]},el={angle[1]}',xlabel=False,ylabel=True)
plt.subplot(r,c,3)
plot_spectrogram(t,f,Sxx_right, f'Spectrogram of Left Channel, (az={angle[0]},el={angle[1]}', xlabel=True,ylabel=True)

plt.subplot(r,c,5)
plt.plot(f,HRTF_left, label='L')
plt.plot(f,HRTF_right, label="R")
plt.legend()
plt.show()
