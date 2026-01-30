from datetime import datetime
from core_app.entities.movimentacao import Movimentacao
from core_app.repositories.movimentacao_repository import MovimentacaoRepository

class MovimentacaoService:
    def __init__(self, repository: MovimentacaoRepository):
        self.repository = repository

    def create_movimentacao(
        self,
        usuario_id: int,
        item_id: int,
        tipo_movi: str,
        valor: float,
        data: datetime | None = None,
        anotacao: str | None = None
    ) -> Movimentacao:

        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")

        data_indicada = data if data else datetime.now()

        movimentacao = Movimentacao(
            usuario_id=usuario_id,
            item_id=item_id,
            tipo_movi=tipo_movi,
            valor=valor,
            data=data_indicada,
            anotacao=anotacao
        )

        return self.repository.create(movimentacao)

    def get_movimentacao_by_id(self, movimentacao_id: int) -> Movimentacao | None:
        return self.repository.find_by_id(movimentacao_id)

    def list_movimentacoes(self) -> list[Movimentacao]:
        return self.repository.find_all()

    def delete_movimentacao(self, movimentacao_id: int) -> None:
        mov = self.repository.find_by_id(movimentacao_id)
        if not mov:
            raise ValueError("Movimentação não encontrada")
        self.repository.delete(mov)
