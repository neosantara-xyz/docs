#!/usr/bin/env python3
"""
Syncs OpenAPI spec from the gateway codebase into new-docs/api-reference/openapi.json.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent
TARGET_PATH = DOCS_DIR / "api-reference" / "openapi.json"
LOCAL_SOURCE = Path("/root/nusantaraai/openapi.json")
LIVE_URL = "https://api.neosantara.xyz/openapi.json"

EXCLUDED_PATHS = {
    "/v1/api/v1/stats/public/exchange-rate",
    "/v1/api/v1/stats/models",
    "/v1/api/v1/stats/catalog",
    "/v1/api/v1/utils/cost-estimate",
    "/v1/public/exchange-rate",
    "/v1/catalog",
    "/v1/conversations",
    "/v1/cursor/chat/completions",
    "/v1/openrouter/models",
    "/v1/system/status",
    "/v1/completions",
    "/v1/cost-estimate",
    "/v1/mcp/keys",
}

def clean_spec(spec: dict) -> dict:
    # Filter out internal/unlisted endpoints
    if "paths" in spec:
        spec["paths"] = {
            path: item
            for path, item in spec["paths"].items()
            if path not in EXCLUDED_PATHS
        }

    # Normalize code snippet models to flagship listed models
    spec_str = json.dumps(spec, ensure_ascii=False)
    spec_str = spec_str.replace("gemini-3-flash", "gemini-3.8-flash")
    spec_str = spec_str.replace("claude-4.5-sonnet", "deepseek-v4.1-flash")
    spec_str = spec_str.replace("claude-sonnet-4-6", "deepseek-v4.1-flash")
    return json.loads(spec_str)

def main():
    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_spec = None

    if LOCAL_SOURCE.exists():
        print(f"Reading OpenAPI spec from local source: {LOCAL_SOURCE}")
        with open(LOCAL_SOURCE, "r", encoding="utf-8") as f:
            raw_spec = json.load(f)
    else:
        print(f"Local file not found, fetching from live endpoint: {LIVE_URL}")
        try:
            req = urllib.request.Request(LIVE_URL, headers={"User-Agent": "Neosantara-DocSync/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw_spec = json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"Error fetching from live endpoint: {e}")
            sys.exit(1)

    # Filter internal endpoints & update flagship models
    clean = clean_spec(raw_spec)

    # Ensure canonical production server
    clean["servers"] = [
        {"url": "https://api.neosantara.xyz", "description": "Neosantara Production Gateway"}
    ]

    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)

    print(f"Successfully synced OpenAPI spec to: {TARGET_PATH}")

if __name__ == "__main__":
    main()
