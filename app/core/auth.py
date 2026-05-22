from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os

from app.core.deps import get_db
from app.models.user import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado"
        )

    return user