import csv
import uuid
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
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

conn = sqlite3.connect('mi_base_local.db')
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return "No file part"
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                process_and_upload_to_sqlite(filepath)
        return redirect(url_for('list_tables'))
    return render_template('upload.html')

def process_and_upload_to_sqlite(filepath):
    try:
        # leemos el archivo que puede ser tipo csv o excel
        if filepath.endswith('.csv'):
            data = pd.read_csv(filepath)
        elif filepath.endswith(('.xls', '.xlsx')):
            data = pd.read_excel(filepath, engine='openpyxl')
        else:
            print(f"Formato no soportado: {filepath}")
            return

        # conecto a SQLite
        conn = sqlite3.connect(DATABASE_PATH)
        table_name = os.path.splitext(os.path.basename(filepath))[0]

        print(f"Creando tabla: {table_name}")
        # guardo los datos en SQLite
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # verifico las tablas existentes
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tablas existentes: {tables}")

        conn.close()
        print(f"Datos cargados en SQLite desde {filepath}")

        print(f"Vista previa de los datos:\n{data.head()}")
    except Exception as e:
        print(f"Error al procesar el archivo {filepath}: {e}")

@app.route('/validate_sample', methods=['POST'])
def validate_sample():
    try:
        #obtenemos los datos del formulario
        population = int(request.form['population'])
        #sample_size = int(request.form['sample_size'])

        #CALCULO VALIDEZ MUESTRA ??
        if (population*(1.64485**2)*0.5*0.5)/(((population-1)*(0.1**2))+((1.64485**2)*0.5*0.5))>10:
            result = "La muestra es válida para representar a la población."
        else:
            result = "La muestra no es válida, debe ser XXXXXXXXXXXX"

        return render_template('upload.html', validation_result=result)
    except ValueError:
        return render_template('upload.html', validation_result="Por favor, introduzca valores numéricos válidos.")


@app.route('/tables')
def list_tables():
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
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

@app.route('/delete_table/<table_name>', methods=['POST'])
def delete_table(table_name):
    try:
        # Validar el nombre de la tabla
        if not table_name.isidentifier():
            return f"Nombre de tabla no válido: {table_name}", 400

        # Conectar a la base de datos
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            conn.commit()

        return redirect(url_for('list_tables'))  # Redirige a la lista de tablas
    except Exception as e:
        return f"Error al eliminar la tabla {table_name}: {e}", 500


@app.route('/join_tables', methods=['GET', 'POST'])
def join_tables():
    if request.method == 'POST':
        table1 = request.form.get('table1')
        column1 = request.form.get('column1')
        table2 = request.form.get('table2')
        column2 = request.form.get('column2')
        
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            query = f"""
            SELECT * FROM {table1}
            INNER JOIN {table2}
            ON {table1}.{column1} = {table2}.{column2};
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return render_template('joined_table.html', data=df.to_html(index=False))
        except Exception as e:
            return f"Error al unir tablas: {e}"

    # Obtener lista de tablas y columnas para el formulario
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    columns = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns[table] = [col[1] for col in cursor.fetchall()]
    conn.close()
    return render_template('join_tables.html', tables=tables, columns=columns)

@app.route('/paste_tables', methods=['GET'])
def paste_tables():
    return render_template('paste_tables.html')

@app.route('/save_pasted_data', methods=['POST'])
def save_pasted_data():
    try:
        data = request.json.get('data', '')

        if not data:
            return "Error: No se recibieron datos", 400

        # Procesar filas y columnas
        rows = [row.split('\t') for row in data.split('\n') if row.strip()]

        # Validar datos
        if not rows or len(set(len(row) for row in rows)) > 1:
            return "Error: Datos inválidos o inconsistencia en columnas", 400

        # Guardar en CSV
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'pasted_data.csv')
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        # Guardar en SQLite
        conn = sqlite3.connect(DATABASE_PATH)
        table_name = f"tabla_{uuid.uuid4().hex[:8]}"  # Nombre único
        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

        return f"Datos guardados correctamente en la tabla '{table_name}' con {len(df)} filas.", 200
    except ValueError as ve:
        return f"Error de validación: {ve}", 400
    except sqlite3.Error as sqle:
        return f"Error de base de datos: {sqle}", 500
    except Exception as e:
        return f"Error inesperado: {e}", 500



if __name__ == '__main__':
    app.run(debug=True)