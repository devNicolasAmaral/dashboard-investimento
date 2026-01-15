from sqlmodel import Session, select
from datetime import date, timedelta
from app.db.init_db import init_db
from app.db.session import engine
from app.models.transaction import Transaction
from app.models.earnings import Earnings

def create_fake_data():
    init_db() 
    
    with Session(engine) as session:
        existing = session.exec(select(Transaction)).first()
        if existing:
            print("O banco já possui dados. Pulando a injeção.")
            return

        print("Inserindo carteira fictícia...")
        
        # DATAS
        hoje = date.today()
        mes_passado = hoje - timedelta(days=30)
        ano_passado = hoje - timedelta(days=365)

        # DADOS
        transacoes = [
            Transaction(data=ano_passado, ticker="PETR4", quantidade=200, preco=28.50, tipo="C"),
            Transaction(data=mes_passado, ticker="VALE3", quantidade=100, preco=75.20, tipo="C"),
            Transaction(data=ano_passado, ticker="WEGE3", quantidade=150, preco=29.00, tipo="C"),
            Transaction(data=ano_passado, ticker="MXRF11", quantidade=500, preco=10.10, tipo="C"),
            Transaction(data=mes_passado, ticker="BBAS3", quantidade=100, preco=26.50, tipo="C"),
        ]

        proventos = [
            Earnings(data=mes_passado, ticker="PETR4", valor_total=350.00, tipo="DIV"),
            Earnings(data=hoje, ticker="PETR4", valor_total=120.00, tipo="JCP"),
            Earnings(data=mes_passado, ticker="MXRF11", valor_total=60.00, tipo="DIV"),
        ]

        # Adiciona e Salva
        session.add_all(transacoes)
        session.add_all(proventos)
        session.commit()
        print("Carteira criada com sucesso no PostgreSQL!")

if __name__ == "__main__":
    create_fake_data()