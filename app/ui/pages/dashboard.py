from nicegui import ui
from sqlmodel import Session, select
from app.db.session import engine
from app.models.transaction import Transaction
from app.services.portfolio import CalculationService
from app.ui.theme import frame
from app.ui.components.kpi_card import kpi_card

def dashboard_page():
    # Busca de Dados
    with Session(engine) as session:
        transacoes = session.exec(select(Transaction)).all()
        posicoes = CalculationService.calculate_positions(transacoes)
    
    # Cálculos Totais para os Cards
    total_investido = sum(p.total_investido for p in posicoes)
    patrimonio_atual = total_investido
    
    # Renderização 
    with frame("Dashboard"):
        
        # Grid de KPIs
        with ui.grid(columns=4).classes('w-full gap-4 mb-6'):
            kpi_card("Patrimônio Total", f"R$ {patrimonio_atual:,.2f}", "▲ 0.0%", "account_balance_wallet")
            kpi_card("Total Investido", f"R$ {total_investido:,.2f}", icone="savings")
            kpi_card("Proventos", "R$ 530.00", icone="payments") # Valor fixo do seed por enquanto
            kpi_card("Rentabilidade", "0.0%", icone="trending_up")

        # Tabela de Ativos
        with ui.card().classes('w-full bg-[#1f2937] border border-gray-700 rounded-2xl p-6'):
            ui.label("Minha Carteira").classes('text-xl font-bold text-white mb-4')
            
            # Header
            with ui.row().classes('w-full border-b border-gray-700 pb-2 mb-2'):
                ui.label('ATIVO').classes('w-1/4 text-gray-400 font-bold text-sm')
                ui.label('QTD').classes('w-1/4 text-gray-400 font-bold text-sm text-center')
                ui.label('PREÇO MÉDIO').classes('w-1/4 text-gray-400 font-bold text-sm text-right')
                ui.label('TOTAL').classes('w-1/4 text-gray-400 font-bold text-sm text-right')

            # Linhas de Dados
            for pos in posicoes:
                with ui.row().classes('w-full py-3 border-b border-gray-700/50 hover:bg-gray-700/30 transition-colors cursor-pointer items-center'):
                    # Ticker
                    with ui.row().classes('w-1/4 items-center gap-2'):
                        ui.avatar(pos.ticker[:2], color='primary', text_color='white').classes('w-8 h-8 text-xs font-bold')
                        ui.label(pos.ticker).classes('text-white font-bold')
                    
                    ui.label(str(pos.quantidade)).classes('w-1/4 text-gray-300 text-center')
                    ui.label(f"R$ {pos.preco_medio:,.2f}").classes('w-1/4 text-gray-300 text-right')
                    ui.label(f"R$ {pos.total_investido:,.2f}").classes('w-1/4 text-white font-bold text-right')