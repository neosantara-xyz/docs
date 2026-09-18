import json
import os

DOCS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT_DIR = os.path.join(os.path.dirname(DOCS_DIR), "external-docs")

# 1. Load docs.json
docs_json_path = os.path.join(DOCS_DIR, "docs.json")
with open(docs_json_path, "r", encoding="utf-8") as f:
    new_docs = json.load(f)

with open(os.path.join(EXT_DIR, "docs.json"), "r", encoding="utf-8") as f:
    ext_docs = json.load(f)

def extract_pages(nav):
    pages = []
    if isinstance(nav, dict):
        for k, v in nav.items():
            pages.extend(extract_pages(v))
    elif isinstance(nav, list):
        for item in nav:
            if isinstance(item, str):
                pages.append(item)
            else:
                pages.extend(extract_pages(item))
    return pages

new_nav_pages = set(extract_pages(new_docs.get("navigation", [])))

def is_valid_target(target):
    target_clean = target.lstrip("/")
    if os.path.exists(os.path.join(DOCS_DIR, f"{target_clean}.mdx")):
        return True
    if os.path.exists(os.path.join(DOCS_DIR, target_clean, "index.mdx")):
        return True
    if target_clean in new_nav_pages:
        return True
    return False

ROUTE_MAP = {
    # Intro / About / Getting Started
    "index": ("/id/index", "/en/index"),
    "intro": ("/id/index", "/en/index"),
    "use-these-docs": ("/id/index", "/en/index"),
    "about": ("/id/gateway/overview", "/en/gateway/overview"),
    "about/billing-pricing": ("/id/guides/faq", "/en/guides/faq"),
    "about/rate-limits": ("/id/guides/rate-limits", "/en/guides/rate-limits"),
    "about/errors": ("/id/api-reference/introduction", "/en/api-reference/introduction"),
    "about/prompt-templates": ("/id/gateway/responses-api/prompt-templates", "/en/gateway/responses-api/prompt-templates"),
    "error-handling": ("/id/api-reference/introduction", "/en/api-reference/introduction"),
    "authentication": ("/id/api-reference/introduction", "/en/api-reference/introduction"),
    "api-introduction": ("/id/api-reference/introduction", "/en/api-reference/introduction"),
    "check-api-key-status": ("/id/api-reference/introduction", "/en/api-reference/introduction"),
    "widget": ("/id/integrations/chat-widget", "/en/integrations/chat-widget"),
    "advanced-examples": ("/id/integrations/overview", "/en/integrations/overview"),

    # Models
    "models-overview": ("/id/gateway/models", "/en/gateway/models"),
    "models": ("/id/gateway/models", "/en/gateway/models"),

    # Operations / Core features
    "batches-overview": ("/id/gateway/operations/batches", "/en/gateway/operations/batches"),
    "files-overview": ("/id/gateway/operations/files", "/en/gateway/operations/files"),
    "conversation-management": ("/id/gateway/responses-api/conversations", "/en/gateway/responses-api/conversations"),
    "response": ("/id/gateway/responses-api", "/en/gateway/responses-api"),
    "webhooks-overview": ("/id/guides/webhooks", "/en/guides/webhooks"),

    # Tools & MCP
    "tools-overview": ("/id/gateway/chat-completions/tool-calling", "/en/gateway/chat-completions/tool-calling"),
    "how-tools": ("/id/gateway/chat-completions/tool-calling", "/en/gateway/chat-completions/tool-calling"),
    "mcp": ("/id/agents/mcp-connector", "/en/agents/mcp-connector"),
    "agent-overview": ("/id/agents/overview", "/en/agents/overview"),

    # Capabilities
    "capability/audio-transcription": ("/id/gateway/capabilities/audio", "/en/gateway/capabilities/audio"),
    "capability/embeddings": ("/id/gateway/capabilities/embeddings", "/en/gateway/capabilities/embeddings"),
    "capability/guardrails": ("/id/guides/guardrails", "/en/guides/guardrails"),
    "capability/image-generation": ("/id/gateway/capabilities/image-generation", "/en/gateway/capabilities/image-generation"),
    "capability/image-understanding": ("/id/gateway/chat-completions/vision", "/en/gateway/chat-completions/vision"),
    "capability/ocr": ("/id/gateway/capabilities/ocr", "/en/gateway/capabilities/ocr"),
    "capability/rag": ("/id/integrations/llama-index", "/en/integrations/llama-index"),
    "capability/reasoning": ("/id/gateway/chat-completions/reasoning", "/en/gateway/chat-completions/reasoning"),
    "capability/stream": ("/id/gateway/chat-completions/streaming", "/en/gateway/chat-completions/streaming"),
    "capability/structured": ("/id/gateway/chat-completions/structured-outputs", "/en/gateway/chat-completions/structured-outputs"),
    "capability/video-generation": ("/id/gateway/capabilities/video-generation", "/en/gateway/capabilities/video-generation"),
    "deepseek-ocr": ("/id/gateway/capabilities/ocr", "/en/gateway/capabilities/ocr"),
    "glm-ocr": ("/id/gateway/capabilities/ocr", "/en/gateway/capabilities/ocr"),

    # SDK OpenAI Compat
    "sdk": ("/id/gateway/overview", "/en/gateway/overview"),
    "sdk/index": ("/id/gateway/overview", "/en/gateway/overview"),
    "sdk/python": ("/id/quickstart", "/en/quickstart"),
    "sdk/python/index": ("/id/quickstart", "/en/quickstart"),
    "sdk/openai-compat": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),
    "sdk/openai-compat/index": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),
    "sdk/openai-compat/chat-completions": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),
    "sdk/openai-compat/tool-calls": ("/id/gateway/chat-completions/tool-calling", "/en/gateway/chat-completions/tool-calling"),
    "sdk/openai-compat/structured-outputs": ("/id/gateway/chat-completions/structured-outputs", "/en/gateway/chat-completions/structured-outputs"),
    "sdk/openai-compat/image-generation": ("/id/gateway/capabilities/image-generation", "/en/gateway/capabilities/image-generation"),
    "sdk/openai-compat/file-input": ("/id/gateway/chat-completions/vision", "/en/gateway/chat-completions/vision"),
    "sdk/openai-compat/embeddings": ("/id/gateway/capabilities/embeddings", "/en/gateway/capabilities/embeddings"),
    "sdk/openai-compat/rest-api": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),
    "sdk/openai-compat/advanced": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),

    # SDK Anthropic Compat
    "sdk/anthropic-compat": ("/id/gateway/anthropic-messages", "/en/gateway/anthropic-messages"),
    "sdk/anthropic-compat/index": ("/id/gateway/anthropic-messages", "/en/gateway/anthropic-messages"),
    "sdk/anthropic-compat/messages": ("/id/gateway/anthropic-messages", "/en/gateway/anthropic-messages"),
    "sdk/anthropic-compat/tool-calls": ("/id/gateway/anthropic-messages/tool-use", "/en/gateway/anthropic-messages/tool-use"),
    "sdk/anthropic-compat/file-attachments": ("/id/gateway/anthropic-messages/vision", "/en/gateway/anthropic-messages/vision"),
    "sdk/anthropic-compat/advanced": ("/id/gateway/anthropic-messages/thinking", "/en/gateway/anthropic-messages/thinking"),

    # SDK Responses API
    "sdk/responses-api": ("/id/gateway/responses-api", "/en/gateway/responses-api"),
    "sdk/responses-api/index": ("/id/gateway/responses-api", "/en/gateway/responses-api"),
    "sdk/responses-api/text-generation": ("/id/gateway/responses-api", "/en/gateway/responses-api"),
    "sdk/responses-api/streaming": ("/id/gateway/responses-api", "/en/gateway/responses-api"),
    "sdk/responses-api/tool-calling": ("/id/gateway/responses-api/tools", "/en/gateway/responses-api/tools"),
    "sdk/responses-api/image-generation": ("/id/gateway/capabilities/image-generation", "/en/gateway/capabilities/image-generation"),
    "sdk/responses-api/image-input": ("/id/gateway/chat-completions/vision", "/en/gateway/chat-completions/vision"),
    "sdk/responses-api/file-input": ("/id/gateway/operations/files", "/en/gateway/operations/files"),

    # Coding Plan
    "coding-plan/best-practice": ("/id/coding-plan/overview", "/en/coding-plan/overview"),
    "coding-plan/faq": ("/id/coding-plan/overview", "/en/coding-plan/overview"),
    "coding-plan/jelma": ("/id/guides/jelma/overview", "/en/guides/jelma/overview"),
    "coding-plan/learning-path": ("/id/coding-plan/overview", "/en/coding-plan/overview"),
    "coding-plan/memory-mechanism": ("/id/coding-plan/overview", "/en/coding-plan/overview"),
    "coding-plan/switching-models": ("/id/coding-plan/model-routes", "/en/coding-plan/model-routes"),

    # Unprefixed existing pages (so unprefixed old URL redirects to default id)
    "coding-plan/overview": ("/id/coding-plan/overview", "/en/coding-plan/overview"),
    "coding-plan/quick-start": ("/id/coding-plan/quick-start", "/en/coding-plan/quick-start"),
    "coding-plan/quota-and-limits": ("/id/coding-plan/quota-and-limits", "/en/coding-plan/quota-and-limits"),
    "coding-plan/tool-integration": ("/id/coding-plan/tool-integration", "/en/coding-plan/tool-integration"),
    "coding-plan/model-routes": ("/id/coding-plan/model-routes", "/en/coding-plan/model-routes"),
    "coding-plan/usage-policy": ("/id/coding-plan/usage-policy", "/en/coding-plan/usage-policy"),
    "quickstart": ("/id/quickstart", "/en/quickstart"),

    # Jelma & Coding Guides
    "guides/ai-coding-tools": ("/id/coding-plan/tool-integration", "/en/coding-plan/tool-integration"),
    "guides/jelma/best-practices": ("/id/guides/jelma/usage", "/en/guides/jelma/usage"),
    "guides/jelma/faq": ("/id/guides/jelma/overview", "/en/guides/jelma/overview"),
    "guides/jelma/reference": ("/id/guides/jelma/usage", "/en/guides/jelma/usage"),
    "guides/jelma/overview": ("/id/guides/jelma/overview", "/en/guides/jelma/overview"),
    "guides/jelma/usage": ("/id/guides/jelma/usage", "/en/guides/jelma/usage"),

    # Integrations
    "integrations": ("/id/integrations/overview", "/en/integrations/overview"),
    "using-neosantara-with-vercels-ai-sdk": ("/id/integrations/vercel-ai-sdk", "/en/integrations/vercel-ai-sdk"),
    "agno": ("/id/integrations/agno", "/en/integrations/agno"),
    "any-llm": ("/id/integrations/any-llm", "/en/integrations/any-llm"),
    "autogen": ("/id/integrations/autogen", "/en/integrations/autogen"),
    "crewai": ("/id/integrations/crewai", "/en/integrations/crewai"),
    "dspy": ("/id/integrations/dspy", "/en/integrations/dspy"),
    "e2b": ("/id/integrations/e2b", "/en/integrations/e2b"),
    "langchain": ("/id/integrations/langchain", "/en/integrations/langchain"),
    "litellm": ("/id/integrations/litellm", "/en/integrations/litellm"),
    "llama-index": ("/id/integrations/llama-index", "/en/integrations/llama-index"),
    "pydantic-ai": ("/id/integrations/pydantic-ai", "/en/integrations/pydantic-ai"),
    "guides/migration": ("/id/gateway/chat-completions", "/en/gateway/chat-completions"),
    "guides/rag-chromadb-example": ("/id/integrations/overview", "/en/integrations/overview"),
    "guides/rag-cloudflare-vectorize-example": ("/id/integrations/overview", "/en/integrations/overview"),
}

