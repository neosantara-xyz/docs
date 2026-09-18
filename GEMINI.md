# GEMINI.md - Neosantara Documentation Style Guide

## Philosophy

Neosantara docs are direct, concrete, and professional. No marketing fluff. No AI-sounding prose. Every sentence earns its place. We cover a massive surface area: an enterprise-grade regional AI gateway, unified OpenAI and Anthropic compatible routing, durable Rupiah PAYG billing, and an integrated Model Context Protocol (MCP) hub. Analogies and commentary add cognitive load without adding understanding. Be direct.

Documentation is written in multiple languages (`id/` and `en/`). Treat the primary language (`id/`) as the source of truth, reflecting Neosantara's mission for regional and Indonesian developers. For Bahasa Indonesia (`id/`), write in a modern, natural, and direct developer tone — NEVER use stiff, archaic, or bureaucratic formal Indonesian ("kata baku kaku"). Strictly avoid "ikhtisar" (use "ringkasan" or "rangkuman"). Use natural developer terms (routing, tools, library, API key, billing, open source) rather than forced textbook translations. Translations to `en/` must preserve technical meaning, code behavior, terminology, links, and page intent while reading naturally in English.

## About This Repo

- **Site builder:** Mintlify. Pages are `.mdx` with YAML frontmatter (`title`, `description`).
- **Navigation:** `docs.json` is the source of truth. Adding a page means adding it there too.
- **Neosantara source:** Accessible at `../nusantaraai` (or `..`). Read it before writing about APIs, parameters, or behavior. Don't guess from memory or training data.
- **Live Models Sync:** Run `python3 scripts/sync_models.py` to fetch active models and token pricing directly from the live API (`https://api.neosantara.xyz/v1/models`) into `_snippets/models-table.mdx`.
- **OpenAPI Spec:** Run `python3 scripts/sync_openapi.py` to sync `openapi.json` into `api-reference/openapi.json`.
- **Reusable snippets:** `_snippets/` holds shared install steps, auth headers, setup blocks, and recurring components. Check there before duplicating content.
- **Multilingual structure:** Uses Mintlify's `navigation.languages` configuration for localized docs (`en/` for English, `id/` for Bahasa Indonesia). Keep translated content in language-specific directories.
- **Verification scripts:** Run `python3 scripts/validate_docs.py` and `python3 scripts/check_snippets.py` before finalizing any documentation PR or task.

## Before Writing Any Page

Define these five things before you write:

1. **What is this page about?** (one sentence)
2. **What does the user need to do?** (the code)
3. **What decisions might they face?** (tables)
4. **Where do they go next?** (links)
5. **What type of page is this?** (tutorial, how-to, reference, or explanation. See Page Types below.)

If you can't answer these clearly, the page will ramble.

For translated pages, also verify:

6. **What is the source page?** Identify the corresponding primary-language page (`id/`).
7. **What technical content must remain unchanged?** Preserve code, API names, parameter names, identifiers, paths, and commands unless the target language explicitly requires otherwise.
8. **What terminology is already established?** Match existing terminology in the target-language docs instead of translating technical terms inconsistently.

## Page Structure

Every page should follow this pattern:

1. **One-line description** - What this page covers (in frontmatter and opening line)
2. **Code first** - Show the pattern immediately
3. **Explain after** - Brief context only if needed
4. **Tables for decisions** - "When to use X vs Y" belongs in a table, not prose
5. **Links at bottom** - "Next steps" or "Developer Resources"

```
❌ Long explanation of what gateways are, provider history, why they matter...
   then eventually some code.

✅ Code example showing the pattern.
   Brief explanation of what it does.
   Table of options/decisions.
   Links to related pages.
```

For multilingual pages:

- Keep the same filename and relative structure as the primary-language page where practical (e.g. `en/gateway/chat-completions.mdx` and `id/gateway/chat-completions.mdx`).
- Use a language-specific directory (`en/`, `id/`).
- Do not duplicate the same page path across multiple language entries in `docs.json`. Mintlify documents this as undefined behavior.
- Translate navigation labels such as "group", "tab", navbar labels, and footer labels so the localized experience is actually localized.
- A translation may have a different navigation structure when the target language needs different content organization, but do not change the technical meaning of the underlying page.

## Page Types

Every page serves one primary documentation need. The four types come from the Diátaxis framework:

