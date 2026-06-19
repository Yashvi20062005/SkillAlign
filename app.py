"""
SkillAlign — AI Career Recommender

Backend: Flask + TF-IDF + Cosine Similarity
No external AI API needed - pure algorithmic logic.
"""

from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# ─────────────────────────────────────────────
#  KNOWLEDGE BASE  (raw_skills dataset)
#  Each role has a name, description, and list of skills/tags.
#  This acts as our "item catalogue" for the recommender.
# ─────────────────────────────────────────────
JOB_ROLES = [
    {
        "title": "Data Scientist",
        "description": "Analyzes complex datasets and builds predictive models.",
        "tags": ["python", "sql", "machine learning", "statistics", "pandas",
                 "numpy", "data analysis", "tensorflow", "scikit-learn", "visualization"]
    },
    {
        "title": "Machine Learning Engineer",
        "description": "Designs, builds, and deploys machine learning systems at scale.",
        "tags": ["python", "machine learning", "tensorflow", "pytorch", "deep learning",
                 "mlops", "docker", "kubernetes", "data pipelines", "model deployment"]
    },
    {
        "title": "Backend Developer",
        "description": "Builds and maintains server-side logic, databases, and APIs.",
        "tags": ["python", "java", "sql", "apis", "rest", "databases",
                 "nodejs", "django", "flask", "microservices"]
    },
    {
        "title": "Frontend Developer",
        "description": "Creates interactive and visually appealing web interfaces.",
        "tags": ["html", "css", "javascript", "react", "typescript", "ui design",
                 "responsive design", "vue", "figma", "web performance"]
    },
    {
        "title": "DevOps Engineer",
        "description": "Bridges development and operations through automation and infrastructure.",
        "tags": ["docker", "kubernetes", "aws", "ci/cd", "linux", "terraform",
                 "ansible", "monitoring", "cloud", "automation"]
    },
    {
        "title": "Cloud Architect",
        "description": "Designs and oversees cloud computing strategies and infrastructure.",
        "tags": ["aws", "azure", "gcp", "cloud", "architecture", "terraform",
                 "networking", "security", "microservices", "automation"]
    },
    {
        "title": "Cybersecurity Analyst",
        "description": "Protects systems and networks from cyber threats and vulnerabilities.",
        "tags": ["security", "networking", "linux", "penetration testing", "firewalls",
                 "cryptography", "siem", "risk assessment", "compliance", "ethical hacking"]
    },
    {
        "title": "Full Stack Developer",
        "description": "Develops both client-side and server-side software.",
        "tags": ["html", "css", "javascript", "react", "nodejs", "python",
                 "sql", "rest", "apis", "databases"]
    },
    {
        "title": "AI Research Scientist",
        "description": "Conducts research to advance the field of artificial intelligence.",
        "tags": ["python", "deep learning", "pytorch", "mathematics", "statistics",
                 "nlp", "computer vision", "reinforcement learning", "research", "tensorflow"]
    },
    {
        "title": "Data Engineer",
        "description": "Builds and maintains data pipelines and storage infrastructure.",
        "tags": ["python", "sql", "spark", "hadoop", "etl", "data pipelines",
                 "aws", "kafka", "databases", "airflow"]
    },
    {
        "title": "Systems Administrator",
        "description": "Manages and maintains IT infrastructure and servers.",
        "tags": ["linux", "networking", "windows", "cloud", "automation",
                 "scripting", "monitoring", "virtualization", "security", "aws"]
    },
    {
        "title": "NLP Engineer",
        "description": "Builds systems that understand and generate human language.",
        "tags": ["python", "nlp", "deep learning", "transformers", "bert",
                 "text processing", "machine learning", "pytorch", "spacy", "llm"]
    },
    {
        "title": "Computer Vision Engineer",
        "description": "Develops systems that interpret and analyze visual information.",
        "tags": ["python", "computer vision", "deep learning", "opencv", "pytorch",
                 "tensorflow", "image processing", "cnn", "machine learning", "cuda"]
    },
    {
        "title": "UI/UX Designer",
        "description": "Designs user experiences and interfaces for digital products.",
        "tags": ["figma", "ui design", "ux research", "prototyping", "css",
                 "html", "user testing", "wireframing", "adobe xd", "design systems"]
    },
    {
        "title": "Blockchain Developer",
        "description": "Develops decentralized applications and smart contracts.",
        "tags": ["blockchain", "solidity", "ethereum", "web3", "cryptography",
                 "javascript", "python", "smart contracts", "defi", "security"]
    },
]


