const API = "https://quiz-auth.9s7khfkcvx.workers.dev";
<<<<<<< HEAD

=======
console.log("Script loaded");
>>>>>>> 844f1faa3e704174828ebd016059307633067f2e
// SIGNUP
async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

<<<<<<< HEAD
  const res = await fetch(API + "/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  alert(await res.text());
}
=======
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
>>>>>>> 844f1faa3e704174828ebd016059307633067f2e

// LOGIN
async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const res = await fetch(API + "/login", {
    method: "POST",
<<<<<<< HEAD
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (data.success) {
    localStorage.setItem("userId", data.userId);
    alert("Logged in");
  } else {
    alert("Login failed");
  }
}
=======
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
>>>>>>> 844f1faa3e704174828ebd016059307633067f2e
