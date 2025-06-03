from dataclasses import dataclass

from repository import UserRepository
from schema import UserLoginSchema
from service.auth import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    def create_user(self, user_name: str, password: str) -> UserLoginSchema:
        user = self.user_repository.create_user(user_name=user_name, password=password)
        access_token = self.auth_service.generate_access_token(user_id = user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

