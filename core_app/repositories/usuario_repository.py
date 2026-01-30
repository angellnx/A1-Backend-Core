from typing import List, Optional
from core_app.models.usuario import Usuario

usuarios_db: List[Usuario] = []

def add_usuario(usuario: Usuario):
    usuarios_db.append(usuario)
    return usuario

def get_usuarios():
    return usuarios_db

def get_usuario_by_id(usuario_id: int):
    for usuario in usuarios_db:
        if usuario.id == usuario_id:
            return usuario
    return None

def update_usuario(usuario_id: int) -> bool:
    for index, usuario in enumerate(usuarios_db):
        if usuario.id == usuario_id:
            usuarios_db[index] = usuario
            return True
    return False

def delete_usuario(usuario_id: int) -> bool:
    for index, usuario in enumerate(usuarios_db):
        if usuario.id == usuario_id:
            del usuarios_db[index]
            return True
    return False