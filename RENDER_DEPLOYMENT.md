# 🚀 How to Deploy to Render (Step-by-Step Guide)

This guide walks you through deploying the **LPU Student Registration Finder** on [Render](https://render.com) using either the **Render Blueprint (1-Click)** or **Manual Web Service** setup.

---

## 📋 Quick Deployment Settings

| Setting | Value |
| :--- | :--- |
| **Runtime / Environment** | `Python` (or `Python 3`) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |
| **Root Directory** | `.` (leave empty / default repository root) |
| **Health Check Path** | `/health` |

---

## 🔑 Required Environment Variables on Render

In your Render Service dashboard (**Environment** tab), add the following environment variables:

| Variable Name | Required | Description / Example Value |
| :--- | :---: | :--- |
| `SPREADSHEET_ID` | **Yes** | `17uwtDRRNBIPZ-jrJ1g9tCP-Zw62zwrz-aO5IsmihgTE` *(or your Google Sheet ID)* |
| `SHEET_NAME` | **Yes** | `Sheet1` |
| `GOOGLE_CREDENTIALS_JSON` | **Yes** | Full raw content of your `credentials.json` service account file |
| `PYTHON_VERSION` | Optional | `3.11.9` |
| `FLASK_DEBUG` | Optional | `False` |

> [!TIP]
> **How to set `GOOGLE_CREDENTIALS_JSON`**:
> 1. Open your Google Service Account `credentials.json` file in a text editor (Notepad, VS Code, etc.).
> 2. Copy the entire JSON content: `{"type": "service_account", "project_id": "...", ...}`.
> 3. In Render -> **Environment** -> **Add Environment Variable**, set Key = `GOOGLE_CREDENTIALS_JSON` and Value = paste the copied JSON text.
> 4. Click **Save Changes**.

---

## 🛠️ Deployment Methods

### Option A: Deploy via Render Blueprint (`render.yaml`) — Recommended

If your repository has `render.yaml` (already included in this project):

1. Push this repository to your **GitHub** / **GitLab** account.
2. Log in to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** in the top right and select **Blueprint**.
4. Connect your GitHub repository (`Registation-No-FInder`).
5. Render will automatically detect `render.yaml` and configure:
   - Service name: `lpu-registration-finder`
   - Build & Start commands
   - Health check `/health`
6. Fill in the prompted Environment Variables:
   - `SPREADSHEET_ID`
   - `GOOGLE_CREDENTIALS_JSON`
7. Click **Apply**. Render will build and deploy your app!

---

### Option B: Manual Web Service Creation

1. Push your repository to **GitHub**.
2. Go to [dashboard.render.com](https://dashboard.render.com) and click **New +** -> **Web Service**.
3. Select **Build and deploy from a Git repository** and connect your repository.
4. Fill in the Web Service details:
   - **Name**: `lpu-registration-finder` (or your preferred name)
   - **Language**: `Python 3`
   - **Branch**: `main` (or `master`)
   - **Region**: Choose the region closest to your users (e.g., *Singapore*, *Frankfurt*, *Oregon*)
   - **Root Directory**: Leave blank (defaults to root)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Instance Type**: `Free`
5. Expand **Advanced** settings:
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: `Yes`
6. Click **Add Environment Variable** for:
   - `SPREADSHEET_ID`: `17uwtDRRNBIPZ-jrJ1g9tCP-Zw62zwrz-aO5IsmihgTE`
   - `SHEET_NAME`: `Sheet1`
   - `GOOGLE_CREDENTIALS_JSON`: *(Paste your service account JSON)*
7. Click **Create Web Service**.

---

### Option C: Using Render Secret Files (Alternative to `GOOGLE_CREDENTIALS_JSON`)

If you prefer uploading `credentials.json` as a secret file instead of an environment variable:
1. In your Render Web Service dashboard, go to the **Environment** tab.
2. Scroll to **Secret Files**.
3. Click **Add Secret File**:
   - **File Name**: `credentials.json` or `/etc/secrets/credentials.json`
   - **Contents**: Paste the content of your `credentials.json`
4. The backend is configured to automatically check `/etc/secrets/credentials.json` and `credentials.json`.

---

## 🔒 Important: Google Sheet Permissions Checklist

Make sure your Google Sheet is shared with your Google Service Account email:
1. Open your Google Sheet in a browser.
2. Click the **Share** button in the top right.
3. Add your Service Account email (found inside `credentials.json` under `"client_email"`, e.g., `xxx@project-name.iam.gserviceaccount.com`).
4. Set permission to **Viewer** (Read-Only).
5. Click **Done**.

---

## 🧪 Verification & Testing

Once deployed, Render will provide a public URL (e.g., `https://lpu-registration-finder.onrender.com`):

1. **Frontend UI**: Open `https://your-service.onrender.com/` in your browser.
2. **Health Check**: Open `https://your-service.onrender.com/health` -> should return:
   ```json
   {
     "status": "healthy",
     "service": "student-registration-finder",
     "sheet_configured": true
   }
   ```
3. **Search API**: Test searching a student name:
   `https://your-service.onrender.com/api/student?query=Ashish`

---

## ❓ Troubleshooting

- **500 Internal Server Error (Google Sheets not accessible)**:
  - Verify that the Service Account email has **Viewer** permissions on the Google Sheet.
  - Check that `SPREADSHEET_ID` is correct and does not contain spaces.
  - Verify that `GOOGLE_CREDENTIALS_JSON` contains valid JSON.

- **404 Page Not Found on Frontend**:
  - The static frontend files are in `Registation_finder/frontend`. The root `wsgi.py` automatically detects and serves them.

- **Slow first response (Cold Start)**:
  - Render free tier instances spin down after 15 minutes of inactivity. The first request after sleep may take ~30-50 seconds while the instance wakes up.
