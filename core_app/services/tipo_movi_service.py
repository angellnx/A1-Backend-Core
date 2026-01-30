from core_app.entities.tipo_movi import TipoMovi
from core_app.repositories.tipo_movi_repository import TipoMoviRepository

class TipoMoviService:

    def __init__(self):
        self._tipos: List[TipoMovi] = []
        self._id_counter = 1

    def criar_tipo(
        self,
        nome: str,
        cor: str,
        tipo: TipoMovimentacaoEnum
    ) -> TipoMovi:

        novo_tipo = TipoMovi(
            id_tipo_movi=self._id_counter,
            nome=nome,
            cor=cor,
            tipo=tipo
        )

        self._tipos.append(novo_tipo)
        self._id_counter += 1
        return novo_tipo

    def listar_tipos(self) -> List[TipoMovi]:
        return self._tipos

    def buscar_por_id(self, id_tipo_movi: int) -> TipoMovi | None:
        return next(
            (t for t in self._tipos if t.id_tipo_movi == id_tipo_movi),
            None
        )
