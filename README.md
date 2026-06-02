# Flask Proyecto — Examen Parcial

## Cómo ejecutar el proyecto

### 1. Crear entorno virtual
```
py -3 -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependencias
```
pip install -r requirements.txt
```

### 3. Ejecutar el servidor
```
python app.py
```

### 4. Abrir en el navegador
```
http://localhost:5000
```

## Usuarios de prueba
| Usuario   | Contraseña | Nombre         |
|-----------|------------|----------------|
| admin     | 1234       | Administrador  |
| usuario1  | abcd       | Juan Pérez     |

## Productos de prueba
| Código | Producto         |
|--------|-----------------|
| P001   | Laptop HP        |
| P002   | Mouse Logitech   |
| P003   | Teclado Mecánico |
| P004   | Monitor Samsung  |
| P005   | Audífonos Sony   |

## Despliegue en Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
