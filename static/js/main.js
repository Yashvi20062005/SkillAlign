/**
 * SkillAlign — AI Career Recommender
 *
 * Handles:
 *   1. Skill tag management (add / remove)
 *   2. Quick-add chip toggling
 *   3. API call to Flask /recommend endpoint
 *   4. Rendering result cards with animated score meters
 */

// ─── DOM refs ─────────────────────────────────────────────
const skillInput    = document.getElementById("skillInput");
const addBtn        = document.getElementById("addBtn");
const skillTags     = document.getElementById("skillTags");
const skillCounter  = document.getElementById("skillCounter");
const recommendBtn  = document.getElementById("recommendBtn");
const resultsPanel  = document.getElementById("resultsPanel");
const errorMsg      = document.getElementById("errorMsg");
const quickChips    = document.querySelectorAll(".chip");

// ─── State ────────────────────────────────────────────────
let skills = [];   // array of skill strings currently added

// ─── Helpers ──────────────────────────────────────────────

/** Update the counter label and enable/disable the main button */
function updateCounter() {
  const n = skills.length;
  skillCounter.textContent = `${n} skill${n !== 1 ? "s" : ""} added · ${
    n < 3 ? `need at least ${3 - n} more` : "ready to analyse ✓"
  }`;
  skillCounter.classList.toggle("ready", n >= 3);
  recommendBtn.disabled = n < 3;
}

/** Render the skill tag pills inside the input area */
function renderTags() {
  skillTags.innerHTML = "";
  skills.forEach((skill, idx) => {
    const tag = document.createElement("span");
    tag.className = "skill-tag";
    tag.innerHTML = `${skill} <button aria-label="Remove ${skill}" data-idx="${idx}">×</button>`;
    skillTags.appendChild(tag);
  });
  updateCounter();
}

/** Add a skill (deduplication + trim) */
function addSkill(raw) {
  const val = raw.trim();
  if (!val) return;
  // Normalise to Title Case for display
  const normalised = val.replace(/\b\w/g, c => c.toUpperCase());
  if (skills.includes(normalised)) return;  // deduplicate
  skills.push(normalised);
  renderTags();
  markChip(normalised, true);
  skillInput.value = "";
}

/** Mark / unmark quick-add chips based on current skills */
function markChip(skillName, used) {
  quickChips.forEach(chip => {
    if (chip.dataset.skill.toLowerCase() === skillName.toLowerCase()) {
      chip.classList.toggle("used", used);
    }
  });
}

// ─── Event Listeners ──────────────────────────────────────

// Add skill via button
addBtn.addEventListener("click", () => addSkill(skillInput.value));

// Add skill via Enter key
skillInput.addEventListener("keydown", e => {
  if (e.key === "Enter") { e.preventDefault(); addSkill(skillInput.value); }
  // Also support comma-separated input
  if (e.key === ",") { e.preventDefault(); addSkill(skillInput.value); }
});

// Remove skill by clicking × on a tag
skillTags.addEventListener("click", e => {
  if (e.target.tagName === "BUTTON") {
    const idx = parseInt(e.target.dataset.idx, 10);
    const removed = skills.splice(idx, 1)[0];
    markChip(removed, false);
    renderTags();
  }
});

// Quick-add chips
quickChips.forEach(chip => {
  chip.addEventListener("click", () => {
    if (!chip.classList.contains("used")) {
      addSkill(chip.dataset.skill);
    }
  });
});

// ─── API Call ─────────────────────────────────────────────

recommendBtn.addEventListener("click", async () => {
  errorMsg.textContent = "";
  const btnText    = recommendBtn.querySelector(".btn-text");
  const btnLoading = recommendBtn.querySelector(".btn-loading");

  // Show loading state
  recommendBtn.disabled = true;
  btnText.style.display    = "none";
  btnLoading.style.display = "inline";

  try {
    const res = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ skills })
    });

    const data = await res.json();

    if (!res.ok) {
      errorMsg.textContent = data.error || "Something went wrong.";
      return;
    }

    renderResults(data.recommendations);

  } catch (err) {
    errorMsg.textContent = "Could not connect to the server. Make sure Flask is running.";
  } finally {
    recommendBtn.disabled = skills.length < 3;
    btnText.style.display    = "inline";
    btnLoading.style.display = "none";
  }
});

// ─── Render Results ───────────────────────────────────────

const RANK_LABELS = ["#1 Best Match", "#2 Strong Match", "#3 Good Match"];

function renderResults(recommendations) {
  if (!recommendations || recommendations.length === 0) {
    resultsPanel.innerHTML = "<p style='color:var(--text-secondary)'>No matches found. Try different skills.</p>";
    return;
  }

  let html = `<div class="results-header">Top ${recommendations.length} Matches · Ranked by Cosine Similarity</div>`;

  recommendations.forEach((rec, i) => {
    const rankClass  = i === 0 ? "rank-1" : "";
    const tagHtml    = rec.tags.slice(0, 6).map(t =>
      `<span class="result-tag">${t}</span>`
    ).join("");

    html += `
      <div class="result-card ${rankClass}">
        <div class="result-rank">${RANK_LABELS[i] || `#${i+1}`}</div>
        <div class="result-title-row">
          <div class="result-title">${rec.title}</div>
          <div class="score-meter">
            <div class="score-value">${rec.score}% match</div>
            <div class="score-bar-bg">
              <div class="score-bar-fill" style="width:0%" data-target="${rec.score}"></div>
            </div>
          </div>
        </div>
        <div class="result-desc">${rec.description}</div>
        <div class="result-tags">${tagHtml}</div>
      </div>
    `;
  });

  resultsPanel.innerHTML = html;

  // Animate score bars after DOM insertion
  requestAnimationFrame(() => {
    document.querySelectorAll(".score-bar-fill").forEach(bar => {
      const target = bar.dataset.target;
      // Small delay so CSS transition plays visibly
      setTimeout(() => { bar.style.width = `${target}%`; }, 80);
    });
  });
}

// ─── Init ─────────────────────────────────────────────────
updateCounter();
