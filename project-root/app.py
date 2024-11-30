from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
DATABASE_PATH = 'mi_base_local.db'

conn = sqlite3.connect('mi_base_local.db')
conn.close()

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
                process_and_upload_to_sqlite(filepath)
        return redirect(url_for('index'))
    return render_template('upload.html')

def process_and_upload_to_sqlite(filepath):
    """
    Procesa el archivo subido y lo carga en SQLite.
    """
    try:
        # Leer el archivo
        if filepath.endswith('.csv'):
            data = pd.read_csv(filepath)
        elif filepath.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filepath)
        else:
            print(f"Formato no soportado: {filepath}")
            return

        # Conectar a SQLite
        conn = sqlite3.connect(DATABASE_PATH)
        table_name = os.path.splitext(os.path.basename(filepath))[0]

        # Guardar los datos en SQLite
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

        print(f"Datos cargados en SQLite desde {filepath}")
    except Exception as e:
        print(f"Error al procesar el archivo {filepath}: {e}")

if __name__ == '__main__':
    app.run(debug=True)