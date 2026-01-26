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

/* ===== POPUP SWITCH ===== */

document.addEventListener("DOMContentLoaded", () => {
  const discoverBtn = document.getElementById("discoverPaths");
  const exploreOverlay = document.getElementById("exploreOverlay");
  const pathOverlay = document.getElementById("pathOverlay");

  if (!discoverBtn) return;

  discoverBtn.addEventListener("click", () => {
    exploreOverlay.classList.remove("active");

    setTimeout(() => {
      pathOverlay.classList.add("active");
    }, 250); // smooth transition
  });
});

/* ===== CLOSE POPUP 2 ===== */

document.addEventListener("DOMContentLoaded", () => {
  const closePath = document.getElementById("closePath");
  const pathOverlay = document.getElementById("pathOverlay");

  if (!closePath) return;

  closePath.addEventListener("click", () => {
    pathOverlay.classList.remove("active");
  });
});
