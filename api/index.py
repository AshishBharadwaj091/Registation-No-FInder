"""
=============================================================================
Vercel Serverless Function Entrypoint
=============================================================================
This file exposes the WSGI Flask `app` instance to Vercel's Python runtime.
All requests matching `/api/*` are handled by this serverless function.
"""
import os
import sys

# Ensure root and backend directory are in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
backend_dir = os.path.join(root_dir, "Registation_finder", "backend")

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import the configured Flask application
from Registation_finder.backend.app import app  # noqa: E402

# Expose app for Vercel WSGI handler
handler = app
app = app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
