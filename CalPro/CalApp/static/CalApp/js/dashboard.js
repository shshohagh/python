document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('addEntryForm');
    var editForm = document.getElementById('editEntryForm');
    var entriesBody = document.getElementById('entriesBody');
    var emptyState = document.getElementById('emptyState');
    var formAlert = document.getElementById('formAlert');
    var editFormAlert = document.getElementById('editFormAlert');
    var modalEl = document.getElementById('addEntryModal');
    var editModalEl = document.getElementById('editEntryModal');
    var modal = modalEl ? new bootstrap.Modal(modalEl) : null;
    var editModal = editModalEl ? new bootstrap.Modal(editModalEl) : null;

    function getCsrfToken(scopeForm) {
        var input = scopeForm.querySelector('input[name=csrfmiddlewaretoken]');
        return input ? input.value : '';
    }

    function updateTotals(data) {
        document.getElementById('requiredValue').textContent = data.required;
        document.getElementById('consumedValue').textContent = data.consumed;
        document.getElementById('remainingValue').textContent = data.remaining;
        document.getElementById('percentLabel').textContent = data.percent + '%';
        
        var guidelineText = document.getElementById('guidelineText');
        if (guidelineText && data.guideline !== undefined) {
            guidelineText.textContent = data.guideline;
        }

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
                    'X-CSRFToken': getCsrfToken(form || document),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    var row = entriesBody.querySelector('tr[data-entry-id="' + id + '"]');
                    if (row) row.remove();
                    toggleEmptyState();
                    updateTotals(data);
                    if (window.showToast) window.showToast('Item removed successfully.', 'success');
                });
        });
    }

    function attachEditHandler(button) {
        button.addEventListener('click', function () {
            var id = button.getAttribute('data-id');
            var name = button.getAttribute('data-name');
            var calories = button.getAttribute('data-calories');

            document.getElementById('editEntryId').value = id;
            document.getElementById('editItemName').value = name;
            document.getElementById('editCalories').value = calories;

            if (editFormAlert) editFormAlert.classList.add('d-none');
            if (editModal) editModal.show();
        });
    }

    entriesBody.querySelectorAll('.delete-entry-btn').forEach(attachDeleteHandler);
    entriesBody.querySelectorAll('.edit-entry-btn').forEach(attachEditHandler);

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (formAlert) formAlert.classList.add('d-none');

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
                        var msg = messages.join(' ') || 'Please check the form and try again.';
                        if (window.showToast) {
                            window.showToast(msg, 'error');
                        } else if (formAlert) {
                            formAlert.textContent = msg;
                            formAlert.classList.remove('d-none');
                        }
                        return;
                    }

                    var entry = result.data.entry;
                    var row = document.createElement('tr');
                    row.setAttribute('data-entry-id', entry.id);
                    row.className = 'entry-new';
                    row.innerHTML =
                        '<td class="item-name">' + entry.item_name + '</td>' +
                        '<td class="item-calories">' + entry.calories + ' kcal</td>' +
                        '<td class="text-end text-nowrap">' +
                        '<button class="btn btn-sm btn-outline-primary edit-entry-btn me-1" data-id="' + entry.id + '" data-name="' + entry.item_name + '" data-calories="' + entry.calories + '"><i class="bi bi-pencil"></i></button>' +
                        '<button class="btn btn-sm btn-outline-danger delete-entry-btn" data-id="' + entry.id + '"><i class="bi bi-trash"></i></button></td>';
                    entriesBody.prepend(row);
                    attachDeleteHandler(row.querySelector('.delete-entry-btn'));
                    attachEditHandler(row.querySelector('.edit-entry-btn'));
                    toggleEmptyState();
                    updateTotals(result.data);

                    form.reset();
                    if (modal) modal.hide();
                    if (window.showToast) window.showToast('Item added successfully.', 'success');
                });
        });
    }

    if (editForm) {
        editForm.addEventListener('submit', function (event) {
            event.preventDefault();
            if (editFormAlert) editFormAlert.classList.add('d-none');

            var id = document.getElementById('editEntryId').value;

            fetch(window.CALORIE_URLS.editBase + id + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(editForm),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: new FormData(editForm),
            })
                .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
                .then(function (result) {
                    if (result.status !== 200) {
                        var errors = result.data.errors || {};
                        var messages = Object.keys(errors).map(function (key) {
                            return errors[key].join(' ');
                        });
                        var msg = messages.join(' ') || 'Please check the form and try again.';
                        if (window.showToast) {
                            window.showToast(msg, 'error');
                        } else if (editFormAlert) {
                            editFormAlert.textContent = msg;
                            editFormAlert.classList.remove('d-none');
                        }
                        return;
                    }

                    var entry = result.data.entry;
                    var row = entriesBody.querySelector('tr[data-entry-id="' + id + '"]');
                    if (row) {
                        row.querySelector('.item-name').textContent = entry.item_name;
                        row.querySelector('.item-calories').textContent = entry.calories + ' kcal';
                        var editBtn = row.querySelector('.edit-entry-btn');
                        if (editBtn) {
                            editBtn.setAttribute('data-name', entry.item_name);
                            editBtn.setAttribute('data-calories', entry.calories);
                        }
                    }
                    
                    updateTotals(result.data);
                    if (editModal) editModal.hide();
                    if (window.showToast) window.showToast('Item updated successfully.', 'success');
                });
        });
    }
});
