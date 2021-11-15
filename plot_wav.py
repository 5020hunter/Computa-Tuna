from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
data_dir = pjoin(dirname('output.wav'),)
wav_fname = pjoin(data_dir, 'output.wav')
samplerate, data = wavfile.read(wav_fname)
length = data.shape[0] / samplerate
time = np.linspace(0, length, data.shape[0])
plt.plot(time, data[:], label="Audio Wave")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
n = len(data)
time = 1/samplerate
yf = np.fft.fft(data)
xf = np.linspace(0, samplerate//2, n//2)
fig, axis = plt.subplots()
axis.plot(xf, 2.0/n * np.abs(yf[:n//2]))
plt.grid()
plt.xlabel("Frequency [hZ]")
plt.ylabel("Magnitude")
plt.show()
#sp=np.fft.fft(data[:, 1])
#frequency=np.fft.fftfreq(data.size)
#plt.plot(data[:, 1],np.abs(sp), label="Fast Fourier Transform (Our Audio)")
#plt.legend()
#plt.xlabel("Frequency [hZ]")
#plt.ylabel("Amplitude")
#plt.show()