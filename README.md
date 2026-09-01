# LPU Student Registration Finder 🎓

A modern, responsive web application for finding student registration numbers from a secure Google Sheet backend.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/AshishBharadwaj091/Registation-No-FInder)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## 📁 Clean & Organized Project Structure

```text
Registation-No-FInder/
├── api/
│   └── index.py                # Vercel Serverless Function entrypoint
├── backend/
│   ├── app.py                  # Core Flask REST API, Google Sheets client & caching
│   ├── requirements.txt        # Backend dependencies
│   └── .env.example            # Environment variables template
├── public/                     # Static Frontend UI assets (HTML, CSS, JS, Images)
│   ├── index.html              # Semantic accessible UI
│   ├── style.css               # Styling & micro-animations
│   ├── script.js               # REST API client & clipboard handler
│   ├── lpu-logo.png            # LPU branding logo
│   └── campus-bg.png           # University campus background
├── wsgi.py                     # Production WSGI entry point (Gunicorn / Render / Local)
├── app.py                      # Root proxy entry point
├── render.yaml                 # Render Blueprint specification
├── vercel.json                 # Vercel Serverless routing & CDN configuration
├── Procfile                    # PaaS process configuration
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container deployment configuration
├── VERCEL_DEPLOYMENT.md        # Comprehensive Vercel serverless deployment guide
├── RENDER_DEPLOYMENT.md        # Comprehensive Render deployment guide
└── README.md
```

---

## ⚡ Deploy to Vercel (Serverless Full-Stack)

1. **Push this repository to GitHub**.
2. Go to [vercel.com/new](https://vercel.com/new) and import your repository.
3. In **Environment Variables**, add:
   - `SPREADSHEET_ID`: Your Google Spreadsheet ID
   - `SHEET_NAME`: `Sheet1`
   - `GOOGLE_CREDENTIALS_JSON`: Paste the full JSON text of your Google Service Account key
4. Click **Deploy**!

👉 For detailed Vercel CLI and dashboard instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md).

---

## 🚀 Deploy to Render

1. **Push this repository to GitHub**.
2. Go to [Render Dashboard](https://dashboard.render.com) and click **New +** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml`.
4. Add your **`SPREADSHEET_ID`** and **`GOOGLE_CREDENTIALS_JSON`**.
5. Click **Apply**!

👉 For detailed Render instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).

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
- **`GET /api/student?query=<student_name>`**: Searches records in the Google Sheet.
- **`GET /api/health`**: Healthcheck endpoint (`{"status": "healthy"}`).
- **`POST /api/refresh-cache`**: Forces a fresh fetch from Google Sheets.
