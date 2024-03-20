import pyaudio
import wave
import threading

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo
RATE = 48000  # Sample rate
RECORD_SECONDS = 2
OUTPUT_FILENAME = "stereo_recording.wav"
WAVE_OUTPUT_FILENAME = "chirp_data/chirp_f0-200-hz_f1-20000-hz_duration-1-s_fs-48000.0-hz.wav"  # The file you want to play

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to play audio
def play_audio():
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    stream_play = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream_play.write(data)
        data = wf.readframes(CHUNK)
    stream_play.stop_stream()
    stream_play.close()

# Recording setup
frames = []
stream_record = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)




# Start recording
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    if i == 0:  # Start playback on first iter
        threading.Thread(target=play_audio).start()
    data = stream_record.read(CHUNK)
    frames.append(data)

print("* Finished recording")

# Stop and close the recording stream
stream_record.stop_stream()
stream_record.close()

# Terminate PyAudio instance
p.terminate()

# Save the recorded audio to a file
wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print(f"* Stereo audio saved as {OUTPUT_FILENAME}")
