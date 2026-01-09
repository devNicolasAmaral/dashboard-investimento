import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import yfinance as yf
import contextlib

DB_NAME = "investimentos.db"

def _conectar():
    return sqlite3.connect(DB_NAME)

def _criar_tabelas():
    conn = _conectar()
    cursor = conn.cursor()
   
    # Tabela de Transações (Compra/Venda)
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

    # NOVA TABELA: Proventos (Dividendos/JCP)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        ticker TEXT NOT NULL,
        valor_total REAL NOT NULL,
        tipo TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

_criar_tabelas()

@dataclass
class Transacao:
    data: datetime
    ticker: str
    quantidade: int
    preco: float
    tipo: str
    id: Optional[int] = None

@dataclass
class Provento:
    data: datetime
    ticker: str
    valor_total: float
    tipo: str # 'D' para Dividendo, 'J' for JCP
    id: Optional[int] = None

# Funções de Transações

def salvar_transacao(t: Transacao):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transacoes (data, ticker, quantidade, preco, tipo)
        VALUES (?, ?, ?, ?, ?)
    """, (str(t.data), t.ticker, t.quantidade, t.preco, t.tipo))
    conn.commit()
    conn.close()

def ler_transacoes():
    transacoes = []
    conn= _conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, ticker, quantidade, preco, tipo FROM transacoes ORDER BY data DESC")
    linhas = cursor.fetchall()
    for row in linhas:
        t = Transacao(id=row[0], data=row[1], ticker=row[2], quantidade=int(row[3]), preco=float(row[4]), tipo=row[5])
        transacoes.append(t)
    conn.close()
    return transacoes

def excluir_transacao(id_transacao):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id_transacao,))
    conn.commit()
    conn.close()

def atualizar_transacao(id_transacao, novo_ticker, nova_data, nova_qtde, novo_preco, novo_tipo):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transacoes SET ticker = ?, data = ?, quantidade = ?, preco = ?, tipo = ? WHERE id = ?
    """, (novo_ticker, str(nova_data), nova_qtde, novo_preco, novo_tipo, id_transacao))
    conn.commit()
    conn.close()

# Funções de Proventos

def salvar_provento(p: Provento):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO proventos (data, ticker, valor_total, tipo)
        VALUES (?, ?, ?, ?)
    """, (str(p.data), p.ticker, p.valor_total, p.tipo))
    conn.commit()
    conn.close()

def ler_proventos():
    proventos = []
    conn= _conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, data, ticker, valor_total, tipo FROM proventos ORDER BY data DESC")
    linhas = cursor.fetchall()
    for row in linhas:
        p = Provento(id=row[0], data=row[1], ticker=row[2], valor_total=float(row[3]), tipo=row[4])
        proventos.append(p)
    conn.close()
    return proventos

def excluir_provento(id_provento):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proventos WHERE id = ?", (id_provento,))
    conn.commit()
    conn.close()

# Funções de Cálculo e API

def calcular_carteira(transacoes):
    carteira = {}
    lista_ordenada = sorted(transacoes, key=lambda x: x.data)

    for t in lista_ordenada:
        ticker = t.ticker
        if ticker not in carteira:
            carteira[ticker] = {'qtde': 0, 'pm': 0.0, 'total_investido': 0.0}
        posicao = carteira[ticker]

        if t.tipo == 'C':
            total_novo = t.quantidade * t.preco
            posicao['total_investido'] += total_novo
            posicao['qtde'] += t.quantidade
            if posicao['qtde'] > 0:
                posicao['pm'] = posicao['total_investido'] / posicao['qtde']
        elif t.tipo == 'V':
            custo_venda = t.quantidade * posicao['pm']
            posicao['total_investido'] -= custo_venda
            posicao['qtde'] -= t.quantidade
        
        if posicao['qtde'] == 0:
            posicao['pm'] = 0.0
            posicao['total_investido'] = 0.0

    return {k: v for k, v in carteira.items() if v['qtde'] > 0}

def obter_precos_atuais(lista_tickers):
    if not lista_tickers: return {}
    mapa_tickers = {f"{t}.SA": t for t in lista_tickers}
    tickers_yf = list(mapa_tickers.keys())
    try:
        dados = yf.download(tickers_yf, period='1d', progress=False)['Close']
        precos = {}
        if len(tickers_yf) == 1:
            try: valor = float(dados.iloc[-1])
            except: valor = float(dados.iloc[-1].iloc[0])
            precos[mapa_tickers[tickers_yf[0]]] = valor
        else:
            ultima_linha = dados.iloc[-1]
            for ticker_sujo, valor in ultima_linha.items():
                if ticker_sujo in mapa_tickers:
                    precos[mapa_tickers[ticker_sujo]] = float(valor)
        return precos
    except Exception:
        return {}
    
def validar_ticker(ticker_limpo):
    ticker_sujo = f"{ticker_limpo}.SA"
    try:
        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            hist = yf.download(ticker_sujo, period='1d', progress=False)
        return len(hist) > 0
    except:
        return False