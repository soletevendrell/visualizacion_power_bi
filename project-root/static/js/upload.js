function updateFileName() {
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (fileInput.files.length > 0) {
        const fileNames = Array.from(fileInput.files).map(file => file.name).join(', ');
        fileNameDisplay.textContent = `Archivo seleccionado: ${fileNames}`;
    } else {
        fileNameDisplay.textContent = 'Ningún archivo seleccionado';
    }
}
