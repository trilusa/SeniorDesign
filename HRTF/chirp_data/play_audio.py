import pyaudio
import wave

# Parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2  # Stereo
RATE = 48000  # Sample rate
WAVE_FILENAME = "stereo_recording.wav"
# WAVE_FILENAME = "chirp_f0-200-hz_f1-20000-hz_duration-1-s_fs-48000.0-hz.wav"

# Initialize PyAudio
p = pyaudio.PyAudio()

# Function to play audio
def play_audio():
    wf = wave.open(WAVE_FILENAME, 'rb')
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

play_audio()
p.terminate()
print(f'Played {WAVE_FILENAME}')

