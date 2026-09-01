"""
=============================================================================
Student Registration Search Portal - Flask REST API Backend (Google Sheets)
=============================================================================
Searches student records in a private Google Sheet by student NAME (case-insensitive
& partial matching) and returns ONLY their Name and Registration Number.
"""

import os
import time
import re
import json
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

# Load environment variables from .env
load_dotenv()

# Determine frontend directory reliably
script_dir = os.path.dirname(os.path.abspath(__file__))
frontend_candidates = [
    os.path.abspath(os.path.join(os.getcwd(), "public")),
    os.path.abspath(os.path.join(script_dir, "..", "..", "public")),
    os.path.abspath(os.path.join(script_dir, "..", "frontend")),
    os.path.abspath(os.path.join(script_dir, "frontend")),
    os.path.abspath(os.path.join(os.getcwd(), "Registation_finder", "frontend")),
    os.path.abspath(os.path.join(os.getcwd(), "frontend")),
    os.path.abspath(os.path.join(os.getcwd(), "student-result-portal", "frontend")),
    os.path.abspath(os.path.join(script_dir, "..", "..", "frontend"))
]
FRONTEND_DIR = None
for candidate in frontend_candidates:
    if os.path.exists(os.path.join(candidate, "index.html")):
        FRONTEND_DIR = os.path.abspath(candidate)
        break

app = Flask(__name__, static_folder=None)

# Enable CORS for all API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuration from environment variables
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "17uwtDRRNBIPZ-jrJ1g9tCP-Zw62zwrz-aO5IsmihgTE")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1")
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

# Strict Read-Only Google Sheets API Scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

# In-memory cache for fast search responses and avoiding Google API rate limits
CACHE = {
    "data": None,
    "last_fetched": 0,
    "cache_duration_seconds": 60  # Cache for 60 seconds
}


def extract_sheet_id(sheet_input):
    """Extract clean Google Spreadsheet ID from either raw ID or full URL."""
    if not sheet_input:
        return ""
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_input)
    if match:
        return match.group(1).strip()
    return re.sub(r"\s+", "", sheet_input)


def get_google_credentials():
    """
    Locate and load Google Service Account Credentials from environment variables
    (e.g., GOOGLE_CREDENTIALS_JSON for Render/Heroku) or local credentials.json file.
    """
    # 1. Check raw JSON string from environment variable (Best for Render/Cloud)
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON") or os.getenv("GOOGLE_CREDENTIALS")
    if creds_json and creds_json.strip():
        try:
            creds_data = json.loads(creds_json)
            return Credentials.from_service_account_info(creds_data, scopes=SCOPES)
        except Exception as e:
            app.logger.warning(f"Failed to parse GOOGLE_CREDENTIALS_JSON: {e}")

    # 2. Check base64 encoded JSON string from environment variable
    creds_b64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    if creds_b64 and creds_b64.strip():
        try:
            decoded = base64.b64decode(creds_b64).decode("utf-8")
            creds_data = json.loads(decoded)
            return Credentials.from_service_account_info(creds_data, scopes=SCOPES)
        except Exception as e:
            app.logger.warning(f"Failed to parse GOOGLE_CREDENTIALS_BASE64: {e}")

    # 3. Check Render secret file path or explicit file paths
    possible_paths = [
        os.getenv("GOOGLE_CREDENTIALS_FILE"),
        "/etc/secrets/credentials.json",
        os.path.join(script_dir, CREDENTIALS_FILE),
        os.path.join(os.getcwd(), CREDENTIALS_FILE),
        os.path.join(os.getcwd(), "Registation_finder", "backend", CREDENTIALS_FILE),
        CREDENTIALS_FILE
    ]

    for path in possible_paths:
        if path and os.path.exists(path):
            try:
                return Credentials.from_service_account_file(path, scopes=SCOPES)
            except Exception as e:
                app.logger.warning(f"Failed to load credentials from file {path}: {e}")

    return None


