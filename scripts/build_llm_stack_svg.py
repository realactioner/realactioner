"""Build llm-agent-stack.svg using skillicons.dev grid + scale (see skill-icons index.js)."""
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent / "assets" / "skills"
FILES = [
    "openai-colored.svg",
    "langchain-colored.svg",
    "langgraph-colored.svg",
    "crewai-colored.svg",
    "huggingface-colored.svg",
]

PER_LINE = 15  # match skillicons ICONS_PER_LINE (we only use one row)
ONE_ICON = 48
SCALE = ONE_ICON / (300 - 44)


def inner_body(path: Path) -> str:
    t = path.read_text(encoding="utf-8").strip()
    t = re.sub(r"^<svg[^>]*>\s*", "", t, count=1)
    t = re.sub(r"\s*</svg>\s*$", "", t, count=1)
    t = re.sub(r"\s*<title>.*?</title>\s*", "", t, count=1, flags=re.DOTALL)
    return t.strip()


def main() -> None:
    n = len(FILES)
    length = min(PER_LINE * 300, n * 300) - 44
    row_count = (n + PER_LINE - 1) // PER_LINE
    height = row_count * 300 - 44
    scaled_w = length * SCALE
    scaled_h = height * SCALE
    w_attr = int(scaled_w) if scaled_w == int(scaled_w) else scaled_w
    h_attr = int(scaled_h) if scaled_h == int(scaled_h) else scaled_h

    groups = []
    for i, name in enumerate(FILES):
        body = inner_body(SKILLS_DIR / name)
        x = (i % PER_LINE) * 300
        y = (i // PER_LINE) * 300
        groups.append(f'  <g transform="translate({x},{y})">\n{body}\n  </g>')

    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w_attr}" height="{h_attr}" '
        f'viewBox="0 0 {length} {height}" fill="none" version="1.1" role="img">\n'
        f"  <title>LLM &amp; Agent Stack</title>\n"
        + "\n".join(groups)
        + "\n</svg>\n"
    )

    dest = SKILLS_DIR / "llm-agent-stack.svg"
    dest.write_text(out, encoding="utf-8")
    print(f"Wrote {dest} viewBox 0 0 {length} {height} size {w_attr}x{h_attr}")


if __name__ == "__main__":
    main()