API_MAP = {
    "api-reference/chat/completions/create": "/id/gateway/chat-completions",
    "api-reference/chat/create-chat-completion": "/id/gateway/chat-completions",
    "api-reference/responses/create": "/id/gateway/responses-api",
    "api-reference/response/create-a-response": "/id/gateway/responses-api",
    "api-reference/messages/create": "/id/gateway/anthropic-messages",
    "api-reference/models/list-available-models": "/id/gateway/models",
    "api-reference/models/get": "/id/gateway/models",
    "api-reference/images/create-image-generation": "/id/gateway/capabilities/image-generation",
    "api-reference/audio/transcription": "/id/gateway/capabilities/audio",
    "api-reference/embeddings/create-embeddings": "/id/gateway/capabilities/embeddings",
    "api-reference/files/upload": "/id/gateway/operations/files",
    "api-reference/files/list": "/id/gateway/operations/files",
    "api-reference/files/get": "/id/gateway/operations/files",
    "api-reference/files/delete": "/id/gateway/operations/files",
    "api-reference/files/download": "/id/gateway/operations/files",
    "api-reference/batches/create": "/id/gateway/operations/batches",
    "api-reference/batches/list": "/id/gateway/operations/batches",
    "api-reference/batches/get": "/id/gateway/operations/batches",
    "api-reference/batches/cancel": "/id/gateway/operations/batches",
    "api-reference/videos/create": "/id/gateway/capabilities/video-generation",
    "api-reference/videos/get": "/id/gateway/capabilities/video-generation",
    "api-reference/videos/content": "/id/gateway/capabilities/video-generation",
    "api-reference/moderations/content-moderation-check": "/id/api-reference/introduction",
    "api-reference/utility/count-tokens": "/id/gateway/anthropic-messages",
    "api-reference/user/usage": "/id/guides/faq",
}

