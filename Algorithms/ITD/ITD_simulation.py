# %matplotlib qt
import time
import numpy as np
import matplotlib.pyplot as plt

t_start = time.time()


# Sample rate config
fs = 96000
ts = 1 / fs
T=.1 #1 second recording

#pulse generation constants
fp=100 #pulses per second
tp=1/fp
f0 = 10000.0 #frequency of sinc
delays=-np.arange(-0.5e-3,0.5e-3,.001e-3) #delay
A=1 #relative attenuation 

#fft config
N=2**10

# #time for pulse generation
# t=np.linspace(-T/2, T/2, T*fs, endpoint=True)
# t_wrapped= t%tp - tp/2
# t_delayed=np.linspace((-T/2)+t0, (T/2)+t0, T*fs, endpoint=True)
# t_wrapped_delayed= t_delayed%tp - tp/2
# #    return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

# #generate sinc pulse trains
# xt=np.where(t_wrapped==0, 1.0, np.sin(2*np.pi*f0*t)/(2*np.pi*f0*t_wrapped))*np.hamming(len(t))
# xt_delayed=A*np.where(t_wrapped_delayed==0, 1.0, np.sin(2*np.pi*f0*t_delayed)/(2*np.pi*f0*t_wrapped_delayed))*np.hanning(len(t))  

         
# xf=np.fft.fft(xt)
# xf_delayed=np.fft.fft(xt_delayed)
# f=np.fft.fftfreq(len(t),ts)
# # f=np.linspace(-fs/2,fs/2,len(t))

# numrow=3
# numcol=1
# plt.subplot(numrow, numcol, 1) # (rows, columns, panel number)
# plt.plot(xt)
# plt.plot(xt_delayed)
# plt.plot(t_wrapped)
# plt.plot(t_wrapped_delayed)
# plt.title('Time Domain Signal')
# plt.xlabel('Time (s)')
# plt.ylabel('Amplitude')
# plt.grid()

# plt.subplot(numrow, numcol, 2)
# plt.plot(f,np.abs(xf)/N)
# plt.plot(f,np.abs(xf_delayed)/N)
# plt.grid()
# plt.title('Magnitude')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')

# mag_thresh = .1 #gets rid of sufficiiently small conponent for plotting 
# plt.subplot(numrow, numcol, 3)
# plt.plot(f,np.angle(xf))
# plt.plot(f,np.angle(xf_delayed))
# plt.grid()
# plt.title('Phase')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Rad')
# plt.show()

# Function to update the plots for each frame


delay_est = np.zeros(len(delays))
i=0

for i in range(len(delays)):
    #time for pulse generation
    t0=delays[i]
    
    t=np.linspace(-T/2, T/2, int(T*fs), endpoint=True)
    t_wrapped= t%tp - tp/2
    t_delayed=np.linspace((-T/2)+t0, (T/2)+t0, int(T*fs), endpoint=True)
    t_wrapped_delayed= t_delayed%tp - tp/2
    #    return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

    #generate sinc pulse trains
    xt=np.where(t_wrapped==0, 1.0, np.sin(2*np.pi*f0*t)/(2*np.pi*f0*t_wrapped))*np.hamming(len(t))
    xt_delayed=A*np.where(t_wrapped_delayed==0, 1.0, 
                          np.sin(2*np.pi*f0*t_delayed)/(2*np.pi*f0*t_wrapped_delayed))*np.hamming(len(t))  

             
    xf=np.fft.fft(xt)
    xf_delayed=np.fft.fft(xt_delayed)
    f=np.fft.fftfreq(len(t),ts)
    
    cross_xf=xf*np.conj(xf_delayed)
    corr_f = np.fft.ifft(cross_xf)
    corr_t = np.correlate(xt,xt_delayed,mode='same')
     # np.argmax(np.fft.fftshift(corr_f))-len(corr_f)/2
    
    # global delay_est_samp,i
    delay_est[i]=np.argmax(np.fft.fftshift(corr_f))-len(corr_f)/2
    i += 1
    
    '''
    plt.clf()
    numrow=3
    numcol=2
    plt.subplot(numrow, numcol, 1) # (rows, columns, panel number)
    plt.plot(t,xt)
    plt.plot(t,xt_delayed)
    plt.plot(t,t_wrapped)
    plt.plot(t,t_wrapped_delayed)
    r=.02
    # plt.xlim((.17,.19))
    
    plt.title(f'Time Domain Signal\ Delay = {t0*1000:.2f} ms ({t0/ts} samples)')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    
    plt.subplot(numrow, numcol, 2)
    plt.plot(corr_t)
    plt.plot(-np.fft.fftshift(corr_f))
    plt.xlim((len(corr_f)//2-50,len(corr_f)//2-50))

    plt.title(f"Correlation, delay estimate={delay_est}samples")
    
    plt.subplot(numrow, numcol, 3)
    plt.plot(f,np.abs(xf)/N)
    plt.plot(f,np.abs(xf_delayed)/N)
    plt.grid()
    plt.title('Magnitude')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim((-f0,f0))

    plt.subplot(numrow, numcol, 5)
    plt.plot(f,np.angle(xf))
    plt.plot(f,np.angle(xf_delayed))
    plt.grid()
    plt.title('Phase')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Rad')
    plt.xlim((-f0,f0))

    # Complex plane representation
    plt.subplot(numrow, numcol, 4)
    plt.scatter(xf.real/N, xf.imag/N,s=25)
    plt.scatter(xf_delayed.real/N, xf_delayed.imag/N,s=25)
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.axis('square')  # Make sure the plot is square
    r=.3
    plt.xlim((-r,r))
    plt.ylim((-r,r))
    plt.title('Complex Plane Representation')
    plt.grid()

    # Mark the beginning and end of the FFT curve
    plt.scatter(xf.real[0], xf.imag[0], color='green', marker='s', s=50)
    plt.scatter(xf.real[-1], xf.imag[-1], color='red', marker='s', s=50)
    '''
# delay_est-=len(corr_f)/2

fig = plt.figure(figsize=(12, 8))

plt.subplot(3,1,1)
plt.plot(delays*1e6,delay_est*ts*1e6)
plt.ylabel("estimated ($\mu$s)")
plt.xlabel("delay ($\mu$s)")
plt.subplot(3,1,2)

plt.plot(delays*1e6,(delays-delay_est*ts)*1e6)
plt.ylabel("abs error ($\mu$s)")
plt.xlabel("delay ($\mu$s)")

plt.subplot(3,1,3)
plt.plot(corr_f)
plt.plot(np.fft.fftshift(corr_f))

t_final=time.time()
print(f"Time to run: {t_final-t_start} seconds")
plt.tight_layout()

plt.show()
