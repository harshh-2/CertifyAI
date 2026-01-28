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