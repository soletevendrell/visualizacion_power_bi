function processExcelData() {
    const rawData = document.getElementById('excelData').value;

    if (!rawData.trim()) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    // Parsear los datos pegados como filas y columnas
    const rows = rawData.split('\n').map(row => row.split('\t'));
    const table = document.createElement('table');
    table.border = '1';

    rows.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(cell => {
            const td = document.createElement('td');
            td.textContent = cell;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    // Mostrar la tabla en la vista previa
    document.getElementById('tablePreview').innerHTML = '';
    document.getElementById('tablePreview').appendChild(table);
}

function saveTable() {
    const rawData = document.getElementById('excelData').value;
    const tableName = document.getElementById('tableName').value;

    if (!rawData.trim()) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    if (!tableName.trim()) {
        alert('Por favor, ingrese un nombre para la tabla.');
        return;
    }

    // Enviar los datos y el nombre de la tabla al backend
    fetch('/save_pasted_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: rawData, tableName: tableName }),
    })
        .then(response => {
            if (response.ok) {
                alert('Datos guardados correctamente en la base de datos.');
            } else {
                alert('Error al guardar los datos.');
            }
        })
        .catch(error => console.error('Error:', error));
}