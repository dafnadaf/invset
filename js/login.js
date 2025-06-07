document.getElementById("loginForm").addEventListener("submit", e => {
  e.preventDefault();
  const u = e.target.user.value.trim();
  const p = e.target.pass.value.trim();
  if (u === "admin" && p === "admin123") {
    sessionStorage.setItem("auth", "ok");
    location.href = "companies.html";
  } else {
    alert("Bad credentials");
  }
});
