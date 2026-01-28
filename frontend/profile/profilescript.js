/* PARTICLES */
particlesJS("particles-js", {
  particles: {
    number: { value: 85 },
    size: { value: 2.5 },
    opacity: { value: 0.45 },
    line_linked: { enable: true, opacity: 0.35 },
    move: { speed: 1.4 }
  }
});

/* AVATAR SWITCH */
const modal = document.getElementById("avatarModal");
const openBtn = document.getElementById("openAvatarModal");
const closeBtn = document.querySelector(".close-modal");
const mainAvatar = document.getElementById("mainAvatar");

openBtn.onclick = () => modal.classList.add("active");
closeBtn.onclick = () => modal.classList.remove("active");

document.querySelectorAll(".avatar-grid img").forEach(img => {
  img.onclick = () => {
    mainAvatar.src = img.src;
    modal.classList.remove("active");

    // backend hook later
    // POST /api/profile/avatar
  };
});