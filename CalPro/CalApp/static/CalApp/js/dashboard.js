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
                    var row = entriesBody.querySelector('[data-entry-id="' + id + '"]');
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
            var catId = button.getAttribute('data-category');
            var name = button.getAttribute('data-name');
            var calories = button.getAttribute('data-calories');

            document.getElementById('editEntryId').value = id;
            var catSelect = document.getElementById('editCategory');
            if (catSelect) catSelect.value = catId;
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

            var formData = new FormData(form);
            if (window.TARGET_DATE) {
                formData.append('date', window.TARGET_DATE);
            }

            fetch(window.CALORIE_URLS.add, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(form),
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
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
                    var catColor = entry.category && entry.category.color ? entry.category.color : 'primary';
                    var catIcon = entry.category && entry.category.icon ? entry.category.icon : '<i class="bi bi-tag fs-4"></i>';
                    var catName = entry.category && entry.category.name ? entry.category.name : 'Uncategorized';
                    var catId = entry.category && entry.category.id ? entry.category.id : '';

                    var row = document.createElement('div');
                    row.setAttribute('data-entry-id', entry.id);
                    row.className = 'd-flex align-items-center gap-3 p-3 rounded bg-white shadow-sm border-0 mb-3 food-log-item entry-new';
                    row.innerHTML =
                        '<div class="bg-' + catColor + ' text-white rounded d-flex align-items-center justify-content-center flex-shrink-0 item-icon-wrapper" style="width: 48px; height: 48px;">' +
                            catIcon +
                        '</div>' +
                        '<div class="flex-grow-1 overflow-hidden">' +
                            '<div class="fw-bold fs-5 text-truncate item-category-name">' + catName + '</div>' +
                            '<div class="small text-muted text-truncate item-name">' + entry.item_name + '</div>' +
                        '</div>' +
                        '<div class="ms-auto d-flex align-items-center gap-3">' +
                            '<div class="fw-bold fs-5 text-nowrap item-calories">' + entry.calories + ' kcal</div>' +
                            '<div class="text-nowrap flex-shrink-0">' +
                                '<button class="btn btn-sm btn-outline-primary edit-entry-btn rounded-circle" style="width: 32px; height: 32px; padding: 0;" data-id="' + entry.id + '" data-category="' + catId + '" data-name="' + entry.item_name + '" data-calories="' + entry.calories + '">' +
                                    '<i class="bi bi-pencil"></i>' +
                                '</button>' +
                                '<button class="btn btn-sm btn-outline-danger delete-entry-btn rounded-circle ms-1" style="width: 32px; height: 32px; padding: 0;" data-id="' + entry.id + '">' +
                                    '<i class="bi bi-trash"></i>' +
                                '</button>' +
                            '</div>' +
                        '</div>';
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
                    var row = entriesBody.querySelector('[data-entry-id="' + id + '"]');
                    if (row) {
                        var catColor = entry.category && entry.category.color ? entry.category.color : 'primary';
                        var catIcon = entry.category && entry.category.icon ? entry.category.icon : '<i class="bi bi-tag fs-4"></i>';
                        var catName = entry.category && entry.category.name ? entry.category.name : 'Uncategorized';
                        var catId = entry.category && entry.category.id ? entry.category.id : '';

                        var iconWrapper = row.querySelector('.item-icon-wrapper');
                        if (iconWrapper) {
                            iconWrapper.className = 'bg-' + catColor + ' text-white rounded d-flex align-items-center justify-content-center flex-shrink-0 item-icon-wrapper';
                            iconWrapper.innerHTML = catIcon;
                        }

                        var catNameEl = row.querySelector('.item-category-name');
                        if (catNameEl) catNameEl.textContent = catName;

                        row.querySelector('.item-name').textContent = entry.item_name;
                        row.querySelector('.item-calories').textContent = entry.calories + ' kcal';
                        var editBtn = row.querySelector('.edit-entry-btn');
                        if (editBtn) {
                            editBtn.setAttribute('data-category', catId);
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

    var waterBtns = document.querySelectorAll('.water-btn');
    var waterGlasses = document.getElementById('waterGlasses');
    
    if (waterBtns.length > 0) {
        waterBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.getAttribute('data-action');
                var formData = new FormData();
                formData.append('action', action);
                if (window.TARGET_DATE) formData.append('date', window.TARGET_DATE);
                
                fetch(window.CALORIE_URLS.updateWater, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(document.body),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    if (data.glasses !== undefined && waterGlasses) {
                        waterGlasses.textContent = data.glasses;
                    }
                });
            });
        });
    }
});
