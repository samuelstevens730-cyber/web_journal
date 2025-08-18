# Web_Journal v0

Tiny local interactive web journal built to learn full-stack fundamentals with FastAPI, SQLite, and LLMs.

---

## Scope:
- Create, read, update, delete (CRUD) journal entries
- Search entries
- Markdown Rendering
- LLM Integration for an interactive journaling experience

---

## Non-Goals (Defer)
- Authentication
- Encryption
- Sync across devices
- Tags
- Images
- Advanced AI features (summarization, recommendations, multi-agent)

---

## Stack
- **Backend:** Python + FastAPI 
- **Database** SQLite + SQLAlchemy ORM
- **Frontend** Jinja2 + htmx 
- **Markdown** Python Markdown
- **LLM:** Either Open AI API or Local LLM via HF or Ollama. 
--

## Project Status
- Database connected
- GET/POST endpoints working

---

## Next Steps
- Update/Delete endpoints
- Search Implementation
- Markdown rendering
- Local LLM Integration

## Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

Visit http://127.0.0.1:8000/docs for the Swagger UI. 
```

```bash
app/
 ├── crud.py          # Database operations (CRUD)
 ├── database.py      # Database setup (engine, session)
 ├── main.py          # FastAPI entrypoint
 ├── models.py        # SQLAlchemy models
 ├── routers/         # API routes (entries, etc.)
 └── schemas.py       # Pydantic schemas
data/
 └── journal.db       # SQLite database
```

## Notes:
- Journal.db is ignored in version control (.gitignore)
- For Debugging, you can enable SQL echo in database.py
- Recommended VS Code extension: SQLite Viewer to inspect the DB

## Roadmap:
- [x] POST/GET entries
- [x] SQLite persistence
- [ ] Update & delete endpoints
- [ ] Search & filter
- [ ] Markdown rendering in UI
- [ ] LLM journaling assistant (basic)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)


