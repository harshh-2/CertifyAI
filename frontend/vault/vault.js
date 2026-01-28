const API = "http://localhost:8000"
const token = localStorage.getItem("token")

if (!token) {
  alert("Login first")
  window.location.href = "../login/login.html"
}

// ---------------- Upload ----------------

async function uploadCert() {
  const file = document.getElementById("fileInput").files[0]

  if (!file) return alert("Select file")

  const formData = new FormData()
  formData.append("file", file)

  const res = await fetch(`${API}/vault/upload`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  })

  const data = await res.json()

  alert(data.status)

  loadCerts()
}

// ---------------- Load Certificates ----------------

async function loadCerts() {

  const res = await fetch(`${API}/vault/my-certificates`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  const data = await res.json()

  const list = document.getElementById("certList")
  list.innerHTML = ""

  data.certificates.forEach(cert => {

    const filename = cert.file_path.split("/").pop()

    list.innerHTML += `
      <div style="margin-bottom:15px">
        <b>${cert.certificate_name}</b><br>
        ${cert.provider}<br>

        <button onclick="viewCert('${filename}')">View</button>
      </div>
    `
  })
}

// ---------------- View ----------------

function viewCert(filename) {
 window.open(`${API}/vault/view/${filename}`, "_blank")
}

// Auto load
loadCerts()
