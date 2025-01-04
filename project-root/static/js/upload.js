document.getElementById('file-upload').addEventListener('change', updateFileName);

function updateFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name-display');
    const allowedExtensions = ['xls', 'xlsx', 'csv'];

    if (fileInput.files.length > 0) {
        const invalidFiles = [];
        const emptyFiles = [];
        const fileNames = Array.from(fileInput.files).map(file => {
            const extension = file.name.split('.').pop().toLowerCase();
            if (!allowedExtensions.includes(extension)) {
                invalidFiles.push(file.name);
            } else if(file.size == 0){
                emptyFiles.push(file.name);
            }
            return file.name;
        }).join(', ');

        if (invalidFiles.length > 0) {
            alert(`Los siguientes archivos no son válidos: ${invalidFiles.join(', ')}`);
            fileInput.value = ''; // Limpia la selección de archivos
            fileNameDisplay.textContent = 'Ningún archivo seleccionado';
        } else {
            fileNameDisplay.textContent = `Archivo seleccionado: ${fileNames}`;
        }
    } else {
        fileNameDisplay.textContent = 'Ningún archivo seleccionado';
    }
}