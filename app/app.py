from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, make_response, redirect, render_template, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.search import endpoint_response  # noqa: E402


app = Flask(__name__, template_folder="templates", static_folder="static")


def _public_url_with_query() -> str:
    query_string = request.query_string.decode("utf-8")
    return f"/?{query_string}" if query_string else "/"


@app.route("/")
def index() -> str:
    return render_template("beta.html")


@app.route("/search")
def search_redirect():
    return redirect(_public_url_with_query(), code=302)


@app.route("/qa")
def qa_index():
    response = make_response(render_template("index.html"))
    response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive"
    return response


@app.route("/beta")
def beta_redirect():
    return redirect(_public_url_with_query(), code=302)


@app.route("/api/search")
def search_api():
    status, payload = endpoint_response(request.args)
    return jsonify(payload), status


if __name__ == "__main__":
    app.run(debug=True)
