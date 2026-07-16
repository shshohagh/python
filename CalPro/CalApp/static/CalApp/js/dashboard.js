document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('addEntryForm');
    var entriesBody = document.getElementById('entriesBody');
    var emptyState = document.getElementById('emptyState');
    var formAlert = document.getElementById('formAlert');
    var modalEl = document.getElementById('addEntryModal');
    var modal = modalEl ? new bootstrap.Modal(modalEl) : null;

    function getCsrfToken(scopeForm) {
        var input = scopeForm.querySelector('input[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }

    function updateTotals(data) {
        document.getElementById('requiredValue').textContent = data.required;
        document.getElementById('consumedValue').textContent = data.consumed;
        document.getElementById('remainingValue').textContent = data.remaining;
        document.getElementById('percentLabel').textContent = data.percent + '%';

        var bar = document.getElementById('progressBar');
        bar.style.width = data.percent + '%';
        bar.classList.remove('bg-success', 'bg-warning', 'bg-danger');
        if (data.percent < 70) {
            bar.classList.add('bg-success');
        } else if (data.percent <= 100) {
            bar.classList.add('bg-warning');
        } else {
            bar.classList.add('bg-danger');
        }
    }

    function toggleEmptyState() {
        if (!emptyState) return;
        emptyState.style.display = entriesBody.children.length ? 'none' : '';
    }

    function attachDeleteHandler(button) {
        button.addEventListener('click', function () {
            if (!confirm('Remove this entry?')) return;
            var id = button.getAttribute('data-id');
            fetch(window.CALORIE_URLS.deleteBase + id + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(form),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    var row = entriesBody.querySelector('tr[data-entry-id="' + id + '"]');
                    if (row) row.remove();
                    toggleEmptyState();
                    updateTotals(data);
                });
        });
    }

    entriesBody.querySelectorAll('.delete-entry-btn').forEach(attachDeleteHandler);

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            formAlert.classList.add('d-none');
            formAlert.textContent = '';

            fetch(window.CALORIE_URLS.add, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(form),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(form),
            })
                .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
                .then(function (result) {
                    if (result.status !== 200) {
                        var errors = result.data.errors || {};
                        var messages = Object.keys(errors).map(function (key) {
                            return errors[key].join(' ');
                        });
                        formAlert.textContent = messages.join(' ') || 'Please check the form and try again.';
                        formAlert.classList.remove('d-none');
                        return;
                    }

                    var entry = result.data.entry;
                    var row = document.createElement('tr');
                    row.setAttribute('data-entry-id', entry.id);
                    row.className = 'entry-new';
                    row.innerHTML =
                        '<td>' + entry.item_name + '</td>' +
                        '<td>' + entry.calories + ' kcal</td>' +
                        '<td class="text-end">' +
                        '<button class="btn btn-sm btn-outline-danger delete-entry-btn" data-id="' + entry.id + '">' +
                        '<i class="bi bi-trash"></i></button></td>';
                    entriesBody.prepend(row);
                    attachDeleteHandler(row.querySelector('.delete-entry-btn'));
                    toggleEmptyState();
                    updateTotals(result.data);

                    form.reset();
                    if (modal) modal.hide();
                });
        });
    }
});
