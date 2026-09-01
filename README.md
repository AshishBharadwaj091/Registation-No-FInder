# LPU Student Registration Finder 🎓

A modern, responsive web application for finding student registration numbers from a secure Google Sheet backend.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## 📁 Project Structure

```text
Registation-No-FInder/
├── wsgi.py                     # Production WSGI entry point (Gunicorn)
├── app.py                      # Root proxy entry point
├── render.yaml                 # Render Blueprint specification
├── Procfile                    # PaaS process configuration
├── requirements.txt            # Production Python dependencies
├── Dockerfile                  # Container deployment configuration
├── RENDER_DEPLOYMENT.md        # Comprehensive Render deployment guide
├── Registation_finder/
│   ├── frontend/
│   │   ├── index.html          # Semantic responsive UI
│   │   ├── style.css           # Styling & animations
│   │   ├── script.js           # REST API client & clipboard handler
│   │   ├── lpu-logo.png        # Branding logo
│   │   └── campus-bg.png       # Background asset
│   └── backend/
│       ├── app.py              # Flask REST API, Google Sheets client & caching
│       ├── requirements.txt    # Backend dependencies
│       └── .env.example        # Environment variables template
└── README.md
```

---

## 🚀 Cloud Deployment (Render)

Deploying to Render takes less than 2 minutes:

1. **Push this repository to GitHub**.
2. Go to [Render Dashboard](https://dashboard.render.com) and click **New +** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml`.
4. Add your **Google Sheet ID** (`SPREADSHEET_ID`) and paste your Google Service Account JSON into **`GOOGLE_CREDENTIALS_JSON`**.
5. Click **Apply**!

👉 For detailed manual and secret file setup instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

---

## 💻 Local Development

### 1. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your `SPREADSHEET_ID` and place your `credentials.json` in the project root or backend folder (or set `GOOGLE_CREDENTIALS_JSON`).

### 3. Run Locally
```bash
# Development server
python app.py

# Or Production Gunicorn server
gunicorn wsgi:app
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📡 API Endpoints

- **`GET /`**: Serves the frontend single page app.
- **`GET /health`**: Healthcheck endpoint for Render (`{"status": "healthy"}`).
- **`GET /api/student?query=<student_name>`**: Searches records in the Google Sheet.
- **`POST /api/refresh-cache`**: Forces a fresh fetch from Google Sheets.
