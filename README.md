# Requisites
You need Python 3.

<code>pip install pyttsx3</code>

# Text2Caption
 Creates subtitle caption files and audio narration from plain text

I made this collection of command line Python tools for myself, but others may 
find them useful too. It became too tedious to use YouTube subtitle editor. I usually wrote 
long description about video, so I thought that I could transform them to subtitles and audio. 
These programs automate that 3-step process and produce timecoded sbv/srt files and wav audio 
where each caption is spoken at the same time as caption is shown.

Notice: subtitle generation should work on every platform, but speech generation works only on Windows. It has been tested on Windows 11.


Since these are for personal use, they are command line tools, and they are as simple 
as possible.

# Basic usage

You have plain text file <code>testfile.txt</code>

<code>python split_and_wrap.py testfile.txt linetext.txt --max-length 100 --min-length 5</code>

generates a file (linetext.txt) where each sentence and headline is on its own line, or several separate lines. 
You can edit this file, and add specific timecode or chapter tag on any lines.

<code>python text2cap.py linetext.txt 5.0 sbv 0.0 subtitle</code>

uses linetext.txt file (from previous step) as input, and generates subtitle file subtitle.sbv with timecodes, 
separate subtitle.sbv.speech file (for speech generation), and chapter file for YouTube. If you 
select srt, then this will generate files subtitle.srt and subtitle.srt.speech.

<code>python text2wav.py subtitle.sbv.speech subtitle.wav 1 1</code>

After this you have 2 files - subtitle.sbv with timecoded captions, and subtitle.wav audio file 
where each caption is spoken using chosen voice. Additionally you have subtitle.chapter file 
which contains list of timecodes and chapter names. If you copy and paste this text to YouTube 
video description, then video automatically shows chapters.

Program detects chapter headlines from raw text if they are on their own line and format:

<code>1. Headline
2.3.6. Subchapter
etc...
</code>
Notice that headline must start with number and there must be "." after last number. Otherwise detection fails. When detected, these headlines are tagged for subsequent processing to subtitles 
and chapter list.

Below is more details of each phase.

# Split plain text to lines
You start with a plain text file. It can be documentation, description or script that you want to use
as captions in the video. You can transform that plain text to separate lines with
split_and_wrap.py which recognizes sentences. In optimal case, one sentence will be 
one caption line. If sentence is too long (longer than max-length), then it is split 
to several caption lines. Min-length parameter is used to avoid misinterpreting certain
expression as sentences, but it does not work perfectly yet.

<code>python split_and_wrap.py input.txt output.txt --max-length 70 --min-length 5</code>

It is best to check the output file in text editor. You can use different max length and 
min length values to enhance results, or edit them manually.

# Create caption file from text
You need text file, where each caption is a separate line. Then text2cap.py creates a new
sbv (YouTube) or srt file with timecodes. Program uses constant duration for each caption.
Other parameters are the first timecode, and output filename

<code>python text2cap.py caption_file duration format_type start_time output_file</code>

Inputs You Control

<code>start_time</code>: the time captions begin (in seconds)

<code>duration</code>: duration of each caption (in seconds)

<code>format_type</code>: "sbv" or "srt"

<code>caption_file</code>: path to your plain text file (one caption per line)

<code>output_file</code>: optional name for the output subtitle file

You can override constant sequential timecoding. Just put time value (in seconds) in the 
beginning of any line, in parenthesis. Example:
<code>(65) This caption is shown at 1:05</code>

Process will automatically continue with overridden time value, and in the example above 
next caption will automatically start at 70 sec etc. If you wish, you can override each line.

This program will generate special subtitle text file (output_file.speech) to be processed with text2wav.py that generates audio track with narration for the video (see below).

# Create narration track for video
Using the special subtitle file this program <code>text2wav.py</code> generates narration as audio (wav) track, 
which you can use as audio track in video editor. For really long narration it may be necessary 
to generate audio in segments, and then append them together in video editor. Unlike previous programs, 
this program works only in Windows, currently.

<code>python text2wav.py captionfile audiofilename voice speechrate</code>

<code>captionfile</code> name of the text file with timecoded captions

<code>audiofilename</code> output filename

<code>voice</code> voice ID (1,2, or 3)

<code>speechrate</code> rate of speech (integer) (0 = normal, negative = slower, positive = faster)

Input file should follow this format. Text2cap.py program will generate this subtitle file 
automatically. Each line should contain timecode (00:00:00) or plain seconds, blank space, 
and caption text.

<code>0:00:00.000 caption line 1</code>

# Future development
I may add new features occasionally. Currently I have no intention to add any kind of GUI.
Following features are planned:

- tag any line to use certain voice
- fades and mixings
- detect lists, ordered and unordered