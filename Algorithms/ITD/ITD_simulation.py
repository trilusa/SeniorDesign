# %matplotlib qt

# import numpy as np
# import matplotlib.pyplot as plt

# N=2**10
# N_frames=5
# fs=96000
# ts=1/fs

# f0=6000.0
# t=np.linspace(0,N*ts,N,endpoint=False)
# t=np.tile(np.linspace(-N*ts/2,N*ts/2,N,endpoint=False), N_frames)
# print(len(t))
# xt=np.sin(f0*2.0*np.pi*t)
# xt=np.sinc(f0*t)



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
N = 2**10

T=1 #1 second recording
fp=20 #pulses per second
tp=1/fp

f0 = 1000.0 #frequency of sinc
fs = 96000
ts = 1 / fs

t0=-.002
A=.9

t=np.linspace(-T/2, T/2, T*fs, endpoint=True)
t_wrapped= t%tp - (tp/2)

t_delayed=np.linspace((-T/2)+t0, (T/2)+t0, T*fs, endpoint=True)
t_wrapped_delayed= t_delayed%tp - tp/2


print(len(t))
# xt=np.sinc(f0*t)
xt=np.sin(2*np.pi*f0*t)/(2*np.pi*f0*t_wrapped)
xt_delayed=A*np.sin(2*np.pi*f0*t_delayed)/(2*np.pi*f0*t_wrapped_delayed)  

         
# xf=np.fft.fft(xt)#[:1+N//2]
# #f = np.fft.fftfreq(N,ts)[:1+N//2]
# f=np.linspace(-fs/2,fs/2,N*N_frames)

numrow=3
numcol=1
plt.subplot(numrow, numcol, 1) # (rows, columns, panel number)
plt.plot(xt)
plt.plot(xt_delayed)
plt.plot(t_wrapped)
plt.plot(t_wrapped_delayed)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

plt.subplot(numrow, numcol, 2)
plt.plot(f,np.abs(xf)/N)
plt.grid()
plt.title('Magnitude')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')

plt.subplot(numrow, numcol, 3)
plt.plot(f,np.angle(xf))
plt.grid()
plt.title('Phase')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Rad')
plt.show()

# taus = np.linspace(0,100e-3, 100)  # Sweep through 0 to 2*pi
# # Function to update the plots for each frame
# def update(tau):
#     xt=np.sinc(f0*t)
#     xt_delay=np.sinc(f0*(t-tau))
#     xf = np.fft.fft(xt)
#     f = np.fft.fftfreq(N, ts)
#     f=np.linspace(0,fs,N,endpoint=False)

#     angle = np.angle(xf)
#     mag=np.abs(xf)/N
#     # Clear previous plots
#     plt.clf()
    
#     # Time domain signal
#     plt.subplot(3, 2, 1)
#     plt.plot(t, xt)
#     plt.ploy(t,xt_delayed)
#     plt.title(f'Time Domain Signal\nDelay = {tau*1000:.2f} ms')
#     plt.xlabel('Time (s)')
#     plt.ylabel('Amplitude')
#     plt.grid()
    
#     # Magnitude Spectrum
#     plt.subplot(3, 2, 3)
#     plt.plot(f,mag)
#     plt.title('Magnitude Spectrum')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Magnitude')
#     plt.grid()
    
#     # Phase Spectrum
#     plt.subplot(3, 2, 5)
#     plt.plot(f,angle)
#     plt.title('Phase Spectrum')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Phase (Radians)')
#     plt.grid()

#     # Complex plane representation
#     plt.subplot(1, 2, 2)
#     plt.scatter(xf.real/N, xf.imag/N,s=25)
#     plt.xlabel('Real')
#     plt.ylabel('Imaginary')
#     plt.axis('square')  # Make sure the plot is square
#     plt.xlim((-1,1))
#     plt.ylim((-1,1))
#     plt.title('Complex Plane Representation')
#     plt.grid()

#     # Mark the beginning and end of the FFT curve
#     plt.scatter(xf.real[0], xf.imag[0], color='green', marker='s', s=50)
#     plt.scatter(xf.real[-1], xf.imag[-1], color='red', marker='s', s=50)

# # Create the animation
# fig = plt.figure(figsize=(12, 8))  # Adjust the figure size as needed
# ani = FuncAnimation(fig, update, phases, interval=100)

# plt.show()