| Type | Purpose | Neosantara Examples |
| :--- | :--- | :--- |
| **Tutorial** | Guided lesson for new users | First API Call, Building your First MCP Agent |
| **How-to Guide** | Task directions for competent users | Streaming responses, setting up Cursor MCP, LiteLLM integration |
| **Reference** | Technical description of the machinery | API reference, parameter tables, model catalog, rate limits |
| **Explanation** | Understanding-oriented discussion | Gateway routing architecture, billing reservation lifecycle, UU PDP compliance |

If a page mixes types (e.g., a how-to that stops to explain concepts), extract the foreign content into its own page and link to it.

A translation must keep the same primary page type as its source page. Do not turn a reference page into a tutorial simply because the target language would be easier to explain differently.

## Context Hygiene

**Start fresh for each section.** Don't let one domain bleed into another. If you're writing Core Gateway docs, don't bring patterns or terminology from MCP Sandbox docs. Each section should be self-contained.

For multilingual work, also keep language contexts isolated. Do not infer terminology from another language when established terminology exists in the target language. Compare against the target-language docs and source page instead.

## Core Rules

### 1. Lead with code

Show the pattern first, explain after. Users are scanning for how to do something.

```python
# ❌ "To route requests to Claude 3.7 Sonnet through Neosantara, you need to configure your OpenAI
#    SDK client with the Neosantara base URL and your API key. Then you pass the model identifier
#    to the chat completions create method. Here's how:"
#    [code]

# ✅
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.neosantara.xyz/v1",
    api_key=os.environ["NEOSANTARA_API_KEY"]
)

response = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "Hello world"}]
)
# "Route requests using OpenAI SDK compatibility."
```

### 2. One concept per section

Don't bundle unrelated ideas. If you're explaining streaming, don't also explain tool calling in the same section.

### 3. Tables over prose for comparisons

```
❌ "You might want to use Gemini Flash when you need ultra-low latency, but
   Claude Sonnet is better for deep reasoning and complex coding. If you're building
   a cost-sensitive prototype, GPT-5.4-mini gives you good efficiency..."

✅ | Use Case | Recommended Model | Context Window |
   | :--- | :--- | :--- |
   | Ultra-fast low latency | `gemini-3.8-flash` | 1M tokens |
   | Deep reasoning & coding | `deepseek-v4.1-flash` | 1M tokens |
   | Cost-effective general | `gpt-5.4-mini` | 128k tokens |
```

### 4. Descriptions must be specific

Every page's `description` field should describe what the page covers, not say "Learn how to."

```
❌ "Learn how to send chat completion requests with Neosantara."
✅ "Send chat requests, stream tokens, and invoke function calling."

❌ "Learn how to connect Cursor to Neosantara."
✅ "Configure Cursor to use Neosantara MCP tools and language models."

❌ "Learn about Neosantara Gateway architecture."
✅ "How Neosantara routes, bills, and secures multi-provider LLM requests."
```

For translated pages, translate the `title` and `description`. Keep API names, product names, code identifiers, and other literal technical terms unchanged where appropriate.

### 5. No em dashes

Em dashes (`—`) are an AI tell. Use periods, commas, or rewrite.

```
❌ "Neosantara provides low regional latency—ideal for Indonesian developers."
✅ "Neosantara provides low regional latency. Ideal for Indonesian developers."

❌ "Each request reserves credits upfront—avoiding overdrafts."
✅ "Each request reserves credits upfront to prevent overdrafts."
```

### 6. No comma splices

Two independent clauses joined by a comma need a period or semicolon.

```
❌ "Run it on your local server, don't take these latency numbers at face value."
✅ "Run it on your local server. Don't take these latency numbers at face value."

❌ "Neosantara bills in Rupiah, you do not need an international credit card."
✅ "Neosantara bills in Rupiah. You do not need an international credit card."
```

### 7. Cut the commentary

Analogies and editorializing waste space.

```
❌ "Juggling multiple AI provider accounts is like spinning plates in a hurricane.
   It works until one drops and your entire production pipeline halts."

✅ "Neosantara unifies multiple AI providers behind one endpoint."
```

### 8. Specific over generic

```
❌ "Use a better model for improved results."
✅ "Use `deepseek-v4.1-flash` for better code generation."

❌ "You can customize various settings."
✅ "Set `temperature=0` to reduce sampling variability."
```

### 9. Tighten wordy phrases

