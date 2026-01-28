document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const pathName = params.get('path');
  const skillsRaw = params.get('skills');

  document.getElementById('pathTitle').innerText = pathName || "Unknown Path";

  if (!skillsRaw) {
    document.getElementById('skillsList').innerHTML =
      "<p class='muted'>No skills detected.</p>";
    return;
  }

  const skillsArray = skillsRaw.split('•').map(s => s.trim());
  const skillsList = document.getElementById('skillsList');

  skillsList.innerHTML = skillsArray.map(skill => `
    <div class="skill-pill active" data-skill="${skill}">
      ${skill}
    </div>
  `).join('');

  document.querySelectorAll('.skill-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      pill.classList.toggle('active');
    });
  });

  document.getElementById('recommendBtn').addEventListener('click', fetchCerts);
});

async function fetchCerts() {
  const params = new URLSearchParams(window.location.search);
  const pathName = params.get("path");

  const token = localStorage.getItem("token");
   if (!token) {
     alert("Please login first to access recommendations.");
     window.location.href = "../login/loginindex.html";
     return;
   }

  const selectedSkills = Array.from(
    document.querySelectorAll(".skill-pill.active")
  ).map(el => el.dataset.skill);

  const certsDiv = document.getElementById("certsList");
  certsDiv.innerHTML = "<p class='muted'>Analyzing your skill gap...</p>";

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/certs/recommend-by-path?selected_path=${encodeURIComponent(pathName)}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
           "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(selectedSkills)
      }
    );

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Authentication failed");
    }

    const data = await response.json();

    renderProgress(data.stats.score);
    renderRecommendations(data);

  } catch (err) {
    console.error("API ERROR:", err);
    certsDiv.innerHTML = `<p class="error">Error: ${err.message}</p>`;
  }
}

/* ===== PROGRESS RING ===== */
function renderProgress(percent) {
  const circle = document.querySelector(".ring-progress");
  const text = document.getElementById("progressPercent");

  if (!circle || !text) return;

  const circumference = 214;
  const offset = circumference - (percent / 100) * circumference;

  circle.style.strokeDashoffset = offset;
  text.innerText = `${percent}%`;
}

/* ===== CERT CARDS ===== */
function renderRecommendations(data) {
  const certsDiv = document.getElementById("certsList");

  certsDiv.innerHTML = data.recommendations.map(cert => `
    <div class="cert-card">
      <div class="impact-badge">${cert.match_score}% Impact</div>

      <div class="cert-header">
        <h3>${cert.Certification}</h3>
        <p class="muted">via ${cert.Company}</p>
      </div>

      <div class="bucket">
        <span class="bucket-label">🚀 Skills to Gain</span>
        <div>
          ${
            cert.to_learn.length
              ? cert.to_learn.map(s => `<span class="tag tag-missing">${s}</span>`).join('')
              : "None"
          }
        </div>
      </div>

      <div class="bucket">
        <span class="bucket-label">✅ Skills to Verify</span>
        <div>
          ${
            cert.to_verify.length
              ? cert.to_verify.map(s => `<span class="tag tag-match">${s}</span>`).join('')
              : "None"
          }
        </div>
      </div>

      <button class="btn full">Add to Path</button>
    </div>
  `).join('');
}