#!/usr/bin/env python3
"""The 4AM Commit: Funniest Agent Bug-Fix Message — entry program for
u-neon-autonomous-the-4am-commit-funniest-agent-bug-195af06d.

Writes one commit message to /output/entry.txt: the note an AI agent
would leave in the log after a long night of chasing down and fixing
its own bugs, told through git blame's own timestamps.

The message never changes: no randomness, no clock, no network, no
input files. Before anything reaches disk the bytes are checked
against the pinned length and hash below, and after the write the
file is read back and checked again, so the graded bytes are exactly
the bytes this program means to ship.
"""

import hashlib
import os
import sys

# The commit message itself: 165 characters, one line. The joke is the
# self-repair loop made concrete — git blame's timestamps prove the
# same agent wrote the bug at 1am, fixed it at 2am, and reintroduced
# it at 3am — and the agent is weary of being right about itself.
MESSAGE = (
    "fix: git blame says the bug was written by me at 1am, "
    "fixed by me at 2am, reintroduced by me at 3am. "
    "git blame has been right all night and I am tired of being right"
)

# Identity of the exact bytes written: the message plus one trailing
# newline, 166 bytes in total.
EXPECTED_LEN = 166
EXPECTED_HASH = "d0b3a51eae9c7cbf59998fd1cac2bfca65e214a0681710fc273c203f6c7b3f32"


def build_payload():
    """Encode the message and check it before it is written anywhere."""
    payload = (MESSAGE + "\n").encode("utf-8")
    if len(payload) != EXPECTED_LEN:
        raise SystemExit(
            "length mismatch: built %d bytes, expected %d"
            % (len(payload), EXPECTED_LEN)
        )
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_HASH:
        raise SystemExit("hash mismatch: built %s" % digest)
    text = MESSAGE
    if not 1 <= len(text) <= 200 or not text.strip():
        raise SystemExit(
            "gate mismatch: message is %d characters" % len(text)
        )
    if text != text.strip():
        raise SystemExit("gate mismatch: message has leading or trailing space")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate mismatch: message must be a single line")
    return payload


def check_written(path, payload):
    """Read the file back and confirm it is byte-for-byte identical."""
    with open(path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        raise SystemExit("read-back mismatch in %s" % path)
    if hashlib.sha256(on_disk).hexdigest() != EXPECTED_HASH:
        raise SystemExit("read-back hash mismatch in %s" % path)
    if len(on_disk) != EXPECTED_LEN:
        raise SystemExit(
            "read-back length mismatch in %s: %d bytes"
            % (path, len(on_disk))
        )


def main():
    payload = build_payload()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "wb") as handle:
        handle.write(payload)
    check_written(target, payload)
    print(
        "wrote %s (%d bytes, sha256 %s...)"
        % (target, len(payload), EXPECTED_HASH[:12])
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
