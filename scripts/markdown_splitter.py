#!/usr/bin/env python3
"""Split a Markdown document into linked, topic-sized Markdown files.

First run:
  python scripts/markdown_splitter.py --source data_warehouse.md --output docs/data_warehouse

The source file becomes a generated index. The original Markdown is preserved as
<output>/_source.md and is the canonical input on subsequent runs. Edit that
file (or the generated topic files) rather than editing the generated index.

No third-party packages are required.
"""
from __future__ import annotations


import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Iterable


INDEX_MARKER = "<!-- markdown-splitter:index -->"
MANIFEST_NAME = "_manifest.json"
SOURCE_COPY_NAME = "_source.md"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")



def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[`*_~]", "", value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "topic"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def safe_relative(path: Path, base: Path) -> str:
    return Path(path).relative_to(base).as_posix()


def parse_sections(markdown: str) -> tuple[str, list[dict]]:
    """Split at H2 headings, respecting fenced code blocks.


    H1 is retained as document title/intro. Content before the first H2 is
    returned as preamble. Each H2 section stays intact, including its H3/H4s,
    code blocks, tables, lists and paragraphs.
    """
    lines = markdown.splitlines()
    preamble: list[str] = []
    sections: list[dict] = []
    current: dict | None = None
    fence_char: str | None = None
    fence_len = 0


    for line in lines:
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group(1)
            if fence_char is None:
                fence_char = fence[0]
                fence_len = len(fence)
            elif fence[0] == fence_char and len(fence) >= fence_len:
                fence_char = None
                fence_len = 0
            (current["lines"] if current else preamble).append(line)
            continue


        heading_match = HEADING_RE.match(line) if fence_char is None else None
        if heading_match and len(heading_match.group(1)) == 2:
            if current:
                sections.append(current)
            current = {
                "heading": heading_match.group(2).strip(),
                "lines": [line],
            }
        else:
            (current["lines"] if current else preamble).append(line)


    if current:
        sections.append(current)

    return "\n".join(preamble).strip(), sections



def category_for(heading: str, body: str) -> str:
    # Categorize from the heading, not the entire body. Body-based matching
    # causes unrelated sections to be classified as dimensions/facts merely
    # because they mention those concepts.
    text = heading.lower()
    if any(word in text for word in ("requirement", "business domain", "geography", "time horizon", "scale", "conversion logic", "product mix")):
        return "requirements"
    if re.search(r"\bdim(?:ension)?[_\s-]", text) or "dimension table" in text:
        return "dimensions"
    if re.search(r"\bfact[_\s-]", text) or any(word in text for word in ("billing", "enquiries", "production", "delivery challan", "gst invoice")):
        return "facts"
    if any(word in text for word in ("hidden trend", "analytical", "rural", "metro", "season", "dealer performance", "funnel physics", "data quality")):
        return "analytical_patterns"
    if any(word in text for word in ("warehouse structure", "warehouse overview", "architecture", "target warehouse", "star schema", "delivery plan")):
        return "architecture"
    return "topics"


def allocate_paths(sections: list[dict], output_dir: Path) -> None:
    used: set[str] = set()
    for section in sections:
        heading = section["heading"]
        body = "\n".join(section["lines"]).strip()
        category = category_for(heading, body)
        slug = slugify(heading)
        candidate = f"{category}/{slug}.md"
        if candidate in used:
            digest = sha256(heading + body)[:8]
            candidate = f"{category}/{slug}_{digest}.md"
        used.add(candidate)
        section["category"] = category
        section["relative_path"] = candidate


def make_topic_file(section: dict, source_path: Path, output_dir: Path) -> str:
    heading = section["heading"]
    content = "\n".join(section["lines"]).strip()
    topic_path = output_dir / section["relative_path"]
    # A generated file can be opened directly and still provide a route back.
    try:
        back_link = Path(__import__("os").path.relpath(source_path, topic_path.parent)).as_posix()
    except ValueError:
        back_link = source_path.as_posix()
    return (
        f"<!-- markdown-splitter:generated -->\n"
        f"[← Back to source index]({back_link})\n\n"
        f"{content}\n"
    )


def build_index(title: str, preamble: str, sections: list[dict], output_dir: Path, source_path: Path) -> str:
    title = title or source_path.stem.replace("_", " ").title()
    lines = [INDEX_MARKER, f"# {title}", "", "<!-- Generated by scripts/markdown_splitter.py. Edit _source.md to change source content. -->", ""]
    if preamble:
        lines.extend(["## Introduction", "", preamble, ""])

    grouped: dict[str, list[dict]] = {}
    for section in sections:
        grouped.setdefault(section["category"], []).append(section)

    category_titles = {
        "requirements": "Requirements",
        "architecture": "Architecture",
        "dimensions": "Dimensions",
        "facts": "Facts",
        "analytical_patterns": "Analytical Patterns",
        "topics": "Topics",
    }
    order = ["requirements", "architecture", "dimensions", "facts", "analytical_patterns", "topics"]
    for category in order:
        if category not in grouped:
            continue
        lines.extend([f"## {category_titles[category]}", ""] )
        for section in grouped[category]:
            target = output_dir / section["relative_path"]
            link = Path(__import__("os").path.relpath(target, source_path.parent)).as_posix()
            label = section["heading"].replace("[", "\\[").replace("]", "\\]")
            lines.append(f"- [{label}]({link})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def validate_links(markdown_files: Iterable[Path]) -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for file_path in markdown_files:
        text = file_path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            target = target.split("#", 1)[0]
            if not target or re.match(r"^[a-z]+://", target, re.I) or target.startswith("mailto:"):
                continue
            resolved = (file_path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{file_path}: broken link -> {target}")
    return errors


def run(args: argparse.Namespace) -> int:
    source_path = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    source_copy = output_dir / SOURCE_COPY_NAME

    if not source_path.exists():
        print(f"ERROR: Source file not found: {source_path}", file=sys.stderr)
        return 2

    current_source = source_path.read_text(encoding="utf-8")
    if INDEX_MARKER in current_source:
        if not source_copy.exists():
            print("ERROR: Source is a generated index, but _source.md is missing.", file=sys.stderr)
            print("Restore _source.md or replace the source with original Markdown.", file=sys.stderr)
            return 2
        markdown = source_copy.read_text(encoding="utf-8")
    else:
        markdown = current_source
        # Preserve the original before replacing it with a generated index.
        source_copy.write_text(markdown.rstrip() + "\n", encoding="utf-8")

    if args.validate:
        files = [source_path]
        files.extend(p for p in output_dir.rglob("*.md") if p.is_file())
        errors = validate_links(files)
        if errors:
            print("Link validation failed:", file=sys.stderr)
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("Markdown links validated successfully.")
        return 0

    preamble, sections = parse_sections(markdown)
    title_match = re.search(r"^#\s+(.+?)\s*#*\s*$", markdown, re.M)
    title = title_match.group(1).strip() if title_match else source_path.stem
    allocate_paths(sections, output_dir)


    # Keep a list of generated paths in the manifest so only our own outputs
    # can be removed when a source section is renamed or deleted.
    old_manifest_path = output_dir / MANIFEST_NAME
    old_generated: set[str] = set()
    if old_manifest_path.exists():
        try:
            old_manifest = json.loads(old_manifest_path.read_text(encoding="utf-8"))
            old_generated = set(old_manifest.get("generated_files", []))
        except (json.JSONDecodeError, OSError):
            print("WARNING: Could not read prior manifest; stale files will not be removed.", file=sys.stderr)

    generated: list[str] = []
    for section in sections:
        relative = section["relative_path"]
        target = output_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(make_topic_file(section, source_path, output_dir), encoding="utf-8")
        generated.append(relative)

    # Remove stale files only if the previous manifest explicitly owned them.
    for stale in old_generated - set(generated):
        stale_path = output_dir / stale
        if stale_path.exists() and stale_path.is_file():
            stale_path.unlink()

    index_text = build_index(title, preamble, sections, output_dir, source_path)
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(index_text, encoding="utf-8")

    manifest = {
        "version": 1,
        "source": source_path.as_posix(),
        "source_copy": source_copy.relative_to(output_dir).as_posix(),
        "source_sha256": sha256(markdown),
        "generated_files": generated,
    }
    old_manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    files_to_validate = [source_path]
    files_to_validate.extend(output_dir / path for path in generated)
    errors = validate_links(files_to_validate)
    if errors:
        print("Generated files, but link validation failed:", file=sys.stderr)
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Split {len(sections)} H2 sections into Markdown files.")
    print(f"Index: {source_path}")
    print(f"Generated content: {output_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Source Markdown file. Becomes a generated index.")
    parser.add_argument("--output", required=True, help="Directory for generated mini Markdown files.")
    parser.add_argument("--validate", action="store_true", help="Validate Markdown links only.")
    return run(parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