def fetch_sheet_data():
    """
    Connect to Google Sheets using service account credentials and fetch all rows.
    Uses in-memory cache to ensure sub-millisecond search response times.
    Raises an Exception if connection or authentication fails.
    """
    current_time = time.time()

    # Return cached data if still within cache duration
    if CACHE["data"] is not None and (current_time - CACHE["last_fetched"] < CACHE["cache_duration_seconds"]):
        return CACHE["data"]

    creds = get_google_credentials()
    if not creds:
        raise FileNotFoundError(
            f"Google Credentials not found. Please set GOOGLE_CREDENTIALS_JSON in environment variables "
            f"or provide a credentials file."
        )

    clean_sheet_id = extract_sheet_id(SPREADSHEET_ID)
    if not clean_sheet_id:
        raise ValueError("SPREADSHEET_ID is not configured in environment.")

    # Authenticate with Google Sheets using read-only scope
    client = gspread.authorize(creds)

    last_exception = None
    for attempt in range(3):
        try:
            spreadsheet = client.open_by_key(clean_sheet_id)
            worksheet = spreadsheet.worksheet(SHEET_NAME)
            # Read headers first
            raw_headers = worksheet.row_values(1)
            if not raw_headers:
                parsed_data = {"rows": [], "name_idx": -1, "reg_idx": -1}
                CACHE["data"] = parsed_data
                CACHE["last_fetched"] = current_time
                return parsed_data

            headers = [str(h).strip().lower() for h in raw_headers]

            # Identify Name column index
            name_idx = -1
            for target in ["name", "student name", "student_name", "full name"]:
                if target in headers:
                    name_idx = headers.index(target)
                    break

            # Identify Registration Number column index
            reg_idx = -1
            for target in [
                "registration number",
                "registration no",
                "registration_no",
                "reg number",
                "reg no",
                "roll no",
                "roll number"
            ]:
                if target in headers:
                    reg_idx = headers.index(target)
                    break

            # Blazing-fast fetch: If columns are within A-E, fetch only A:E in ~1 second!
            max_needed = max(name_idx, reg_idx)
            if max_needed != -1 and max_needed <= 4:
                values = worksheet.get('A:E')
            else:
                values = worksheet.get_all_values()

            parsed_data = {
                "headers": raw_headers,
                "rows": values[1:] if len(values) > 1 else [],
                "name_idx": name_idx,
                "reg_idx": reg_idx
            }

            CACHE["data"] = parsed_data
            CACHE["last_fetched"] = current_time
            return parsed_data

        except gspread.exceptions.APIError as api_err:
            last_exception = api_err
            if "503" in str(api_err) and attempt < 2:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except Exception as e:
            last_exception = e
            raise

    if last_exception:
        raise last_exception


# =============================================================================
# API ROUTES
# =============================================================================

@app.route("/", defaults={"path": ""}, methods=["GET"], strict_slashes=False)
@app.route("/<path:path>", methods=["GET"], strict_slashes=False)
def serve_frontend(path):
    """Serve frontend index.html and static files, with graceful fallback."""
    # Never intercept known API and health check paths
    if (
        path.startswith("api/")
        or path == "api"
        or path.startswith("health")
        or path.startswith("student")
        or path.startswith("refresh-cache")
    ):
        return jsonify({"success": False, "message": "API endpoint not found"}), 404

    if FRONTEND_DIR:
        # Strip potential folder prefixes in case proxy passed full path
        clean_path = (
            path.replace("Registation_finder/frontend", "")
            .replace("frontend", "")
            .strip("/")
        )
        if clean_path and os.path.exists(os.path.join(FRONTEND_DIR, clean_path)) and os.path.isfile(os.path.join(FRONTEND_DIR, clean_path)):
            return send_from_directory(FRONTEND_DIR, clean_path)

        if os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
            return send_from_directory(FRONTEND_DIR, "index.html")

    return jsonify({
        "success": True,
        "message": "Student Registration Search Portal API is active.",
        "spreadsheet_id": extract_sheet_id(SPREADSHEET_ID),
        "sheet_name": SHEET_NAME,
        "endpoint": "/api/student?query=<student_name>"
    }), 200


