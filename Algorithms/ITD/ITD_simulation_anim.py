%matplotlib qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
N = 2**10
fs = 96000
ts = 1 / fs
f0 = 6000.0
t = np.linspace(0.0, N * ts, N, endpoint=False)
phases = np.linspace(0, 2 * np.pi, 100)  # Sweep through 0 to 2*pi
# Function to update the plots for each frame
def update(phi):
    xt = np.sin(f0 * 2.0 * np.pi * t + phi)*np.blackman_harris(N)
    xf = np.fft.fft(xt)
    f = np.fft.fftfreq(N, ts)
    f=np.linspace(0,fs,N,endpoint=False)

    angle = np.angle(xf)
    mag=np.abs(xf)/N
    # Clear previous plots
    plt.clf()
    
    # Time domain signal
    plt.subplot(3, 2, 1)
    plt.plot(t, xt)
    plt.title(f'Time Domain Signal\nInitial Phase = {phi:.2f} radians')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    
    # Magnitude Spectrum
    plt.subplot(3, 2, 3)
    plt.plot(f,mag)
    plt.title('Magnitude Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid()
    
    # Phase Spectrum
    plt.subplot(3, 2, 5)
    plt.plot(f,angle)
    plt.title('Phase Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Radians)')
    plt.grid()

    # Complex plane representation
    plt.subplot(1, 2, 2)
    plt.scatter(xf.real/N, xf.imag/N,s=25)
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.axis('square')  # Make sure the plot is square
    plt.xlim((-1,1))
    plt.ylim((-1,1))
    plt.title('Complex Plane Representation')
    plt.grid()

    # Mark the beginning and end of the FFT curve
    plt.scatter(xf.real[0], xf.imag[0], color='green', marker='s', s=50)
    plt.scatter(xf.real[-1], xf.imag[-1], color='red', marker='s', s=50)

# Create the animation
fig = plt.figure(figsize=(12, 8))  # Adjust the figure size as needed
ani = FuncAnimation(fig, update, phases, interval=100)

plt.show()
