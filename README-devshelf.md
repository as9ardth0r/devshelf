# DevShelf

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat&logo=rust&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

DevShelf is an app for centralizing and finding technical and creative resources, powered by an analysis and search engine written in **Rust**, exposed to **Python** via [PyO3](https://pyo3.rs/), consumed by a **FastAPI** backend, and displayed in a **React** frontend.

🇬🇧 English (this page) | 🇫🇷 [Version française](README.fr.md)

<!-- Add a screenshot or demo GIF here -->

## 📐 Architecture

```
rust-core/       → Rust module compiled as a Python extension (PyO3 + maturin)
                    - text analysis (word count, reading time, keywords)
                    - weighted search engine (title matches score higher than body matches)
backend-python/   → FastAPI, SQLite persistence (SQLModel)
                    - calls the compiled Rust module directly
frontend/         → React interface (Vite)
                    - lists, adds and searches resources through the API
```

The Rust module isn't an isolated demo: it's compiled into a native library (`.so`) importable directly from Python (`import rust_core`), and it's the one computing each resource's metadata as well as the search ranking.

## ⚡ Running it locally

### 1. The Rust core (build this first)

```bash
cd rust-core
python3 -m venv ../venv
source ../venv/bin/activate
pip install maturin
maturin develop --release
```

This compiles `rust-core` and installs it as a Python module (`rust_core`) directly into the virtual environment.

### 2. The backend

```bash
cd ../backend-python
pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://localhost:8000` (interactive docs at `/docs`). The SQLite database (`devshelf.db`) is created automatically on first run.

### 3. The frontend

```bash
cd ../frontend
npm install
npm run dev
```

The interface is available at `http://localhost:5173`.

## 🧪 Sanity check

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/resources/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Rust test","category":"Backend","content":"Rust is fast and safe."}'
curl "http://localhost:8000/resources/search/?q=rust"
```

## 🧱 Tech stack

| Layer | Tech |
|---|---|
| Analysis / search engine | Rust + PyO3 |
| API | Python (FastAPI + SQLModel) |
| Database | SQLite |
| Frontend | React (Vite) |

## 📄 License

MIT
