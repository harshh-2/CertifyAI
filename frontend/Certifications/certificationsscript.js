document.addEventListener('DOMContentLoaded', () => {

    const params = new URLSearchParams(window.location.search);
    const pathName = params.get('path');
    const skillsRaw = params.get('skills');

    // Set title
    document.getElementById('pathTitle').innerText = pathName || "Unknown Path";

    if (!skillsRaw) {
        document.getElementById('skillsList').innerHTML =
            "<p>No skills provided.</p>";
        return;
    }

    const skillsArray = skillsRaw.split('•').map(s => s.trim());

    const skillsList = document.getElementById('skillsList');

    skillsList.innerHTML = skillsArray.map(skill => {
        const id = skill.toLowerCase().replace(/[^a-z0-9]/g, '-');
        return `
            <div>
              <input type="checkbox" checked value="${skill}" id="${id}">
              <label for="${id}">${skill}</label>
            </div>
        `;
    }).join('');

    document.getElementById('recommendBtn')
        .addEventListener('click', fetchCerts);

});

// ===== BACKEND CALL =====
async function fetchCerts() {
    const params = new URLSearchParams(window.location.search);
    const pathName = params.get("path");

    const selectedSkills = Array.from(
        document.querySelectorAll("#skillsList input:checked")
    ).map(cb => cb.value);

    const certsDiv = document.getElementById("certsList");
    certsDiv.innerHTML = "<p>Loading recommendations...</p>";

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/certs/recommend-by-path?selected_path=${encodeURIComponent(pathName)}`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(selectedSkills) // ✅ ARRAY ONLY
            }
        );

        if (!response.ok) {
            const err = await response.text();
            throw new Error(err);
        }

        const data = await response.json();

        certsDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;

    } catch (err) {
        console.error("API ERROR:", err);
        certsDiv.innerHTML =
            "<p class='error'>Backend validation failed (check console).</p>";
    }
}
