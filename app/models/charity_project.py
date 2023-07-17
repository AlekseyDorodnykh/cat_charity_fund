from sqlalchemy import Column, String, Text

from app.core import constants
from app.models.base import AbstractModel


class CharityProject(AbstractModel):
    """Модель для хранения информации о благотворительных проектах."""
    CLASS_REPR = '{name} {description:.30}'

    name = Column(String(constants.NAME_LENGTH), unique=True, nullable=False)
    description = Column(Text)

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return self.CLASS_REPR.format(
            name=self.name, description=self.description
        )
