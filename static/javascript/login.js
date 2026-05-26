// START: LOGIN_SCRIPT
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const rememberMe = document.getElementById('rememberMe');
    const roleInputs = document.querySelectorAll('input[name="role"]');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            // Validation: Role must be selected
            let roleSelected = false;
            roleInputs.forEach(input => {
                if (input.checked) {
                    roleSelected = true;
                }
            });

            if (!roleSelected) {
                e.preventDefault();
                alert('Please select your category (Student, Teacher, Staff, or Parent) before logging in.');
                return;
            }

            // Validation: Remember Me must be checked
            if (!rememberMe.checked) {
                e.preventDefault();
                alert('You must check the "Remember Me" box to login.');
                return;
            }
        });
    }

    // START: PASSWORD_TOGGLE_LOGIC
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            // Toggle the type attribute
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle the icon
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
    // END: PASSWORD_TOGGLE_LOGIC

    // Add some smooth interaction for inputs
    const inputs = document.querySelectorAll('.input-group input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.parentElement.classList.remove('focused');
            }
        });
    });
});
// END: LOGIN_SCRIPT
