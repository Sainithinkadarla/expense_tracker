from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ExpenseBase(BaseModel):
    amount: float 
    date: datetime = Field(default=datetime.now())
    note: str
    category: str
    sub_category: str | None = None

    model_config = ConfigDict(from_attributes = True)

class ExpenseRead(ExpenseBase):
    id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpensePartialUpdate(BaseModel):
    date: datetime | None = None
    amount: float | None = None
    note: str | None = None
    category: str | None = None
    sub_category: str | None = None