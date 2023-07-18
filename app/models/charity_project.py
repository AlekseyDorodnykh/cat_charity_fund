from sqlalchemy import Column, String, Text

from app.core import constants
from app.models.base import InvestmentModel


class CharityProject(InvestmentModel):
    """Модель для хранения информации о благотворительных проектах."""

    name = Column(String(constants.NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text)

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        base_repr = super().__repr__()
        return f'{base_repr} {self.name} {self.description:.30}'
