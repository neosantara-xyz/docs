#!/usr/bin/env python3
"""
Fetches active model catalog directly from the live Neosantara API endpoint
(https://api.neosantara.xyz/v1/models) or local gateway catalog and generates
up-to-date Markdown table snippets in snippets/ (e.g. models-table.mdx, models-reasoning-table.mdx).

Strictly filters for non-deprecated, user-facing listed models and resolves internal
provider names to public brands.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent
GATEWAY_DIR = DOCS_DIR.parent
SNIPPETS_DIR = DOCS_DIR / "snippets"
BASE_URL = os.environ.get("NEOSANTARA_BASE_URL", "https://api.neosantara.xyz/v1")
API_KEY = os.environ.get("NEOSANTARA_API_KEY", "")

CAPABILITY_PRESETS = {
    "all": {
        "filename": "models-table.mdx",
        "filter": lambda m: True,
        "title": "Semua Model Aktif",
        "description": "Seluruh model aktif yang tersedia di Neosantara"
    },
    "reasoning": {
        "filename": "models-reasoning-table.mdx",
        "filter": lambda m: "reasoning" in m.get("capabilities", []),
        "title": "Model Penalaran (Reasoning)",
        "description": "Model yang mendukung rantai pemikiran (chain-of-thought) dan parameter reasoning effort"
    },
    "vision": {
        "filename": "models-vision-table.mdx",
        "filter": lambda m: "vision" in m.get("capabilities", []),
        "title": "Model Multimodal (Vision)",
        "description": "Model yang mendukung input gambar dan analisis visual dokumen"
    },
    "tools": {
        "filename": "models-tools-table.mdx",
        "filter": lambda m: any(c in m.get("capabilities", []) for c in ["function_calling", "tool_calling"]),
        "title": "Model Tool Calling",
        "description": "Model yang mendukung function calling dan pemanggilan tools eksternal"
    },
    "json": {
        "filename": "models-json-table.mdx",
        "filter": lambda m: any(c in m.get("capabilities", []) for c in ["structured_outputs", "json_mode", "structured_output"]),
        "title": "Model Output Terstruktur",
        "description": "Model yang mendukung respons JSON mode dan pemenuhan skema ketat"
    },
    "embeddings": {
        "filename": "models-embeddings-table.mdx",
        "filter": lambda m: "embeddings" in m.get("capabilities", []),
        "title": "Model Embeddings",
        "description": "Model representasi vektor teks untuk pencarian semantik dan pipeline RAG"
    },
    "image": {
        "filename": "models-image-table.mdx",
        "filter": lambda m: "image_generation" in m.get("capabilities", []),
        "title": "Model Generasi Gambar",
        "description": "Model pembuatan gambar visual dari teks via /v1/images/generations"
    },
    "ocr": {
        "filename": "models-ocr-table.mdx",
        "filter": lambda m: "ocr" in m.get("capabilities", []),
        "title": "Model OCR",
        "description": "Model ekstraksi teks dan formulir terstruktur via /v1/ocr"
    },
    "audio": {
        "filename": "models-audio-table.mdx",
        "filter": lambda m: "audio_transcription" in m.get("capabilities", []),
        "title": "Model Audio & Transkripsi",
        "description": "Model pemrosesan suara dan transkripsi via /v1/audio"
    }
}

def resolve_public_owner(m_id, owned_by=""):
    m_id_lower = m_id.lower()
    owned_lower = (owned_by or "").lower()
    
    if m_id_lower.startswith(("nusantara", "garda", "archipelago", "vision-emas", "neosantara", "nusa-embedding")):
        return "Neosantara"
    if "sahabatai" in m_id_lower or "sahabat" in m_id_lower:
        return "GoTo"
    if "sea-lion" in m_id_lower:
        return "AI Singapore"
    if any(k in m_id_lower for k in ["glm", "cogview", "cogvideo", "z.ai"]):
        return "zAI"
    if "kimi" in m_id_lower:
        return "Moonshot"
    if "gemini" in m_id_lower or "gemma" in m_id_lower or "imagen" in m_id_lower:
        return "Google"
    if "nemotron" in m_id_lower:
        return "NVIDIA"
    if "llama" in m_id_lower or "muse" in m_id_lower:
        return "Meta"
    if "gpt" in m_id_lower or "text-embedding" in m_id_lower or "whisper" in m_id_lower:
        return "OpenAI"
    if "claude" in m_id_lower:
        return "Anthropic"
    if "mistral" in m_id_lower or "magistral" in m_id_lower or "devstral" in m_id_lower or "codestral" in m_id_lower:
        return "Mistral AI"
    if "command" in m_id_lower or "embed-multilingual" in m_id_lower:
        return "Cohere"
    if "grok" in m_id_lower:
        return "xAI"
    if "mimo" in m_id_lower or "xiaomi" in m_id_lower:
        return "Xiaomi"
    if "qwen" in m_id_lower or "tongyi" in m_id_lower:
        return "Alibaba Cloud"
    if "deepseek" in m_id_lower:
        return "DeepSeek"
    if "granite" in m_id_lower:
        return "IBM"
    if "longcat" in m_id_lower or "meituan" in m_id_lower:
        return "Meituan"
    if "pollinations" in m_id_lower:
        return "Pollinations AI"
    if "titan" in m_id_lower or "nova" in m_id_lower or "luma" in m_id_lower or "bedrock" in owned_lower:
        return "Amazon"
    if "stable-diffusion" in m_id_lower or "sdxl" in m_id_lower:
        return "Stability AI"
    if "laguna" in m_id_lower or "poolside" in m_id_lower:
        return "Poolside"
    if "minimax" in m_id_lower:
        return "MiniMax"
    if "bonsai" in m_id_lower or "prism" in m_id_lower:
        return "Prism ML"
    if "cerebras" in m_id_lower:
        return "Cerebras"
    if "agnes" in m_id_lower:
        return "Agnes AI"
    if "nv-embed" in m_id_lower:
        return "NVIDIA"
    if "ling" in m_id_lower or "inclusionai" in m_id_lower:
        return "InclusionAI"
    if "step" in m_id_lower:
        return "StepFun"
        
    return owned_by.capitalize() if owned_by else "Neosantara"

def fetch_models_from_api(base_url=BASE_URL, api_key=API_KEY):
    url = f"{base_url.rstrip('/')}/models"
    headers = {"User-Agent": "Neosantara-DocSync/1.0"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", [])
    except Exception as e:
        print(f"Notice: Could not fetch from live endpoint {url}: {e}")
        return None

def load_models_from_local_catalog():
    try:
        script = """
        const { INDONESIA_MODELS } = require('./Nusantara/models');
        const list = Object.entries(INDONESIA_MODELS)
          .filter(([_, m]) => m.listed === true)
          .map(([id, m]) => ({
            id,
            owned_by: m.owned_by || m.provider,
            context_window: m.context_window || m.contextWindow || (m.max_tokens ? m.max_tokens * 4 : 128000),
            capabilities: m.capabilities || [],
            pricing: m.pricing,
            deprecated: Boolean(m.deprecated),
            listed: m.listed !== false
          }));
        console.log(JSON.stringify(list));
        """
        res = subprocess.run(["node", "-e", script], cwd=str(GATEWAY_DIR), capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Notice: Could not load local catalog: {e}")
        return None

def format_context(ctx):
    if not ctx:
        return "N/A"
    if isinstance(ctx, int):
        if ctx >= 1_000_000:
            return f"{ctx / 1_000_000:.1f}M tokens".replace(".0M", "M")
        elif ctx >= 1_000:
            return f"{ctx // 1_000}k tokens"
        return f"{ctx:,} tokens"
    return str(ctx)

def format_pricing(pricing):
    if not pricing or not isinstance(pricing, dict):
        return "-"
    curr = pricing.get("currency", "USD")
    if "per_second" in pricing:
        sec = pricing["per_second"]
        if curr == "USD":
            return f"${str(sec).lstrip('$')}/sec"
        try:
            return f"Rp {int(sec):,}/sec"
        except Exception:
            return f"Rp {sec}/sec"
    if "per_image" in pricing:
        img = pricing["per_image"]
        if isinstance(img, dict):
            img = img.get("1024x1024") or (next(iter(img.values())) if img else 0)
        if curr == "USD":
            return f"${str(img).lstrip('$')}/img"
        try:
            return f"Rp {int(img):,}/img"
        except Exception:
            return f"Rp {img}/img"
        
    prompt = pricing.get("prompt")
    completion = pricing.get("completion")
    
    # Check nested per_million_tokens
    if prompt is None and "per_million_tokens" in pricing:
        prompt = pricing["per_million_tokens"].get("input", 0)
        completion = pricing["per_million_tokens"].get("output", 0)
        
    if prompt or completion:
        if curr == "USD":
            p_str = str(prompt).lstrip("$")
            c_str = str(completion).lstrip("$")
            return f"${p_str} / ${c_str}"
        try:
            p_val = int(prompt) if float(prompt).is_integer() else prompt
            c_val = int(completion) if float(completion).is_integer() else completion
            return f"Rp {p_val:,} / Rp {c_val:,}"
        except Exception:
            return f"Rp {prompt} / Rp {completion}"
    return "Free / Included"

def format_capabilities(caps):
    if not caps:
        return "Text"
    labels = []
    if any(k in caps for k in ["function_calling", "tool_calling"]):
        labels.append("Tools")
    if "vision" in caps:
        labels.append("Vision")
    if "reasoning" in caps:
        labels.append("Reasoning")
    if any(k in caps for k in ["structured_outputs", "json_mode", "structured_output"]):
        labels.append("JSON")
    if "embeddings" in caps:
        labels.append("Embeddings")
    if "image_generation" in caps:
        labels.append("Image Gen")
    if "ocr" in caps:
        labels.append("OCR")
    if "audio_transcription" in caps:
        labels.append("Audio")
    return ", ".join(labels) if labels else "Text"

def generate_markdown(models):
    processed = []
    for m in models:
        m_id = m.get("id", "")
        owner = resolve_public_owner(m_id, m.get("owned_by", ""))
        ctx = format_context(m.get("context_window"))
        caps = format_capabilities(m.get("capabilities", []))
        price = format_pricing(m.get("pricing"))
        processed.append((owner, m_id, ctx, caps, price))
        
    # Sort by owner, then model id
    processed.sort(key=lambda x: (x[0].lower(), x[1].lower()))

    lines = [
        "| Model ID | Provider | Context Window | Capabilities | Pricing (Input/Output per 1M) |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for owner, m_id, ctx, caps, price in processed:
        lines.append(f"| `{m_id}` | {owner} | {ctx} | {caps} | {price} |")

    return "\n".join(lines) + "\n"

def sync_capability_snippet(models, preset_key, preset_cfg, output_path=None):
    filter_fn = preset_cfg["filter"]
    filtered_models = [m for m in models if filter_fn(m)]
    
    target_file = Path(output_path) if output_path else (SNIPPETS_DIR / preset_cfg["filename"])
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    md = generate_markdown(filtered_models)
    target_file.write_text(md, encoding="utf-8")
    print(f"[{preset_key.upper()}] Written {len(filtered_models)} active models to {target_file.relative_to(DOCS_DIR)}")
    return len(filtered_models)

def list_capabilities(models):
    caps_count = {}
    for m in models:
        for c in m.get("capabilities", []):
            caps_count[c] = caps_count.get(c, 0) + 1
            
    print("\nCapabilities breakdown for active non-deprecated models:")
    print("=" * 60)
    for cap, count in sorted(caps_count.items(), key=lambda x: x[1], reverse=True):
        print(f" - {cap:<25}: {count:>3} models")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(
        description="Sync model tables and capability snippets directly from /v1/models"
    )
    parser.add_argument(
        "-c", "--capability",
        help=f"Filter by capability preset ({', '.join(CAPABILITY_PRESETS.keys())}) or custom capability name"
    )
    parser.add_argument(
        "-o", "--output",
        help="Custom output file path (useful when generating a single capability snippet)"
    )
    parser.add_argument(
        "--include-deprecated",
        action="store_true",
        help="Include deprecated models (excluded by default)"
    )
    parser.add_argument(
        "--base-url",
        default=BASE_URL,
        help="Neosantara API base URL"
    )
    parser.add_argument(
        "--api-key",
        default=API_KEY,
        help="Neosantara API Key (optional)"
    )
    parser.add_argument(
        "--list-capabilities",
        action="store_true",
        help="List all capabilities available across active models and exit"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Sync models-table.mdx and all capability presets into snippets/"
    )

    args = parser.parse_args()
    SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Fetch raw models
    raw_models = fetch_models_from_api(base_url=args.base_url, api_key=args.api_key)
    if not raw_models:
        print("Falling back to local gateway catalog...")
        raw_models = load_models_from_local_catalog()

    if not raw_models:
        print("Error: Could not retrieve models from either API or local catalog.")
        sys.exit(1)

    # 2. Filter active, non-deprecated, listed models
    active_models = [
        m for m in raw_models
        if (args.include_deprecated or not m.get("deprecated", False))
        and (m.get("listed") is not False)
    ]

    print(f"Loaded {len(active_models)} active non-deprecated listed models.")

    # 3. Handle --list-capabilities
    if args.list_capabilities:
        list_capabilities(active_models)
        return

    # 4. Handle specific capability request
    if args.capability:
        cap_key = args.capability.lower()
        if cap_key in CAPABILITY_PRESETS:
            preset = CAPABILITY_PRESETS[cap_key]
        else:
            # Dynamic custom capability filter
            preset = {
                "filename": f"models-{cap_key}-table.mdx",
                "filter": lambda m: cap_key in m.get("capabilities", []),
                "title": f"Model {cap_key.capitalize()}",
                "description": f"Model dengan kapabilitas {cap_key}"
            }
        sync_capability_snippet(active_models, cap_key, preset, output_path=args.output)
        return

    # 5. Default or --all: generate all presets
    print(f"\nGenerating all model snippets to {SNIPPETS_DIR.relative_to(DOCS_DIR)}/...")
    print("-" * 60)
    for key, preset in CAPABILITY_PRESETS.items():
        sync_capability_snippet(active_models, key, preset)
    print("-" * 60)
    print("All model capability snippets generated successfully.\n")

if __name__ == "__main__":
    main()
