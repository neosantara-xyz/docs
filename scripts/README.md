# Documentation Scripts

Automation and validation tools for Neosantara documentation.

## Scripts Overview

### `validate_docs.py`
Validates that:
1. Every page referenced in `docs.json` (across all languages and tabs) exists in the filesystem.
2. Identifies orphaned `.mdx` files not declared in `docs.json`.
3. Verifies that all internal links `[text](/path)` resolve to valid routes.

```bash
python3 scripts/validate_docs.py
```

### `check_snippets.py`
Verifies that all snippet imports (`import X from '/_snippets/...'`) in `.mdx` files point to existing files in `_snippets/`.

```bash
python3 scripts/check_snippets.py
```

### `sync_models.py`
Queries the live Neosantara API endpoint (`https://api.neosantara.xyz/v1/models`) or fallback local catalog to fetch active, non-deprecated, listed models and automatically generates reusable snippets in `snippets/`:
- `snippets/models-table.mdx` (semua model aktif)
- `snippets/models-reasoning-table.mdx` (filter: kapabilitas `reasoning`)
- `snippets/models-vision-table.mdx` (filter: kapabilitas `vision`)
- `snippets/models-tools-table.mdx` (filter: kapabilitas `tools` / `function_calling`)
- `snippets/models-json-table.mdx` (filter: kapabilitas `json` / `structured_outputs`)
- `snippets/models-embeddings-table.mdx` (filter: kapabilitas `embeddings`)
- `snippets/models-image-table.mdx` (filter: kapabilitas `image_generation`)
- `snippets/models-ocr-table.mdx` (filter: kapabilitas `ocr`)
- `snippets/models-audio-table.mdx` (filter: kapabilitas `audio_transcription`)

```bash
# Sinkronkan seluruh tabel dan snippet kapabilitas
python3 scripts/sync_models.py

# Filter kapabilitas tertentu saja (misal: reasoning)
python3 scripts/sync_models.py --capability reasoning

# Filter kapabilitas dengan custom output path
python3 scripts/sync_models.py --capability vision --output snippets/custom-vision.mdx

# Tampilkan rincian kapabilitas yang tersedia di katalog
python3 scripts/sync_models.py --list-capabilities
```

### `sync_openapi.py`
Syncs the authoritative OpenAPI contract from `/root/nusantaraai/openapi.json` into `api-reference/openapi.json` for interactive API reference generation.

```bash
python3 scripts/sync_openapi.py
```
