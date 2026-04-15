# 🚀 CodeCraftHub Course Tracker API

A lightweight, beginner-friendly Flask REST API designed to track learning progress. This application uses a local JSON file for data persistence, making it easy to set up and run without external databases.

## 📋 Features

- **Full CRUD:** Create, Read, Update, and Delete courses.
- **RESTful Routing:** Standard URL patterns for resource management.
- **Data Persistence:** Saves data to `courses.json` automatically.
- **Validation:** Ensures valid date formats (**YYYY-MM-DD**) and specific status labels.
- **Insights:** A dedicated statistics endpoint to track your learning velocity.

---

## 🛠️ Setup & Installation

1.  **Install dependencies:**
    ```bash
    pip install flask
    ```
2.  **Run the application:**
    ```bash
    python app.py
    ```
    _The server will start at `http://localhost:5000`._

---

## 🛣️ API Endpoints

### 1. Courses Collection

| Method | Endpoint       | Description           |
| :----- | :------------- | :-------------------- |
| `GET`  | `/api/courses` | Retrieve all courses. |
| `POST` | `/api/courses` | Create a new course.  |

**POST Body Example:**

```json
{
  "name": "Mastering Flask",
  "description": "Learn to build REST APIs with Python.",
  "target_date": "2026-12-31",
  "status": "In Progress"
}
```

### 2. Individual Course Operations

| Method   | Endpoint            | Description                         |
| :------- | :------------------ | :---------------------------------- |
| `GET`    | `/api/courses/<id>` | Get details of a specific course.   |
| `PUT`    | `/api/courses/<id>` | Update fields of a specific course. |
| `DELETE` | `/api/courses/<id>` | Remove a course from the tracker.   |

### 3. Analytics

| Method | Endpoint             | Description                             |
| :----- | :------------------- | :-------------------------------------- |
| `GET`  | `/api/courses/stats` | Get total counts and status breakdowns. |

---

## 📊 Data Structure

Each course entry contains the following schema:

- **id**: (Integer) Auto-generated unique identifier.
- **name**: (String) Title of the course.
- **description**: (String) Short summary.
- **target_date**: (String) Format `YYYY-MM-DD`.
- **status**: (String) `Not Started`, `In Progress`, or `Completed`.
- **created_at**: (Timestamp) ISO-8601 format.

---

## 💻 Example Usage (cURL)

**Get Statistics:**

```bash
curl http://localhost:5000/api/courses/stats
```

**Get a Specific Course (ID: 1):**

```bash
curl http://localhost:5000/api/courses/1
```

**Update Course Status:**

```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{"status": "Completed"}' \
     http://localhost:5000/api/courses/1
```

**Delete a Course:**

```bash
curl -X DELETE http://localhost:5000/api/courses/2
```

---

## ⚠️ Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Request successful.
- `201 Created`: Resource created successfully.
- `400 Bad Request`: Missing fields or invalid data format.
- `404 Not Found`: The requested Course ID does not exist.
- `500 Internal Server Error`: File I/O issues or server-side crashes.

```

```
