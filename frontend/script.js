console.log("script.js loaded");

/* PARTICLES */
particlesJS("particles-js", {
  particles: {
    number: { value: 95 },
    size: { value: 2.6 },
    opacity: { value: 0.52 },
    line_linked: { enable: true, opacity: 0.35, width: 1.2 },
    move: { speed: 1.4 }
  }
});

/* NAVBAR */
document.getElementById("hamburger")
  .addEventListener("click", () =>
    document.getElementById("mobileMenu").classList.toggle("active")
  );

/* FEATURE SELECTOR + GLOW RESPONSE */
const features = {
  ai: {
    title: "AI-Powered Guidance",
    desc: "Intelligent recommendations connecting certifications, resumes, and careers.",
    glow: "#3b82f6"
  },
  cert: {
    title: "Certification Intelligence",
    desc: "Discover certifications that matter for your specific domain.",
    glow: "#22c55e"
  },
  career: {
    title: "Career Path Mapping",
    desc: "Step-by-step roadmaps from student to professional.",
    glow: "#8b5cf6"
  }
};

const circles = document.querySelectorAll(".venn-circle");
const titleEl = document.getElementById("featureTitle");
const descEl = document.getElementById("featureDesc");

circles.forEach(circle => {
  circle.addEventListener("click", () => {
    circles.forEach(c => c.classList.remove("active"));
    circle.classList.add("active");

    const key = circle.dataset.feature;
    titleEl.textContent = features[key].title;
    descEl.textContent = features[key].desc;

    /* CENTER GLOW RESPONSE */
    document.documentElement.style.setProperty("--glow", features[key].glow);
  });
});

/* ================= START EXPLORING POPUP ================= */

document.addEventListener("DOMContentLoaded", () => {
  const exploreBtn = document.querySelector(".hero-primary");
  const exploreOverlay = document.getElementById("exploreOverlay");
  const closeExplore = document.getElementById("closeExplore");

  if (!exploreBtn || !exploreOverlay || !closeExplore) return;

  exploreBtn.addEventListener("click", () => {
    exploreOverlay.classList.add("active");
  });

  closeExplore.addEventListener("click", () => {
    exploreOverlay.classList.remove("active");
  });

  exploreOverlay.addEventListener("click", (e) => {
    if (e.target === exploreOverlay) {
      exploreOverlay.classList.remove("active");
    }
  });
});



document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");

  // Desktop
  const authLinks = document.getElementById("auth-links");
  const profileLinks = document.getElementById("profile-links");

  // Mobile
  const mobileLogin = document.getElementById("mobile-login");
  const mobileSignup = document.getElementById("mobile-signup");
  const mobileProfile = document.getElementById("mobile-profile");
  const mobileLogout = document.getElementById("mobile-logout");

  if (token) {
    authLinks.style.display = "none";
    profileLinks.style.display = "flex";

    mobileLogin.style.display = "none";
    mobileSignup.style.display = "none";
    mobileProfile.style.display = "block";
    mobileLogout.style.display = "block";
  } else {
    authLinks.style.display = "flex";
    profileLinks.style.display = "none";

    mobileLogin.style.display = "block";
    mobileSignup.style.display = "block";
    mobileProfile.style.display = "none";
    mobileLogout.style.display = "none";
  }
});

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  window.location.href = "/";
}



