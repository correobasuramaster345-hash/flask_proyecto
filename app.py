from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_examen_2025'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
# ── Base de datos ──────────────────────────────────────────
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def get_db():
    db = sqlite3.connect(DB_PATH)

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL
    )''')
    db.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL,
        stock INTEGER,
        categoria TEXT
    )''')
    # Insertar datos de prueba si las tablas están vacías
    if not db.execute('SELECT * FROM usuarios').fetchone():
        db.execute("INSERT INTO usuarios (username, password, nombre) VALUES ('admin', '1234', 'Administrador')")
        db.execute("INSERT INTO usuarios (username, password, nombre) VALUES ('usuario1', 'abcd', 'Juan Pérez')")
    if not db.execute('SELECT * FROM productos').fetchone():
        productos = [
            ('P001', 'Laptop HP', 'Laptop HP Core i5 8GB RAM 256GB SSD', 2500.00, 10, 'Tecnología'),
            ('P002', 'Mouse Logitech', 'Mouse inalámbrico ergonómico', 85.00, 50, 'Accesorios'),
            ('P003', 'Teclado Mecánico', 'Teclado mecánico RGB retroiluminado', 220.00, 25, 'Accesorios'),
            ('P004', 'Monitor Samsung', 'Monitor 24 pulgadas Full HD IPS', 950.00, 15, 'Tecnología'),
            ('P005', 'Audífonos Sony', 'Audífonos inalámbricos con cancelación de ruido', 380.00, 30, 'Audio'),
        ]
        db.executemany("INSERT INTO productos (codigo, nombre, descripcion, precio, stock, categoria) VALUES (?,?,?,?,?,?)", productos)
    db.commit()
    db.close()

# ── Rutas ──────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE username=? AND password=?', (username, password)).fetchone()
        db.close()
        if user:
            session['usuario'] = username
            session['nombre'] = user['nombre']
            return redirect(url_for('principal'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/principal')
def principal():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('principal.html', nombre=session['nombre'])

@app.route('/buscador')
def buscador():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('buscador.html')

@app.route('/api/buscar_producto', methods=['POST'])
def buscar_producto():
    codigo = request.json.get('codigo', '').strip().upper()
    db = get_db()
    producto = db.execute('SELECT * FROM productos WHERE codigo=?', (codigo,)).fetchone()
    db.close()
    if producto:
        return jsonify({
            'encontrado': True,
            'codigo': producto['codigo'],
            'nombre': producto['nombre'],
            'descripcion': producto['descripcion'],
            'precio': producto['precio'],
            'stock': producto['stock'],
            'categoria': producto['categoria']
        })
    else:
        return jsonify({'encontrado': False, 'mensaje': 'Producto no encontrado'})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── Inicio ─────────────────────────────────────────────────
# Inicializar la base de datos siempre al arrancar
with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)