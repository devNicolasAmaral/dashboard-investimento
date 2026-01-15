from pydantic import BaseModel

class PositionSummary(BaseModel):
    ticker: str
    quantidade: int
    preco_medio: float
    total_investido: float
    
    preco_atual: float = 0.0
    valor_total_atual: float = 0.0
    rentabilidade_pct: float = 0.0
    lucro_prejuizo: float = 0.0
    percentual_carteira: float = 0.0