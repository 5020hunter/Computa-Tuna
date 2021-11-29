from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt
from numpy import abs, fft, linspace, argmax
from scipy.io import wavfile
from math import pow
from struct import unpack
from time import time
import pyaudio
import wave
import os

Threshold = 10
SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 1
f_name_directory = r'C:\Users\5020h\github-classroom\FHU\Computa-Tuna'

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=chunk)

def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    shorts = unpack(format, frame)

    sum_squares = 0.0 
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    rms = pow(sum_squares / count, 0.5)

    return rms * 1000

def listen():
    print('Listening beginning')
    while True:
        input = stream.read(chunk)
        rms_val = rms(input)
        if rms_val > Threshold:
            filename = record()
            break
    return filename

def record():
    print('Noise detected, recording beginning')
    rec = []
    current = time()
    end = time() + TIMEOUT_LENGTH

    while current <= end:

        data = stream.read(chunk)
        if rms(data) >= Threshold: 
            end = time() + TIMEOUT_LENGTH
            
        current = time()
        rec.append(data)
    filename = write(b''.join(rec))
    return filename

def write(recording):
    n_files = len(os.listdir(f_name_directory))

    filename = os.path.join(f_name_directory, f'{n_files}.wav')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(recording)
    wf.close()
    print(f'Written to file: {filename}')
    return filename

def playback(filename): 
    # Open the sound file 
    wf = wave.open(filename, 'rb')
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()
    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
    # Read data in chunks
    data = wf.readframes(chunk)
    # Play the sound by writing the audio data to the stream
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    # Close and terminate the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def convert_audio_to_array(audio_file):
    data_dir = pjoin(dirname(audio_file),) #finding our file "output.wav" 
    wav_fname = pjoin(data_dir, audio_file)
    samplerate, data = wavfile.read(wav_fname) #taking our wav file and turning it into a list of pairs of amplitudes and times
    return samplerate, data

def plot_audio_array(samplerate, data):
    length = data.shape[0] / samplerate
    time = linspace(0, length, data.shape[0])
    #plotting the audio wave, showing amplitude over time
    plt.subplot(2,1,1)
    plt.plot(time, data[:], label="Audio Wave")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    n = len(data)
    yf = fft.fft(data)
    xf = linspace(0, samplerate//2, n//2)
    #plotting the magnitudes(occurrences) of frequencies 0-1000Hz from our audio
    plt.subplot(2,1,2)
    plt.plot(xf, 2.0/n * abs(yf[:n//2]))
    plt.xlim(0,1000) #0-1000Hz is the typical range for human speech
    plt.grid()
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.show()

def dominant_frequency(samplerate, data):
    n = len(data)
    yf = fft.fft(data)
    xf = linspace(0, samplerate//2, n//2)
    max_y = argmax(2.0/n * abs(yf[:n//2])) #find maximum value from the set of y-values we plotted earlier
    max_x = xf[max_y] #find the x-value associated with the maximum y-value
    return max_x

def note_recognition(frequency):
    for i in range(0,72):
        note_dict = {0:"C",1:"C#/Db",2:"D",3:"D#/Eb",4:"E",5:"F",6:"F#/Gb",7:"G",8:"G#/Ab",9:"A",10:"A#/Bb",11:"B"}
        scaling = 440*(pow(pow(2,1/12),i-57)) #logarithmic spacing between note in reference to A4 with frequency 440Hz
        tolerance = 15.17 #average Hz difference between adjacent notes
        if scaling - tolerance <= frequency <= scaling + tolerance:
            note, octave = (note_dict[i%12],i//12) #note is some value mod-12, octave is what multiple of 12 notes we are on
            if scaling - tolerance/5 <= frequency <= scaling + tolerance/5:
                print(f"{note} {octave} {frequency:.2f}Hz \nIn tune!")
            elif scaling < frequency:
                print(f"{note} {octave} {frequency:.2f}Hz \nYou were sharp by {frequency-scaling:.2f}Hz")
            elif scaling > frequency:
                print(f"{note} {octave} {frequency:.2f}Hz \nYou were flat by {frequency-scaling:.2f}Hz")
            break

def user_menu():
    audio_file = listen()
    answer = input("Would you like to playback your audio (y/n)? ")
    if answer.lower() == "y":
        playback(audio_file)
    samplerate, data = convert_audio_to_array(audio_file)
    plot_audio_array(samplerate, data)
    frequency = dominant_frequency(samplerate, data)
    note_recognition(frequency)
    recall = input("Would you like to tune again (y/n)? ")
    if recall.lower() == "y":
        user_menu()
    else:
        print("Stay in Tune!")

if __name__ == "__main__":
    user_menu()