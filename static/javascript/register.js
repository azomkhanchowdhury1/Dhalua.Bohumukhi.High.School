// START: REGISTER_SCRIPT
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const roleInputs = document.querySelectorAll('input[name="role"]');

    registerForm.addEventListener('submit', (e) => {
        let roleSelected = false;
        roleInputs.forEach(input => {
            if (input.checked) {
                roleSelected = true;
            }
        });

        if (!roleSelected) {
            e.preventDefault();
            alert('Please select your registration category (Student, Teacher, Staff, or Parent).');
            return;
        }
    });

    const inputs = document.querySelectorAll('.input-group input, .input-group textarea');
    inputs.forEach(input => {
        // To handle initial state if browser autofills
        if (input.value !== '') {
            input.classList.add('has-content');
        }

        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.parentElement.classList.remove('focused');
                input.classList.remove('has-content');
            } else {
                input.classList.add('has-content');
            }
        });
    });
});
// END: REGISTER_SCRIPT
