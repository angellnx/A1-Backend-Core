from typing import List, Any
from core_app.domain.models.transaction_type import TransactionType, TransactionTypeEnum

class TransactionTypeService:

    def __init__(self, repository: Any):
        # repository is expected to have create, find_all and find_by_id methods
        self.repository = repository

    def create_type(
        self,
        name: str,
        color: str,
        tipo: TransactionTypeEnum
    ) -> TransactionType:

        new_type = TransactionType(
            id=None,
            name=name,
            color=color,
            type=tipo
        )

        # ID assignment will happen inside the repository
        return self.repository.create(new_type)

    def list_types(self) -> List[TransactionType]:
        return self.repository.find_all()

    def get_type_by_id(self, id: int) -> TransactionType | None:
        return self.repository.find_by_id(id)
