from typing import List, Dict
from app.models.transaction import Transaction
from app.schemas.portfolio import PositionSummary

class CalculationService:
    
    @staticmethod
    def calculate_positions(transactions: List[Transaction]) -> List[PositionSummary]:
        """
        Recebe o histórico bruto de transações e calcula a posição atual (PM, Qtd).
        """
        carteira: Dict[str, dict] = {}
        
        # Garante ordem cronológica para o cálculo do PM ser exato
        lista_ordenada = sorted(transactions, key=lambda t: t.data)

        for t in lista_ordenada:
            ticker = t.ticker
            
            if ticker not in carteira:
                carteira[ticker] = {
                    'qtde': 0, 
                    'total_investido': 0.0, 
                    'pm': 0.0
                }
            
            posicao = carteira[ticker]

            if t.tipo == 'C':
                custo_compra = t.quantidade * t.preco
                posicao['total_investido'] += custo_compra
                posicao['qtde'] += t.quantidade
                
                # Recalcula Preço Médio Ponderado
                if posicao['qtde'] > 0:
                    posicao['pm'] = posicao['total_investido'] / posicao['qtde']
            
            elif t.tipo == 'V':
                custo_venda = t.quantidade * posicao['pm']
                posicao['total_investido'] -= custo_venda
                posicao['qtde'] -= t.quantidade
            
            # Limpeza se zerou a posição
            if posicao['qtde'] <= 0:
                posicao['qtde'] = 0
                posicao['total_investido'] = 0.0
                posicao['pm'] = 0.0

        # Converte o dicionário sujo em uma lista de Objetos Pydantic limpos
        resultados = []
        for ticker, dados in carteira.items():
            if dados['qtde'] > 0:
                resultados.append(PositionSummary(
                    ticker=ticker,
                    quantidade=dados['qtde'],
                    preco_medio=dados['pm'],
                    total_investido=dados['total_investido']
                ))
                
        return resultados