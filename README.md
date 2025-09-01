# Text2Caption
 Creates caption files from plain text

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

<code>python text2cap.py input.txt duration captionformat starttime captionfile</code>

Inputs You Control
start_time: where captions begin (in seconds)

caption_length: duration of each caption (in seconds)

format_type: "sbv" or "srt"

caption_file: path to your plain text file (one caption per line)

output_file: optional name for the output subtitle file

