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

        print(f"Creando tabla: {table_name}")
        # Guardar los datos en SQLite
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verificar tablas existentes
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tablas existentes: {tables}")

        conn.close()
        print(f"Datos cargados en SQLite desde {filepath}")

#        if filepath.endswith('.csv'):
#            data = pd.read_csv(filepath)
#        elif filepath.endswith(('.xls', '.xlsx')):
#            data = pd.read_excel(filepath)
#        else:
#            print(f"Formato no soportado: {filepath}")
#            return

        print(f"Vista previa de los datos:\n{data.head()}")
    except Exception as e:
        print(f"Error al procesar el archivo {filepath}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tables')
def list_tables():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return render_template('tables.html', tables=tables)
    except Exception as e:
        return f"Error al listar tablas: {e}"

@app.route('/table/<table_name>')
def show_table(table_name):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return render_template('table.html', table_name=table_name, data=df.to_html(index=False))
    except Exception as e:
        return f"Error al mostrar la tabla {table_name}: {e}"


if __name__ == '__main__':
    app.run(debug=True)