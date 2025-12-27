# Qode Boss – Secure AI Coding Challenge App

Qode Boss es una aplicación full‑stack que genera retos de programación usando IA.  
Cada usuario inicia sesión de forma segura, recibe un número limitado de preguntas al día y puede practicar lógica y lectura de código con una interfaz moderna en modo oscuro.

---

## ✨ Características principales

- 🤖 **Retos generados por IA**  
  - Preguntas tipo test en **español** sobre distintos lenguajes (Python, JavaScript, TypeScript, PHP, etc.).  
  - Preguntas con fragmentos de código y explicación detallada de la respuesta correcta.

- 🎚️ **Niveles de dificultad**  
  - Fácil, Media y Difícil, con diferencias reales en el tipo de preguntas.

- 🔐 **Autenticación con Clerk**  
  - Login y registro gestionados por Clerk.  
  - Avatar del usuario visible en la interfaz.  
  - Menú de usuario con opción de logout.

- ⏱️ **Sistema de cuotas por usuario**  
  - Cada usuario comienza con **5 retos disponibles**.  
  - Cada **2 horas** se regenera **1 reto** hasta un máximo de 5.  
  - Las cuotas se cuentan por usuario autenticado.

- 📜 **Historial de retos**  
  - Lista de retos generados por el usuario actual (no de otros usuarios).  
  - Al hacer clic en un reto del historial, puedes revisarlo y volver a responderlo.

- 🎨 **UI moderna en modo oscuro**  
  - Layout tipo dashboard con sidebar, header, tarjetas y sombras suaves.  
  - Tarjetas independientes para:
    - Generador de retos.
    - Pregunta y respuestas.
    - Historial.

---

## 🧱 Tecnologías

**Frontend**

- React + Vite  
- React Router  
- Clerk React SDK  
- CSS modular (sin framework pesado, estilo custom tipo “SaaS dark dashboard”)

**Backend**

- FastAPI (Python)  
- SQLAlchemy + SQLite (por defecto)  
- `uv` para gestión de entorno y dependencias  
- OpenAI API (modelos tipo `gpt-4o-mini`)

---

## 📂 Estructura del proyecto

QodeBoss/
backend/
server.py
src/
app.py
ai_generator.py
routes/
challenge.py
webhooks.py
database/
models.py
db.py
utils/
...
frontend/
index.html
vite.config.js
src/
App.jsx
App.css
layout/
Layout.jsx
Layout.css
challenge/
ChallengeGenerator.jsx
MCQChallenge.jsx
ChallengeGenerator.css
MCQChallenge.css
history/
HistoryPanel.jsx
auth/
ClerkProviderWithRoutes.jsx
AuthenticationPage.jsx

text

---

## ⚙️ Requisitos previos

- Node.js (LTS recomendado)  
- Python 3.10+  
- Cuenta de:
  - **OpenAI** (o proveedor compatible) para obtener una API key.
  - **Clerk** para autenticación (publishable key + secret key).

---

## 🚀 Cómo clonar y ejecutar Qode Boss

### 1. Clonar el repositorio

git clone https://github.com/misk0zz/QodeBoss.git
cd QodeBoss

text

---

### 2. Configurar y arrancar el backend (FastAPI)

1. Ir a la carpeta `backend`:

cd backend

text

2. Crear entorno con `uv` y sincronizar dependencias (si usas uv):

pip install uv
uv sync

text

> Si prefieres `pip`, instala las dependencias que estén en `pyproject.toml` / `requirements.txt`.

3. Crear archivo `.env` dentro de `backend/src/` (o donde lo uses) con tus claves:

OPENAI_API_KEY=tu_clave_de_openai
CLERK_SECRET_KEY=tu_clave_secreta_de_clerk

text

4. Lanzar el servidor:

python -m uv run .\server.py

text

El backend arrancará en `http://localhost:8000`.

---

### 3. Configurar y arrancar el frontend (React)

1. Abrir otra terminal y moverse a `frontend`:

cd ../frontend

text

2. Instalar dependencias:

npm install

text

3. Crear archivo `.env` en `frontend` (si se usa Vite con variables de Clerk):

VITE_CLERK_PUBLISHABLE_KEY=tu_publishable_key_de_clerk
VITE_API_BASE_URL=http://localhost:8000/api

text

4. Arrancar el dev server:

npm run dev

text

Vite te mostrará una URL como `http://localhost:5173/`.

---

### 4. Usar la aplicación

1. Abre `http://localhost:5173/` en tu navegador.
2. Regístrate / inicia sesión con Clerk.
3. En la página principal:
- Elige dificultad.
- Haz clic en **Generar reto**.
- Lee el enunciado y el código (si lo hay).
- Selecciona una respuesta y pulsa **Comprobar respuesta**.
4. Ve a la pestaña **Historial** para:
- Ver los retos que tú has generado.
- Hacer clic en cualquiera de ellos y revisarlo.

---

## 🔐 Seguridad y buenas prácticas

- Los archivos `.env` están en `.gitignore` y **no deben subirse** a GitHub.
- Si cambias de clave de OpenAI o Clerk, actualiza solo tus `.env` locales.
- El backend nunca expone las claves de OpenAI ni de Clerk al frontend.

---

## 🛠️ Personalización

Algunas ideas para extender Qode Boss:

- Guardar y mostrar la respuesta original de cada reto en el historial.
- Filtros por lenguaje, tema o etiqueta.
- Modo “examen” con límite de tiempo.
- Página pública con estadísticas (número de retos resueltos, racha diaria, etc.).

---

## 🤝 Contribuir

Si quieres abrir issues, sugerir mejoras o enviar PRs:

1. Haz un fork del repositorio.
2. Crea una rama para tu cambio:

git checkout -b feature/nueva-funcionalidad

text

3. Haz commit y push de tus cambios.
4. Abre un Pull Request describiendo qué has añadido o mejorado.

---

## 📄 Licencia

Puedes añadir aquí la licencia que prefieras (por ejemplo MIT) si decides hacer el proyecto open source.
