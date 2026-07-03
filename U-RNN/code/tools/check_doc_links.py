"""Documentation link integrity checker for the U-RNN repository.

Purpose
-------
Validate every Markdown document in the repo so the README + ``tutorials/``
split never ships a broken link. There is no unit-test surface for docs, so
this script is the "run a check, don't assume" gate for documentation changes.

Checks
------
1. Relative file links/images resolve to an existing file
   (catches wrong ``../../`` depth, sibling typos, broken ``code/``/``figs/`` paths).
   Both Markdown ``[text](path)`` / ``![alt](path)`` and inline HTML
   ``src="..."`` / ``href="..."`` are inspected.
2. Fragment links (``file.md#anchor`` and same-file ``#anchor``) point at a real
   heading, using GitHub's heading-slug rules.
3. Stale-pattern sweep across all Markdown for references that should no longer
   exist after the migration: ``Section <N>``, ``README.md#...``,
   ``U-RNN#<N>``, ``](#<N>...``.

Arguments
---------
``root`` (positional, optional): directory to scan. Defaults to the repository
root (the parent of the ``code/`` directory that holds this script).

Output
------
Prints every problem as ``path:line: reason`` and a final summary. Exit code is
0 when clean, 1 when any broken link or stale reference is found.

Usage
-----
    cd code && python tools/check_doc_links.py ..      # scan whole repo
    python code/tools/check_doc_links.py               # same, run from repo root
    python code/tools/check_doc_links.py tutorials     # scan a subtree
"""

from __future__ import annotations

import os
import re
import sys

# Directories never worth scanning (artifacts, data, vendored, private).
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".claude", ".vscode",
    "exp", "data", "build", "dist", "wandb", ".ipynb_checkpoints",
    ".egg-info",
}

# Markdown link/image: capture the target inside (...).
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
# Inline HTML attributes used in the docs (img src, a href).
ATTR_RE = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"')
# ATX heading.
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")

# Stale references that must be empty after the README -> tutorials migration.
STALE_PATTERNS = [
    re.compile(r"Section\s+\d+"),
    re.compile(r"README\.md#"),
    re.compile(r"U-RNN#\d"),
    re.compile(r"\]\(#\d"),
]

SKIP_LINK_PREFIXES = ("http://", "https://", "mailto:", "tel:", "//", "data:")


def slugify(heading: str) -> str:
    """Approximate GitHub's anchor slug for a heading line."""
    text = heading.strip().lower()
    # Drop inline code backticks and markdown link syntax, keep visible text.
    text = text.replace("`", "")
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Remove anything that is not a word char (unicode), whitespace or hyphen.
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "-")


def heading_slugs(path: str) -> set:
    """All heading anchors defined in a Markdown file (with de-dup suffixes)."""
    slugs = set()
    counts = {}
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                m = HEADING_RE.match(line)
                if not m:
                    continue
                base = slugify(m.group(1))
                n = counts.get(base, 0)
                slug = base if n == 0 else f"{base}-{n}"
                counts[base] = n + 1
                slugs.add(slug)
    except OSError:
        pass
    return slugs


def find_md_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.endswith(".egg-info")
        ]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def iter_targets(line: str):
    for m in LINK_RE.finditer(line):
        yield m.group(1).strip()
    for m in ATTR_RE.finditer(line):
        yield m.group(1).strip()


def check_file(path: str, problems: list):
    md_dir = os.path.dirname(path)
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    own_slugs = None  # lazily computed for same-file fragments

    for lineno, line in enumerate(lines, 1):
        for pat in STALE_PATTERNS:
            if pat.search(line):
                problems.append((path, lineno, f"stale reference: {pat.pattern!r} in {line.strip()!r}"))
        for raw in iter_targets(line):
            # Strip optional link title:  (path "title")
            target = raw.split()[0] if raw else raw
            if not target or target.startswith("#"):
                frag = target[1:]
                if frag:
                    nonlocal_slugs = heading_slugs(path)
                    if frag not in nonlocal_slugs:
                        problems.append((path, lineno, f"missing same-file anchor #{frag}"))
                continue
            if target.startswith(SKIP_LINK_PREFIXES):
                continue
            file_part, _, frag = target.partition("#")
            file_part = file_part.split("?")[0]
            if not file_part:
                continue
            resolved = os.path.normpath(os.path.join(md_dir, file_part))
            if not os.path.exists(resolved):
                problems.append((path, lineno, f"broken link target: {target}"))
                continue
            if frag and resolved.lower().endswith(".md"):
                if frag not in heading_slugs(resolved):
                    problems.append((path, lineno, f"missing anchor #{frag} in {file_part}"))


def main(argv):
    if len(argv) > 1:
        root = argv[1]
    else:
        # repo root = parent of the code/ dir that contains this script
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root = os.path.abspath(root)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}")
        return 2

    problems: list = []
    md_files = sorted(find_md_files(root))
    for path in md_files:
        check_file(path, problems)

    rel = lambda p: os.path.relpath(p, root)
    broken = [p for p in problems if "broken link" in p[2] or "missing anchor" in p[2]]
    stale = [p for p in problems if "stale reference" in p[2]]

    for path, lineno, reason in problems:
        print(f"{rel(path)}:{lineno}: {reason}")

    print(f"\nScanned {len(md_files)} Markdown files under {root}")
    print(f"{len(broken)} broken links/anchors, {len(stale)} stale refs")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