| Before | After |
| :--- | :--- |
| "Here's how they work:" | "The execution flow:" |
| "For more information see the X documentation." | "See X." |
| "You can also run the request asynchronously" | "Run asynchronously with `/v1/responses`" |
| "The `model` parameter is the model to send to the gateway. It can be..." | "The `model` parameter accepts:" |
| "If this is your first time using Neosantara, you can start here" | "New to Neosantara? Start with the quickstart." |
| "After getting familiarized with" | "After getting familiar with" |
| "This example shows how to..." | [Remove - let the code speak] |
| "Here's how it looks:" | [Remove - show the visual] |
| "It's important to note that" | [Remove - just state it] |
| "Basically" / "Essentially" | [Remove] |

### 10. Link lists: no "View the..." pattern

```markdown
❌ Developer Resources
- View the [Chat Completions guide](/en/gateway/chat-completions)
- View the [OpenResponses schema](/en/gateway/responses-api)

✅ Developer Resources
- [Chat Completions guide](/en/gateway/chat-completions)
- [OpenResponses schema](/en/gateway/responses-api)
```

For multilingual docs, prefer links to the same locale when the localized target exists. Do not send users from a translated page to an untranslated page when an equivalent localized page exists.

### 11. Q&A lists → Tables

```markdown
❌ Common questions:
- **How do I stream responses?** -> See [streaming completions](/en/gateway/chat-completions#streaming-responses).
- **How do I connect Cursor?** -> See [Cursor integration](/en/agents/cursor).

✅ | Task | Guide |
   | :--- | :--- |
   | Stream responses | [Streaming completions](/en/gateway/chat-completions#streaming-responses) |
   | Connect Cursor | [Cursor integration](/en/agents/cursor) |
```

### 12. Card descriptions: vary them

```
❌ "Learn how to build your first agent."
❌ "Learn how to connect your first tool."
❌ "Learn how to configure your first proxy."

✅ "Build your first autonomous agent with tools and memory."
✅ "Connect sandboxed execution tools via MCP."
✅ "Route requests through the regional OpenAI-compatible proxy."
```

Translate card titles and descriptions for localized navigation pages. Keep them concise and specific.

### 13. No contrastive negation

Don't define things by what they aren't. State what they are directly.

```
❌ "Neosantara isn't just a reverse proxy — it's an enterprise AI orchestration gateway."
❌ "OpenResponses isn't a simple chat endpoint. It's a persistent execution model."

✅ "Neosantara is an enterprise AI gateway with regional routing and durable billing."
✅ "OpenResponses provides persistent execution and asynchronous job retrieval."
```

### 14. Preserve technical identifiers across languages

Do not translate:

- Python, TypeScript, JSON, YAML, Bash, SQL, or other code syntax
- Package names and import paths (`openai`, `@anthropic-ai/sdk`, `litellm`, `agno`)
- Class, method, function, parameter, and variable names
- File paths and directory names
- CLI commands
- URLs and endpoint routes (`/v1/chat/completions`, `/v1/responses`, `/v1/mcp`)
- Environment variable names (`NEOSANTARA_API_KEY`, `NEOSANTARA_BASE_URL`)
- API field names (`prompt_tokens`, `completion_tokens`, `total_tokens`)
- Literal values where they are part of the API contract

Translate the surrounding explanation:

✅ Set `model="deepseek-v4.1-flash"` to execute reasoning requests.  
❌ Set `model_name="deepseek-v4.1-flash"` untuk menjalankan penalaran.

---

## Multilingual Documentation

Mintlify supports localized navigation through `navigation.languages`. Each language entry contains a language code and its navigation structure. The first language is default unless another entry sets `default: true`.

### Language Directories

Use language-specific directories for content:

```text
new-docs/
├── _snippets/           # Shared reusable snippets across languages
│   ├── set-api-key.mdx
│   └── base-url-config.mdx
├── en/                  # English documentation (Primary)
│   ├── index.mdx
│   ├── quickstart.mdx
│   ├── gateway/
│   ├── agents/
│   └── integrations/
└── id/                  # Indonesian documentation
    ├── index.mdx
    ├── quickstart.mdx
    ├── gateway/
    ├── agents/
    └── integrations/
```

Keep filenames and directory structure aligned with the primary language where practical. This makes missing or stale translations easy to detect.

### `docs.json` Configuration

