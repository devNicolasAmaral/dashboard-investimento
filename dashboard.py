import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime
from investimento import ler_transacoes, calcular_carteira, obter_precos_atuais, salvar_transacao, Transacao, validar_ticker


# Função auxiliar para corrigir formatação de valores
def formatar_br(valor):
    texto = f"R$ {valor:,.2f}"

    return texto.replace(",", "X").replace(".", ",").replace("X", ".")

@st.dialog("Novo Registro")
def open_modal_registro():
    tipo_op = st.radio("Qual operação você realizou?", ["Compra", "Venda"], horizontal=True)
    
    cor_destaque = "green" if tipo_op == "Compra" else "red"
    st.markdown(f"Preencha os dados da sua <span style='color:{cor_destaque}'><b>{tipo_op}</b></span>:", unsafe_allow_html=True)

    ticker_op = st.text_input("Ticker (ex: PETR4)").upper().strip()
    data_op = st.date_input("Data da Operação", datetime.now())
    qtde_op = st.number_input("Quantidade", min_value=1, step=1)
    preco_op = st.number_input("Preço Unitário (R$)", min_value=0.01, step=0.01, format="%.2f")
    
    if st.button("Salvar Registro", use_container_width=True):

        if not ticker_op:
            st.error("O Ticker é obrigatório.")
            return
        
        ticker_limpo = ticker_op.replace(".SA", "")
        
        if not validar_ticker(ticker_limpo):
            st.error(f"O ativo '{ticker_limpo}' não existe na B3.")
            return

        if tipo_op == "Venda":
            historico_atual = ler_transacoes()
            carteira_atual = calcular_carteira(historico_atual)
            
            qtd_em_maos = carteira_atual.get(ticker_limpo, {}).get('qtde', 0)
            
            if qtd_em_maos == 0:
                st.error(f"Você não tem {ticker_limpo} na carteira para vender.")
                return
            elif qtde_op > qtd_em_maos:
                st.error(f"Saldo insuficiente! Você tem {qtd_em_maos} e tentou vender {qtde_op}.")
                return

        tipo_codigo = "C" if tipo_op == "Compra" else "V"
        
        nova_transacao = Transacao(
            data=data_op,
            ticker=ticker_limpo,
            quantidade=qtde_op,
            preco=preco_op,
            tipo=tipo_codigo
        )
        
        salvar_transacao(nova_transacao)
        
        st.success("Salvo com sucesso!")
        import time
        time.sleep(0.5)
        st.rerun()

def formatar_pct(valor):
    return f"{valor:,.2f}%".replace(".", ",")

# --- Função Mestra de Estilização (Substitui a mini_metric) ---
def gerar_card_html(label, value, delta_str=None, delta_val=0, is_simple=False):
    """
    Gera um container Flexbox. O HTML está alinhado à esquerda
    para evitar que o Markdown interprete como bloco de código.
    """
    
    if delta_str:
        if delta_val > 0:
            cor = "#28a745" # Verde
            seta = "▲"
        elif delta_val < 0:
            cor = "#dc3545" # Vermelho
            seta = "▼"
        else:
            cor = "#b0b0b0" # Cinza
            seta = ""
        html_delta = f'<span style="font-size: 14px; font-weight: bold; color: {cor};">{seta} {delta_str}</span>'
    else:
        html_delta = "" 

    font_size_val = "20px" if is_simple else "24px"

    # ATENÇÃO: O código HTML abaixo está 'feio' (colado na esquerda) propositalmente.
    # Se você indentar as linhas do HTML, o Streamlit vai achar que é código e não vai funcionar.
    return f"""
<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 60px; width: 100%;">
<span style="font-size: {font_size_val}; font-weight: bold; color: white; line-height: 1.1;">{value}</span>
{html_delta}
</div>
"""

st.set_page_config(
    page_title = "Minha Carteira",
    layout = "wide"
)

# Função do modal de Compra e Venda

st.title("Dashboard de Investimentos")

# Botão que chama a função de compra e venda
col_titulo, col_botao = st.columns([4 , 1])

with col_botao:
    st.write("") 
    st.write("") 
    if st.button("Novo Registro", use_container_width=True):
        open_modal_registro()
#-----------------------------------------------

st.subheader("Visão Geral")

col1, col2, col3 = st.columns(3)

historico = ler_transacoes()

if not historico:
    st.warning("Sua carteira está vazia. Use o terminal para registrar operações.")
    st.stop()

carteira = calcular_carteira(historico)

tickers = list(carteira.keys())

with st.spinner(f"Baixando cotação de {len(tickers)} ativos..."):
    precos_atuais = obter_precos_atuais(tickers)

dados_tabela = []
total_investido = 0.0
total_atual = 0.0

