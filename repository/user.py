from poetry.console.commands import self
from sqlalchemy import insert, select
from sqlalchemy.orm import Session


from dataclasses import dataclass
from models import UserProfile

@dataclass
class UserRepository:
    db_session: Session

    def create_user(self, user_name: str, password: str, access_token:str) -> UserProfile:
        query = insert(UserProfile).values(
            user_name=user_name,
            password=password,
            access_token=access_token
        ).returning(UserProfile.id)
        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(user_id)

    def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile  | None:
        query = select(UserProfile).where(UserProfile.user_name == username)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()