# Student Result Portal - Flask Backend 🐍

A lightweight, beginner-friendly REST API built with **Python 3**, **Flask**, and **Flask-CORS** to serve student examination results.

---

## 📁 Backend Structure

```text
backend/
├── app.py               # Flask application, REST endpoints, CORS & mock dataset
├── requirements.txt     # Python package dependencies
├── .env                 # Local server environment configuration
├── .env.example         # Template for environment variables (and future Google Sheets keys)
└── README.md            # Backend instructions and testing guide
```

---

## 🛠️ Step-by-Step Setup Guide (Windows)

### 1. Open Terminal in the `backend` folder
```powershell
cd "d:\100 Project\Backend project\New folder\student-result-portal\backend"
```

### 2. Create a Python Virtual Environment
Creating a virtual environment ensures dependencies don't conflict with other projects:
```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment
- **On Windows PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  *(If you get a script execution policy error on PowerShell, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and then run the activate command again).*

- **Or on Windows Command Prompt (cmd.exe)**:
  ```cmd
  venv\Scripts\activate.bat
  ```

Once activated, your terminal prompt will show `(venv)`.

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Start the Flask Server
```powershell
python app.py
```

The server will start at:
👉 **`http://127.0.0.1:5000`**

---

## 📡 API Endpoint Reference

### Search Student Result
**Endpoint:** `GET /api/student`  
**Query Parameters:**
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | string | **Yes** | Student Name or Registration Number (case-insensitive) |

#### Example Request:
```http
GET http://127.0.0.1:5000/api/student?query=Ashish
```
or
```http
GET http://127.0.0.1:5000/api/student?query=12345
```

---

## 📥 Sample API Responses

### 1. Success Response (`200 OK`)
```json
{
  "success": true,
  "student": {
    "registration_no": "12345",
    "name": "Ashish Kumar",
    "cpp": 85,
    "python": 90,
    "web_development": 88,
    "total": 263,
    "percentage": 87.67,
    "result": "Pass"
  }
}
```

### 2. Student Not Found (`404 Not Found`)
```json
{
  "success": false,
  "message": "Student not found"
}
```

### 3. Empty Query (`400 Bad Request`)
```json
{
  "success": false,
  "message": "Please enter a student name or registration number"
}
```

---

## 🧪 Testing the API

### Method A: Browser
Simply paste these URLs in Google Chrome or Microsoft Edge:
1. Health check: `http://127.0.0.1:5000/`
2. Search Ashish: `http://127.0.0.1:5000/api/student?query=Ashish`
3. Search by Registration No: `http://127.0.0.1:5000/api/student?query=12345`
4. Test Fail Student: `http://127.0.0.1:5000/api/student?query=12348`
5. Test Not Found: `http://127.0.0.1:5000/api/student?query=Unknown`

### Method B: Postman
1. Open **Postman**.
2. Create a new **HTTP Request**.
3. Select method: **`GET`**.
4. Enter URL: `http://127.0.0.1:5000/api/student?query=Ashish`.
5. Click **Send** and inspect the returned JSON body and HTTP status code (`200 OK`).

---

## 🔄 Request Flow Architecture

```text
[ User Browser / Frontend ]
           │
           │  1. GET /api/student?query=Ashish
           ▼
   [ Flask REST API ]  (app.py on port 5000)
           │
           │  2. Validates query & searches in dataset
           ▼
    [ Mock Dataset ]   (MOCK_STUDENTS list)
           │
           │  3. Formats student record as JSON
           ▼
[ JSON Response: 200 OK ]
           │
           │  4. JavaScript parses student & updates result card
           ▼
[ Rendered Student Scorecard UI ]
```
