import threading
import sounddevice as sd
import numpy as np
import wave

class ThreadedAudioPlayer(threading.Thread):
    def __init__(self, file_path):
        super(ThreadedAudioPlayer, self).__init__()
        self.file_path = file_path
        self.running = True
        print("Audio Player Initialized")

    def run(self):
        data, samplerate = self.load_wave_file()
        # Loop while 'running' is True
        while self.running:
            print("Wave playing")
            sd.play(data, samplerate)
            sd.wait()  # Wait for the playback to finish
            print("Wave done playing")
            

    def stop(self):
        print("Player stopping")
        self.running = False
        sd.stop()
        print("Player stopped")


    def load_wave_file(self):
        with wave.open(self.file_path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            data = np.frombuffer(frames, dtype=np.int16)
            samplerate = wf.getframerate()
        return data, samplerate

# Usage
if __name__ == "__main__":
    audio_file_path = '/home/adrian/Documents/SeniorDesign/BinauralHearingProcessing/SeniorDesign/Algorithms/HRTF/white_noise_data/white_noise.wav'  # Change this to your audio file path
    player = ThreadedAudioPlayer(audio_file_path)
    player.start()  # Start the thread
    input("Press Enter to stop playback\n")
    player.stop()  # Stop the thread
    player.join()  # Wait for thread to finish
