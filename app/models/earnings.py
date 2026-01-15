from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Earnings(SQLModel, table=True):
    __tablename__ = "proventos"

    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True)
    data: date
    valor_total: float
    tipo: str  # "DIV" ou "JCP"