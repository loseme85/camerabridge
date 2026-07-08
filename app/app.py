from __future__ import annotations

import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.search import endpoint_response  # noqa: E402


app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
@app.route("/search")
def index() -> str:
    return render_template("index.html")


@app.route("/qa")
def qa_index() -> str:
    return render_template("index.html")


@app.route("/beta")
def beta_index() -> str:
    return render_template("beta.html")


@app.route("/api/search")
def search_api():
    status, payload = endpoint_response(request.args)
    return jsonify(payload), status


if __name__ == "__main__":
    app.run(debug=True)
