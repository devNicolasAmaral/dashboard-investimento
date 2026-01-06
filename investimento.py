import sqlite3
from dataclasses import dataclass
from datetime import datetime
import yfinance as yf
import contextlib

DB_NAME = "investimentos.db"

def _conectar():
    return sqlite3.connect(DB_NAME)

def _criar_tabelas():
    conn = _conectar()
    cursor = conn.cursor()
   
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        ticker TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Executa a criação da tabela quando esse módulo é importado pelo dashboard
_criar_tabelas()

@dataclass
class Transacao:
    data: datetime
    ticker: str
    quantidade: int
    preco: float
    tipo: str

def salvar_transacao(t: Transacao):
    conn = _conectar()
    cursor = conn.cursor()

    # Como o SQLite não tem tipo para data, padronizei como texto ISO (YYYY-MM-DD)
    # para queo "ORDER BY DATA" funcione
    if isinstance(t.data, (datetime, float)):
        data_str = str(t.data)
    else:
        # Se vier do st.date_input (objeto date), o str() já converte para o formato certo
        data_str = str(t.data)

    cursor.execute("""
        INSERT INTO transacoes (data, ticker, quantidade, preco, tipo)
        VALUES (?, ?, ?, ?, ?)
    """, (data_str, t.ticker, t.quantidade, t.preco, t.tipo))

    conn.commit()
    conn.close()

    print(f"Log: {t.tipo} de {t.ticker} registrada no Banco de Dados")

def ler_transacoes():
    transacoes = []
    conn= _conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT data, ticker, quantidade, preco, tipo FROM transacoes ORDER BY data ASC")
    linhas = cursor.fetchall()

    for row in linhas:
        t = Transacao(
            data=row[0],
            ticker=row[1],
            quantidade = int(row[2]),
            preco = float(row[3]),
            tipo = row[4] 
        )

        transacoes.append(t)
    
    conn.close()
    return transacoes

def calcular_carteira(transacoes):
    carteira = {}

    for t in transacoes:
        ticker = t.ticker

        if ticker not in carteira:
            carteira[ticker] = {'qtde': 0, 'pm': 0.0, 'total_investido': 0.0}

        posicao = carteira[ticker]

        if t.tipo == 'C':
            # Na compra: Aumenta quantidade e recalculamos o preço médio (pm).
            total_novo = t.quantidade * t.preco
            posicao['total_investido'] += total_novo
            posicao['qtde'] += t.quantidade

            if posicao['qtde'] > 0:
                posicao['pm'] = posicao['total_investido'] / posicao['qtde']
        elif t.tipo == 'V':
            # Na venda: Diminui quantidade e abate o valor investido.
            # O pm não muda na venda.
            custo_venda = t.quantidade * posicao['pm']
            posicao['total_investido'] -= custo_venda
            posicao['qtde'] -= t.quantidade

        # Se zerou a posição, reseta valores para evitar erros de arredondamento
        if posicao['qtde'] == 0:
            posicao['pm'] = 0.0
            posicao['total_investido'] = 0.0

    # Filtro  para retornar só quem tem saldo positivo.
    return {k: v for k, v in carteira.items() if v['qtde'] > 0}
    
# Busca cotação em lote no Yahoo Finance (Integração com API)    
def obter_precos_atuais(lista_tickers):
    if not lista_tickers:
        return {}
    
    # O Yahoo precisa do sufixo .SA para ações brasileiras
    mapa_tickers = {f"{t}.SA": t for t in lista_tickers}
    tickers_yf = list(mapa_tickers.keys())

    try:
        # period='1d' pega o último fechamento disponível,
        dados = yf.download(tickers_yf, period = '1d', progress = False) ['Close']
        precos = {}

        # O Pandas muda o formato se for 1 ativo (Series) ou vários (DataFrame)
        if len(tickers_yf) == 1:
            try:
                # Tenta pegar o valor direto
                valor = float(dados.iloc[-1])
            except:
                # Fallback: as vezes o yfinance devolve um DataFrame de 1 célula
                valor = float(dados.iloc[-1].iloc[0])
            
            ticker_limpo = mapa_tickers[tickers_yf[0]]
            precos[ticker_limpo] = valor
        else:
            # Loop para pegar a última linha de cada coluna
            ultima_linha = dados.iloc[-1]
            for ticker_sujo, valor in ultima_linha.items():
                if ticker_sujo in mapa_tickers:
                    ticker_limpo = mapa_tickers[ticker_sujo]
                    precos[ticker_limpo] = float(valor)
        
        return precos
    except Exception as e:
        print(f"erro na APT Yahoo Finance {e}")
        return {}
    
# Verifica se o ticker existe na B3 antes de deixar salvar.    
def validar_ticker(ticker_limpo):
    ticker_sujo = f"{ticker_limpo}.SA"
    try:
        # contextlib para esconder logs do yfinance
        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            hist = yf.download(ticker_sujo, period= '1d', progress = False)
        return len(hist) > 0
    except Exception:
        return False
