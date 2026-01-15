from sqlmodel import Session, select
from app.db.session import engine
from app.models.transaction import Transaction
from app.services.portfolio import CalculationService

def testar_cerebro():
    print("Iniciando teste de lógica financeira...")
    
    with Session(engine) as session:
        # Busca dados brutos no Postgres
        statement = select(Transaction)
        transacoes = session.exec(statement).all()
        print(f"-> Encontradas {len(transacoes)} transações no banco.")
        
        # Processa através do Service
        posicoes = CalculationService.calculate_positions(transacoes)
        
        # Exibe o resultado
        print("\nCarteira")
        print(f"{'TICKER':<10} | {'QTD':<5} | {'PM (R$)':<10} | {'INVESTIDO (R$)':<15}")
        print("-" * 50)
        
        total_investido = 0
        for p in posicoes:
            print(f"{p.ticker:<10} | {p.quantidade:<5} | {p.preco_medio:<10.2f} | {p.total_investido:<15.2f}")
            total_investido += p.total_investido
            
        print("-" * 50)
        print(f"TOTAL: R$ {total_investido:,.2f}")

if __name__ == "__main__":
    testar_cerebro()