```json
{
  "navigation": {
    "languages": [
      {
        "language": "id",
        "default": true,
        "tabs": [
          {
            "tab": "Beranda",
            "groups": [
              {
                "group": "Memulai",
                "pages": ["id/index", "id/quickstart"]
              }
            ]
          }
        ]
      },
      {
        "language": "en",
        "tabs": [
          {
            "tab": "Home",
            "groups": [
              {
                "group": "Getting Started",
                "pages": ["en/index", "en/quickstart"]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

Rules:
- Use supported language codes (`id`, `en`).
- Give every language its own navigation structure.
- Never reference the same page path from more than one language entry.
- Put Bahasa Indonesia (`id`) first with `"default": true`.
- Translate navigation labels such as group and tab names.
- Use language-specific navbar, footer, and banner settings when they need localized labels.

### Translation Workflow

For a new or changed page:
1. Author and verify the primary-language page (`id/`) first.
2. Verify the content against the gateway code (`/root/nusantaraai`) or live endpoint.
3. Translate and mirror to the English page (`en/`).
4. Preserve code and technical identifiers across both languages.
5. Review terminology against existing target-language docs.
6. Update translated frontmatter (`title`, `description`).
7. Verify locale-specific links.
8. Verify the translated page is included in the correct language navigation in `docs.json`.
9. Run `python3 scripts/validate_docs.py` and `python3 scripts/check_snippets.py`.

### Backend Verification Invariants (Source of Truth: `/root/nusantaraai`)

Before writing any billing, rate limit, or routing documentation, ALWAYS verify against the gateway backend:

1. **Rate Limiting (`config/redisClient.js` & `middleware/checkUptash.js`)**:
   - Limit metrics are **RPM** (Requests Per Minute), **ITPM** (Input Tokens Per Minute), **OTPM** (Output Tokens Per Minute), and **Promo RPM** for 100% discounted models on Free tier.
   - Never document generic unverified token limits. Input tokens are checked pre-flight via `estimateInputTokens` against ITPM; output tokens are settled post-flight via `settleOTPM` against OTPM.
   - Tier limits:
     - `Free`: 10 RPM, 30.000 ITPM, 8.000 OTPM
     - `Basic`: 50 RPM, 500.000 ITPM, 80.000 OTPM
     - `Standard`: 1.000 RPM, 2.000.000 ITPM, 320.000 OTPM
     - `Pro`: 2.000 RPM, 5.000.000 ITPM, 800.000 OTPM
     - `Enterprise`: 4.000 RPM, 10.000.000 ITPM, 1.600.000 OTPM
2. **Native Frameworks (Zero `base_url` required)**:
   - **Any-LLM**: `any-llm-sdk[neosantara]` with provider id `neosantara` (`AnyLLM.create("neosantara")`).
   - **LiteLLM**: Native provider `completion(model="neosantara/<model>", ...)`.
   - **Agno**: Native model provider `from agno.models.neosantara import Neosantara`, `Agent(model=Neosantara(id="..."))`.
3. **Durable PAYG Billing (`service/billingReservationService.js`)**:
   - Credit lifecycle: `reserve` -> `settle` -> `refund`.
   - Balances and ledger use `NUMERIC(20,6)` in Rupiah (IDR). Minimum deposit floor is Rp 15.000 via Mayar (QRIS/VA).
4. **Indonesian Guardrails**:
   - UU PDP No. 27/2022 automated PII redaction activated per-request via `X-Guard: on` / `X-Guard: enabled`.

### Translation Quality

A translation is not a license to rewrite the technical content.

**Preserve:**
- API behavior
- Parameter semantics
- Code examples
- Warnings and constraints
- Links and destinations
- Section intent
- Tables and decision criteria

**Adapt:**
- Natural phrasing
- Grammar
- Sentence order when needed for readability
- Navigation labels
- Examples that are explicitly language- or region-specific

Do not invent localized terminology when the project already uses an established technical term.

### Partial Translations

A locale may lag behind the primary language. Do not silently fabricate missing translations.
When a source page has changed but its translation does not exist:
- Leave the translated page untouched if no verified translation has been produced.
- Add the page to the translation work queue.
- Do not create low-confidence machine translations just to make the directory look complete.
- Do not alter the source page solely to simplify translation.

---

## Indonesian Style Guide: Modern Developer Tone (No Stiff / Bureaucratic Formalism)

Neosantara is built by and for developers. Indonesian documentation (`id/`) must be written in a modern, direct, and natural tech tone. **Do NOT use stiff, bureaucratic formal Indonesian ("kata baku kaku")** that reads like a government decree, an outdated textbook, or an academic thesis.

### Absolute Rules for Bahasa Indonesia:

1. **STRICT BAN on "Ikhtisar"**:
   - NEVER use the word "ikhtisar" anywhere in page titles, navigation, links, or body text.
   - Always use **"Ringkasan"** or **"Rangkuman"** instead.
2. **Never Force Stiff Formal Translations ("Kata Baku Kaku")**:
   - Indonesian developers speak and think in standard tech terminology.
   - Use established industry terms: `routing`, `tools`, `library`, `SDK`, `API key`, `endpoint`, `request`, `response`, `payload`, `billing`, `token`, `open source`, `error`, `debug`, `browser`.
   - Forcing literal translations like *perutean*, *perkakas*, *pustaka*, *kunci API*, *peladen*, *peramban*, *galat*, *pengawakutuan* sounds robotic, alienating, and unnatural.

### Terminology Comparison Table (Avoid Stiff Bureaucratic Words)

| Kaku / Baku Birokratis (HINDARI) | Gaya Developer Modern (GUNAKAN) | Alasan / Konteks |
| :--- | :--- | :--- |
| **Ikhtisar** | **Ringkasan / Rangkuman** | **DILARANG KERAS.** "Ikhtisar" kaku dan berbau buku teks lama. Gunakan "Ringkasan" atau "Rangkuman". |
| Perutean | Routing / Me-route | Developer AI terbiasa dengan istilah *routing* (*fallback routing*, *routing regional*). |
| Perkakas | Tool / Tools | "Perkakas" berkonotasi alat pertukangan fisik. Gunakan *tool*, *MCP tools*, *tool-calling*. |
| Pustaka | Library / SDK | Gunakan *library* orkestrasi atau *SDK resmi*. |
| Kunci API | API key | Standar industri di Indonesia adalah *API key*. |
| Peladen | Server | Selalu gunakan *server* (*server MCP*, *upstream server*). |
| Peramban | Browser | Gunakan *browser* atau *web browser*. |
| Surel | Email | Gunakan *email*. |
| Galat | Error | Gunakan *error* (*pesan error*, *status error 503*). |
| Unduh / Unggah | Download / Upload | Gunakan *download* dan *upload*. |
| Pengawakutuan | Debug / Debugging | Istilah kaku membingungkan developer. |
| Model Sumber Terbuka | Model Open Source | Komunitas developer menggunakan istilah *open source*. |
| Rekayasa Perintah | Prompt Engineering | Istilah baku terdengar aneh. Gunakan *prompt engineering*. |
| Penagihan (berlebihan) | Billing / Reservasi Saldo | Gunakan istilah *billing*, *PAYG billing*, *reservasi saldo*. |
| Permintaan / Tanggapan (berlebihan) | Request / Respons | Diperbolehkan menggunakan *request* dan *respons* untuk konteks teknis HTTP. |

---

## Words and Phrases to Avoid

| Word/Phrase | Why | Use Instead |
| :--- | :--- | :--- |
| "Ikhtisar" | Stiff, archaic textbook term | "Ringkasan" or "Rangkuman" |
| Stiff "kata baku" (perutean, perkakas, pustaka, peladen, galat, dll.) | Unnatural and robotic to Indonesian software developers | Natural tech terms (routing, tools, library, server, error) |
| "Learn how to..." | Generic, passive | Specific action statement |
| "Seamlessly" | AI tell, meaningless | Describe actual behavior |
| "Let's explore" | Filler | [Remove, just explain] |
| "It's worth noting" | Filler | [Remove, just state it] |
| "Basically" / "Essentially" | Filler | [Remove] |
| "Beautiful" / "Elegant" | Subjective | Describe function |
| "Incredible" / "Powerful" | Hyperbolic | State facts |
| "Leading framework" | Unsubstantiated | State facts |
| "Happy building!" | Unnecessary | End with links |
| "Here's how it looks:" | Filler | [Remove] |
| Em dashes (`U+2014`) | AI tell | Periods or rewrite |
| "It's not X, it's Y" / "X isn't just Y" | Contrastive negation, AI tell | State what it is directly |

These rules apply to every language. Translate the rule's intent, not its exact English wording.

---

## Capitalization & Terminology

| Wrong | Right |
| :--- | :--- |
| id in prose | ID. Preserve literal source identifiers such as `id` parameters. |
| pydantic | Pydantic |
| vector db | vector database |
| 3rd party | third-party |
| Hackernews | HackerNews |
| higher level (adjective) | higher-level |
| multi turn | multi-turn |
| back-and-forth conversations | multi-turn conversations |
| api key | API key |
| payg | Pay-As-You-Go (PAYG) |
| rupiah | Rupiah (IDR) |
| mcp | Model Context Protocol (MCP) |

---

## The Three Pillars of Neosantara

Use on landing and overview pages where Neosantara is being introduced. Don't repeat the framing on every page. When you do use it, use these exact verbs and labels:

| Pillar | Verb | Description |
| :--- | :--- | :--- |
| **Gateway** | Route | Unified OpenAI and Anthropic endpoint routing across 100+ models with regional latency |
| **MCP Hub** | Connect | Secure Model Context Protocol tool execution, sandbox environments, and web search |
| **Billing & Guardrails** | Settle & Protect | Durable Rupiah PAYG credit reservation and automated UU PDP No. 27/2022 PII redaction |

When translated, preserve the three-layer structure and product meaning. Do not invent alternate terminology that makes the architecture inconsistent across languages.

---

## Code Examples

- No verbose comment blocks (`# ************* Create Client *************`).
- Minimal inline comments: code should be self-explanatory.
- Keep examples consistent across related pages and languages.
- Show the minimal working example first, then variations.
- Code blocks in MDX must always specify a valid language tag (`python`, `typescript`, `bash`, `json`, `env`).

