from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
data_dir = pjoin(dirname('output.wav'),) #finding our file "output.wav" 
wav_fname = pjoin(data_dir, 'output.wav')
samplerate, data = wavfile.read(wav_fname) #taking our wav file and turning it into a list of pairs of amplitudes and times
length = data.shape[0] / samplerate
time = np.linspace(0, length, data.shape[0])
#plotting the audio wave, showing amplitude over time
plt.plot(time, data[:], label="Audio Wave")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

n = len(data)
yf = np.fft.fft(data)
xf = np.linspace(0, samplerate//2, n//2)
#plotting the magnitudes(occurrences) of frequencies 0-1000Hz from our audio
plt.plot(xf, 2.0/n * np.abs(yf[:n//2]))
plt.xlim(0,1000) #0-1000Hz is the typical range for human speech
plt.grid()
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")
plt.show()