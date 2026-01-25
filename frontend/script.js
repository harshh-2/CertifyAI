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

async function signupUser() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // ✅ Frontend-only validation
  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return;
  }

  const data = {
    username: document.getElementById("username").value,
    email: document.getElementById("email").value,
    password: password,
    year_of_college: parseInt(document.getElementById("year").value),
    age: parseInt(document.getElementById("age").value),
    institution: document.getElementById("institution").value,
    gender: document.getElementById("gender").value
  };

  const res = await fetch("http://127.0.0.1:8000/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const result = await res.json();

  if (res.ok) {
    // ✅ store token if returned
    localStorage.setItem("token", result.access_token);
    window.location.href = "/frontend/login/loginindex.html";
  } else {
    alert(result.detail || "Signup failed");
  }
}