redirects = []
seen_sources = set()

def add_redirect(source, destination):
    src = "/" + source.strip("/")
    dst = "/" + destination.strip("/")
    if src == dst:
        return
    if src in seen_sources:
        return
    if not is_valid_target(dst):
        print(f"Error: {dst} is invalid target")
        return
    seen_sources.add(src)
    redirects.append({"source": src, "destination": dst})

# 1. ROUTE_MAP
for route, (target_id, target_en) in ROUTE_MAP.items():
    add_redirect(f"/{route}", target_id)
    add_redirect(f"/id/{route}", target_id)
    add_redirect(f"/en/{route}", target_en)

# 2. API_MAP
for api_route, target in API_MAP.items():
    add_redirect(f"/{api_route}", target)
    add_redirect(f"/en/{api_route}", target.replace("/id/", "/en/"))
    add_redirect(f"/id/{api_route}", target)

# 3. Models
models_dir = os.path.join(EXT_DIR, "models")
if os.path.exists(models_dir):
    for f in sorted(os.listdir(models_dir)):
        if f.endswith(".mdx"):
            model_slug = f[:-4]
            add_redirect(f"/models/{model_slug}", "/id/gateway/models")
            add_redirect(f"/en/models/{model_slug}", "/en/gateway/models")
            add_redirect(f"/id/models/{model_slug}", "/id/gateway/models")

# 4. Old external-docs redirects
for r in ext_docs.get("redirects", []):
    src = r["source"]
    add_redirect(src, "/id/gateway/models" if "/models/" in src else "/id/gateway/overview")

print(f"Applying {len(redirects)} redirects to docs.json...")
new_docs["redirects"] = redirects

with open(docs_json_path, "w", encoding="utf-8") as f:
    json.dump(new_docs, f, indent=2, ensure_ascii=False)

print("Applied successfully.")
