# Proyecto 2 — Renta de Herramientas (Asistente Inteligente y Recomendador)

**Materia:** Tópicos Selectos de Tecnologías Web y Móvil  
**Profesor:** Eduardo Alcaraz  
**Alumno:** David Maldonado Barajas (22121348)  
**Tema Asignado:** Renta de herramientas (Asistente inteligente para el comprador integrado al recomendador)

---

## 1. Descripción del Proyecto

Segunda versión del sistema de renta de herramientas. Partiendo de la base del Proyecto 1, se integra un **Asistente Virtual inteligente** que atiende al comprador a través de una pantalla de chat conectada por API REST.

El sistema completo integra:
- **Backend API REST (Django + SQLite):** Catálogo de 18 herramientas y kits, persistencia de rentas con generación automática de folios, recomendador híbrido (Árbol de Decisión + Reglas de seguridad) y endpoint del asistente inteligente con clasificación de intenciones (`modelo_asistente.joblib`).
- **Frontend Cliente (Flutter Web):** Aplicación interactiva de 4 pestañas: Recomendador, Catálogo, Buscar Folio y el nuevo Chat del Asistente.
- **Documentación:**
  - **[PATRONES.md](./PATRONES.md):** Análisis de patrones de software actualizado (Adapter, Separación cliente/servidor, Recomendador vs. Asistente, MVC, etc.).
  - **[EXPLICACION.md](./EXPLICACION.md):** Guía completa de la arquitectura, mapa de archivos, manejo de errores y defensa del proyecto.

---

## 2. Requisitos Previos

- Python 3.10+ (o superior)
- Flutter SDK (para ejecutar el cliente web en Chrome)
- Google Chrome

---

## 3. Instalación y Ejecución

### Paso 1: Levantar el Backend (Django)

Desde una terminal, ubicarse en la carpeta `proyecto_2`:

```bash
cd proyecto_2

# 1. Crear y activar entorno virtual (opcional)
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

### Paso 2: Levantar el Frontend (Flutter Web)

En **otra terminal**, dentro de la carpeta del proyecto:

```bash
cd proyecto_2/frontend_flutter

# 1. Descargar dependencias
flutter pub get

# 2. Ejecutar en el navegador
flutter run -d chrome
```

La aplicación abrirá Chrome automáticamente conectándose al backend en `http://127.0.0.1:8000`.

---

## 4. Endpoints Principales de la API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/catalogo/` | Retorna el inventario completo de herramientas individuales y kits. |
| `POST` | `/api/recomendar/` | Recibe características de la obra y devuelve la sugerencia (ML + Reglas). |
| `POST` | `/api/rentas/` | Registra una orden de renta y genera un folio único auditable. |
| `GET` | `/api/rentas/<folio>/` | Consulta el detalle, costo y estado de una orden por su folio. |
| `POST` | `/api/asistente/` | Recibe el mensaje del chat, detecta la intención y responde orientando al usuario. |

---

## 5. Comandos Útiles

- **Ejecutar pruebas unitarias automatizadas (7 tests):**
  ```bash
  python manage.py test
  ```
- **Reentrenar el recomendador de herramientas (Árbol ML):**
  ```bash
  python entrenamiento/entrenar_arbol.py
  ```
- **Reentrenar el clasificador del asistente (Chat):**
  ```bash
  python entrenamiento/entrenar_asistente.py
  ```
