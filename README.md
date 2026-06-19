# 🧭 SkillAlign — AI Career Recommender

**A content-based recommendation engine that matches your skills to the tech career paths they align with best — built entirely from scratch with TF-IDF and cosine similarity, no external AI API required.**

Enter the skills you know, and SkillAlign mathematically ranks 15 tech roles by how closely your profile matches each one — turning a classic information-retrieval technique into a fast, transparent career-matching tool.

---

## ✨ Highlights

- **Real recommender system logic** — TF-IDF vectorization and cosine similarity, the same techniques behind search engines and content recommendation
- **15 curated tech roles** — from Data Scientist and ML Engineer to DevOps, Cybersecurity, and Blockchain Developer, each with a hand-built skill profile
- **Instant, explainable results** — every match comes with a similarity score, a description, and the specific skills driving the match
- **Polished, interactive UI** — animated score meters, quick-add skill chips, and a visual breakdown of the recommendation pipeline
- **Zero external dependencies** — no AI API, no database, no build step — just Flask and pure Python math

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Algorithm:** TF-IDF vectorization + Cosine Similarity (built from scratch)
- **Frontend:** HTML, CSS, vanilla JavaScript

---

## 📁 Project Structure

```
SkillAlign/
├── app.py                  # Flask app, job role catalogue, and recommendation logic
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main page markup
└── static/
    ├── css/
    │   └── style.css       # Styling for the UI
    └── js/
        └── main.js         # Skill input handling, API calls, and result rendering
```

---

## 🚀 How to Run This Project (Windows — VS Code)

Follow these steps exactly to run SkillAlign on your local machine.

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/) installed
- [VS Code](https://code.visualstudio.com/) installed

---

### Step 1 — Extract the zip
Right-click `SkillAlign.zip` → **Extract All** → extract it to your Desktop.
You will get a folder called `SkillAlign`.

---

### Step 2 — Open the folder in VS Code
Open VS Code → click **File** → **Open Folder** → select the `SkillAlign` folder → click **Select Folder**.

---

### Step 3 — Open the terminal
Press `` Ctrl + ` `` (backtick) or go to **Terminal** → **New Terminal**.
The terminal will open at the bottom, already inside your project folder.

---

### Step 4 — Create a virtual environment
Run this command in the terminal:
```bash
python -m venv venv
```
This creates an isolated Python environment for the project.

> ✅ Only needs to be done **once**.

---

### Step 5 — Activate the virtual environment
```bash
venv\Scripts\Activate.ps1
```
You will see `(venv)` appear at the start of your terminal line — this means it is active.

> ⚠️ If you get an execution policy error, run this first, then try Step 5 again:
> ```bash
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

---

### Step 6 — Install dependencies
```bash
pip install -r requirements.txt
```
This installs Flask and everything else the project needs.

> ✅ Only needs to be done **once**.

---

### Step 7 — Run the app
```bash
venv\Scripts\python.exe app.py
```
You should see this output in the terminal:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
* Debugger is active!
```

---

### Step 8 — Open in your browser
Open Chrome or Edge and go to:
```
http://127.0.0.1:5000
```
SkillAlign will be live and ready to use. Add at least 3 skills and click **Analyse My Profile** to see your top career matches.

---

### Step 9 — Stop the app
When you are done, go back to the terminal and press:
```
Ctrl + C
```

---

## 🔁 Running Again Next Time

From the second time onwards, you only need **3 steps**:

```bash
# 1. Activate the virtual environment
venv\Scripts\Activate.ps1

# 2. Run the app
venv\Scripts\python.exe app.py

# 3. Open in browser
http://127.0.0.1:5000
```

---

## 🔌 API Reference

| Route | Method | Description |
|---|---|---|
| `/` | `GET` | Renders the SkillAlign web interface |
| `/recommend` | `POST` | Accepts a list of skills and returns the top 3 ranked career matches |

**Example request:**
```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "TensorFlow", "Statistics"]}'
```

**Example response:**
```json
{
  "recommendations": [
    {
      "title": "Data Scientist",
      "description": "Analyzes complex datasets and builds predictive models.",
      "score": 78.4,
      "tags": ["python", "sql", "machine learning", "statistics", "pandas"]
    }
  ]
}
```

> ⚠️ A minimum of 3 skills is required — fewer than that returns a `400` error.

---

## 🧠 How the Recommendation Works

1. **Vocabulary Building** — every unique skill across all 15 job roles is collected into a shared vocabulary space
2. **TF-IDF Weighting** — each role's skill list is converted into a weighted vector; rare skills score higher than generic ones
3. **User Vectorization** — your entered skills are converted into a vector using the same vocabulary
4. **Cosine Similarity** — the angle between your vector and each role's vector is measured; closer = better match
5. **Ranking** — all 15 roles are scored and sorted; top 3 are returned with their similarity percentage

---

## 📄 License

This project is open for personal and educational use. Feel free to fork it, expand the job role catalogue, or adapt the logic to a different domain.
