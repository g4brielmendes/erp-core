from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.module import Module
from app.schemas.module import ModuleCreate
from app.core.auth import get_current_user

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("/")
def create_module(
    dados: ModuleCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    module = Module(
        nome=dados.nome,
        url=dados.url,
        porta=dados.porta
    )

    db.add(module)
    db.commit()
    db.refresh(module)

    return module


@router.get("/")
def list_modules(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Module).all()