#takes dominant frequency from FFT and returns a note name/octave
from os.path import dirname, join as pjoin
from scipy.io import wavfile
import numpy as np
data_dir = pjoin(dirname('output.wav'),)
wav_fname = pjoin(data_dir, 'output.wav')
samplerate, data = wavfile.read(wav_fname)
n = len(data)
yf = np.fft.fft(data)
xf = np.linspace(0, samplerate//2, n//2)
max_y = np.argmax(2.0/n * np.abs(yf[:n//2]))
max_x = xf[max_y]

tolerance = 0.60
for octave in range(0,6):
    if (octave+1)-tolerance <= max_x/16.35 <= (octave+1)+tolerance:
        note = ("C", octave)
    elif (octave+1)-tolerance <= max_x/17.32 <= (octave+1)+tolerance:
        note = ("C#/Db", octave)
    elif (octave+1)-tolerance <= max_x/18.35 <= (octave+1)+tolerance:
        note = ("D", octave)
    elif (octave+1)-tolerance <= max_x/19.45 <= (octave+1)+tolerance:
        note = ("D#/Eb", octave)
    elif (octave+1)-tolerance <= max_x/20.60 <= (octave+1)+tolerance:
        note = ("E", octave)
    elif (octave+1)-tolerance <= max_x/21.83 <= (octave+1)+tolerance:
        note = ("F", octave)
    elif (octave+1)-tolerance <= max_x/23.12 <= (octave+1)+tolerance:
        note = ("F#/Gb", octave)
    elif (octave+1)-tolerance <= max_x/24.50 <= (octave+1)+tolerance:
        note = ("G", octave)
    elif (octave+1)-tolerance <= max_x/25.96 <= (octave+1)+tolerance:
        note = ("G#/Ab", octave)
    elif (octave+1)-tolerance <= max_x/27.50 <= (octave+1)+tolerance:
        note = ("A", octave)
    elif (octave+1)-tolerance <= max_x/29.14 <= (octave+1)+tolerance:
        note = ("A#/Bb", octave)
    elif (octave+1)-tolerance <= max_x/30.87 <= (octave+1)+tolerance:
        note = ("B", octave)
print(note)