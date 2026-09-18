#!/usr/bin/env python3
"""
Validates docs.json navigation entries against filesystem MDX pages,
detects orphaned MDX pages, and checks for broken internal links.
Supports single-language and multilingual (navigation.languages) configs.
"""

import json
import os
import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent

def extract_pages(nav_obj):
    pages = []
    if isinstance(nav_obj, list):
        for item in nav_obj:
            pages.extend(extract_pages(item))
    elif isinstance(nav_obj, dict):
        if "languages" in nav_obj:
            pages.extend(extract_pages(nav_obj["languages"]))
        if "tabs" in nav_obj:
            pages.extend(extract_pages(nav_obj["tabs"]))
        if "groups" in nav_obj:
            pages.extend(extract_pages(nav_obj["groups"]))
        if "pages" in nav_obj:
            pages.extend(extract_pages(nav_obj["pages"]))
        if "page" in nav_obj and isinstance(nav_obj["page"], str):
            pages.append(nav_obj["page"])
        if "root" in nav_obj and isinstance(nav_obj["root"], str):
            pages.append(nav_obj["root"])
    elif isinstance(nav_obj, str):
        pages.append(nav_obj)
    return pages

def main():
    docs_json_path = DOCS_DIR / "docs.json"
    if not docs_json_path.exists():
        print(f"Error: {docs_json_path} not found")
        sys.exit(1)

    with open(docs_json_path, "r", encoding="utf-8") as f:
        docs_data = json.load(f)

    nav = docs_data.get("navigation", {})
    referenced_pages = extract_pages(nav)
    print(f"Loaded {len(referenced_pages)} page references from docs.json")

    errors = []

    openapi_spec = {}
    openapi_path = DOCS_DIR / "api-reference" / "openapi.json"
    if openapi_path.exists():
        try:
            openapi_spec = json.loads(openapi_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    openapi_paths = openapi_spec.get("paths", {})

    # 1. Check that all referenced pages exist
    for page in referenced_pages:
        if page.startswith("http://") or page.startswith("https://"):
            continue
        endpoint_match = re.match(r"^(GET|POST|PUT|DELETE|PATCH)\s+(/\S*)", page)
        if endpoint_match:
            method, ep_path = endpoint_match.groups()
            method_lower = method.lower()
            if ep_path not in openapi_paths or method_lower not in openapi_paths[ep_path]:
                errors.append(f"Referenced OpenAPI endpoint not found in spec: {page}")
            continue
        page_clean = page.lstrip("/")
        mdx_path = DOCS_DIR / f"{page_clean}.mdx"
        md_path = DOCS_DIR / f"{page_clean}.md"
        if not (mdx_path.exists() or md_path.exists()):
            errors.append(f"Missing page in filesystem: {page} (expected {mdx_path})")

    # 2. Check for orphaned MDX files (excluding snippets and snippets)
    all_mdx_files = list(DOCS_DIR.glob("**/*.mdx"))
    for file in all_mdx_files:
        rel = file.relative_to(DOCS_DIR).as_posix()
        if rel.startswith("snippets/") or rel.startswith("snippets/"):
            continue
        stem = rel[:-4]
        if stem not in referenced_pages and f"/{stem}" not in referenced_pages:
            print(f"[Notice] Orphaned page not in docs.json: {rel}")

    # 3. Check for broken internal links in markdown and frontmatter related topics
    link_pattern = re.compile(r'\[([^\]]+)\]\((/[^)]+)\)')
    for file in all_mdx_files:
        content = file.read_text(encoding="utf-8")
        links_to_check = []
        for match in link_pattern.finditer(content):
            links_to_check.append(match.group(2))

        # Check frontmatter 'related' links
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            related_match = re.search(r'related:\s*\n((?:\s*-\s*.*\n?)*)', fm)
            if related_match:
                for line in related_match.group(1).splitlines():
                    line = line.strip()
                    if line.startswith("-"):
                        val = line[1:].strip()
                        if ":" in val and not val.startswith(("http://", "https://")):
                            parts = val.split(":", 1)
                            val = parts[1].strip()
                        if val.startswith("/") and not val.startswith("//"):
                            links_to_check.append(val)

        for raw_link in links_to_check:
            target_url = raw_link.split("#")[0].lstrip("/")
            if not target_url:
                continue
            target_mdx = DOCS_DIR / f"{target_url}.mdx"
            target_index = DOCS_DIR / target_url / "index.mdx"
            # In multilingual Mintlify, links can be root-relative to language prefix
            # or directly without prefix if rewritten
            if not (target_mdx.exists() or target_index.exists() or (DOCS_DIR / target_url).exists()):
                # Try relative to current file language if applicable
                rel_parts = file.relative_to(DOCS_DIR).parts
                lang_prefix = rel_parts[0] if rel_parts and rel_parts[0] in ("en", "id") else ""
                if lang_prefix:
                    alt_target = DOCS_DIR / lang_prefix / f"{target_url}.mdx"
                    if alt_target.exists():
                        continue
                errors.append(f"Broken link in {file.relative_to(DOCS_DIR)}: {raw_link}")

    # 4. Check that all icons in docs.json and MDX exist in Lucide icon library
    lucide_dir = DOCS_DIR.parent / "dashboard" / "node_modules" / "lucide-react" / "dist" / "esm" / "icons"
    if lucide_dir.exists():
        lucide_icons = set(f.stem for f in lucide_dir.glob("*.js"))
        # Check docs.json icons
        def check_json_icons(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    curr_path = f"{path}.{k}" if path else k
                    if k == "icon" and isinstance(v, str):
                        if v not in lucide_icons:
                            errors.append(f"Invalid Lucide icon \"{v}\" in docs.json at {curr_path}")
                    else:
                        check_json_icons(v, curr_path)
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    check_json_icons(item, f"{path}[{idx}]")

        check_json_icons(docs_data)

        # Check MDX icons
        for file in all_mdx_files:
            file_content = file.read_text(encoding="utf-8")
            fm_m = re.match(r"^---\s*\n(.*?)\n---", file_content, re.DOTALL)
            if fm_m:
                im = re.search(r"^icon:\s*[\"\x27]?([a-zA-Z0-9_-]+)[\"\x27]?", fm_m.group(1), re.MULTILINE)
                if im and im.group(1) not in lucide_icons:
                    errors.append(f"Invalid Lucide frontmatter icon \"{im.group(1)}\" in {file.relative_to(DOCS_DIR)}")
            # Check component icons (<Card icon="...", <Icon icon="...", etc.)
            for comp_m in re.finditer(r"<[A-Za-z0-9]+\s+[^>]*\bicon=[\"\x27]([a-zA-Z0-9_-]+)[\"\x27]", file_content):
                ic_name = comp_m.group(1)
                if ic_name not in lucide_icons:
                    errors.append(f"Invalid Lucide component icon \"{ic_name}\" in {file.relative_to(DOCS_DIR)}")

    if errors:
        print("\nValidation Failed:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)

    print("All docs.json page references, icons, and internal links verified successfully.")

if __name__ == "__main__":
    main()
