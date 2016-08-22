import pyaudio
import wave


def beep(filename):
    wf = wave.open(filename, 'rb')
    pya = pyaudio.PyAudio()
    stream = pya.open(format=pya.get_format_from_width(wf.getsampwidth()),
                      channels=wf.getnchannels(),
                      rate=wf.getframerate(),
                      output=True)
    data = wf.readframes(1024)

    while data != '':
        stream.write(data)
        data = wf.readframes(1024)

    stream.close()
    pya.terminate()