---

## Mintlify Components

| Component | When to use |
| :--- | :--- |
| `<CardGroup cols={N}>` + `<Card title icon href>` | Navigation grids on overview pages |
| `<Steps>` + `<Step title>` | Sequential setup or tutorial steps |
| `<CodeGroup>` | Variants of the same example (Python/TypeScript, curl/SDK, async/sync) |
| `<Tabs>` + `<Tab title>` | Alternative views of the same content (Bash, .env, PowerShell) |
| `<Accordion>` / `<AccordionGroup>` | FAQ entries, optional details |
| `<Note>` `<Tip>` `<Warning>` `<Info>` `<Check>` | Callouts. Use sparingly. |
| `<Snippet file="name.mdx">` or `import Snippet from '/_snippets/...'` | Pull shared content from `_snippets/` |
| `<Frame>` | Wrap images that need a caption or border |

When translating components:
- Keep component names and attributes unchanged.
- Translate visible component content such as titles and labels.
- Keep `href` targets locale-correct (e.g. `/en/...` vs `/id/...`).

---

## Page Templates

The Overview template maps to Explanation pages, Tutorial/Guide maps to Tutorial or How-to, and Usage/Example maps to How-to.

### Overview Page Template

```markdown
---
title: "What is X?"
description: "One sentence defining X concretely."
---

**Bold one-liner expanding on the definition.**

[Code example - the simplest working version]

## Key Concepts

| Concept | Description |
| :--- | :--- |
| A | What A does |
| B | What B does |

## Learn How To

<CardGroup cols={3}>
  <Card title="Build X" href="/en/x/building">
    Create your first X with [specifics]
  </Card>
</CardGroup>

## Developer Resources

- [X reference](/en/reference/x)
- [X examples](/en/cookbook/x)
```

