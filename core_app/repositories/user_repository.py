from typing import List, Optional
from core_app.domain.models.user import User

users_db: List[User] = []

def add_user(user: User):
    users_db.append(user)
    return user

def get_users() -> List[User]:
    return users_db

def get_user_by_id(user_id: int) -> Optional[User]:
    for user in users_db:
        if user.id == user_id:
            return user
    return None

def update_user(user_id: int, updated_user: User) -> bool:
    for index, user in enumerate(users_db):
        if user.id == user_id:
            users_db[index] = updated_user
            return True
    return False

def delete_user(user_id: int) -> bool:
    for index, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[index]
            return True
    return False
