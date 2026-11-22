# Clean "Bling - Erica Kennedy.rtf" into plain text for audiobook narration.
# Requires: pip install striprtf
import re
import sys
from striprtf.striprtf import rtf_to_text

input_file = sys.argv[1] if len(sys.argv) > 1 else "Bling - Erica Kennedy.rtf"
output_file = sys.argv[2] if len(sys.argv) > 2 else "Bling_Cleaned.txt"

# RTF is ASCII; non-ASCII characters are encoded as \'xx / \uNNNN escapes,
# which striprtf decodes. A real parser also skips embedded image hex data.
with open(input_file, "r", encoding="latin-1") as f:
    text = rtf_to_text(f.read(), errors="ignore")

text = text.replace(" ", " ")

# Map Unicode subscript/superscript digits to normal digits (OCR sometimes emits them).
text = text.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹", "01234567890123456789"))

# Remove lines that are page furniture, not story text.
junk_line = re.compile(
    r"""^[ \t]*(?:
        Bling[ \t]+\d+                              # "Bling 77" (odd-page header)
      | \d+[ \t]+[♦•◆][ \t]+ERICA[ \t]+KENNEDY      # "170 ♦ ERICA KENNEDY" (even-page header)
      | \d{1,3}                                     # bare page number
      | [•♦◆*·]+                                    # ornament / bullet-only lines
      | Digitized[ \t]+by[ \t]+the[ \t]+Internet[ \t]+Archive.*
      | https?://\S+                                # stray URL lines (archive.org link)
    )[ \t]*$""",
    re.VERBOSE | re.IGNORECASE,
)
lines = [ln for ln in text.splitlines() if not junk_line.match(ln)]
text = "\n".join(lines)

# Collapse runs of blank lines to a single blank line.
text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(text.strip() + "\n")

print("Cleanup complete! Saved to", output_file)
