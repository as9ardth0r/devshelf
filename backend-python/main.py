from fastapi import FastAPI

app = FastAPI(
    title="DevShelf API",
    description="API backend pour la gestion des ressources DevShelf",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API de DevShelf"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
