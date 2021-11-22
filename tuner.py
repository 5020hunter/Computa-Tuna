from os.path import dirname, join as pjoin
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import math
import pyaudio
import wave
import time

def record_audio(seconds, filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 16000  # Record at 16000 samples per second
    seconds = seconds
    filename = filename
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print('Recording')
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []  # Initialize array to store frames
    # Store data in chunks for 3 seconds
    for frame in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
        frame+=1
    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
    print('Finished Recording')
    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def playback_audio(audio_file):
    filename = audio_file
    # Set chunk size of 1024 samples per data frame
    chunk = 1024  
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
    time = np.linspace(0, length, data.shape[0])
    #plotting the audio wave, showing amplitude over time
    plt.subplot(2,1,1)
    plt.plot(time, data[:], label="Audio Wave")
    plt.legend()
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    n = len(data)
    yf = np.fft.fft(data)
    xf = np.linspace(0, samplerate//2, n//2)
    #plotting the magnitudes(occurrences) of frequencies 0-1000Hz from our audio
    plt.subplot(2,1,2)
    plt.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.xlim(0,1000) #0-1000Hz is the typical range for human speech
    plt.grid()
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.show()

def dominant_frequency(samplerate, data):
    n = len(data)
    yf = np.fft.fft(data)
    xf = np.linspace(0, samplerate//2, n//2)
    max_y = np.argmax(2.0/n * np.abs(yf[:n//2])) #find maximum value from the set of y-values we plotted earlier
    max_x = xf[max_y] #find the x-value associated with the maximum y-value
    return max_x

def note_recognition(frequency):
    for i in range(0,72):
        note_dict = {0:"C",1:"C#/Db",2:"D",3:"D#/Eb",4:"E",5:"F",6:"F#/Gb",7:"G",8:"G#/Ab",9:"A",10:"A#/Bb",11:"B"}
        scaling = 440*(math.pow(math.pow(2,1/12),i-57)) #logarithmic spacing between note in reference to A4 with frequency 440Hz
        tolerance = 5 #Hz above/below we consider in tune
        if scaling - tolerance <= frequency <= scaling + tolerance:
            note, octave = (note_dict[i%12],i//12) #note is some value mod-12, octave is what multiple of 12 notes we are on
            print(note, octave)
            break

def user_menu():
    seconds = float(input("How many seconds would you like to record? "))
    filename = input("What would you like to name the file? ")
    filename = filename + ".wav"
    record_audio(seconds, filename)
    answer = input("Would you like to playback your audio (y/n)? ")
    if answer.lower() == "y":
        playback_audio(filename)
    samplerate, data = convert_audio_to_array(filename)
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