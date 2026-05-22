from pydantic import BaseModel

class ModuleCreate(BaseModel):
    nome: str
    url: str
    porta: int