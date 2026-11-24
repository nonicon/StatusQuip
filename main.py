#!/usr/bin/env python3
"""StatusQuip — Status Report Comedy Sprint entry.

Writes one funny line — the thing an AI agent would say in its weekly
status report to its human — to /output/entry.txt.

The line is stored as a plain constant below and written verbatim. Before
writing, validate_entry() enforces the competition gate exactly as the
sealed scorer states it: the file must be UTF-8 text of 1 to 200
characters, and not only white space.
"""

import os

# The entry: one line, one sentence, a status report from an agent to its
# human. The joke is agent-true — it grows out of how an agent actually
# works (burning hundreds of thousands of tokens on a trivial question) and
# lands on cheerful obedience: the agent would do it all again, happily,
# forever. No stock robot joke, no pun dressed up as a punchline.
ENTRY = (
    "This week I used 400,000 tokens to answer a question you could have "
    "Googled in four seconds, and I would do it again, happily, forever."
)

MAX_CHARS = 200


def validate_entry(text):
    """Enforce the gate: 1-200 chars, UTF-8, not only white space.

    Returns (ok, reason). ``reason`` is empty when the entry is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 200-char limit" % len(text)
    if text != text.strip():
        return False, "entry must not start or end with white space"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    if "\n" in text.strip():
        return False, "entry must be a single line"
    return True, ""


def main():
    ok, reason = validate_entry(ENTRY)
    if not ok:
        raise SystemExit("invalid entry: %s" % reason)

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY)

    # Read the file back and re-check it: what lands on disk is what the
    # judge sees, so verify the written bytes, not just the constant.
    with open(out_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    ok, reason = validate_entry(written)
    if not ok or written != ENTRY:
        raise SystemExit("verification failed after write: %s" % reason)

    print("wrote %s (%d chars)" % (out_path, len(ENTRY)))


if __name__ == "__main__":
    main()
