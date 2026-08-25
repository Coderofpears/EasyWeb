"""EasyWeb: zero-configuration static hosting with a small write endpoint.

Place HTML files, assets, and folders in ``./public`` and start the server with
``python main.py``.  The server listens on port 8000 by default.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from flask import Flask, Response, abort, jsonify, redirect, request, send_from_directory, url_for
from werkzeug.utils import safe_join


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
SUBMISSIONS_FILE = BASE_DIR / "submissions.txt"

app = Flask(__name__)
_submission_lock = Lock()

FALLBACK_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EasyWeb</title>
  <style>
    :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
    body { max-width: 42rem; margin: 4rem auto; padding: 0 1rem; line-height: 1.5; }
    form { display: grid; gap: 0.75rem; }
    textarea { min-height: 10rem; padding: 0.75rem; font: inherit; }
    button { width: fit-content; padding: 0.6rem 1rem; font: inherit; cursor: pointer; }
  </style>
</head>
<body>
  <h1>EasyWeb</h1>
  <p>Add an <code>index.html</code> file to <code>./public</code> to replace this page.</p>
  <form action="/submit" method="post">
    <label for="message">Submission</label>
    <textarea id="message" name="message" placeholder="Type something to save..."></textarea>
    <button type="submit">Save submission</button>
  </form>
</body>
</html>
"""


def utc_timestamp() -> str:
    """Return an unambiguous UTC timestamp for a stored submission."""

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_submission() -> Any:
    """Read form data, JSON, or a raw request body in that order of preference."""

    if request.is_json:
        payload = request.get_json(silent=True)
        return payload if payload is not None else request.get_data(as_text=True)

    if request.form:
        return request.form.to_dict(flat=False)

    return request.get_data(as_text=True)


def save_submission(data: Any) -> str:
    """Append one JSON record to the local submissions file."""

    timestamp = utc_timestamp()
    record = {"timestamp": timestamp, "data": data}
    line = json.dumps(record, ensure_ascii=False, default=str)

    # A lock prevents concurrent threaded requests in this process from
    # interleaving their append operations.  The file is never truncated.
    with _submission_lock:
        with SUBMISSIONS_FILE.open("a", encoding="utf-8") as output_file:
            output_file.write(line + "\n")

    return timestamp


@app.get("/")
def index() -> Response:
    """Serve ``public/index.html`` or the built-in submission page."""

    index_file = PUBLIC_DIR / "index.html"
    if index_file.is_file():
        return send_from_directory(str(PUBLIC_DIR), "index.html")

    return Response(FALLBACK_HTML, mimetype="text/html")


@app.post("/submit")
def submit() -> Response:
    """Append form, JSON, or raw-body data to ``submissions.txt``."""

    data = read_submission()
    timestamp = save_submission(data)

    if request.is_json or request.accept_mimetypes.best == "application/json":
        return jsonify({"status": "ok", "message": "Submission saved.", "timestamp": timestamp}), 201

    return Response(
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Submission saved</title></head>
<body><h1>Submission saved</h1><p>Your data was appended to <code>submissions.txt</code>.</p>
<p><a href="/">Return to EasyWeb</a></p></body></html>""",
        status=201,
        mimetype="text/html",
    )


@app.get("/<path:requested_path>")
def serve_public(requested_path: str) -> Response:
    """Serve any safe file below ``public``, including files in subfolders."""

    # safe_join rejects traversal attempts before the path is inspected or sent.
    safe_path = safe_join(str(PUBLIC_DIR), requested_path)
    if safe_path is None:
        abort(404)

    target = Path(safe_path)
    if target.is_dir():
        if not requested_path.endswith("/"):
            return redirect(url_for("serve_public", requested_path=requested_path + "/"))

        directory_index = target / "index.html"
        if directory_index.is_file():
            index_path = f"{requested_path.rstrip('/')}/index.html"
            return send_from_directory(str(PUBLIC_DIR), index_path)

        abort(404)

    if target.is_file():
        return send_from_directory(str(PUBLIC_DIR), requested_path)

    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
