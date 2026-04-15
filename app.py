# -*- coding: utf-8 -*-
# app.py
# A beginner-friendly Flask REST API for CodeCraftHub-style course tracking
# Features:
# - CRUD endpoints under /api/courses
# - Data persisted in a JSON file named courses.json (auto-created if missing)
# - Each course has: id (auto-generated), name, description, target_date (YYYY-MM-DD),
#   status (Not Started | In Progress | Completed), created_at (timestamp)
# - Basic error handling for missing fields, not-found, invalid values, and file I/O errors

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import datetime

app = Flask(__name__)
CORS(app)

# 1) Data storage configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "courses.json")

# Ensure the data file exists on startup
if not os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump([], f, indent=2)
    except Exception as e:
        # In a real app you’d log this; for beginners we print to console
        print(f"Error creating data file: {e}")

# 2) Helper functions (data access and validation)
def load_courses():
    """Load the list of courses from the JSON file. Returns a list."""
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # If the file is corrupted, treat as empty
        return []
    except Exception as e:
        # Unexpected read error
        print(f"Error reading data file: {e}")
        return []

def save_courses(data):
    """Atomically write the entire course list back to the JSON file."""
    tmp_path = DATA_FILE + ".tmp"
    try:
        with open(tmp_path, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, DATA_FILE)
    except Exception as e:
        print(f"Error writing data file: {e}")
        raise

def get_next_id(items):
    """Compute the next auto-generated ID starting from 1."""
    if not items:
        return 1
    max_id = max((item.get("id", 0) for item in items), default=0)
    return max_id + 1

def is_valid_date(value):
    """Validate that date is in YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
        return True
    except Exception:
        return False

def is_valid_status(value):
    """Validate allowed status values."""
    return value in ("Not Started", "In Progress", "Completed")

# Statistics for the courses
@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """Returns a summary of course counts by status."""
    try:
        courses = load_courses()
        
        # Initialize counts
        stats = {
            "total_courses": len(courses),
            "by_status": {
                "Not Started": 0,
                "In Progress": 0,
                "Completed": 0
            }
        }

        # Aggregate data
        for course in courses:
            status = course.get("status")
            if status in stats["by_status"]:
                stats["by_status"][status] += 1
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to calculate stats: {str(e)}"}), 500

# API endpoints

# POST /api/courses - Add a new course
# GET  /api/courses - Get all courses
@app.route("/api/courses", methods=["GET", "POST"])
def courses_root():
    if request.method == "GET":
        # Return all courses
        try:
            courses = load_courses()
            return jsonify(courses), 200
        except Exception:
            return jsonify({"error": "Failed to read data"}), 500

    if request.method == "POST":
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Required fields
        required = ["name", "description", "target_date", "status"]
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        if not is_valid_date(payload["target_date"]):
            return jsonify({"error": "Invalid target_date format. Use YYYY-MM-DD"}), 400

        if not is_valid_status(payload["status"]):
            return jsonify({"error": "Invalid status. Must be one of Not Started, In Progress, Completed"}), 400

        courses = load_courses()
        new_id = get_next_id(courses)

        course = {
            "id": new_id,
            "name": payload["name"],
            "description": payload["description"],
            "target_date": payload["target_date"],
            "status": payload["status"],
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }

        courses.append(course)
        try:
            save_courses(courses)
        except Exception:
            return jsonify({"error": "Failed to write data to file"}), 500

        return jsonify(course), 201

# GET /api/courses/ - Get a specific course
# PUT /api/courses/ - Update a course
# DELETE /api/courses/ - Delete a course
@app.route("/api/courses/<int:course_id>", methods=["GET", "PUT", "DELETE"])
def course_detail(course_id):
    courses = load_courses()
    # Find the index and the course object
    idx = next((i for i, c in enumerate(courses) if c.get("id") == course_id), None)
    
    if idx is None:
        return jsonify({"error": "Course not found"}), 404

    if request.method == "GET":
        return jsonify(courses[idx])

    if request.method == "PUT":
        payload = request.get_json(silent=True)
        if not payload:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        course = courses[idx]
        updated = False

        # Update fields if present in payload
        for field in ["name", "description", "status", "target_date"]:
            if field in payload:
                if field == "target_date" and not is_valid_date(payload[field]):
                    return jsonify({"error": "Invalid date format"}), 400
                if field == "status" and not is_valid_status(payload[field]):
                    return jsonify({"error": "Invalid status"}), 400
                
                course[field] = payload[field]
                updated = True

        if not updated:
            return jsonify({"error": "No valid fields provided for update"}), 400

        save_courses(courses)
        return jsonify(course)

    if request.method == "DELETE":
        deleted = courses.pop(idx)
        save_courses(courses)
        return jsonify(deleted)
    
@app.route("/")
def index():
    return render_template("index.html")

# Run the app
if __name__ == "__main__":
    app.run(debug=True)