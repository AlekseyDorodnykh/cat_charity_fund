from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractModel


class Donation(AbstractModel):
    """Модель пожертвования."""

    CLASS_REPR = 'от {user} {comment:.30}'

    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return self.CLASS_REPR.format(
            user=self.user_id, comment=self.comment
        )
