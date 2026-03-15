from database import * 
from schemas import * 
from models import * 

from sqlalchemy import select


async def testing():
    async with create_async_session() as session:
        query = select(Expense).where(Expense.category == "Food").order_by(Expense.date.desc())
        result = await session.execute(query)
        # print(result.fetchall())
        # print(result.fetchall())
        output = [ExpenseRead.model_validate(exp).model_dump() for exp in result.scalars().all()]
        # output = [exp._asdict() for exp in result.scalars().all()]
        from pprint import pprint
        pprint(output)
        print(output)
        return output


import asyncio

asyncio.run(testing())