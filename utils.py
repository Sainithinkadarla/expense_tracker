from schemas import ExpenseRead

async def list_of_objects_parser(result):
    expenses = result.scalars().all()
    return [ExpenseRead.model_validate(exp).model_dump() for exp in expenses]
