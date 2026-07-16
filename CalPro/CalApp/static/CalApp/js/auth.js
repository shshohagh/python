document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.toggle-password').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var targetId = btn.getAttribute('data-target');
            var input = document.getElementById(targetId);
            if (!input) return;
            var icon = btn.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.replace('bi-eye', 'bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.replace('bi-eye-slash', 'bi-eye');
            }
        });
    });

    var registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            var pw1 = registerForm.querySelector('#id_password1');
            var pw2 = registerForm.querySelector('#id_password2');
            if (pw1 && pw2 && pw1.value !== pw2.value) {
                event.preventDefault();
                pw2.classList.add('is-invalid');
                var existing = registerForm.querySelector('.password-mismatch-error');
                if (!existing) {
                    var div = document.createElement('div');
                    div.className = 'text-danger small mt-1 password-mismatch-error';
                    div.textContent = 'Passwords do not match.';
                    pw2.insertAdjacentElement('afterend', div);
                }
            }
        });
    }
});
