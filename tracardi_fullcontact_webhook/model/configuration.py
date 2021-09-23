from typing import Optional

from pydantic import BaseModel
from tracardi.domain.entity import Entity


class PII(BaseModel):
    email: Optional[str] = None
    twitter: Optional[str] = None


class Configuration(BaseModel):
    source: Entity
    pii: PII
