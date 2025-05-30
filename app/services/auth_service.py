from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.user import User
from typing import Optional


class AuthService:
    @staticmethod
    def register(email: str, username: str, password: str) -> User:
        # implement business rules here
        # a user cannot register with already existing email
        # a user cannot register with already existing username

        if UserRepository.get_by_email(email):
            raise ValueError(
                f"Email '{email}' already exists. Please try another one.")

        if UserRepository.get_by_username(username):
            raise ValueError(
                f"Username '{username}' already exists. Please try another one.")

        user = UserRepository.create_user(email, username, password)

        # create a profile for the user along with user creation
        ProfileRepository.create(user.id)

        return user
