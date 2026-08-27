# EasyWeb Agent and Contributor Guide

## Overview

EasyWeb is a single-file Python web server designed for zero-configuration,
drop-in static hosting. Place an HTML file, asset, or folder in `public/`, run
`python main.py`, and the content is available at the matching URL path.

## Directory architecture

```text
EasyWeb/
├── main.py          # Core server logic (static serving)
├── AGENTS.md        # AI agent instructions & documentation
├── README.md        # User-facing documentation
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

1. Maintain the single-file constraint for `main.py`. Keep server behavior and
   static-file routing in that file unless the project owner explicitly changes
   this requirement.
2. Keep static file access confined to `public/`. Preserve path-traversal
   protections when changing routing code.
3. Avoid committing caches, generated content, or virtual environments.
4. Prefer small, dependency-light changes. Update `requirements.txt` when a
   runtime dependency is genuinely necessary.
5. Validate changes with a syntax check before handing them off.
6. Keep documentation (AGENTS.md and README.md) synchronized with `main.py`
   capabilities.

## Server behavior

- `GET /` serves `public/index.html` when it exists. Otherwise it serves an
  embedded HTML page with a link to index.html.
- `GET /<path>` serves files and nested files from `public/`. Directories are
  redirected to a trailing-slash URL and use their `index.html` when present.
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

You should also check:
- The root fallback (when `public/index.html` is missing)
- A file under `public/`
- A nested folder file
- Directory redirect behavior

## Change workflow

Keep commits focused and describe the user-visible behavior. Review the diff
before committing, and do not rewrite unrelated user changes. The canonical
remote is:

```text
https://github.com/Coderofpears/EasyWeb.git
```
