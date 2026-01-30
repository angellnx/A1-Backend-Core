# core_app/services/usuario_service.py

from core_app.entities.usuario import Usuario
from core_app.repositories.usuario_repository import UsuarioRepository

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def create_usuario(self, email: str, username: str, nome: str, senha: str, telefone: str | None = None) -> Usuario:
        if not email:
            raise ValueError("Email é obrigatório")
        if not username:
            raise ValueError("Username é obrigatório")
        if not nome:
            raise ValueError("Nome do usuário é obrigatório")
        if not senha:
            raise ValueError("Senha é obrigatória")
        if not telefone:
            raise ValueError("Telefone é obrigatório")

        usuario = Usuario(
            email=email,
            username=username,
            nome=nome,
            senha=senha,
            telefone=telefone
        )

        return self.repository.create(usuario)

    def get_usuario_by_id(self, usuario_id: int) -> Usuario | None:
        return self.repository.find_by_id(usuario_id)

    def list_usuarios(self) -> list[Usuario]:
        return self.repository.find_all()

    def delete_usuario(self, usuario_id: int) -> None:
        usuario = self.repository.find_by_id(usuario_id)

        if not usuario:
            raise ValueError("Usuário não encontrado")

        self.repository.delete(usuario)
