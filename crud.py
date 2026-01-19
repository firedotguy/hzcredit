from sqlalchemy.orm import Session

from models.user import User
from logger import get_logger

l = get_logger()


def get_user(db: Session, user_id: int) -> User | None:
    l.info('get user user_id=%s', user_id)
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, name: str, user_id: int) -> User:
    l.info('create user user_id=%s name=%s', user_id, name)
    user = User(
        name=name,
        user_id=user_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    l.debug('user created id=%s', user.id)
    return user