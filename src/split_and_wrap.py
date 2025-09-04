import argparse
import textwrap
import re

CHAPTER_RE = re.compile(r'^(\d+(?:\.\d+)*\.)\s+(.*)$')

def mark_chapters_with_id(text):
    
    def repl(m):
        # strip trailing dot from the numeric ID
        chap_id = m.group(1).replace('.'," ")
        title  = m.group(2)
        return f'(chapter) {chap_id} {title}'
    return CHAPTER_RE.sub(repl, text)

def split_sentences(text):
    """
    Split text into raw sentences on '.', '?', '!', or newline.
    Keeps delimiters (., ?, !) at end of each sentence.
    """
    sentences = []
    current = ""
    for char in text:
        if char in ".?!":
            current += char
            if current.strip():
                sentences.append(current.strip())
            current = ""
        elif char == "\n":
            if current.strip():
                sentences.append(current.strip())
            current = ""
        else:
            current += char
    if current.strip():
        sentences.append(current.strip())
    return sentences

def merge_short_sentences(sentences, min_words):
    """
    Merge any sentence fragment with fewer than min_words back into
    its neighbor to avoid splitting on abbreviations.
    """
    merged = []
    i = 0
    while i < len(sentences):
        #
        tokens = sentences[i].split()
        if len(tokens) < min_words and sentences[i][:9] != "(chapter)":
            # Merge into next if possible
            if i + 1 < len(sentences):
                sentences[i + 1] = sentences[i] + " " + sentences[i + 1]
            else:
                # Merge into previous if last fragment
                if merged:
                    merged[-1] += " " + sentences[i]
            # Skip adding the short fragment itself
        else:
            merged.append(sentences[i])
        i += 1
    return merged

def wrap_sentences(sentences, max_length):
    """
    Wrap each sentence into lines up to max_length without
    breaking words or hyphens.
    """
    wrapped = []
    for sentence in sentences:
        lines = textwrap.wrap(
            sentence,
            width=max_length,
            break_long_words=False,
            break_on_hyphens=False
        )
        wrapped.extend(lines)
    return wrapped

def main():
    
    parser = argparse.ArgumentParser(
        description="Split text into sentences and wrap each line."
    )
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument("output_file", help="Path to the output text file.")
    parser.add_argument(
        "--max-length",
        type=int,
        default=70,
        help="Maximum characters per line (default: 70)."
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=5,
        help="Minimum words per sentence fragment before merging (default: 5)."
    )
    args = parser.parse_args()

    # Read full text
    with open(args.input_file, "r", encoding="utf-8") as f:
        text_orig = f.read()
    text = ""
    lines = text_orig.splitlines()
    for line in lines:
        #print(mark_chapters_with_id(line))
        text = text + mark_chapters_with_id(line) + "\n"
    #print(text)     

    # Split, merge short fragments, then wrap
    raw_sentences = split_sentences(text)
    sentences = merge_short_sentences(raw_sentences, args.min_length)
    wrapped_lines = wrap_sentences(sentences, args.max_length)

    # Write output
    with open(args.output_file, "w", encoding="utf-8") as f:
        for line in wrapped_lines:
            f.write(line + "\n")

    print(
        f"Processed {len(sentences)} sentences "
        f"(merged from {len(raw_sentences)} fragments); "
        f"output saved to {args.output_file}."
    )

if __name__ == "__main__":
    main()