### Tutorial/Guide Page Template

```markdown
---
title: "Building X"
description: "What you'll build and the key pattern."
---

[Code example - complete working version]

## How It Works

1. Step one
2. Step two
3. Step three

## Options

| Option | Default | Description |
| :--- | :--- | :--- |
| `model` | `"gemini-3.8-flash"` | Model identifier to dispatch |

## Next Steps

| Task | Guide |
| :--- | :--- |
| Do Y | [Y guide](/en/y) |
```

### Usage/Example Page Template

````markdown
---
title: "X with Y"
description: "What this combination achieves."
---

<Steps>
  <Step title="Configure environment">
```bash
    export NEOSANTARA_API_KEY="nsk_..."
```
  </Step>
  <Step title="Initialize client">
```python
    [code]
```
  </Step>
  <Step title="Execute">
```bash
    python main.py
```
  </Step>
</Steps>
````

---

## Validation Commands

```bash
# Preview locally (run from new-docs root)
mint dev

# Validate all page references in docs.json and internal links
python3 scripts/validate_docs.py

# Verify snippet import resolutions
python3 scripts/check_snippets.py

# Sync models catalog from live API endpoint (https://api.neosantara.xyz/v1/models)
python3 scripts/sync_models.py

# Sync OpenAPI contract from gateway
python3 scripts/sync_openapi.py

# Mintlify standard checks (when mint CLI installed)
mint broken-links
mint validate
```

Before merging a change, verify:
- `docs.json` includes the page under the correct language.
- The target-language file exists.
- Frontmatter is valid.
- Localized links point to the correct language (`/en/...` or `/id/...`).
- Code examples and technical identifiers remain correct.
- Navigation labels match the target language.
- `python3 scripts/validate_docs.py` passes with exit code 0.