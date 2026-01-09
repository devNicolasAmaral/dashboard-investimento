import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
from investimento import (
    ler_transacoes, calcular_carteira, obter_precos_atuais, salvar_transacao, 
    Transacao, validar_ticker, excluir_transacao, atualizar_transacao,
    salvar_provento, ler_proventos, excluir_provento, Provento
)

st.set_page_config(page_title="Minha Carteira", layout="wide")

# Funções Visuais
def formatar_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Função auxiliar para mini cards na tabela
def gerar_card_html(label, value, delta_str=None, delta_val=0, is_simple=False):
    if delta_str:
        cor = "#28a745" if delta_val > 0 else "#dc3545" if delta_val < 0 else "#b0b0b0"
        seta = "▲" if delta_val > 0 else "▼" if delta_val < 0 else ""
        html_delta = f'<span style="font-size: 14px; font-weight: bold; color: {cor};">{seta} {delta_str}</span>'
    else:
        html_delta = "" 

    font_size_val = "20px" if is_simple else "24px"
    
    return f"""
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 60px; width: 100%;">
        <span style="font-size: {font_size_val}; font-weight: bold; color: white; line-height: 1.1;">{value}</span>
        {html_delta}
    </div>
    """

# Transação ou Provento
@st.dialog("Novo Registro")
def open_modal_registro():
    # Abas para separar o tipo de registro
    tab1, tab2 = st.tabs(["Negociação (Compra/Venda)", "Proventos (Div/JCP)"])
    
    # Compra e venda
    with tab1:
        tipo_op = st.radio("Operação", ["Compra", "Venda"], horizontal=True)
        cor_destaque = "green" if tipo_op == "Compra" else "red"
        st.markdown(f"Registrar <span style='color:{cor_destaque}'><b>{tipo_op}</b></span>:", unsafe_allow_html=True)

        t_ticker = st.text_input("Ticker", key="t_ticker").upper().strip()
        t_data = st.date_input("Data", datetime.now(), key="t_data")
        t_qtde = st.number_input("Quantidade", min_value=1, step=1, key="t_qtde")
        t_preco = st.number_input("Preço Unitário (R$)", min_value=0.01, step=0.01, format="%.2f", key="t_preco")
        
        if st.button("Salvar Negociação", use_container_width=True):
            if not t_ticker:
                st.error("Ticker obrigatório.")
                return
            
            ticker_limpo = t_ticker.replace(".SA", "")
            if not validar_ticker(ticker_limpo):
                st.error("Ativo não encontrado.")
                return

            if tipo_op == "Venda":
                carteira_atual = calcular_carteira(ler_transacoes())
                qtd_em_maos = carteira_atual.get(ticker_limpo, {}).get('qtde', 0)
                if t_qtde > qtd_em_maos:
                    st.error(f"Venda maior que saldo ({qtd_em_maos}).")
                    return

            tipo_cod = "C" if tipo_op == "Compra" else "V"
            nova_t = Transacao(data=t_data, ticker=ticker_limpo, quantidade=t_qtde, preco=t_preco, tipo=tipo_cod)
            salvar_transacao(nova_t)
            st.success("Negociação salva!")
            time.sleep(0.5)
            st.rerun()

    # Proventos
    with tab2:
        st.markdown("Registrar <span style='color:#FFD700'><b>Recebimento</b></span>:", unsafe_allow_html=True)
        
        tipo_prov = st.radio("Tipo", ["Dividendo", "JCP"], horizontal=True)
        p_ticker = st.text_input("Ticker", key="p_ticker").upper().strip()
        p_data = st.date_input("Data Pagamento", datetime.now(), key="p_data")
        p_valor = st.number_input("Valor TOTAL Recebido (R$)", min_value=0.01, step=0.01, format="%.2f", help="Coloque o valor total que caiu na conta, não o valor por cota.")
        
        if st.button("Salvar Provento", use_container_width=True):
            if not p_ticker:
                st.error("Ticker obrigatório.")
                return
            
            ticker_limpo = p_ticker.replace(".SA", "")
            # Valida o ticker para proventos
            if not validar_ticker(ticker_limpo):
                st.error("Ativo não encontrado.")
                return
                
            tipo_cod = "DIV" if tipo_prov == "Dividendo" else "JCP"
            novo_p = Provento(data=p_data, ticker=ticker_limpo, valor_total=p_valor, tipo=tipo_cod)
            salvar_provento(novo_p)
            st.success("Provento registrado!")
            time.sleep(0.5)
            st.rerun()

# Header e Botão
st.title("Dashboard de Investimentos")
c_tit, c_btn = st.columns([4, 1])
with c_btn:
    st.write("")
    st.write("")
    if st.button("Novo Registro", use_container_width=True):
        open_modal_registro()

# Leitura de dados
transacoes = ler_transacoes()
proventos = ler_proventos()

if not transacoes and not proventos:
    st.warning("Carteira vazia. Adicione um registro.")
    st.stop()

carteira = calcular_carteira(transacoes)
tickers = list(carteira.keys())

with st.spinner("Atualizando cotações..."):
    precos_atuais = obter_precos_atuais(tickers)

# Processamento Tabela Principal
dados_tabela = []
total_investido = 0.0
total_atual = 0.0

