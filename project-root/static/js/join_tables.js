function updateColumns(tableId, columnId) {
    const tableSelect = document.getElementById(tableId);
    const columnSelect = document.getElementById(columnId);
    const selectedTable = tableSelect.value;

    columnSelect.innerHTML = '<option value="" disabled selected>Seleccione una columna</option>';

    fetch(`/get_columns?table=${selectedTable}`)
        .then(response => response.json())
        .then(columns => {
            columns.forEach(col => {
                const option = document.createElement('option');
                option.value = col;
                option.textContent = col;
                columnSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error al cargar columnas:', error));
}