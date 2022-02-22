from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from ..schemas import Token
from sqlalchemy.orm import Session
from ..models import User
from ..utils import check_password
from ..token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@router.post("/", response_model=Token)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exists")

    if check_password(request.password, user.password):
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Password")
