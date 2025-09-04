import os
import sys
import re
from datetime import timedelta
import wave
import tempfile
import comtypes.client
sapi_path = os.path.join(
    os.environ['SystemRoot'],
    'System32', 'Speech', 'Common', 'sapi.dll'
)
comtypes.client.GetModule(sapi_path)

from comtypes.gen import SpeechLib

def read_captions_with_timecodes(path: str):
    """
    Returns a list of tuples: (override_time | None, caption_text).
    Lines starting with '(number)' define override_time.
    """
    pattern = re.compile(r"^\(\s*(\d+(?:\.\d+)?)\s*\)\s*(.*)$")
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue
            m = pattern.match(line)
            if m:
                override = float(m.group(1))
                text = m.group(2).strip()
            else:
                override = None
                text = line
            entries.append((override, text))
    return entries

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

def merge_wavs(segments, out_filename,voice_no,speechrate):
    """
    `segments`: list of dicts with keys:
       - 'text': string to speak
       - 'start': float start time in seconds
    Writes merged audio to `out_filename`.
    """
    # Create a temp dir for snippet WAVs
    tmpdir = tempfile.mkdtemp(prefix="tts_snippets_")
    wav_paths = []
    
    # 1) Generate individual WAVs
    for i, (tcode, captext) in enumerate(segments, start=1):
        path = os.path.join(tmpdir, f"seg_{i}.wav")
        tts_to_wav(captext, path, voice_id=voice_no, rate=speechrate)
        wav_paths.append((path, tcode))
    
    # 2) Read parameters from first WAV
    params = None
    for path, _ in wav_paths:
        with wave.open(path, 'rb') as wf:
            params = wf.getparams()  # nchannels, sampwidth, framerate, nframes, comptype, compname
        break
    
    nchannels, sampwidth, framerate, _, comptype, compname = params
    byte_depth = nchannels * sampwidth
    
    # 3) Compute total frames needed
    total_frames = 0
    for path, start in wav_paths:
        with wave.open(path, 'rb') as wf:
            nframes = wf.getnframes()
        start_frame = int(start * framerate)
        total_frames = max(total_frames, start_frame + nframes)
    
    # 4) Create a silent master buffer
    master_buffer = bytearray(total_frames * byte_depth)
    
    # 5) Overlay each snippet into the master buffer
    for path, start in wav_paths:
        start_frame = int(start * framerate)
        offset_bytes = start_frame * byte_depth
        
        with wave.open(path, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
        
        # Overwrite silence with snippet data
        master_buffer[offset_bytes : offset_bytes + len(frames)] = frames
    
    # 6) Write out the merged WAV
    with wave.open(out_filename, 'wb') as out_wf:
        out_wf.setnchannels(nchannels)
        out_wf.setsampwidth(sampwidth)
        out_wf.setframerate(framerate)
        out_wf.setcomptype(comptype, compname)
        out_wf.writeframes(master_buffer)
    
    # 7) Cleanup temp WAVs
    for path, _ in wav_paths:
        os.remove(path)
    os.rmdir(tmpdir)
    print(f"Merged WAV saved as: {out_filename}")

# Example usage
if __name__ == "__main__":
    caption_file = sys.argv[1]
    output_file = sys.argv[2]
    voice_no = sys.argv[3]
    speechrate = sys.argv[4]
    entries = read_captions_with_timecodes(caption_file)
    
    merge_wavs(entries, output_file, int(voice_no), int(speechrate))
