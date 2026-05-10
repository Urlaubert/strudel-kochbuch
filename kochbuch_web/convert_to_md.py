"""Convert .strudel files in lehrbuch/ to .md files in lehrbuch_md/.

The .strudel files use this convention:

  // =====================================================
  // Kapitel NN — Titel
  // =====================================================
  // Optional intro text.
  // More intro.
  // =====================================================


  // -----------------------------------------------------
  // Sub-section heading
  // -----------------------------------------------------
  // Prose comment lines.

  code_block_line_1
  code_block_line_2

  // More prose after the code.

Conversion:
  - First === banner with title -> H1.
  - Subsequent === banners with title -> H2.
  - --- light separators with title -> H3.
  - Comment lines (`// ...`) -> prose paragraphs.
  - Non-comment, non-empty lines -> grouped into ```strudel code blocks.
  - Banner/separator lines themselves don't produce output.
  - An empty line *between code lines* doesn't break the code block — strudel
    code can have blank lines in it. A code block ends at the first comment
    line or banner.
"""

from __future__ import annotations

from pathlib import Path

LEHRBUCH = Path(__file__).parent.parent / "lehrbuch"
OUT = Path(__file__).parent.parent / "lehrbuch_md"
OUT.mkdir(exist_ok=True)


def is_banner_line(line: str) -> bool:
    """Match `// ====...====` lines."""
    s = line.rstrip()
    if not s.startswith("//"):
        return False
    body = s[2:].strip()
    return len(body) >= 5 and set(body) <= {"="}


def is_separator_line(line: str) -> bool:
    """Match `// ----...----` lines."""
    s = line.rstrip()
    if not s.startswith("//"):
        return False
    body = s[2:].strip()
    return len(body) >= 5 and set(body) <= {"-"}


def comment_text(line: str) -> str | None:
    """Return the text after `// ` or None if not a comment line."""
    s = line.rstrip()
    if not s.startswith("//"):
        return None
    rest = s[2:]
    if rest.startswith(" "):
        rest = rest[1:]
    return rest


def convert(source: str) -> str:
    lines = source.split("\n")
    n = len(lines)
    out: list[str] = []

    h1_done = False
    code_buf: list[str] = []

    def flush_code() -> None:
        # Trim leading/trailing empty lines.
        while code_buf and not code_buf[0].strip():
            code_buf.pop(0)
        while code_buf and not code_buf[-1].strip():
            code_buf.pop()
        if code_buf:
            out.append("")
            out.append("```strudel")
            out.extend(code_buf)
            out.append("```")
            out.append("")
            code_buf.clear()

    def looks_like_diagram(lines: list[str]) -> bool:
        """Heuristic: ASCII diagrams have either leading whitespace or
        characteristic chars (|, X .) on most lines."""
        if len(lines) < 2:
            return False
        diagram_chars = set("|/\\_-=^.<>+*▶")
        diagram_lines = 0
        for ln in lines:
            if not ln.strip():
                continue
            stripped = ln.strip()
            # Indented (column-aligned diagram):
            if ln.startswith(" "):
                diagram_lines += 1
                continue
            # Lines that are mostly diagram chars:
            non_alnum = sum(1 for c in stripped if not c.isalnum() and not c.isspace())
            if non_alnum > len(stripped) * 0.4 and len(stripped) >= 4:
                diagram_lines += 1
                continue
            # Lines like "X . . X . . X ." — repeated short tokens.
            tokens = stripped.split()
            if len(tokens) >= 4 and all(len(t) <= 2 for t in tokens):
                diagram_lines += 1
                continue
        non_empty = sum(1 for ln in lines if ln.strip())
        return non_empty >= 2 and diagram_lines >= max(2, non_empty * 0.6)

    def emit_prose(buf: list[str]) -> None:
        # Trim leading/trailing empty entries.
        while buf and not buf[0]:
            buf.pop(0)
        while buf and not buf[-1]:
            buf.pop()
        if not buf:
            return
        # Group into runs separated by empty lines. Each run becomes either
        # a paragraph (joined with spaces) or a fenced ``` block (preserved).
        para: list[str] = []

        def flush_para() -> None:
            if not para:
                return
            if looks_like_diagram(para):
                out.append("")
                out.append("```")
                out.extend(para)
                out.append("```")
                out.append("")
            else:
                out.append(" ".join(para))
                out.append("")
            para.clear()

        for ln in buf:
            if ln == "":
                flush_para()
            else:
                para.append(ln)
        flush_para()

    i = 0
    while i < n:
        line = lines[i]

        # Banner: collect title from following non-empty comment lines.
        if is_banner_line(line):
            flush_code()
            j = i + 1
            title_lines: list[str] = []
            while j < n:
                lj = lines[j]
                if is_banner_line(lj):
                    j += 1
                    break
                t = comment_text(lj)
                if t is None:
                    # Non-comment line means the banner block was malformed.
                    break
                if t.strip():
                    title_lines.append(t.strip())
                j += 1
            if title_lines:
                title = " ".join(title_lines)
                level = "#" if not h1_done else "##"
                out.append(f"{level} {title}")
                out.append("")
                h1_done = True
            i = j
            continue

        # Separator: collect heading from following non-empty comment lines.
        if is_separator_line(line):
            flush_code()
            j = i + 1
            heading_lines: list[str] = []
            while j < n:
                lj = lines[j]
                if is_separator_line(lj):
                    j += 1
                    break
                t = comment_text(lj)
                if t is None:
                    break
                if t.strip():
                    heading_lines.append(t.strip())
                j += 1
            if heading_lines:
                heading = " ".join(heading_lines)
                out.append(f"### {heading}")
                out.append("")
            i = j
            continue

        # Comment block.
        c = comment_text(line)
        if c is not None:
            flush_code()
            buf: list[str] = [c]
            i += 1
            while i < n:
                lj = lines[i]
                if is_banner_line(lj) or is_separator_line(lj):
                    break
                t = comment_text(lj)
                if t is None:
                    # End of comment block — but allow truly empty lines
                    # inside if the next line is also a comment.
                    if not lj.strip():
                        # Peek ahead for another comment.
                        k = i + 1
                        while k < n and not lines[k].strip():
                            k += 1
                        if k < n and comment_text(lines[k]) is not None and not is_banner_line(lines[k]) and not is_separator_line(lines[k]):
                            buf.append("")
                            i = k
                            continue
                    break
                buf.append(t)
                i += 1
            emit_prose(buf)
            continue

        # Code line (or empty line within a code stretch).
        # If we're not already in a code block and this line is empty, just skip.
        if not line.strip() and not code_buf:
            i += 1
            continue
        code_buf.append(line)
        i += 1

    flush_code()

    # Collapse multiple empty lines.
    cleaned: list[str] = []
    prev_empty = False
    for ln in out:
        if ln.strip() == "":
            if not prev_empty:
                cleaned.append("")
            prev_empty = True
        else:
            cleaned.append(ln)
            prev_empty = False
    return "\n".join(cleaned).strip() + "\n"


def main() -> None:
    files = sorted(LEHRBUCH.glob("*.strudel"))
    for src in files:
        text = src.read_text(encoding="utf-8")
        md = convert(text)
        dest = OUT / (src.stem + ".md")
        dest.write_text(md, encoding="utf-8")
        print(f"  {src.name} -> {dest.name} ({len(md)} chars)")


if __name__ == "__main__":
    main()
