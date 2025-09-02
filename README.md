# Requisites
You need Python 3.

<code>pip install pyttsx3</code>

# Text2Caption
 Creates subtitle caption files and audio narrative from plain text

I made this collection of command line Python tools for myself, but others may 
find them useful too. It became too tedious to use YouTube subtitle editor. I usually wrote 
long description about video, so I thought that I could transform them to subtitles and audio. 
These programs automate that 3-step process and produce timecoded sbv/srt files and wav audio 
where each caption is spoken at the same time as caption is shown.

Since these are for personal use, they are command line tools, and they are as simple 
as possible.

# Split plain text to lines
Assuming you have a text file with plain text description that you want to use
as captions in the video. You can transform that plain text to separate lines with
split_and_wrap.py

<code>python split_and_wrap.py input.txt output.txt --max-length 70 --min-length 5</code>

It is best to check the output file in text editor. You can use different max length and 
min length values to enhance results, or edit them manually.

# Create caption file from text
You need text file, where each caption is a separate line. Then text2cap.py creates a new
sbv (YouTube) or srt file with timecodes. Program uses constant duration for each caption.
Other parameters are the first timecode, and output filename

<code>python text2cap.py caption_file duration format_type start_time output_file</code>

Inputs You Control

<code>start_time</code>: where captions begin (in seconds)

<code>duration</code>: duration of each caption (in seconds)

<code>format_type</code>: "sbv" or "srt"

<code>caption_file</code>: path to your plain text file (one caption per line)

<code>output_file</code>: optional name for the output subtitle file

You can override constant sequential timecoding. Just put time value (in seconds) in the 
beginning of any line, in parenthesis. Example:
<code>(65) This caption is shown at 1:05</code>

Process will automatically continue with overridden time value, and in the example above 
next caption will automatically start at 70 sec etc. If you wish, you can override each line.

This program will generate special subtitle text file (output_file.speech) for text2wav.py that generates audio 
track with narration for the video (see below).

# Create narration track for video
Using the special subtitle file this program <code>text2wav.py</code> generates narration as audio (wav) track, 
which you can use as audio track in video editor. For really long narration it may be necessary 
to generate audio in segments, and then append them together in video editor. Unlike previous programs, 
this program works only in Windows, currently.

<code>text2wav.py captionfile audiofilename</code>

<code>captionfile</code> name of the text file with timecoded captions
<code>audiofilename</code> output filename

Input file should follow this format. Text2cap.py program will generate this subtitle file 
automatically. Each line should contain timecode (00:00:00) or plain seconds, blank space, 
and caption text.

<code>0:00:00.000 caption line 1</code>

# Future development
I may add new features occasionally. Currently I have no intention to add any kind of GUI.
Following features are planned:

- different voices
- fades and mixings