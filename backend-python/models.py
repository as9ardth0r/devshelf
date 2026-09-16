from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ResourceBase(SQLModel):
    title: str
    category: str
    content: str


class Resource(ResourceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word_count: int = 0
    reading_time_minutes: float = 0.0
    keywords: str = ""  # stocké comme "mot1,mot2,mot3"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ResourceCreate(ResourceBase):
    pass


class ResourceRead(ResourceBase):
    id: int
    word_count: int
    reading_time_minutes: float
    keywords: list[str]
    created_at: datetime
