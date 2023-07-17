from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.core.constants import NAME_LENGTH


class CharityProjectCreate(BaseModel):
    """Схема для создания проекта благотворительности."""

    name: str = Field(..., max_length=NAME_LENGTH)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Дом для котиков',
                'description': 'Сбор средств на дом',
                'full_amount': 100000,
            }
        }


class CharityProjectUpdate(BaseModel):
    """Схема для обновления проекта благотворительности."""

    name: Optional[str] = Field(max_length=NAME_LENGTH)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1
        schema_extra = {
            'example': {
                'name': 'Кото_аптека',
                'description': 'Круглосуточная аптека для четвероногих',
                'full_amount': 70000,
            }
        }


class CharityProjectDB(CharityProjectCreate):
    """Схема для возвращения проекта благотворительности из БД."""

    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
