let loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", function (event) {
  event.preventDefault();

  let valid = true;
  let loginUsername = document.getElementById("username");
  let loginPassword = document.getElementById("password");
  let loginUsernameError = document.getElementById("usernameError");
  let loginPasswordError = document.getElementById("passwordError");

  let username = loginUsername.value.trim();
  let password = loginPassword.value.trim();

  // Validate username
  if (username.length < 5) {
    loginUsernameError.innerText =
      "Username must be at least 5 characters long.";
    valid = false;
  } else {
    loginUsernameError.innerText = "";
  }

  // Validate password
  if (password.length < 6) {
    loginPasswordError.innerText =
      "Password must be at least 6 characters long.";
    valid = false;
  } else {
    loginPasswordError.innerText = "";
  }

  // If all inputs are valid
  if (valid) {
    // Fake check: simulate a user found in database
    // Replace this with real backend logic
    let found = username === "admin" && password === "admin123";

    if (found) {
      alert("Login successful!");
      loginForm.reset();
      // Redirect to dashboard.html
      window.location.href = "dashboard.html";
    } else {
      alert("Invalid username or password.");
    }
  }
});
