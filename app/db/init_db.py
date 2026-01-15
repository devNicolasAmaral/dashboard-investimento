from sqlmodel import SQLModel
from app.db.session import engine

from app.models.transaction import Transaction
from app.models.earnings import Earnings

def init_db():
    print("Criando tabelas no banco de dados...")

    SQLModel.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")