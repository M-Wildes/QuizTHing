const API = "https://quiz-auth.9s7khfkcvx.workers.dev";
console.log("Script loaded");
// SIGNUP
async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

const res = await fetch(API + "/signup", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({ email, password })
});

const text = await res.text();
console.log("Response:", text); // 👈 ADD THIS
msg.innerText = text;
}
console.log("Script loaded");

// LOGIN
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(API + "/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });
  console.log("Script loaded");

  if (!res.ok) {
    document.getElementById("message").innerText = "Login failed";
    return;
  }

  const data = await res.json();
  console.log("Script loaded");

  // store user session (basic version)
  localStorage.setItem("userId", data.userId);

  document.getElementById("message").innerText = "Logged in!";
}

console.log("Script loaded");