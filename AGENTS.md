# EasyWeb Agent and Contributor Guide

## Overview

EasyWeb is a single-file Python web server designed for zero-configuration,
drop-in static hosting combined with a small backend file-writing endpoint.
Place an HTML file, asset, or folder in `public/`, run `python main.py`, and
the content is available at the matching URL path. Form submissions and raw
JSON requests can be appended locally for simple prototypes, landing pages,
and lightweight data collection.

## Directory architecture

```text
EasyWeb/
├── main.py          # Core server logic (static serving + file I/O)
├── AGENTS.md        # AI agent instructions & documentation
├── requirements.txt # Dependencies
└── public/          # Place HTML files and folders here to host them
```

The `public/` directory is runtime content. For example:

```text
public/
├── index.html
├── about.html
├── styles.css
└── blog/
    └── post.html
```

These files are served as `/`, `/about.html`, `/styles.css`, and
`/blog/post.html` respectively. A folder containing its own `index.html` is
also served at the folder URL.

## Agent guidelines and rules

1. Maintain the single-file constraint for `main.py`. Keep server behavior,
   static-file routing, and the submission handler in that file unless the
   project owner explicitly changes this requirement.
2. Keep file-writing operations safe and append-only by default. Do not
   truncate, replace, or delete collected submissions without explicit user
   approval. Preserve timestamps and use UTF-8 when adding new output.
3. Do not add a complex database ORM or database service unless explicitly
   requested. The local append-only file is intentional for this project.
4. Keep static file access confined to `public/`. Preserve path-traversal
   protections when changing routing code.
5. Avoid committing secrets, personal submissions, generated caches, or
   virtual environments. Treat `submissions.txt` as local data.
6. Prefer small, dependency-light changes. Update `requirements.txt` when a
   runtime dependency is genuinely necessary.
7. Validate changes with a syntax check and a focused request test before
   handing them off.

## Server behavior

- `GET /` serves `public/index.html` when it exists. Otherwise it serves an
  embedded HTML form that posts to `/submit`.
- `GET /<path>` serves files and nested files from `public/`. Directories are
  redirected to a trailing-slash URL and use their `index.html` when present.
- `POST /submit` accepts HTML form fields, JSON payloads, or a raw request body.
  Each request is appended as one timestamped JSON record per line to
  `submissions.txt`.
- JSON requests, or requests that explicitly prefer JSON, receive a JSON
  success response. Browser form posts receive a small HTML confirmation page.
- The development server binds to `0.0.0.0:8000` when started with
  `python main.py`.

## Setup and run

From the repository root:

```bash
python -m venv .venv
# Activate the environment using the command for your shell.
pip install -r requirements.txt
python main.py
```

Then open <http://localhost:8000>. Add or edit files in `public/` and refresh
the browser to serve them.

## Verification checklist

Before committing a change, confirm that:

```bash
python -m py_compile main.py
```

You should also check the root fallback, a file under `public/`, a nested
folder file, and both form and JSON submissions. Remove any test submission
data afterward only when it was created solely for the test and the user has
not asked to preserve it.

## Change workflow

Keep commits focused and describe the user-visible behavior. Review the diff
before committing, and do not rewrite unrelated user changes. The canonical
remote is:

```text
https://github.com/Coderofpears/EasyWeb.git
```