for ticker, dados in carteira.items():
    qtde = dados['qtde']
    pm = dados['pm']

    preco_atual = precos_atuais.get(ticker, pm)

    val_investido = qtde * pm
    val_atual = qtde * preco_atual
    lucro_rs = val_atual - val_investido
    rentabilidade_pct = ((preco_atual / pm) - 1) * 100

    total_investido += val_investido
    total_atual += val_atual

    dados_tabela.append({
        "Ativo": ticker,
        "Quantidade": qtde,
        "Preço Médio": pm,
        "Preço Atual": preco_atual,
        "Total Atual": val_atual,
        "Lucro": lucro_rs,
        "Rentabilidade": rentabilidade_pct
    })

df = pd.DataFrame(dados_tabela)

lucro_total = total_atual - total_investido

if total_investido > 0:
    rentabilidade_geral = ((total_atual / total_investido) - 1) * 100
else:
    rentabilidade_geral = 0

col1.metric("Patrimônio Total", formatar_br(total_atual))
col2.metric("Custo de Aquisição", formatar_br(total_investido))

delta_formatado = f"{rentabilidade_geral:,.2f}%".replace(".", ",")
col3.metric(
    "Lucro / Prejuízo",
    formatar_br(lucro_total),
    delta_formatado
)

st.divider()
st.subheader("Distribuição da Carteira")

df["Label_Formatada"] = df["Total Atual"].apply(formatar_br)

fig = px.pie(
    df, 
    values="Total Atual", 
    names="Ativo",
    hole=0.4,
    custom_data=["Label_Formatada"]
)

fig.update_traces(
    hovertemplate="<b>%{label}</b><br>Valor: %{customdata[0]}<br>Representação: %{percent}"
)

st.plotly_chart(fig)

st.divider()
st.subheader("Detalhamento")

# --- Passo 1: Calcular a % na Carteira ---
# Criamos uma nova coluna no DataFrame para não ter que fazer conta dentro do visual
if total_atual > 0:
    df["% Carteira"] = (df["Total Atual"] / total_atual) * 100
else:
    df["% Carteira"] = 0.0

# --- Passo 2: Cabeçalho das 5 Colunas ---
# Usamos proporções (lista de números) em vez de um número inteiro
# Isso dá mais espaço para as colunas com métricas e menos para as simples
cols = st.columns([1.5, 1, 1.5, 1.5, 1])

cols = st.columns([1.5, 1, 1.2, 1.2, 1])

# Coluna 1: Esquerda (Texto)
cols[0].markdown("**Ativo / Qtde**")

# Colunas 2 a 5: Centralizadas (Números)
# Usamos HTML simples para forçar o centro nos títulos
cols[1].markdown("<div style='text-align: center;'><b>Preço Médio</b></div>", unsafe_allow_html=True)
cols[2].markdown("<div style='text-align: center;'><b>Preço Atual</b></div>", unsafe_allow_html=True)
cols[3].markdown("<div style='text-align: center;'><b>Patrimônio Atual</b></div>", unsafe_allow_html=True)
cols[4].markdown("<div style='text-align: center;'><b>% Carteira</b></div>", unsafe_allow_html=True)

st.divider()

# Loop de Exibição
for index, row in df.iterrows():
    
    c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1.2, 1.2, 1])
    
    with c1:
        # Coluna 1 (Texto/Ativo) - Flexbox manual para alinhar
        # Também removemos a indentação interna do HTML
        st.markdown(
f"""<div style="display: flex; flex-direction: column; justify-content: center; height: 60px;">
<span style='font-weight: bold; font-size: 20px; color: white;'>{row['Ativo']}</span>
<span style='font-size: 14px; color: #888;'>{row['Quantidade']} cotas</span>
</div>""", 
            unsafe_allow_html=True
        )
        
    with c2:
        # Coluna 2 (Preço Médio) - Simples
        html = gerar_card_html(
            label="PM", 
            value=formatar_br(row['Preço Médio']), 
            is_simple=True
        )
        st.markdown(html, unsafe_allow_html=True)
        
    with c3:
        # Coluna 3 (Cotação) - Completa
        html = gerar_card_html(
            label="Cotação",
            value=formatar_br(row['Preço Atual']),
            delta_str=f"{row['Rentabilidade']:,.2f}%".replace(".", ","),
            delta_val=row['Rentabilidade']
        )
        st.markdown(html, unsafe_allow_html=True)
        
    with c4:
        # Coluna 4 (Patrimônio) - Completa
        html = gerar_card_html(
            label="Total",
            value=formatar_br(row['Total Atual']),
            delta_str=formatar_br(row['Lucro']),
            delta_val=row['Lucro']
        )
        st.markdown(html, unsafe_allow_html=True)
        
    with c5:
        # Coluna 5 (% Carteira) - HTML direto sem indentação
        html = f"""
<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 60px;">
<span style="font-size: 20px; font-weight: bold;">{row['% Carteira']:,.2f}%</span>
</div>""".replace(".", ",")
        st.markdown(html, unsafe_allow_html=True)
    
    # Linha divisória
    st.markdown("---")