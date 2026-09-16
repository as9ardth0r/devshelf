# DevShelf

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat&logo=rust&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)

DevShelf est une application pour centraliser et retrouver des ressources techniques et créatives, avec un moteur d'analyse et de recherche écrit en **Rust**, exposé à **Python** via [PyO3](https://pyo3.rs/), consommé par une API **FastAPI**, et affiché dans une interface **React**.

<!-- Ajoute une capture d'écran ou un GIF de démo ici -->

## 📐 Architecture

```
rust-core/       → Module Rust compilé en extension Python (PyO3 + maturin)
                    - analyse de texte (nombre de mots, temps de lecture, mots-clés)
                    - moteur de recherche pondéré (le titre compte plus que le contenu)
backend-python/   → API FastAPI, persistance SQLite (SQLModel)
                    - appelle directement le module Rust compilé
frontend/         → Interface React (Vite)
                    - liste, ajoute et recherche des ressources via l'API
```

Le module Rust n'est pas un module isolé : il est compilé en bibliothèque native (`.so`) importable directement en Python (`import rust_core`), et c'est lui qui calcule les métadonnées de chaque ressource ainsi que le classement de recherche — pas juste une démo qui tourne dans son coin.

## ⚡ Lancer le projet en local

### 1. Le cœur Rust (à compiler en premier)

```bash
cd rust-core
python3 -m venv ../venv
source ../venv/bin/activate
pip install maturin
maturin develop --release
```

Ceci compile `rust-core` et l'installe comme module Python (`rust_core`) directement dans l'environnement virtuel.

### 2. Le backend

```bash
cd ../backend-python
pip install -r requirements.txt
uvicorn main:app --reload
```

L'API est disponible sur `http://localhost:8000` (doc interactive sur `/docs`). La base SQLite (`devshelf.db`) est créée automatiquement au premier lancement.

### 3. Le frontend

```bash
cd ../frontend
npm install
npm run dev
```

L'interface est disponible sur `http://localhost:5173`.

## 🧪 Vérifier que tout fonctionne

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/resources/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Rust","category":"Backend","content":"Rust est rapide et sûr."}'
curl "http://localhost:8000/resources/search/?q=rust"
```

## 🧱 Stack technique

| Couche | Techno |
|---|---|
| Moteur d'analyse/recherche | Rust + PyO3 |
| API | Python (FastAPI + SQLModel) |
| Base de données | SQLite |
| Frontend | React (Vite) |

## 📄 Licence

MIT