for ticker, dados in carteira.items():
    qtde = dados['qtde']
    pm = dados['pm']
    preco_atual = precos_atuais.get(ticker, pm)
    
    val_investido = qtde * pm
    val_atual = qtde * preco_atual
    
    total_investido += val_investido
    total_atual += val_atual
    
    lucro = val_atual - val_investido
    rent = ((preco_atual/pm)-1)*100 if pm > 0 else 0
    
    dados_tabela.append({
        "Ativo": ticker,
        "Quantidade": qtde,
        "Preço Médio": pm,
        "Preço Atual": preco_atual,
        "Total Atual": val_atual,
        "Lucro": lucro,
        "Rentabilidade": rent
    })

df = pd.DataFrame(dados_tabela)

# Cálculos Gerais
lucro_patrimonial = total_atual - total_investido
rent_geral = ((total_atual/total_investido)-1)*100 if total_investido > 0 else 0

if total_atual > 0:
    df["% Carteira"] = (df["Total Atual"] / total_atual) * 100
else:
    df["% Carteira"] = 0.0

# Cálculo de Proventos
total_proventos = sum(p.valor_total for p in proventos)

lucro_com_proventos = lucro_patrimonial + total_proventos

st.subheader("Visão Geral")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Patrimônio", formatar_br(total_atual))
kpi2.metric("Investido", formatar_br(total_investido))
kpi3.metric("Proventos Recebidos", formatar_br(total_proventos), delta=None)

# O KPI de Resultado mostra o lucro total (Valorização + Dividendos)
kpi4.metric(
    "Resultado Global", 
    formatar_br(lucro_com_proventos), 
    delta=f"{(lucro_com_proventos/total_investido)*100:.2f}%" if total_investido > 0 else None
)

st.divider()

# Gráfico
st.subheader("Distribuição")
if not df.empty:
    fig = px.pie(df, values="Total Atual", names="Ativo", hole=0.4)
    st.plotly_chart(fig)

# Tabela detalhada
st.subheader("Detalhamento")
cols = st.columns([1.5, 1, 1.2, 1.2, 1])
cols[0].markdown("**Ativo / Qtde**")
cols[1].markdown("<div style='text-align: center;'><b>Preço Médio</b></div>", unsafe_allow_html=True)
cols[2].markdown("<div style='text-align: center;'><b>Preço Atual</b></div>", unsafe_allow_html=True)
cols[3].markdown("<div style='text-align: center;'><b>Patrimônio Atual</b></div>", unsafe_allow_html=True)
cols[4].markdown("<div style='text-align: center;'><b>% Carteira</b></div>", unsafe_allow_html=True)
st.divider()

for _, row in df.iterrows():
    c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1.2, 1.2, 1])
    with c1:
        st.markdown(f"<div style='font-weight:bold; font-size:20px; margin-top:5px;'>{row['Ativo']}</div>", unsafe_allow_html=True)
        st.caption(f"{row['Quantidade']} cotas")
    with c2:
        st.markdown(gerar_card_html("PM", formatar_br(row['Preço Médio']), is_simple=True), unsafe_allow_html=True)
    with c3:
        st.markdown(gerar_card_html("Cotação", formatar_br(row['Preço Atual']), f"{row['Rentabilidade']:,.2f}%", row['Rentabilidade']), unsafe_allow_html=True)
    with c4:
        st.markdown(gerar_card_html("Total", formatar_br(row['Total Atual']), formatar_br(row['Lucro']), row['Lucro']), unsafe_allow_html=True)
    with c5:
        st.markdown(f"<div style='text-align:center; margin-top:15px; font-weight:bold; font-size:18px;'>{row['% Carteira']:,.2f}%</div>", unsafe_allow_html=True)
    st.markdown("---")

# Históricos
c_hist1, c_hist2 = st.columns(2)

# Histórico de proventos
with c_hist1:
    st.subheader("Histórico de Proventos")
    if proventos:
        dados_prov = [{"Data": pd.to_datetime(p.data).date(), "Ticker": p.ticker, "Valor": p.valor_total, "Tipo": p.tipo, "ID": p.id, "Excluir": False} for p in proventos]
        df_prov = pd.DataFrame(dados_prov)
        
        editor_prov = st.data_editor(
            df_prov, 
            hide_index=True, 
            column_config={
                "ID": None,
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                "Excluir": st.column_config.CheckboxColumn("Excluir?")
            },
            key="editor_proventos"
        )
        
        if st.button("Salvar Exclusões (Proventos)"):
            mudou = False
            for _, row in editor_prov.iterrows():
                if row["Excluir"]:
                    excluir_provento(row["ID"])
                    mudou = True
            if mudou:
                st.rerun()
    else:
        st.info("Nenhum provento registrado.")

# Histórico de negociação
with c_hist2:
    st.subheader("Histórico de Negociações")
    if transacoes:
        dados_neg = [{"Data": pd.to_datetime(t.data).date(), "Ticker": t.ticker, "Op": t.tipo, "Qtd": t.quantidade, "Preço": t.preco, "ID": t.id, "Excluir": False} for t in transacoes]
        df_neg = pd.DataFrame(dados_neg)
        
        editor_neg = st.data_editor(
            df_neg, 
            hide_index=True, 
            column_config={
                "ID": None,
                "Data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
                "Preço": st.column_config.NumberColumn("Preço", format="R$ %.2f"),
                "Excluir": st.column_config.CheckboxColumn("Excluir?")
            },
            key="editor_negociacoes"
        )

        if st.button("Salvar Correções (Negociações)"):
            mudou = False
            for _, row in editor_neg.iterrows():
                if row["Excluir"]:
                    excluir_transacao(row["ID"])
                    mudou = True
                else:
                    pass 
            if mudou:
                st.rerun()
    else:
        st.info("Nenhuma negociação registrada.")