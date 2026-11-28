"""Generate the pill-shaped tag SVGs used in README.md.

Usage: python3 pills/make_pills.py
Add or rename a tag in TAGS, rerun, and reference pills/<slug>.svg from README.md.
"""

import re
from pathlib import Path

from PIL import ImageFont

FONT_PATH = "/usr/share/fonts/truetype/msttcorefonts/arial.ttf"
BOLD_FONT_PATH = "/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf"
TITLE = "Servus!"
TITLE_SIZE = 64
TITLE_COLORS = {"dark": "#E6EDF3", "light": "#1F2328"}
FONT_SIZE = 11
HEIGHT = 20
PAD_X = 9
DOT_R = 3
DOT_GAP = 6

STYLES = {
    "math": {"fill": "#2B2640", "stroke": "#4A3F70", "text": "#DCD3F5"},
    "physics": {"fill": "#1E2939", "stroke": "#3A5478", "text": "#CFDDF2"},
    "cs": {"fill": "#22272E", "stroke": "#3D444D", "text": "#D6DCE2"},
    "master": {"fill": "#1E2A24", "stroke": "#3A5A48", "text": "#D2E6D9"},
}

LANG_DOTS = {
    "C++": "#F34B7D",
    "Java": "#B07219",
    "Python": "#3572A5",
    "Basics in C#": "#178600",
    "JavaScript": "#F1E05A",
    "TypeScript": "#3178C6",
    "PHP": "#4F5D95",
    "Rust": "#DEA584",
    "TypeScript Academy · CoddyKit": "#3178C6",
    "Problem Solving (Basic) · HackerRank": "#2EC866",
}

TAGS = {
    "math": [
        "Discrete Structures",
        "Analytical Geometry",
        "Linear Algebra",
        "Statistics",
        "Calculus 1",
        "Calculus 2",
        "Calculus 3",
        "Differential Equations",
        "Numerical Analysis",
    ],
    "physics": [
        "Mechanics & Thermodynamics",
        "Electromagnetism, Relativity & Quantum Physics",
    ],
    "cs": [
        "C++",
        "Java",
        "Python",
        "Basics in C#",
        "Data Structures",
        "Computer Architecture",
        "Operating Systems",
        "Artificial Intelligence",
        "Software Engineering",
        "Database Design and Management",
        "Introduction to Data Mining",
        "JavaScript",
        "TypeScript",
        "PHP",
        "Rust",
        "TypeScript Academy · CoddyKit",
        "Problem Solving (Basic) · HackerRank",
    ],
    "master": [
        "Software Technologies: Advanced Topics",
        "Software Technologies 2 (Project)",
        "Models of Software Systems",
        "Service-Based Software Systems",
        "Software Systems Architectures",
        "Software Systems Patterns",
        "Object-Oriented Analysis & Design",
        "Internet Technologies & Web Programming",
        "Machine Learning",
        "Project Management",
        "Technology Entrepreneurship 1",
        "Technology Entrepreneurship 2",
        "Professional Ethics",
        "Organizational Behavior & Leadership",
    ],
}


def slug(label):
    s = label.replace("C++", "cpp").replace("C#", "csharp")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pill(label, style, font):
    text_w = round(font.getlength(label))
    dot = LANG_DOTS.get(label)
    left = PAD_X + (DOT_R * 2 + DOT_GAP if dot else 0)
    width = left + text_w + PAD_X
    r = HEIGHT / 2
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{HEIGHT}" '
        f'viewBox="0 0 {width} {HEIGHT}" role="img" aria-label="{escape(label)}">',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{HEIGHT - 1}" rx="{r - 0.5}" '
        f'fill="{style["fill"]}" stroke="{style["stroke"]}"/>',
    ]
    if dot:
        parts.append(f'<circle cx="{PAD_X + DOT_R}" cy="{r}" r="{DOT_R}" fill="{dot}"/>')
    parts.append(
        f'<text x="{left}" y="{r}" dominant-baseline="central" fill="{style["text"]}" '
        f'font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif" '
        f'font-size="{FONT_SIZE}" textLength="{text_w}" lengthAdjust="spacingAndGlyphs">'
        f"{escape(label)}</text>"
    )
    parts.append("</svg>")
    return "".join(parts)


def title(text, color, font):
    ascent, _ = font.getmetrics()
    left, top, right, _ = font.getbbox(text)
    width = right - left + 2
    baseline = ascent - top + 1
    height = baseline + 1
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(text)}">'
        f'<text x="1" y="{baseline}" fill="{color}" font-weight="700" '
        f'font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif" '
        f'font-size="{TITLE_SIZE}" textLength="{width - 2}" lengthAdjust="spacingAndGlyphs">'
        f"{escape(text)}</text></svg>"
    )


def main():
    out = Path(__file__).parent
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    for group, labels in TAGS.items():
        for label in labels:
            (out / f"{slug(label)}.svg").write_text(pill(label, STYLES[group], font) + "\n")
    bold = ImageFont.truetype(BOLD_FONT_PATH, TITLE_SIZE)
    for theme, color in TITLE_COLORS.items():
        (out / f"title-{theme}.svg").write_text(title(TITLE, color, bold) + "\n")


if __name__ == "__main__":
    main()
