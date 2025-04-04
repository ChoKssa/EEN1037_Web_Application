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

  if (username === "") {
    loginUsernameError.textContent = "Username is required.";
    valid = false;
  }
  else {
    loginUsernameError.textContent = "";
  }
  if (password === "") {
    loginPasswordError.textContent = "Password is required.";
    valid = false;
  }
  else {
    loginPasswordError.textContent = "";
  }

  // If all inputs are valid
  if (valid) {
    loginForm.submit();
  }
});
