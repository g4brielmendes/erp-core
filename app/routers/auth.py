from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.deps import get_db
from app.core.security import hash_senha

from app.schemas.auth import Login
from app.core.security import verificar_senha, criar_token

from app.core.auth import get_current_user

from app.models.refresh_token import RefreshToken
from datetime import datetime, timedelta
from app.core.security import criar_refresh_token

from fastapi import HTTPException

from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )

    db_user = User(
        nome=user.nome,
        email=user.email,
        senha_hash=hash_senha(user.senha),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "msg": "Usuário criado com sucesso"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuário desativado"
        )

    if not verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    access_token = criar_token({
        "sub": user.email,
        "role": user.role
    })

    refresh_token = criar_refresh_token({
        "sub": user.email,
        "role": user.role
    })

    db_refresh = RefreshToken(
        user_id=user.id,
        refresh_token=refresh_token,
        expira_em=datetime.utcnow() + timedelta(days=7)
    )

    db.add(db_refresh)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
@router.get("/verify")
def verify(user = Depends(get_current_user)):
    return {
    "valid": True,
    "user": {
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "role": user.role
    }
}

@router.get("/private")
def private(user = Depends(get_current_user)):
    return {"msg": "Você está autenticado", "user": user}

@router.post("/refresh")
def refresh(token: str, db: Session = Depends(get_db)):

    db_token = db.query(RefreshToken).filter(
        RefreshToken.refresh_token == token
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token inválido"
        )

    if db_token.expira_em < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Refresh token expirado"
        )

    user = db.query(User).filter(User.id == db_token.user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    new_access = criar_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": new_access
    }