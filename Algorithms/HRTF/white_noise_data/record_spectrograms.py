import time
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.io import wavfile
from scipy.signal import spectrogram
import serial
import threading
import pickle
# from Audio.audio_player import ThreadedAudioPlayer
# Parameters
# file_name = "/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav"
# wav_sample_rate, wav_signal = wavfile.read(file_name)

sample_rate = 96000
dead_time = 1.5 #amount of time to cuttof the front 
dead_samples = int(dead_time * sample_rate)
record_duration = 5+dead_time
N = int(record_duration * sample_rate)
pickle_name = 'raw_numbers_data_az15deg_el2deg.pkl'
angles= [(az, el) for az in range(10, 191, 15) for el in range(50, 151, 2)]
print(len(angles))
def send_angle_thread(ser, angles, ok_to_send_angle_event, ok_to_record_event):
    print("send_angle_thread: started")
    ser.write(('90,90\n').encode()) #set to 90.90
    ser.flush()
    time.sleep(3)
    for angle in angles:
        # print("send_angle_thread: waiting")
        ok_to_send_angle_event.wait()
        ok_to_send_angle_event.clear()
        # print("send_angle_thread: done waiting")
        angles_str = ','.join(str(a) for a in angle)
        print(f"send_angle_thread: sending angles ({angles_str})")
        ser.write((angles_str + '\n').encode())
        ser.flush()
        time.sleep(.3) #wait to move and settle
        # print("angles_sent")
        # if angle is not angles[-1]: # is it not the last angle?
        ok_to_record_event.set()
        # else:
        #     stop_event.set()
    print("send_angle_thread: done")

def record_thread(record_duration, sample_rate, output_buf, ok_to_send_angle_event, ok_to_record_event, angles):
    # while not stop_event.is_set():
    print("record_thread: started")
    for angle in angles:
        # print("record_thread: waiting")
        ok_to_record_event.wait()
        ok_to_record_event.clear()
        # print("record_thread: done waiting")
        recording = sd.rec(int(record_duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
        print("record_thread: recording started")
        time.sleep(record_duration+.5)
        # output_buf.append(recording)
        print(f"record_thread: Angle {angle} completed")
        # print("record_thread: Recording written to buffer")
        # compute_and_save_HRTF(recording, sample_rate, angle)
        L = recording[dead_samples:,0]
        R = recording[dead_samples:,1]
        ok_to_send_angle_event.set()
        with open(pickle_name, 'ab') as file:
            pickle.dump((L,R,angle,sample_rate),file)
            print(f" L and R channels to {pickle_name} ({len(L)} samples @ {sample_rate}hz)")
    print("record_thread: done")

# def compute_and_save_HRTF(recording, sample_rate, angle):
#         dead_time = 1.5 #amount of time to cuttof the front 
#         dead_samples = int(dead_time * sample_rate)
#         L = recording[dead_samples:,0]
#         R = recording[dead_samples:,1]
#         print(f"L len;{L.shape}, R len: {R.shape}")
#         f, t, Sxx_left = compute_spectrogram(L,sample_rate)
#         f, t, Sxx_right = compute_spectrogram(R,sample_rate)
#         HRTF_left = np.mean(Sxx_left,axis=1)
#         HRTF_right= np.mean(Sxx_right,axis=1)
#         pickle.dump((HRTF_left, HRTF_right, angle), file)
        # pickle.dump((L,R,angle,sample_rate),file)
        # print(f"Succesfully saved L and R channels to {pickle_name} ({len(L)} samples @ {sample_rate}hz)")


# def play_thread(data,sample_rate):
#     # while True:
#     sd.play(data, sample_rate)
#     print("Wav is playing")
#     sd.wait() # Wait until recording is finished

    # print("Wave file finished")

print("Script Began")
t0=time.time()
# Connect to arduino
ser = serial.Serial('/dev/ttyACM0', 9600)  # Change '/dev/ttyACM0' to your Arduino's port
ser.flush()
time.sleep(1)

print(f"N samples={N} (2**{np.log2(N)}) samples\n duration={record_duration}\n sample_rate={sample_rate}")

#shared variables
shared_recording = []
ok_to_send_angle_event = threading.Event()
ok_to_record_event = threading.Event()
# stop_event = threading.Event()
# stop_event.clear()
ok_to_record_event.clear()
ok_to_send_angle_event.set()

# player = ThreadedAudioPlayer(file_name)


arduino = threading.Thread(target=send_angle_thread, args=(ser,angles,ok_to_send_angle_event, ok_to_record_event))
record = threading.Thread(target=record_thread, args=(
    record_duration,sample_rate, shared_recording, ok_to_send_angle_event, ok_to_record_event, angles))
# player = threading.Thread(target=play_thread,args=(wav_signal, wav_sample_rate))

# player.start()
arduino.start()

time.sleep(20)
record.start()
# player.start()

# Wait for recording and send angle threads to complete
arduino.join()
record.join()
# player.join()
t1=time.time()

repeat_char = 10098 * '\u2588'
print('\033[32m' + f"{repeat_char}" + '\033[m')
print(f"Runtime: {(t1-t0)/60} min")

'''
recording = shared_recording#[0] if shared_recording else None

if recording is None:
    raise TypeError
plt.figure(figsize=(10, 6))
r=3
c=2
print(type(shared_recording), len(shared_recording))#, recording[:,0].shape) 
#cuttoff the first ~1.36 second (2^17 samples), this is a work around
# for i in range(len(shared_recording)):
i=0
recording = shared_recording[i]
L = recording[dead_samples:,0]
R = recording[dead_samples:,1]

print(f"L len;{L.shape}, R len: {R.shape}")

f, t, Sxx_left = compute_spectrogram(L,sample_rate)
f, t, Sxx_right = compute_spectrogram(R,sample_rate)

HRTF_left = np.mean(Sxx_left,axis=1)
HRTF_right= np.mean(Sxx_right,axis=1)


print(f"Sxx shape={Sxx_left.shape}\tHRTF shape={HRTF_left.shape}")

plt.subplot(r,c,i+1)
plot_spectrogram(t,f,Sxx_left, f'Spectrogram of Right Channel, (az={angles[i][0]},el={angles[i][1]}',xlabel=False,ylabel=True)
plt.subplot(r,c,i+3)
plot_spectrogram(t,f,Sxx_right, f'Spectrogram of Left Channel', xlabel=True,ylabel=True)

plt.subplot(r,c,i+5)
plt.plot(f,HRTF_left, label='L')
plt.plot(f,HRTF_right, label="R")
plt.xlim(0,15000)
plt.legend()
plt.show()
'''