"""
Root app.py proxy for WSGI / Gunicorn compatibility.
"""
from wsgi import app

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    default_host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"
    host = os.getenv("HOST", default_host)
    app.run(host=host, port=port)