# ─────────────────────────────────────────────
#  STEP 1 — BUILD THE VOCABULARY
#  Collect all unique terms across all job roles.
#  This is our shared "vocabulary space."
# ─────────────────────────────────────────────
def build_vocabulary(roles):
    vocab = set()
    for role in roles:
        for tag in role["tags"]:
            vocab.add(tag.lower())
    return sorted(list(vocab))  # sorted for consistent indexing


# ─────────────────────────────────────────────
#  STEP 2 — COMPUTE TF-IDF VECTORS
#  TF  = how often a term appears in THIS document
#  IDF = log(total docs / docs containing the term)
#  Weight = TF × IDF  → specific terms score higher
# ─────────────────────────────────────────────
def compute_idf(roles, vocabulary):
    total_docs = len(roles)
    idf = {}
    for term in vocabulary:
        docs_with_term = sum(1 for role in roles if term in [t.lower() for t in role["tags"]])
        # Add 1 to numerator and denominator (Laplace smoothing) to avoid log(0)
        idf[term] = math.log((total_docs + 1) / (docs_with_term + 1)) + 1
    return idf


def compute_tfidf_vector(tags, vocabulary, idf):
    tag_list = [t.lower() for t in tags]
    total_terms = len(tag_list)
    vector = []
    for term in vocabulary:
        tf = tag_list.count(term) / total_terms if total_terms > 0 else 0
        vector.append(tf * idf.get(term, 0))
    return vector


def compute_user_vector(user_skills, vocabulary, idf):
    """
    User provides 3+ skills. We treat them as a bag-of-words document.
    TF = 1/total_skills for each skill present (binary-like).
    """
    skills = [s.strip().lower() for s in user_skills]
    total = len(skills)
    vector = []
    for term in vocabulary:
        tf = skills.count(term) / total if total > 0 else 0
        vector.append(tf * idf.get(term, 0))
    return vector


# ─────────────────────────────────────────────
#  STEP 3 — COSINE SIMILARITY
#  cos(θ) = (A · B) / (||A|| × ||B||)
#  Range: 0 (no match) to 1 (perfect match)
# ─────────────────────────────────────────────
def cosine_similarity(vec_a, vec_b):
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a ** 2 for a in vec_a))
    magnitude_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0  # Cold Start: zero vector → no match
    return dot_product / (magnitude_a * magnitude_b)


# ─────────────────────────────────────────────
#  STEP 4 — RANKING PIPELINE
#  Ingestion → Scoring → Sorting → Filtering (Top-N)
# ─────────────────────────────────────────────
def recommend(user_skills, top_n=3):
    vocabulary = build_vocabulary(JOB_ROLES)
    idf = compute_idf(JOB_ROLES, vocabulary)

    # Build user vector from provided skills
    user_vec = compute_user_vector(user_skills, vocabulary, idf)

    # Score every job role against the user profile
    scored = []
    for role in JOB_ROLES:
        role_vec = compute_tfidf_vector(role["tags"], vocabulary, idf)
        score = cosine_similarity(user_vec, role_vec)
        scored.append({
            "title": role["title"],
            "description": role["description"],
            "score": round(score * 100, 1),   # convert to percentage
            "tags": role["tags"]
        })

    # Sort descending and return Top-N
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


# ─────────────────────────────────────────────
#  FLASK ROUTES
# ─────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    skills_input = data.get("skills", [])

    if len(skills_input) < 3:
        return jsonify({"error": "Please provide at least 3 skills."}), 400

    results = recommend(skills_input, top_n=3)
    return jsonify({"recommendations": results})


if __name__ == "__main__":
    app.run(debug=True)
