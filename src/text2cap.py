import sys
import re
from datetime import timedelta

def format_sbv_time(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total = int(td.total_seconds())
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours}:{minutes:02}:{secs:02}.000"

def format_srt_time(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total = int(td.total_seconds())
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    millis = int((td.total_seconds() - total) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def read_captions_with_overrides(path: str):
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

def generate_subtitles(caption_file: str, caption_length: float, format_type: str = "sbv", output_file: str = None, start_time: float = 0.0):
    """
    caption_file: path to txt file (one caption per line, optional '(time)' override)
    caption_length: duration of each caption in seconds
    format_type: 'sbv' or 'srt'
    output_file: optional output filename
    start_time: initial caption time if no override on first line
    """
    if format_type not in ("sbv", "srt"):
        raise ValueError("format_type must be 'sbv' or 'srt'")
    entries = read_captions_with_overrides(caption_file)
    output_file_2 = output_file + ".speech"
    if output_file is None:
        output_file = f"captions.{format_type}"
        output_file_2 = "captions.speech"

    current = start_time
    
    with open(output_file, "w", encoding="utf-8") as out:
        for idx, (override, text) in enumerate(entries, start=1):
            if override is not None:
                current = override
            end = current + caption_length
            

            if format_type == "sbv":
                out.write(f"{format_sbv_time(current)},{format_sbv_time(end)}\n")
                out.write(f"{text}\n\n")
            else:  # SRT
                out.write(f"{idx}\n")
                out.write(f"{format_srt_time(current)} --> {format_srt_time(end)}\n")
                out.write(f"{text}\n\n")

            current = end
    print(f"{format_type.upper()} file created: {output_file}")
    current = start_time
    
    with open(output_file_2, "w", encoding="utf-8") as out:
        for idx, (override, text) in enumerate(entries, start=1):
            if override is not None:
                current = override
            end = current + caption_length
            

            out.write(f"({current})")
            out.write(" ")
            out.write(f"{text}\n")
            

            current = end

    print(f"{format_type.upper()} file created: {output_file_2}")

# Example usage
if __name__ == "__main__":
    tfile = sys.argv[1]
    clength = sys.argv[2]
    cformat = sys.argv[3]
    cstart = sys.argv[4]
    cfile = sys.argv[5]
    print(cstart)
    generate_subtitles(
        caption_file=tfile,
        caption_length=float(clength),
        format_type=cformat,
        output_file=cfile+"."+cformat,
        start_time=float(cstart)
    )
