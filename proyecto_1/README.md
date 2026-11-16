# Proyecto 1 — Renta de Herramientas (Recomendador Inteligente)

**Materia:** Tópicos Selectos de Tecnologías Web y Móvil  
**Profesor:** Eduardo Alcaraz  
**Alumno:** David Maldonado Barajas (22121348)  
**Tema Asignado:** Renta de herramientas

---

## Descripción del Proyecto

Sistema para la renta y recomendación de herramientas y kits de trabajo para construcción, plomería, electricidad, carpintería, pintura, etc.

El proyecto integra:

- **Backend API REST (con Django y SQLite)**, es un catálogo de herramientas, gestión de rentas con generación automática de folios y motor híbrido de recomendación (Árbol de Decisión en `scikit-learn` + Reglas de negocio y seguridad física en `rentas/reglas.py`).
- **Frontend Cliente (Flutter Web)**, es una aplicación interactiva para consultar el catálogo, solicitar recomendaciones en tiempo real y confirmar rentas con folio.

---

## Requisitos Previos

- Python 3.10+ (o superior)
- Flutter SDK ( para compilar/ejecutar el cliente web)
- Navegador Google Chrome

---

## Instalación y Ejecución

### Paso 1. Levantar el Backend (Django)

Desde la carpeta `proyecto_1`:

```bash
cd proyecto_1

# 1. Crear y activar entorno virtual
python -m venv .venv
# En Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# En Linux / macOS:
source .venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Aplicar migraciones a la base de datos
python manage.py migrate

# 4. Iniciar el servidor local
python manage.py runserver
```

El servidor web quedará activo en `http://127.0.0.1:8000/`.

---

### Paso 2. Levantar el Frontend (Flutter Web)

En **otra terminal**, dentro de la carpeta del proyecto:

```bash
cd proyecto_1/frontend_flutter

# 1. Descargar dependencias
flutter pub get

# 2. Ejecutar en el navegador
flutter run -d chrome
```

La aplicación abrirá Chrome automáticamente conectándose al backend en `http://127.0.0.1:8000`.

## 5. Comandos Útiles

- **Ejecutar pruebas unitarias automatizadas (7 tests):**
  ```bash
  python manage.py test
  ```
- **Reentrenar el modelo de Machine Learning:**
  ```bash
  python entrenamiento/entrenar_arbol.py
  ```
