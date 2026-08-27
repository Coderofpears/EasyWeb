"""EasyWeb: zero-configuration static hosting for HTML files and folders.

Place HTML files, assets, and folders in ``./public`` and start the server with
``python main.py``. The server listens on port 8000 by default.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, Response, abort, redirect, send_from_directory, url_for
from werkzeug.utils import safe_join

# Server port
Port = 8000

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"

app = Flask(__name__)
#Change this if you want a custom 404 site.
FALLBACK_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>EasyWeb</title>
</head>
<body>
  <h1>404 - There is nothing at this website.</h1>
  <a href="/index.html">
    <button type="button">Go to index.html</button>
  </a>
</body>
</html>
"""


@app.get("/")
def index() -> Response:
    """Serve ``public/index.html`` or the built-in fallback page."""

    index_file = PUBLIC_DIR / "index.html"
    if index_file.is_file():
        return send_from_directory(str(PUBLIC_DIR), "index.html")

    return Response(FALLBACK_HTML, mimetype="text/html")


@app.get("/<path:requested_path>")
def serve_public(requested_path: str) -> Response:
    """Serve any safe file below ``public``, including files in subfolders."""

    safe_path = safe_join(str(PUBLIC_DIR), requested_path)
    if safe_path is None:
        abort(404)

    target = Path(safe_path)

    if target.is_dir():
        if not requested_path.endswith("/"):
            return redirect(
                url_for("serve_public", requested_path=requested_path + "/")
            )

        directory_index = target / "index.html"
        if directory_index.is_file():
            index_path = f"{requested_path.rstrip('/')}/index.html"
            return send_from_directory(str(PUBLIC_DIR), index_path)

        abort(404)

    if target.is_file():
        return send_from_directory(str(PUBLIC_DIR), requested_path)

    abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Port, debug=False)
