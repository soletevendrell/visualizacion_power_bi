function processExcelData() {
    const excelData = document.getElementById('excelData').value.trim();
    const tableName = document.getElementById('tableName').value.trim();

    if (!excelData || !tableName) {
        alert('Por favor, complete todos los campos antes de continuar.');
        return;
    }

    document.getElementById('tablePreview').innerHTML = `<p>Datos procesados para la tabla: <strong>${tableName}</strong></p>`;
}

function saveTable() {
    const tableName = document.getElementById('tableName').value.trim();

    if (!tableName) {
        alert('Por favor, ingrese un nombre de tabla antes de guardar.');
        return;
    }

    // para guardar los datos en la bd
    alert(`Datos guardados en la tabla: ${tableName}`);
}
