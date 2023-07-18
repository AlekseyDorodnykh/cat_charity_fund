from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentModel


class Donation(InvestmentModel):
    """Модель пожертвования."""

    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        base_repr = super().__repr__()
        return f'{base_repr} от {self.user_id} {self.comment:.30}'
