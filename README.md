# Text2Caption
 Creates caption files from plain text

I made this collection of command line Python tools for myself, but others may 
find them useful too. It became too tedious to use YouTube subtitle editor. I usually wrote 
long description about video, so I thought that I could transform them to subtitles. 
These programs automate that 2-step process and produce timecoded sbv and srt files.

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