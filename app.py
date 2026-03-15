from fastmcp import FastMCP, exceptions 
from contextlib import asynccontextmanager 


from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import create_all_tables, create_async_session
from schemas import ExpenseCreate, ExpenseRead, ExpensePartialUpdate
from models import Expense
from utils import list_of_objects_parser

@asynccontextmanager
async def lifespan(app: FastMCP):
    await create_all_tables()
    yield

app = FastMCP(lifespan=lifespan, name="Expense Tracker MCP")
# app = FastMCP(name="Expense Tracker MCP")

@app.tool
async def create_expense(expense_create: ExpenseCreate):
    """Creating a expense"""
    async with create_async_session() as session:
        expense = Expense(**expense_create.model_dump())
        session.add(expense)
        await session.commit()
        # return f"Expense created with id : {expense.id}"
        # return ExpenseRead(**expense.__dict__)
        return ExpenseRead.model_validate(expense).model_dump_json()
    
@app.tool
async def get_expenses_by_cat(category: str):
    """Get all expenses of that category"""
    async with create_async_session() as session:
        query = select(Expense).where(Expense.category == category)
        result = await session.execute(query)
        return await list_of_objects_parser(result=result)


@app.tool
async def get_expenses():
    """Get all expenses"""
    async with create_async_session() as session:
        query = select(Expense).order_by(Expense.date.desc())
        result = await session.execute(query)
        return await list_of_objects_parser(result=result)
    
@app.tool
async def get_between_dates(start_date: str, end_date: str):
    """Get expenses from between dates"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    async with create_async_session() as session:
        query = select(Expense).where(Expense.date.between(start, end))
        result = await session.execute(query)
        return await list_of_objects_parser(result=result)
    
@app.tool
async def get_exp_between_dates_with_category(start_date: str, end_date: str, category: str):
    "Get expenses from between dates of a category"
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    async with create_async_session() as session:
        query = select(Expense).where(and_(Expense.date.between(start, end), Expense.category == category))


if __name__ == "_main__":
    app.run()