# Web_Journal v0

Tiny local interactive web journal to learn full-stack fundamentals with **FastAPI**, **SQLite**, and **LLMs**. v0 is intentionally boring: CRUD + search + Markdown, with safe defaults.

---

## Scope (v0)
- Create, read, update, delete (CRUD) journal entries
- Search entries (SQLite `LIKE`)
- Markdown → safe HTML rendering (Python-Markdown + Bleach)
- LLM **reachability** planned (no tuning)

**Non-Goals (defer):** Auth, encryption, sync, tags, images, advanced AI (summarization, recommendations, multi-agent).

---

## Stack
- **Backend:** Python + FastAPI  
- **Database:** SQLite + SQLAlchemy ORM  
- **Frontend:** Jinja2 + htmx (skeleton next)  
- **Markdown:** Python-Markdown (+ Bleach sanitize + linkify)  
- **LLM:** OpenAI API or local (HF/Ollama) — **planned**

---

## Project Status (today)
- ✅ SQLite schema + indexes; app boots with health check
- ✅ Create + Read: `POST /entries` (form), `GET /entries/{id}`
- ✅ **Update:** `PATCH /entries/{id}` (JSON). On any `content_md` change we re-render and sanitize `content_html`.  
- ✅ **List:** `GET /entries?limit&offset` (JSON), newest-first  
- ✅ **Delete:** `DELETE /entries/{id}` (JSON, 204) and **form delete** `POST /entries/{id}/delete` (303 redirect to list)
- ✅ **Search:** `GET /entries/search?q=&limit=&offset=` (JSON) — escapes `%` and `_`; empty `q` returns `[]`
- ✅ Sanitizer pipeline verified (strips `<script>`, event handlers; keeps links/code)
- ⏳ Minimal Jinja index (`GET /`) + htmx live search
- ⏳ LLM ping + basic reflection endpoint

---

## API Surface (v0)

> Dev JSON routes are included for testing; the canonical delete flow is **form POST → redirect**.

### Entries
- **Create (form):** `POST /entries`  
  Body (form): `title`, `content_md`  
  Returns: `EntryRead` (`id`, `title`, `content_md`, `content_html`)

- **Read:** `GET /entries/{id}` → `EntryRead`

- **List:** `GET /entries?limit=20&offset=0` → `list[EntryRead]` (ordered by `created_at DESC`)

- **Update (JSON PATCH):** `PATCH /entries/{id}`  
  Body (JSON): `{"title"?: string, "content_md"?: string}`  
  Behavior: when `content_md` changes, we **render + sanitize** into `content_html`. `updated_at` bumps **only** on material change.

- **Delete (JSON):** `DELETE /entries/{id}` → **204 No Content** on success, 404 if missing

- **Delete (form, canonical):** `POST /entries/{id}/delete` → **303 See Other** redirect to `/entries` (temporary) or `/` (once templates land)

### Search
- **Search (JSON):** `GET /entries/search?q=&limit=&offset=` → `list[EntryRead]`  
  Notes: Uses SQLite `LIKE` on `title, content_md`; escapes `%` and `_`; empty/whitespace `q` → `[]`.

---

## Conventions & Invariants
- **Sanitize on save:** On create and on any `content_md` change, render Markdown → sanitize + linkify into `content_html`. Client HTML is never trusted.
- **Timestamps:** `updated_at` bumps only on **material** change (title or content); v0 stores naïve UTC.
- **Ordering:** Lists & search are **newest-first** (`created_at DESC`). Pagination defaults: `limit=20`, `offset=0`.
- **Router order:** Declare static routes like `/entries/search` **before** dynamic routes like `/entries/{id}` to avoid collisions.

---

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
# Swagger UI → http://127.0.0.1:8000/docs
```

Project layout:
```bash
app/
 ├── crud.py          # DB operations (CRUD, search)
 ├── database.py      # Engine, session
 ├── main.py          # FastAPI entrypoint + router
 ├── models.py        # SQLAlchemy models
 ├── routers/         # API routes (entries, etc.)
 ├── markdown_utils.py# Markdown → safe HTML
 └── schemas.py       # Pydantic schemas
data/
 └── journal.db       # SQLite database
```

**Notes**
- `data/journal.db` is git-ignored.
- For debugging, enable SQL echo in `database.py`.
- VS Code tip: “SQLite Viewer” extension helps inspect the DB quickly.

---

## Roadmap
- [x] POST/GET entries
- [x] SQLite persistence
- [x] **PATCH update** with sanitize-on-save + single timestamp bump
- [x] **List + Delete** (JSON delete + canonical form delete with redirect)
- [x] **Search** (`LIKE` with wildcard escaping)
- [ ] Minimal Jinja index + htmx search
- [ ] LLM journaling assistant (basic `/ai/ping`, per-entry reflect)
- [ ] Migrate to tz-aware datetimes in DB

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
