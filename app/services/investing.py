from datetime import datetime
from typing import List

from app.models.base import AbstractModel


def allocate_donations(
    target: AbstractModel,
    sources: List[AbstractModel],
) -> List[AbstractModel]:
    """Распределяет средства по благотворительным проектам."""
    results = []
    for source in sources:
        fund_to_allocate = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0),
        )
        for entity in source, target:
            entity.invested_amount = (
                entity.invested_amount or 0
            ) + fund_to_allocate
            if entity.full_amount == entity.invested_amount:
                entity.fully_invested = True
                entity.close_date = datetime.now()
        results.append(source)
        if target.fully_invested:
            break
    return results
