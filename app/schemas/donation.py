from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreate(BaseModel):
    """Схема для создания пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extras = Extra.forbid
        schema_extra = {
            'example': {
                'comment': 'Лучшим котикам',
                'full_amount': 5000,
            }
        }


class DonationDB(DonationCreate):
    """Схема для возвращения пожертвования из БД."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationsDB(DonationDB):
    """Схема для возвращения всех пожертвований из БД."""
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
