# ⚡ How to Deploy to Vercel (Serverless Full-Stack Guide)

This guide walks you through deploying the **LPU Student Registration Finder** on **Vercel** with a **Serverless Python Backend** (`/api/*`) and a **Global CDN Static Frontend**.

---

## 🏗️ Architecture Overview

- **Frontend**: Served automatically from `Registation_finder/frontend` via Vercel's Global Edge Network (sub-millisecond load times).
- **Backend API**: Runs on Vercel Serverless Python Functions via `api/index.py` (zero idle server costs, scales to 0 and auto-scales on demand).
- **Routing**: Managed by `vercel.json` rewrites.

---

## 🔑 Required Environment Variables on Vercel

In your Vercel Project settings (**Settings** &rarr; **Environment Variables**), add the following:

| Variable Name | Required | Example / Description |
| :--- | :---: | :--- |
| `SPREADSHEET_ID` | **Yes** | `17uwtDRRNBIPZ-jrJ1g9tCP-Zw62zwrz-aO5IsmihgTE` *(or your Google Sheet ID)* |
| `SHEET_NAME` | **Yes** | `Sheet1` |
| `GOOGLE_CREDENTIALS_JSON` | **Yes** | Paste the entire content of your `credentials.json` |

> [!TIP]
> **How to add `GOOGLE_CREDENTIALS_JSON` on Vercel**:
> 1. Open your `credentials.json` file in VS Code or Notepad.
> 2. Copy the entire JSON text (`{"type": "service_account", ...}`).
> 3. In Vercel Project &rarr; **Settings** &rarr; **Environment Variables**:
>    - **Key**: `GOOGLE_CREDENTIALS_JSON`
>    - **Value**: Paste the copied JSON text
>    - Select Environments: **Production**, **Preview**, and **Development**
> 4. Click **Save**.

---

## 🚀 Deployment Methods

### Option A: Deploy via Vercel Web Dashboard (Recommended)

1. **Push this repository to GitHub**:
   ```bash
   git add .
   git commit -m "Add Vercel serverless deployment"
   git push origin main
   ```

2. Go to [vercel.com/new](https://vercel.com/new) and log in.
3. Under **Import Git Repository**, select your repository (`Registation-No-FInder`).
4. In the configuration screen:
   - **Project Name**: `lpu-registration-finder` (or your preferred name)
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (leave default)
5. Expand the **Environment Variables** section and add:
   - `SPREADSHEET_ID`: `your_spreadsheet_id`
   - `SHEET_NAME`: `Sheet1`
   - `GOOGLE_CREDENTIALS_JSON`: *(Paste your service account JSON)*
6. Click **Deploy**.
7. In ~30-60 seconds, your site will be live at `https://your-project.vercel.app`! 🎉

---

### Option B: Deploy via Vercel CLI

If you have Node.js / npm installed, you can deploy in one command:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login and Deploy**:
   ```bash
   vercel
   ```
   Follow the interactive prompts (accept defaults).

3. **Add Environment Variables via CLI**:
   ```bash
   vercel env add SPREADSHEET_ID production
   vercel env add SHEET_NAME production
   vercel env add GOOGLE_CREDENTIALS_JSON production
   ```

4. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

---

## 🔒 Important: Google Sheet Permissions Checklist

Make sure your Google Sheet is shared with your Google Service Account:
1. Open your Google Sheet in a browser.
2. Click **Share** (top right).
3. Paste the `"client_email"` found inside your `credentials.json` (e.g. `sheet-reader@xxx.iam.gserviceaccount.com`).
4. Set permission to **Viewer** (Read-Only).
5. Click **Done**.

---

## 🧪 Verification & Testing on Vercel

Once deployed, test your Vercel URL (e.g., `https://lpu-registration-finder.vercel.app`):

1. **Frontend**: Open `https://your-project.vercel.app/` &rarr; verify search UI and student cards render smoothly.
2. **Health Check**: Open `https://your-project.vercel.app/api/health` &rarr; returns:
   ```json
   {
     "status": "healthy",
     "service": "student-registration-finder",
     "sheet_configured": true
   }
   ```
3. **Search API**: Open `https://your-project.vercel.app/api/student?query=Ashish` &rarr; returns matched student records.

---

## ❓ Troubleshooting

- **500 Server Error (Google Sheet Not Accessible)**:
  - Check that the Google Sheet is shared with the Service Account's `client_email`.
  - Check that `GOOGLE_CREDENTIALS_JSON` in Vercel Environment Variables is valid JSON.

- **Vercel Function Timeout**:
  - Vercel Hobby tier allows 10s execution for serverless functions (Pro allows 60s). Because caching is enabled in `app.py`, repeated queries respond in milliseconds.
