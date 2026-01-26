const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

let w, h;
function resize() {
  w = canvas.width = window.innerWidth;
  h = canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

/* PARTICLES */
const particles = Array.from({ length: 70 }, () => ({
  x: Math.random() * w,
  y: Math.random() * h,
  vx: (Math.random() - 0.5) * 0.25,
  vy: (Math.random() - 0.5) * 0.25,
  r: Math.random() * 1.8 + 0.6
}));

function animate() {
  ctx.clearRect(0, 0, w, h);
  particles.forEach(p => {
    p.x += p.vx;
    p.y += p.vy;
    if (p.x < 0 || p.x > w) p.vx *= -1;
    if (p.y < 0 || p.y > h) p.vy *= -1;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(139,92,246,0.6)";
    ctx.fill();
  });
  requestAnimationFrame(animate);
}
animate();

/* ---------------- SIGNUP LOGIC ---------------- */

async function signupUser() {
  const password = document.getElementById("password").value.trim();
  const confirm = document.getElementById("confirmPassword").value.trim();

  if (password !== confirm) {
    alert("Passwords do not match");
    return;
  }

  const payload = {
    username: document.getElementById("username").value.trim(),
    year_of_college: document.getElementById("year").value,
    age: document.getElementById("age").value,
    institution: document.getElementById("institution").value.trim(),
    gender: document.getElementById("gender").value,
    email: document.getElementById("email").value.trim(),
    password: password
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/auth/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Signup failed");
      return;
    }

    alert("Account created successfully!");
    window.location.href = "/login/loginindex.html";

  } catch (err) {
    console.error(err);
    alert("Backend server not reachable");
  }
}

