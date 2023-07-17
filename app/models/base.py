from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core import constants
from app.core.db import Base


class AbstractModel(Base):
    """Базовый  абстрактный класс."""

    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            'invested_amount <= full_amount',
            name='check_invested_amount_not_exceed_full_amount',
        ),
    )

    full_amount = Column(Integer)
    invested_amount = Column(
        Integer, default=constants.DEFAULT_INVESTED_AMOUNT
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)


    def __repr__(self):
        return super().__repr__()
