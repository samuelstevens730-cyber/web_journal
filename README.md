# Web_Journal v0

Tiny local interactive web journal for learning full-stack fundamentals.

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
- **Backend:**Python + fastAPI 
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
'''bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

Visit http://127.0.0.1:8000/docs for the Swagger UI. 

