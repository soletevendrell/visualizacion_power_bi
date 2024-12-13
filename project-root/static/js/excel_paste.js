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

    if (!rawData.trim()) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    // Enviar los datos al backend
    fetch('/save_pasted_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: rawData }),
    })
        .then(response => {
            if (response.ok) {
                return response.text(); // Leer el mensaje del servidor
            } else {
                throw new Error('Error al guardar los datos.');
            }
        })
        .then(message => alert(message))
        .catch(error => console.error('Error:', error));
}

