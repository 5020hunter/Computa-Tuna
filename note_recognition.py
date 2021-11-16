#takes dominant frequency from FFT and returns a note name/octave
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import numpy as np
import math
data_dir = pjoin(dirname('output.wav'),)
wav_fname = pjoin(data_dir, 'output.wav')
samplerate, data = wavfile.read(wav_fname)
n = len(data)
yf = np.fft.fft(data)
xf = np.linspace(0, samplerate//2, n//2)
max_y = np.argmax(2.0/n * np.abs(yf[:n//2]))
max_x = xf[max_y]

for i in range(0,72):
    note_dict = {0:"C",1:"C#/Db",2:"D",3:"D#/Eb",4:"E",5:"F",6:"F#/Gb",7:"G",8:"G#/Ab",9:"A",10:"A#/Bb",11:"B"}
    scaling = 440*(math.pow(math.pow(2,1/12),i-57))
    tolerance = 5
    if scaling - tolerance <= max_x <= scaling + tolerance:
        note, octave = (note_dict[i%12],i//12)
        print(note, octave)