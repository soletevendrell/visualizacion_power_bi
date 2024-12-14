function showPopup(tableName) {
    document.getElementById('tableName').textContent = tableName;
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/delete_table/${encodeURIComponent(tableName)}`;
    document.getElementById('deletePopup').classList.add('visible');
}

function closePopup() {
    document.getElementById('deletePopup').classList.remove('visible');
}
