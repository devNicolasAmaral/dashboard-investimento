from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel

class Transaction(SQLModel, table=True):
    __tablename__ = "transacoes" 

    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True) 
    data: date
    quantidade: int
    preco: float
    tipo: str  # "C" ou "V"