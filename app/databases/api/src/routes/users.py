import os
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlmodel import Session, select

from ..models.user import User, UserUpdate
from ..models.address import Address

from ..clients.sqlite import engine


ROUTE_NAME = os.path.basename(__file__).replace(".py", "")

router = APIRouter(prefix=f"/{ROUTE_NAME}", tags=[ROUTE_NAME])


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/", response_model=User)
def create_user(user_data: User, session: Session = Depends(get_session)):
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    return session.exec(select(User).offset(skip).limit(limit)).all()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int = Path(..., title="The ID of the user to retrieve"), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_data: User, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)

    return user


@router.patch("/{user_id}", response_model=User)
def patch_user(user_id: int, user_data: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return user
