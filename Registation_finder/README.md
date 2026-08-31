# Student Result Search Portal 🎓

A modern, responsive, and full-stack student examination result portal.

---

## 📁 Complete Project Structure

```text
student-result-portal/
├── frontend/
│   ├── index.html          # Semantic HTML5 markup, accessible search & scorecard UI
│   ├── style.css           # Academic slate/navy design, animations, mobile-first CSS & print view
│   └── script.js           # REST API client connecting to Flask backend (GET /api/student)
├── backend/
│   ├── app.py              # Flask application, REST endpoints, CORS & mock dataset
│   ├── requirements.txt    # Python dependencies (Flask, Flask-Cors, python-dotenv)
│   ├── .env                # Local server configuration
│   ├── .env.example        # Template for server & future Google Sheets credentials
│   └── README.md           # Backend setup, virtualenv guide & API documentation
└── README.md               # Main project documentation & quickstart guide
```

---

## ⚡ How to Run the Project (Step-by-Step)

### Step 1: Start the Flask Backend (Terminal 1)
```powershell
# 1. Navigate to the backend folder
cd "d:\100 Project\Backend project\New folder\student-result-portal\backend"

# 2. Create a virtual environment (first time only)
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Start the server
python app.py
```
Your backend will run at:
👉 **`http://127.0.0.1:5000`**

---

### Step 2: Open the Frontend (Terminal 2 or File Explorer)

> [!NOTE]
> This project uses **HTML, CSS, and Vanilla JavaScript** with a **Python Flask** backend.
> Do **NOT** run `npm run dev` because there is no Node/React bundle.

Choose any simple method:

#### Option A: Direct Double Click (Easiest)
Navigate to `student-result-portal/frontend/` and double-click **`index.html`** to open in any web browser.

#### Option B: Python HTTP Server
```powershell
python -m http.server 3000 --directory "d:\100 Project\Backend project\New folder\student-result-portal\frontend"
```
Then open: **`http://localhost:3000`**

---

## 📡 REST API Reference

### Search Endpoint: `GET /api/student`
Query Parameters:
- `query` *(required)*: Student Name or Registration Number.

#### Examples:
- `GET http://127.0.0.1:5000/api/student?query=Ashish`
- `GET http://127.0.0.1:5000/api/student?query=12345`

#### Responses:
- **Success (`200 OK`)**:
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
- **Student Not Found (`404 Not Found`)**:
  ```json
  {
    "success": false,
    "message": "Student not found"
  }
  ```
- **Empty Search (`400 Bad Request`)**:
  ```json
  {
    "success": false,
    "message": "Please enter a student name or registration number"
  }
  ```

---

## 🔄 End-to-End Request Flow

```text
[ User Types "Ashish" & Clicks Search ]
                  │
                  ▼
[ Frontend (script.js) ]
  • Validates input
  • Triggers loading spinner
  • Sends HTTP Request:
    GET http://127.0.0.1:5000/api/student?query=Ashish
                  │
                  ▼
[ Flask REST API (app.py) ]
  • CORS middleware allows origin
  • Sanitizes & normalizes query to lowercase
  • Searches student records
                  │
                  ▼
[ Python Data Matching ]
  • Matches name substring or registration_no
  • Prepares JSON response with HTTP 200 / 404 / 400
                  │
                  ▼
[ JSON Response received in Frontend ]
  • script.js parses response
  • Renders Student Name, Registration No, Subject Marks
  • Computes grade pills (A+, A, B, C, F)
  • Updates Pass / Fail badge & progress bars
                  │
                  ▼
[ Verified Result Card Displayed to User ]
```
