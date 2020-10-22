import pyaudio
import wave
import speech_recognition as sr
from commands import Commander


running = True


def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    pa = pyaudio.PyAudio()

    stream = pa.open(
        format=pa.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    data_stream = wf.readframes(chunk)

    while data_stream:
        stream.write(data_stream)
        data_stream = wf.readframes(chunk)

    stream.close()
    pa.terminate()


r = sr.Recognizer()
cmd = Commander()


def input_audio():
    print("Speak after sound....")

    play_audio("./audio/hey.wav")

    with sr.Microphone() as source:
        print("Say something:")
        audio = r.listen(source)

    play_audio("./audio/end.wav")

    command = ""

    try:
        command = r.recognize_google(audio)
    except:
        print("I am sorry, I couldn't understand you")

    cmd.discover(command)
    if "bye" in command:
        global running
        running = False


while running:
    input_audio()
