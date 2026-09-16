from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, select

import rust_core
from models import Resource, ResourceCreate, ResourceRead

DATABASE_URL = "sqlite:///./devshelf.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="DevShelf API",
    description="API backend pour la gestion des ressources DevShelf",
    version="1.0.0",
    lifespan=lifespan,
)

# Pour le dev local avec le frontend Vite (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_read_model(resource: Resource) -> ResourceRead:
    return ResourceRead(
        id=resource.id,
        title=resource.title,
        category=resource.category,
        content=resource.content,
        word_count=resource.word_count,
        reading_time_minutes=resource.reading_time_minutes,
        keywords=resource.keywords.split(",") if resource.keywords else [],
        created_at=resource.created_at,
    )


@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenue sur l'API de DevShelf"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/resources/", response_model=ResourceRead)
def create_resource(item: ResourceCreate):
    # Le module Rust calcule les métadonnées (nombre de mots, temps de
    # lecture, mots-clés) - c'est le vrai point d'intégration Python <-> Rust.
    analysis = rust_core.analyze_text(item.content)

    resource = Resource(
        title=item.title,
        category=item.category,
        content=item.content,
        word_count=analysis["word_count"],
        reading_time_minutes=analysis["reading_time_minutes"],
        keywords=",".join(analysis["keywords"]),
    )
    with Session(engine) as session:
        session.add(resource)
        session.commit()
        session.refresh(resource)
        return _to_read_model(resource)


@app.get("/resources/", response_model=list[ResourceRead])
def list_resources():
    with Session(engine) as session:
        resources = session.exec(select(Resource)).all()
        return [_to_read_model(r) for r in resources]


@app.get("/resources/{resource_id}", response_model=ResourceRead)
def get_resource(resource_id: int):
    with Session(engine) as session:
        resource = session.get(Resource, resource_id)
        if not resource:
            raise HTTPException(status_code=404, detail="Ressource introuvable")
        return _to_read_model(resource)


@app.get("/resources/search/", response_model=list[ResourceRead])
def search_resources(q: str):
    with Session(engine) as session:
        all_resources = session.exec(select(Resource)).all()

    # Le classement par pertinence est calculé côté Rust (voir rust-core/src/lib.rs).
    ranked = rust_core.search_resources(
        q, [(r.id, r.title, r.content) for r in all_resources]
    )
    resources_by_id = {r.id: r for r in all_resources}
    return [_to_read_model(resources_by_id[rid]) for rid, _score in ranked]
