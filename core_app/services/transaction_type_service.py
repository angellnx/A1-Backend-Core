from typing import List
from core_app.domain.models.transaction_type import TransactionType, TransactionTypeEnum

class TransactionTypeService:

    def __init__(self):
        self._types: List[TransactionType] = []
        self._id_counter = 1

    def create_type(
        self,
        name: str,
        color: str,
        tipo: TransactionTypeEnum
    ) -> TransactionType:

        new_type = TransactionType(
            id=self._id_counter,
            name=name,
            color=color,
            type=tipo
        )

        self._types.append(new_type)
        self._id_counter += 1
        return new_type

    def list_types(self) -> List[TransactionType]:
        return self._types

    def get_type_by_id(self, id: int) -> TransactionType | None:
        return next(
            (t for t in self._types if t.id == id),
            None
        )
