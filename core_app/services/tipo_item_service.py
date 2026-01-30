from core_app.entities.tipo_item import TipoItem
from core_app.repositories.tipo_item_repository import TipoItemRepository

class TipoItemService:
    def __init__(self, repository: TipoItemRepository):
        self.repository = repository

    def create_tipo_item(self, nome: str, cor: str) -> TipoItem:
        if not nome:
            raise ValueError("Nome do tipo é obrigatório")
        if not cor:
            raise ValueError("Cor é obrigatória")

        tipo_item = TipoItem(
            nome=nome,
            cor=cor
        )

        return self.repository.create(tipo_item)

    def get_tipo_item_by_nome(self, nome: str) -> TipoItem | None:
        return self.repository.find_by_id(nome)

    def list_tipos_item(self) -> list[TipoItem]:
        return self.repository.find_all()

    def delete_tipo_item(self, nome: str) -> None:
        tipo = self.repository.find_by_id(nome)
        if not tipo:
            raise ValueError("Tipo de item não encontrado")
        self.repository.delete(tipo)
