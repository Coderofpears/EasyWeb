# EasyWeb

EasyWeb is a tiny, single-file Python web server for dropping a folder of
static files into `public/` and serving them immediately. It requires zero
configuration—just add your HTML files, stylesheets, and assets, then run it.

The repository includes a small example gallery so you can see nested pages,
assets, and client-side JavaScript all working from the same server.

## Quick start

```bash
python -m venv .venv
# Activate .venv using the command for your shell.
pip install -r requirements.txt
python main.py
```

Open [http://localhost:8000](http://localhost:8000). The server binds to
`0.0.0.0:8000`.

## Drop-in hosting

Every file below `public/` is available at its matching URL path:

| File | URL |
| --- | --- |
| `public/index.html` | `/` |
| `public/about.html` | `/about.html` |
| `public/blog/post.html` | `/blog/post.html` |
| `public/assets/logo.svg` | `/assets/logo.svg` |
| `public/docs/index.html` | `/docs/` |

Folders with an `index.html` receive a trailing-slash redirect when opened
without the slash. Files are sent directly from `public/`, and path traversal
outside that directory is rejected.

If `public/index.html` is absent, EasyWeb serves a built-in fallback page
with a link to `index.html`. This means a completely empty checkout is still
usable after installing Flask.

## Included examples

Start the server and use the gallery at `/` or open these pages directly:

| Example | URL | What it demonstrates |
| --- | --- | --- |
| Northstar Studio | `/examples/landing/` | A polished landing page, nested CSS, SVG, and responsive layout |
| Signal Contact | `/examples/contact/` | A browser form with client-side handling |
| Field Notes | `/examples/blog/` | A small multi-page site with an article route and shared stylesheet |
| Pulse Dashboard | `/examples/dashboard/` | A static dashboard with client-side filtering and rendering |

The examples use no external CDNs, build tools, fonts, or JavaScript packages.
They are intentionally plain files that can be copied, edited, and served
immediately.

## Production note

`python main.py` starts Flask's development server for convenience. If this
is exposed to the public internet, put a production WSGI server and a reverse
proxy in front of it.
