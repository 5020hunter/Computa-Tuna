from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import scipy
data_dir = pjoin(dirname('output.wav'),)
wav_fname = pjoin(data_dir, 'output.wav')
samplerate, data = wavfile.read(wav_fname)
length = data.shape[0] / samplerate
time = np.linspace(0., length, data.shape[0])
plt.plot(time, data[:, 0], label="Left channel")
plt.plot(time, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
sp=np.fft.fft(data)
frequency=np.fft.fftfreq(data.shape[0], d=1/44100)
plt.plot(data,np.abs(sp))
plt.legend()
plt.xlabel("Frequency [hZ]")
plt.ylabel("Amplitude")
plt.show()
print(sp)
print(frequency)