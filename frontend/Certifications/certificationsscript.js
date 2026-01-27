document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const pathName = params.get('path');
    const skillsRaw = params.get('skills');

    document.getElementById('pathTitle').innerText = pathName || "Unknown Path";

    if (!skillsRaw) {
        document.getElementById('skillsList').innerHTML = "<p>No skills detected.</p>";
        return;
    }

    const skillsArray = skillsRaw.split('•').map(s => s.trim());
    const skillsList = document.getElementById('skillsList');

    skillsList.innerHTML = skillsArray.map(skill => {
        const id = skill.toLowerCase().replace(/[^a-z0-9]/g, '-');
        return `
            <div class="skill-checkbox-wrapper">
              <input type="checkbox" checked value="${skill}" id="${id}" class="skill-check">
              <label for="${id}">${skill}</label>
            </div>
        `;
    }).join('');

    document.getElementById('recommendBtn').addEventListener('click', fetchCerts);
});

  async function fetchCerts() {
    const params = new URLSearchParams(window.location.search);
    const pathName = params.get("path");

    // 1. GET THE TOKEN (Critical Fix)
    const token = localStorage.getItem("token"); 
    
    if (!token) {
        alert("Please login first to access the DigiVault recommendations.");
        window.location.href = "../login/loginindex.html"; // Redirect to login if no token
        return;
    }

    const selectedSkills = Array.from(
        document.querySelectorAll(".skill-check:checked")
    ).map(cb => cb.value);

    const certsDiv = document.getElementById("certsList");
    certsDiv.innerHTML = "<div class='loader'>Analyzing your skill gap...</div>";

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/certs/recommend-by-path?selected_path=${encodeURIComponent(pathName)}`,
            {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}` // Sends the identity to the backend
                },
                body: JSON.stringify(selectedSkills) 
            }
        );

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Authentication Failed");
        }

        const data = await response.json();
        renderRecommendations(data); // Call a helper to make it look pretty

    } catch (err) {
        console.error("API ERROR:", err);
        certsDiv.innerHTML = `<p class='error'>Error: ${err.message}</p>`;
    }
}
function renderRecommendations(data) {
    const certsDiv = document.getElementById("certsList");
    const status = document.getElementById("progressStatus");
    
    status.innerHTML = `You have mastered <strong>${data.stats.count}/${data.stats.total}</strong> path skills (${data.stats.score}%).`;

    certsDiv.innerHTML = data.recommendations.map(cert => `
        <div class="cert-card">
            <div class="impact-badge">${cert.match_score}% Impact</div>
            <h3>${cert.Certification}</h3>
            <span class="issuer">via ${cert.Company}</span>

            <div class="bucket">
                <span class="bucket-label" style="color:var(--warning)">🚀 Skills to Gain</span>
                <div>${cert.to_learn.map(s => `<span class="tag tag-missing">${s}</span>`).join('') || 'None'}</div>
            </div>

            <div class="bucket">
                <span class="bucket-label" style="color:var(--success)">✅ Skills to Verify</span>
                <div>${cert.to_verify.map(s => `<span class="tag tag-match">${s}</span>`).join('') || 'None'}</div>
            </div>

            <button class="vault-btn" onclick=" ">Add to Path</button>
        </div>
    `).join('');
}