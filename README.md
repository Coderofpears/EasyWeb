# EasyWeb

EasyWeb is a tiny Flask web server for dropping a folder of static files into
`public/` and serving it immediately. It also includes one deliberately small
backend endpoint for appending form, JSON, or raw request data to a local,
timestamped file.

The repository includes a small example gallery so you can see nested pages,
assets, JavaScript, forms, and client-side data all working from the same
server.

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

If `public/index.html` is absent, EasyWeb serves an embedded page with a form
that posts to `/submit`. This means a completely empty checkout is still
usable after installing Flask.

## Included examples

Start the server and use the gallery at `/` or open these pages directly:

| Example | URL | What it demonstrates |
| --- | --- | --- |
| Northstar Studio | `/examples/landing/` | A polished landing page, nested CSS, SVG, and responsive layout |
| Signal Contact | `/examples/contact/` | A browser form that sends JSON to `/submit` and displays the response |
| Field Notes | `/examples/blog/` | A small multi-page site with an article route and shared stylesheet |
| Pulse Dashboard | `/examples/dashboard/` | A static dashboard with client-side filtering and rendering |

The examples use no external CDNs, build tools, fonts, or JavaScript packages.
They are intentionally plain files that can be copied, edited, and served
immediately.

## Writing data

`POST /submit` accepts three input styles:

### HTML forms

```bash
curl -i -X POST http://localhost:8000/submit \
  -H "Accept: application/json" \
  --data-urlencode "name=Ada" \
  --data-urlencode "message=Hello from a form"
```

### JSON

```bash
curl -i http://localhost:8000/submit \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"source":"curl","rating":5}'
```

### Raw request bodies

```bash
curl -i -X POST http://localhost:8000/submit \
  -H "Content-Type: text/plain" \
  --data-binary "plain text is accepted too"
```

Each successful request is appended as one UTF-8 JSON record per line to
`submissions.txt`:

```json
{"timestamp":"2026-08-25T20:00:00Z","data":{"rating":5}}
```

The file is intentionally append-only and is not served from `public/`.
Back it up, rotate it, or replace it with a real database only when the
application requirements justify that change.

## Production note

`python main.py` starts Flask's development server for convenience. If this
is exposed to the public internet, put a production WSGI server and a reverse
proxy in front of it, restrict who can call `/submit`, and add size/rate
limits appropriate to the data being collected.
