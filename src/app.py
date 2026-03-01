#!/usr/bin/env python3
"""
NKP Demo Connector — minimal sample app that verifies connectivity to Weaviate.
Demonstrates catalog dependency flow: enable Weaviate first, then this app.
"""
import os
import sys
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

WEAVIATE_URL = os.environ.get("WEAVIATE_URL", "http://weaviate.weaviate.svc.cluster.local:80")

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>NKP Demo Connector</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 600px; margin: 2rem auto; padding: 1rem; }
    .status { padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    .ok { background: #d4edda; color: #155724; }
    .err { background: #f8d7da; color: #721c24; }
    h1 { color: #333; }
    code { background: #f4f4f4; padding: 0.2em 0.4em; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>NKP Demo Connector</h1>
  <p>Sample app demonstrating NKP catalog composability. This app depends on <strong>Weaviate</strong>.</p>
  <h2>Status</h2>
  <div class="status {{ status_class }}">{{ message }}</div>
  <p><small>Weaviate URL: <code>{{ weaviate_url }}</code></small></p>
</body>
</html>
"""


def check_weaviate():
    """Check if Weaviate is reachable."""
    try:
        import requests
        r = requests.get(f"{WEAVIATE_URL.rstrip('/')}/v1/.well-known/ready", timeout=5)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)


@app.route("/")
def index():
    ok, detail = check_weaviate()
    status_class = "ok" if ok else "err"
    if ok:
        message = "Weaviate: Connected"
    else:
        message = f"Weaviate: Not reachable ({detail}). Enable Weaviate in the workspace first."
    return render_template_string(
        HTML,
        status_class=status_class,
        message=message,
        weaviate_url=WEAVIATE_URL,
    )


@app.route("/health")
def health():
    ok, _ = check_weaviate()
    return jsonify({"weaviate": "ok" if ok else "unreachable"}), 200 if ok else 503


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
