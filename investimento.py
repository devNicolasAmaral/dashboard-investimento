from dataclasses import dataclass
from datetime import datetime
import csv
import os
import yfinance as yf
import contextlib

@dataclass
class Transacao:
    data: datetime
    ticker: str
    quantidade: int
    preco: float
    tipo: str

ARQUIVO_DADOS = "carteira.csv"

# Função para limpar o terminal
def limpar_tela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Função para salvar as transações em um arquivo CSV
def salvar_transacao(t: Transacao):
    arquivo_existe = os.path.isfile(ARQUIVO_DADOS)

    with open(ARQUIVO_DADOS, mode = 'a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)

        if not arquivo_existe:
            writer.writerow(['Data', 'Ticker', 'Quantidade', 'Preco', 'Tipo'])

        writer.writerow([t.data, t.ticker, t.quantidade, t.preco, t.tipo])
    
    print(f"Transação de {t.ticker.upper()} salva no disco com sucesso!")

# Função para ler as transações e retornar em seus tipos corretos
def ler_transacoes():
    lista_transacoes = []

    if not os.path.isfile(ARQUIVO_DADOS):
        return lista_transacoes
    
    with open(ARQUIVO_DADOS, mode = 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f) # Para usar o cabeçalho automaticamente

        for row in reader:
            t = Transacao(
                data=row['Data'],
                ticker=row['Ticker'],
                quantidade=int(row['Quantidade']),
                preco=float(row['Preco']),         
                tipo=row['Tipo']
            )
            lista_transacoes.append(t)

    return lista_transacoes

# Função para cálculo da posição e preço médio
def calcular_carteira(transacoes):
    carteira = {}

    for t in transacoes:
        ticker = t.ticker

        if ticker not in carteira:
            carteira[ticker] = {'qtde': 0, 'pm': 0.0}
        
        posicao = carteira[ticker]

        if t.tipo == 'C':
            total_atual = posicao['qtde'] * posicao['pm']
            total_novo = t.quantidade * t.preco
            nova_qtde = posicao['qtde'] + t.quantidade

            if nova_qtde > 0:
                novo_pm = (total_atual + total_novo) / nova_qtde
                posicao['pm'] = novo_pm
                posicao['qtde'] = nova_qtde
        elif t.tipo == 'V':
            posicao['qtde'] -= t.quantidade

    return {k: v for k, v in carteira.items() if v['qtde'] > 0}

# função para pegar os preços na B3 pelo yahoo finance 
def obter_precos_atuais(lista_tickers):
    print(f"Buscando cotações para: {lista_tickers}...")

    mapa_tickers = {f"{t}.SA": t for t in lista_tickers}

    tickers_yf = list(mapa_tickers.keys())
    try:
        dados = yf.download(tickers_yf, period = '1d', progress = False) ['Close']

        precos = {}

        if len(tickers_yf) == 1:
            ticker_sujo = tickers_yf[0]
            ticker_limpo = mapa_tickers[ticker_sujo]

            valor = float(dados.iloc[-1])
            precos[ticker_limpo] = valor
        else:
            ultima_linha = dados.iloc[-1]
            for ticker_sujo, valor in ultima_linha.items():
                if ticker_sujo in mapa_tickers:
                    ticker_limpo = mapa_tickers[ticker_sujo]
                    precos[ticker_limpo] = float(valor)

        return precos
    
    except Exception as e:
        print(f" Erro ao buscar dados: {e}")
        return {}

# Função para exibir o relatório
def exibir_relatorio(carteira):
    if not carteira:
        print("Carteira vazia.")
        return
    
    tickers = list(carteira.keys())

    precos_mercado = obter_precos_atuais(tickers)

    print("\n" + "=" * 60)
    print(f"{'ATIVO':<10} | {'QTDE':<6} | {'PM (R$)':<10} | {'ATUAL (R$)':<10} | {'LUCRO (R$)':<12}")
    print("-" * 60)

    total_investido = 0
    total_atual = 0

    for ticker, dados in carteira.items():
        qtde = dados['qtde']
        pm = dados['pm']

        preco_atual = precos_mercado.get(ticker, 0.0)

        valor_posicao_compra = qtde * pm
        valor_posicao_atual = qtde * preco_atual
        
        lucro_rs = valor_posicao_atual - valor_posicao_compra
        lucro_percent = ((preco_atual / pm) - 1) * 100 if pm > 0 else 0

        total_investido += valor_posicao_compra
        total_atual += valor_posicao_atual

        print(f"{ticker:<10} | {qtde:<6} | {pm:<10.2f} | {preco_atual:<10.2f} | {lucro_rs:>10.2f} ({lucro_percent:>6.2f}%)")

    print("-" * 60)
    print(f"TOTAL INVESTIDO: R$ {total_investido:,.2f}")
    print(f"PATRIMÔNIO HOJE: R$ {total_atual:,.2f}")
    
    lucro_total = total_atual - total_investido
    print(f"RESULTADO GERAL: R$ {lucro_total:,.2f}")
    print("="*60 + "\n")

# Função para validar a existencia de um ticker
def validar_ticker(ticker_limpo):
    print(f"Verificando {ticker_limpo} na B3...")

    ticker_sujo = f"{ticker_limpo}.SA"

    try:
        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            hist = yf.download(ticker_sujo, period = "1d", progress = False)

        if len(hist) > 0:
            return True
        else:
            return False
        
    except Exception:
        return False

# Função para Interface do Sistema
def solicitar_dados_operacao():
    print("\n--- Nova Operação ---")

    ticker = input("Digite o Ticker (ex: PETR4): ").strip().upper()
    ticker = ticker.replace(".SA", "")

    if not ticker or len(ticker) < 3 or ticker.isnumeric():
        print("Erro: Formato de ticker inválido.")
        input("Pressione [ENTER] para tentar novamente...")
        return None, None, None
    
    if not validar_ticker(ticker):
        print(f"Erro: O ativo '{ticker}' não foi encontrado na bolsa.")
        print("Dica: Verifique a digitação ou se é um ativo listado na B3.")
        input("Pressione [ENTER] para tentar novamente...")
        return None, None, None
    
    try:
        qtde = int(input(f"Quantidade de {ticker}: "))
        if qtde <= 0:
            print("A quantidade deve ser maior que zero.")
            input("Pressione [ENTER] para tentar novamente...")
            return None, None, None
        
        preco = float(input("Preço Unitário: "))
        if preco < 0:
            print("O preço não pode ser negativo.")
            input("Pressione [ENTER] para tentar novamente...")
            return None, None, None
        
    except ValueError:
        print("Erro: Quantidade deve ser número inteiro e o preço deve separar as casas decimais com ponto.")
        input("Pressione [ENTER] para tentar novamente...")
        return None, None, None

    return ticker, qtde, preco

if __name__ == "__main__":
    while True:
        limpar_tela()

        print("\n" + "=" * 40)
        print("     GESTOR DE INVESTIMENTOS (CLI)")
        print("=" * 40)
        print("[1] Registrar COMPRA")
        print("[2] Registrar VENDA")
        print("[3] Ver Carteira Atualizada")
        print("[4] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1" or opcao == "2":
            ticker, qtde, preco = solicitar_dados_operacao()

            if ticker:
                tipo_operacao = "C" if opcao == "1" else "V"

                nova_t = Transacao(
                    data = datetime.now(),
                    ticker = ticker, 
                    quantidade = qtde,
                    preco = preco,
                    tipo = tipo_operacao
                )

                salvar_transacao(nova_t)
                input("\n Pressione [ENTER] para continuar...")
        elif opcao == "3":
            print("\n Carregando dados do disco e da web...")

            historico = ler_transacoes()
            carteira = calcular_carteira(historico)

            limpar_tela()
            exibir_relatorio(carteira)
            
            input("\nPressione [ENTER] para voltar ao menu...")

        elif opcao == "4":
            print("Encerrando sistema. Bons investimentos!")
            break
        else:
            print("Opção inválida Digite 1, 2, 3 ou 4.")
    