/* const columns = {{ columns | tojson | safe }}; */
console.log({});

function updateColumns(tableId, columnId) {
    const tableSelect = document.getElementById(tableId);
    const columnSelect = document.getElementById(columnId);
    const selectedTable = tableSelect.value;

    columnSelect.innerHTML = '<option value="" disabled selected>Seleccione una columna</option>';

    if (selectedTable && {}[selectedTable]) {
        {}[selectedTable].forEach(col => {
            const option = document.createElement('option');
            option.value = col;
            option.textContent = col;
            columnSelect.appendChild(option);
        });
    }
}

window.updateColumns = updateColumns;
