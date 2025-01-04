/*
function processExcelData() {
    const rawData = document.getElementById('excelData').value;

    if (!rawData.trim()) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    // Parsear los datos pegados como filas y columnas
    const rows = rawData.split('\n').map(row => row.split('\t'));
    const maxColumns = Math.max(...rows.map(row => row.length));
    rows.forEach(row => {
        while (row.length < maxColumns) {
            row.push('');
        }
    });


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
*/
function processExcelData() {
    const rawData = document.getElementById('excelData').value;

    if (!rawData.trim()) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    // Parsear los datos pegados
    const rows = rawData.split('\n').map(row => row.split('\t'));
    const maxColumns = Math.max(...rows.map(row => row.length));

    // Rellenar celdas vacías
    const filledRows = rows.map(row => {
        const newRow = [];
        let lastValue = '';

        for (let i = 0; i < maxColumns; i++) {
            if (row[i] && row[i].trim()) {
                lastValue = row[i].trim();
                newRow.push(lastValue);
            } else {
                newRow.push(lastValue); // Hereda el valor más cercano
            }
        }
        return newRow;
    });

    // Asegurar que todas las filas tengan la misma longitud
    filledRows.forEach(row => {
        while (row.length < maxColumns) {
            row.push('');
        }
    });

    // Crear tabla HTML de vista previa
    const table = document.createElement('table');
    table.border = '1';

    filledRows.forEach(row => {
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
    const rawData = document.getElementById('excelData').value.trim();
    const tableName = document.getElementById('tableName').value.trim();

    if (!rawData) {
        alert('Por favor, pegue datos válidos desde Excel.');
        return;
    }

    if (!tableName) {
        alert('Por favor, ingrese un nombre para la tabla.');
        return;
    }

    const rows = rawData.split('\n').map(row => row.split('\t'));
    if (rows.some(row => row.length !== rows[0].length)) {
        alert('Los datos tienen filas con columnas inconsistentes.');
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
                return response.text().then(err => {
                    alert(`Error al guardar los datos: ${err}`);
                });
            }
        })
        .catch(error => console.error('Error:', error));
}