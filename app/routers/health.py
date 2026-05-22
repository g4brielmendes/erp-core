from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests

from app.core.deps import get_db
from app.models.module import Module

router = APIRouter(tags=["Health"])


@router.get("/health")
def health(db: Session = Depends(get_db)):

    modules = db.query(Module).filter(Module.ativo == True).all()

    services = {
        "core": "online"
    }

    for module in modules:

        try:
            response = requests.get(
                f"{module.url}:{module.porta}/health",
                timeout=3
            )

            if response.status_code == 200:
                services[module.nome] = "online"
            else:
                services[module.nome] = "offline"

        except:
            services[module.nome] = "offline"

    return {
        "status": "ok",
        "services": services
    }