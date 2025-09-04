import os
import sys
import re
from datetime import timedelta
import wave
import tempfile
import pyttsx3
import comtypes.client
sapi_path = os.path.join(
    os.environ['SystemRoot'],
    'System32', 'Speech', 'Common', 'sapi.dll'
)
comtypes.client.GetModule(sapi_path)
from comtypes.gen import SpeechLib

def tts_to_wav(text, filename, voice_id=None, rate=0):
    """
    Render `text` to `filename` using Windows SAPI.
    Optionally specify `voice_id` (string) and `rate` (int).
    """
    speaker = comtypes.client.CreateObject("SAPI.SpVoice")
    stream  = comtypes.client.CreateObject("SAPI.SpFileStream")
    stream.Open(filename, SpeechLib.SSFMCreateForWrite)
    
    if voice_id:
        speaker.Voice = speaker.GetVoices().Item(voice_id)
    if rate:
        speaker.Rate = rate
    
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()

if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        print(voice.id)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 125)
    engine.say("I hear your favorite gum is coming back in style.")
    engine.runAndWait()
    