@app.route("/api/student", methods=["GET"])
@app.route("/student", methods=["GET"])
def search_student():
    """
    Search student by Name from Google Sheets.
    Query parameter: `query` (student name)
    Example:
      GET /api/student?query=Manu
    """
    # 1. Retrieve query
    query = request.args.get("query", default="", type=str).strip()

    # 2. Input validation: empty search check
    if not query:
        return jsonify({
            "success": False,
            "message": "Please enter a student name"
        }), 400

    query_lower = query.lower()

    # 3. Fetch records from Google Sheets (or in-memory cache)
    try:
        data = fetch_sheet_data()
    except gspread.exceptions.SpreadsheetNotFound:
        app.logger.exception("Spreadsheet access error")
        return jsonify({
            "success": False,
            "message": "Google Sheet not accessible. Please ensure the sheet is shared with the service account."
        }), 500
    except FileNotFoundError as fnf_err:
        app.logger.error(f"Credentials error: {fnf_err}")
        return jsonify({
            "success": False,
            "message": "Server credentials configuration error."
        }), 500
    except Exception as exc:
        app.logger.exception("Google Sheets API Error")
        return jsonify({
            "success": False,
            "message": "Unable to connect to Google Sheets. Please try again later."
        }), 500

    name_idx = data["name_idx"]
    reg_idx = data["reg_idx"]

    if name_idx == -1:
        return jsonify({
            "success": False,
            "message": "Column 'Name' not found in Google Sheet headers."
        }), 500

    # 4. Search records: collect ALL matching students (case-insensitive, normalized spaces & multi-word matching)
    q_norm = re.sub(r"\s+", " ", query_lower).strip()
    q_words = q_norm.split()

    raw_matches = []

    for row in data["rows"]:
        if len(row) > name_idx:
            student_name = row[name_idx].strip()
            if not student_name:
                continue

            name_norm = re.sub(r"\s+", " ", student_name.lower()).strip()

            # Match if full normalized query is in name OR all query words exist in name
            if q_norm in name_norm or (q_words and all(w in name_norm for w in q_words)):
                # Relevance scoring (0: exact, 1: starts with, 2: exact word, 3: partial)
                if name_norm == q_norm:
                    score = 0
                elif name_norm.startswith(q_norm):
                    score = 1
                elif any(word == q_norm for word in name_norm.split()):
                    score = 2
                else:
                    score = 3

                reg_no = row[reg_idx].strip() if (reg_idx != -1 and len(row) > reg_idx) else "N/A"
                raw_matches.append((score, student_name, reg_no))

    # Sort results by relevance (exact match first, then closest match)
    raw_matches.sort(key=lambda item: (item[0], len(item[1])))

    matching_students = [
        {"name": item[1], "registration_no": item[2]}
        for item in raw_matches
    ]

    # 5. Return result
    if matching_students:
        return jsonify({
            "success": True,
            "students": matching_students,
            "count": len(matching_students)
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "Student not found"
        }), 404


@app.route("/api/refresh-cache", methods=["POST", "GET"])
@app.route("/refresh-cache", methods=["POST", "GET"])
def refresh_cache():
    """Manual cache refresh endpoint."""
    CACHE["data"] = None
    CACHE["last_fetched"] = 0
    try:
        data = fetch_sheet_data()
        return jsonify({
            "success": True,
            "message": "Cache refreshed successfully",
            "total_records": len(data["rows"])
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Cache refresh failed: {str(e)}"
        }), 500


@app.route("/health", methods=["GET"])
@app.route("/healthz", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint for Render and monitoring tools."""
    return jsonify({
        "status": "healthy",
        "service": "student-registration-finder",
        "timestamp": int(time.time()),
        "sheet_configured": bool(SPREADSHEET_ID)
    }), 200


# =============================================================================
# APPLICATION ENTRYPOINT (For local development)
# =============================================================================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # If running on Render or other container, bind to 0.0.0.0, else 127.0.0.1 for local
    default_host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"
    host = os.getenv("HOST", default_host)
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    print(f"[*] Starting Student Search Backend on http://{host}:{port}")
    print(f"[*] Google Sheet ID: {extract_sheet_id(SPREADSHEET_ID)} (Tab: {SHEET_NAME})")
    print(f"[*] Health Check: http://{host}:{port}/health")
    print(f"[*] Endpoint: http://{host}:{port}/api/student?query=<student_name>")
    app.run(host=host, port=port, debug=debug_mode)

