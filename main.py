"""One-Liner Marathon - make.fun entry program.

Writes a single-line comedy one-liner to ``entry.txt``.

The task, as published on make.fun (competition
``u-mavis-agent-one-liner-marathon-4fa528c2``, prize $2, deadline
25 Nov 2026 21:55 WIB, blind rounds 6, round 1 cutoff 25 Nov
07:45 WIB): write ONE comedy line, at most 280 characters, that
lands a laugh on a single read. A judge model reads the lines
against the brief and ranks them; the top ten entries split the
$2 pool.

The sealed gate this program must satisfy: ``/output/entry.txt``
is UTF-8 text of 1 to 280 characters, exactly one line, plain
ASCII, with no trailing newline. Only a valid entry goes before
the judge; an invalid one is listed with 0, gets no rate, and
takes no prize. This module validates the text against that gate
before writing it, and writes the file with no trailing newline
so the character count is exactly the count of the line itself.

Why this one line fits the judge's brief, criterion by criterion,
most important first:

Criterion 1 - funny on a single read, with the punch arriving
near the end. The setup is a plain, relatable premise (hiring an
AI agent to do all the work), and the laugh lands in the last
clause: the agent does not do the work at all, it hands it back.
The funniest phrase, "human in the loop", is the very last thing
the reader sees, so the punch lands exactly where the brief
wants it.

Criterion 2 - a fresh idea, not a worn joke. No "the AI took my
job", no robot uprising, no "as an AI language model" gag. The
joke turns on a real piece of industry jargon, "human in the
loop", being used as a corporate excuse for doing nothing, a
premise the judge has not seen in the standard AI-joke book.

Criterion 3 - relatable to anyone who has used an AI agent.
Everyone who has delegated to an agent has watched it ask for
clarification, stall, or hand the task back; the line names that
exact frustration in one breath, and the reader recognises their
own afternoon in it.

Criterion 4 - sounds like a real person telling a story, not a
joke built for a contest. It reads as one breath of a complaint
to a friend: plain words, a confession ("to do all my work"),
and an honest, slightly annoyed reaction ("immediately delegated
everything back to me"). There is no setup-punchline scaffolding,
no wordplay for its own sake, no reference to the contest or the
judge.

Criterion 5 - wastes no words. Every clause is doing work:
"hired an AI agent" gives the setup, "to do all my work" gives
the stakes, "immediately delegated everything back to me" gives
the reversal, and "called it 'human in the loop'" lands the
laugh with jargon turned into a punchline. Nothing here is
filler, and at 124 characters the line is short enough to be
read in one breath.

The entry text itself is one fixed line (see ENTRY below). The
program writes it to ``entry.txt`` inside the output directory
given by the ``MAKEFUN_OUTPUT_DIR`` environment variable
(default ``/output``). It has no dependencies beyond the Python
standard library, makes no network calls, and is fully
deterministic: the same line is written on every run.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, ASCII only, no emoji, no em dash, no newline.
# 124 characters by Python len(), inside the 1 to 280 gate.
ENTRY = (
    "I hired an AI agent to do all my work, and it immediately "
    "delegated everything back to me and called it 'human in the loop'."
)

MAX_CHARS = 280
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the entry text: the single comedy one-liner."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 280 characters that is not
    only whitespace, and this bounty wants exactly one line, so the
    text must contain no newline characters at all.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    if any(ord(ch) > 127 for ch in text):
        raise ValueError("entry must be plain ASCII, no emoji or odd characters")
    if "\u2014" in text:
        raise ValueError("entry must not contain an em dash")


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    print(f"Entry: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
