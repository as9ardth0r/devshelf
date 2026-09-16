from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="DevShelf API",
    description="API backend pour la gestion des ressources DevShelf",
    version="1.0.0",
)


class ResourceItem(BaseModel):
    title: str
    category: str
    content: str


@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API de DevShelf"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/resources/")
def create_resource(item: ResourceItem):
    return {
        "status": "success",
        "message": "Ressource enregistrée avec succès",
        "data": item,
    }
