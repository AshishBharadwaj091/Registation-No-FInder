"""
=============================================================================
WSGI Entry Point for Production Deployment (Render, Gunicorn, Docker)
=============================================================================
"""
import os
import sys

# Add project root and backend directory to Python sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, "Registation_finder", "backend")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from Registation_finder.backend.app import app  # noqa: E402

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    default_host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"
    host = os.getenv("HOST", default_host)
    app.run(host=host, port=port)
