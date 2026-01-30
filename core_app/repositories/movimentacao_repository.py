from typing import List, Optional
from core_app.domain.models.movimentacao import Movimentacao

movimentacoes_db: List[Movimentacao] = []

def add_movimentacao(mov: Movimentacao) -> Movimentacao:
    movimentacoes_db.append(mov)
    return mov

def get_movimentacoes() -> List[Movimentacao]:
    return movimentacoes_db

def get_movimentacao_by_id(mov_id: int) -> Optional[Movimentacao]:
    for mov in movimentacoes_db:
        if mov.id_movimentacao == mov_id:
            return mov
    return None

def update_movimentacao(mov_id: int, updated_mov: Movimentacao) -> Optional[Movimentacao]:
    for index, mov in enumerate(movimentacoes_db):
        if mov.id_movimentacao == mov_id:
            movimentacoes_db[index] = updated_mov
            return updated_mov
    return None

def delete_movimentacao(mov_id: int) -> bool:
    for index, mov in enumerate(movimentacoes_db):
        if mov.id_movimentacao == mov_id:
            movimentacoes_db.pop(index)
            return True
    return False
