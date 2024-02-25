document.getElementById('signup_form').addEventListener('submit', function(event) {
      // Validation for password
      var password = document.getElementById('new_pass').value;
      var passwordError = document.getElementById('passwordError');

      if (password.length < 8 || password.length > 20) {
        passwordError.textContent = 'Password should be 8 to 20 characters long.';
        event.preventDefault(); // Prevent form submission
      } else if (!/^[a-zA-Z0-9]+$/.test(password)) {
        passwordError.textContent = 'Password should only contain alphanumeric characters.';
        event.preventDefault();
      } else {
        passwordError.textContent = 'Success'; // Clear any previous error messages
      }
    });