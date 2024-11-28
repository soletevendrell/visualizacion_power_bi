from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return "No file part"
        files = request.files.getlist('files[]')
        for file in files:
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                process_file(filepath)
        return redirect(url_for('index'))
    return render_template('upload.html')

def process_file(filepath):
    """
    Procesa el archivo subido (CSV o Excel) y genera una vista previa.
    """
    try:
        if filepath.endswith('.csv'):
            data = pd.read_csv(filepath)
        elif filepath.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filepath)
        else:
            print(f"Formato no soportado: {filepath}")
            return

        print(f"Archivo procesado: {filepath}")
        print(data.head())  # Vista previa en consola
        # Aquí puedes agregar lógica adicional para guardar o transformar los datos
    except Exception as e:
        print(f"Error al procesar el archivo {filepath}: {e}")

if __name__ == '__main__':
    app.run(debug=True)