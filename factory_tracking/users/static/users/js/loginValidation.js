document.addEventListener("DOMContentLoaded", function () {
  let loginForm = document.getElementById("loginForm");
  console.log("entering loginValidation.js");


  loginForm.addEventListener("submit", function (event) {
    console.log("Form submitted");
    //event.preventDefault();

    let valid = true;
    let loginUsername = document.getElementById("username");
    let loginPassword = document.getElementById("password");
    let loginUsernameError = document.getElementById("usernameError");
    let loginPasswordError = document.getElementById("passwordError");

    let username = loginUsername.value.trim();
    let password = loginPassword.value.trim();

    if (username.length < 5) {
      loginUsernameError.textContent = "Username must be at least 5 characters long.";
      valid = false;
    } else {
      loginUsernameError.textContent = "";
    }

    if (password.length < 5) {
      loginPasswordError.textContent = "Password must be at least 5 characters long.";
      valid = false;
    } else {
      loginPasswordError.textContent = "";
    }
    if (!valid) {
      event.preventDefault(); // Prevent form submission if there are errors
      console.log("Form submission prevented due to validation errors");
    }

    // If all inputs are valid
    if (valid) {
      loginForm.submit();
      console.log("Form submitted successfully");
    }
  });
});
