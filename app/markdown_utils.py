# app/markdown_utils.py
import markdown as md
import bleach

# Minimal allowlist for v0 (tight by default)
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "blockquote", "code", "pre", "a"
]
ALLOWED_ATTRS = {
    "a": ["href", "title", "rel"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

def render_md_to_safe_html(text: str) -> str:
    # 1) Convert Markdown → HTML
    raw_html = md.markdown(
        text,
        extensions=["fenced_code", "codehilite", "tables", "sane_lists"]
    )
    # 2) Sanitize
    clean = bleach.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    # 3) Linkify plain URLs (still sanitized)
    clean = bleach.linkify(clean, skip_tags=["code", "pre"])
    return clean
