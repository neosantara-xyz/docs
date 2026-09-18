#!/usr/bin/env python3
"""
Checks that snippet imports and usage in MDX files point to existing files in snippets/.
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent
SNIPPETS_DIR = DOCS_DIR / "snippets"

def main():
    if not SNIPPETS_DIR.exists():
        print(f"Error: {SNIPPETS_DIR} does not exist")
        sys.exit(1)

    import_regex = re.compile(r"import\s+(\w+)\s+from\s+['\"](/snippets/[^'\"]+)['\"]")
    errors = []
    checked_count = 0

    for mdx_file in DOCS_DIR.glob("**/*.mdx"):
        if mdx_file.is_relative_to(SNIPPETS_DIR):
            continue
        content = mdx_file.read_text(encoding="utf-8")
        for match in import_regex.finditer(content):
            component_name, snippet_path = match.groups()
            target_file = DOCS_DIR / snippet_path.lstrip("/")
            checked_count += 1
            if not target_file.exists():
                errors.append(
                    f"In {mdx_file.relative_to(DOCS_DIR)}: snippet not found '{snippet_path}' (imported as {component_name})"
                )

    print(f"Checked {checked_count} snippet imports.")
    if errors:
        print("\nSnippet validation errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    print("Snippet checks passed.")

if __name__ == "__main__":
    main()
