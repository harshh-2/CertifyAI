/* PARTICLES */
particlesJS("particles-js", {
  particles: {
    number: { value: 80 },
    size: { value: 2.5 },
    opacity: { value: 0.45 },
    line_linked: { enable: true, opacity: 0.35 },
    move: { speed: 1.4 }
  }
});

/* AVATAR MODAL */
const avatarModal = document.getElementById("avatarModal");
const openAvatar = document.getElementById("openAvatarModal");
const closeAvatar = document.querySelector(".close-avatar");
const mainAvatar = document.getElementById("mainAvatar");

openAvatar.onclick = () => avatarModal.classList.add("active");
closeAvatar.onclick = () => avatarModal.classList.remove("active");

document.querySelectorAll(".avatar-grid img").forEach(img => {
  img.onclick = () => {
    mainAvatar.src = img.src;
    avatarModal.classList.remove("active");
  };
});

/* EDIT PROFILE */
const editBtn = document.getElementById("editProfileBtn");
const editModal = document.getElementById("editModal");
const cancelEdit = document.getElementById("cancelEdit");
const saveEdit = document.getElementById("saveEdit");

editBtn.onclick = () => {
  document.getElementById("editName").value = profileName.innerText;
  document.getElementById("editCourse").value = profileCourse.innerText;
  document.getElementById("editAbout").value = profileAbout.innerText;
  editModal.classList.add("active");
};

cancelEdit.onclick = () => editModal.classList.remove("active");

saveEdit.onclick = async () => {
  const payload = {
    name: editName.value,
    course: editCourse.value,
    about: editAbout.value,
    skills: editSkills.value.split(",").map(s => s.trim()),
    avatar: mainAvatar.src
  };

  profileName.innerText = payload.name;
  profileCourse.innerText = payload.course;
  profileAbout.innerText = payload.about;

  editModal.classList.remove("active");

  await fetch("http://127.0.0.1:8000/api/profile/update", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
};

/* UPLOAD RESUME */
const resumeBtn = document.getElementById("uploadResumeBtn");
const resumeModal = document.getElementById("resumeModal");
const cancelResume = document.getElementById("cancelResume");
const uploadResume = document.getElementById("uploadResume");

resumeBtn.onclick = () => resumeModal.classList.add("active");
cancelResume.onclick = () => resumeModal.classList.remove("active");

uploadResume.onclick = async () => {
  const file = document.getElementById("resumeFile").files[0];
  if (!file) return alert("Select a resume first");

  const formData = new FormData();
  formData.append("resume", file);

  await fetch("http://127.0.0.1:8000/api/profile/upload-resume", {
    method: "POST",
    body: formData
  });

  resumeModal.classList.remove("active");
};

//Load profile + certificates
document.addEventListener("DOMContentLoaded", () => {
  loadProfile();
  bindUI();
});

async function loadProfile() {
  const token = localStorage.getItem("token");

  const res = await fetch("http://127.0.0.1:8000/profile/me", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const data = await res.json();

  // Profile text
  document.getElementById("profileName").innerText = data.user.username;
  document.getElementById("profileCourse").innerText = data.user.course;
  document.getElementById("profileAbout").innerText = data.user.about || "";

  // Prefill edit modal
  document.getElementById("editName").value = data.user.username;
  document.getElementById("editCourse").value = data.user.course;
  document.getElementById("editAbout").value = data.user.about || "";
  document.getElementById("editSkills").value =
    (data.user.skills || []).join(", ");

  renderCertificates(data.certificates);
}

//RENDER CERTIFICATES
function renderCertificates(certs) {
  const grid = document.getElementById("certGrid");

  if (!certs.length) {
    grid.innerHTML = `
      <div class="cert-card add-cert">
        <span>+</span>
        <p>Add Certification</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = certs.map(cert => `
    <div class="cert-card">
      <img src="${getProviderLogo(cert.provider)}">
      <h3>${cert.certificate_name}</h3>
      <p>Issued by ${cert.provider}</p>
      <button class="cert-btn"
        onclick="window.open('http://127.0.0.1:8000/${cert.file_path}')">
        View Credential
      </button>
    </div>
  `).join("") + `
    <div class="cert-card add-cert">
      <span>+</span>
      <p>Add Certification</p>
    </div>
  `;
}

function getProviderLogo(provider) {
  const map = {
    AWS: "https://upload.wikimedia.org/wikipedia/commons/9/93/Amazon_Web_Services_Logo.svg",
    IBM: "https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg",
    Cisco: "https://upload.wikimedia.org/wikipedia/commons/6/64/Cisco_logo.svg"
  };

  return map[provider] || "https://via.placeholder.com/120";
}

function bindUI() {
  document.getElementById("editProfileBtn").onclick =
    () => document.getElementById("editModal").style.display = "flex";

  document.getElementById("cancelEdit").onclick =
    () => document.getElementById("editModal").style.display = "none";

  document.getElementById("saveEdit").onclick = saveProfile;
}

// SAVE PROFILE
async function saveProfile() {
  const token = localStorage.getItem("token");

  const payload = {
    username: document.getElementById("editName").value,
    course: document.getElementById("editCourse").value,
    about: document.getElementById("editAbout").value,
    skills: document
      .getElementById("editSkills")
      .value
      .split(",")
      .map(s => s.trim())
  };

  await fetch("http://127.0.0.1:8000/profile/update", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  alert("Profile updated");
  location.reload();
}


// TO UPLOAD CERTIFICATE
function openCertUpload() {
  document.getElementById("certUploadInput").click();
}

document.getElementById("certUploadInput").addEventListener("change", uploadCert);

async function uploadCert(e) {
  const file = e.target.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  const token = localStorage.getItem("token");

  const res = await fetch("http://127.0.0.1:8000/vault/upload", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.detail || "Upload failed");
    return;
  }

  alert("Certificate uploaded successfully!");
  location.reload(); // reload profile + certs
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  window.location.href = "/";
}