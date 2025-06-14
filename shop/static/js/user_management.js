document.addEventListener('DOMContentLoaded', function () {
    const editableCells = document.querySelectorAll('.excel-table .editable');

    editableCells.forEach(cell => {
        cell.addEventListener('dblclick', function () {
            const originalValue = this.textContent;
            const field = this.getAttribute('data-field');
            const userId = this.parentElement.getAttribute('data-user-id');
            const input = document.createElement('input');
            input.value = originalValue === '-' ? '' : originalValue;
            input.className = 'form-control';

            if (field === 'is_staff' || field === 'is_active') {
                input.type = 'checkbox';
                input.checked = originalValue === 'Да';
            }

            this.textContent = '';
            this.appendChild(input);
            input.focus();

            input.addEventListener('blur', function () {
                const newValue = field === 'is_staff' || field === 'is_active' ? input.checked : input.value;
                saveField(userId, field, newValue, originalValue, cell);
            });

            input.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    const newValue = field === 'is_staff' || field === 'is_active' ? input.checked : input.value;
                    saveField(userId, field, newValue, originalValue, cell);
                }
            });
        });
    });

    function saveField(userId, field, newValue, originalValue, cell) {
        const data = { [field]: newValue };
        fetch(`/admin/users/${userId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                cell.textContent = field === 'is_staff' || field === 'is_active' ? (newValue ? 'Да' : 'Нет') : newValue || '-';
            } else {
                cell.textContent = originalValue;
                alert(data.error || 'Ошибка сохранения');
            }
        })
        .catch(() => {
            cell.textContent = originalValue;
            alert('Ошибка сервера');
        });
    }
});