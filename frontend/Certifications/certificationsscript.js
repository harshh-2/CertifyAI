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
        window.location.href = "../index.html"; // Redirect to login if no token
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

// 2. PRETTY RENDERER (Impactful UI)
function renderRecommendations(data) {
    const certsDiv = document.getElementById("certsList");
    
    if (data.recommendations.length === 0) {
        certsDiv.innerHTML = "<p>You're already industry-ready! Check the DigiVault for advanced certs.</p>";
        return;
    }

    certsDiv.innerHTML = data.recommendations.map(cert => `
        <div class="cert-card">
            <div class="cert-badge">${cert.match_score}% Impact</div>
            <h3>${cert.Certification}</h3>
            <p><strong>Provider:</strong> ${cert.Company}</p>
            <div class="gap-info">
                <span class="gap-tag missing">Fills Gap: ${cert.matching_skills.join(', ')}</span>
            </div>
            <button class="vault-btn" onclick="saveToVault('${cert.Certification}')">Add to Roadmap</button>
        </div>
    `).join('');
}