from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import get_db
from ..schemas import UsersResponse, SignUp, EditUserModel
from sqlalchemy.orm import Session
from ..models import User
from ..utils import make_password
from sqlalchemy.exc import IntegrityError
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/", response_model=List[UsersResponse])
def get_users(db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    users = db.query(User).all()
    return users


@router.post("/sign-up", response_model=UsersResponse)
def signup(request: SignUp,  response: Response, db: Session = Depends(get_db)):
    hashed_password = make_password(request.password)
    new_user = User(email=request.email, password=hashed_password, name=request.name)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        response.status_code = status.HTTP_201_CREATED
        return new_user

    except Exception as error:
        if type(error) == IntegrityError:
            error = "Email already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.delete("/")
def delete_user(db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    email = current_user.email

    user = db.query(User).filter(User.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exists")
    user_name = user.first().name
    user.delete(synchronize_session=False)
    db.commit()
    message = f"User {user_name} is deleted"
    return {"message": message}


@router.put("/", response_model=UsersResponse)
def edit_user(request: EditUserModel, db: Session = Depends(get_db), current_user: UsersResponse = Depends(get_current_user)):
    email = current_user.email

    user = db.query(User).filter(User.email == email)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exists")

    user.update({"name": request.name})
    db.commit()
    return user.first()
