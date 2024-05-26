from typing import Optional

from sqlalchemy.orm import Session

from app.db.models import User


def get_user_by_id(
    *,
    user_id: int,
    session_db: Session
) -> Optional[User]:
    return session_db.query(User).get(user_id)


def get_user_by_username(
    *,
    username: str,
    session_db: Session
) -> Optional[User]:
    return session_db.query(User).filter(User.username == username).first()


def filter_user_active(
    *,
    user_id: int,
    session_db: Session
) -> Optional[User]:
    return session_db.query(User).filter(
        User.id == user_id, User.is_active == True
    ).first()
