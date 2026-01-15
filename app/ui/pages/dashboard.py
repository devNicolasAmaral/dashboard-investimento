from nicegui import ui
from app.ui.theme import frame
from dataclasses import dataclass
from typing import List, Dict

# Estrutura de dados para representar os ativos financeiros
@dataclass
class Ativo:
    ticker: str
    qtd: int
    preco_medio: float
    preco_atual: float
    total_proventos: float = 0.0

    @property
    def saldo_total(self) -> float:
        return self.qtd * self.preco_atual

    @property
    def custo_total(self) -> float:
        return self.qtd * self.preco_medio

    @property
    def proventos_acumulados(self) -> float:
        return self.qtd * self.total_proventos

# Simulação de dados atuais (Backend Mock)
def get_carteira_mock() -> List[Ativo]:
    return [
        Ativo('PETR4', 4000, 24.50, 38.50, total_proventos=1.50),
    ]

# Simulação de dados históricos para o gráfico (Jan - Dez)
def get_historico_mock() -> Dict[str, List[float]]:
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    carteira = [100000, 102500, 98000, 105000, 110000, 108000, 115000, 122000, 119000, 130000, 142000, 154000]
    cdi = [100000 * (1.009 ** i) for i in range(12)]
    ipca = [100000 * (1.004 ** i) for i in range(12)]

    return {'meses': meses, 'carteira': carteira, 'cdi': cdi, 'ipca': ipca}

# Gera o SVG de fundo dos cards (Sparklines)
def get_sparkline_svg(color: str = '#10B981', type: str = 'up') -> str:
    if type == 'up':
        path = "M0 30 Q 10 25, 20 28 T 40 20 T 60 15 T 80 5 L 80 40 L 0 40 Z"
        fill_opacity = "0.1"
    elif type == 'down':
        path = "M0 5 Q 10 10, 20 8 T 40 15 T 60 25 T 80 35 L 80 40 L 0 40 Z"
        fill_opacity = "0.1"
    else: 
        path = "M0 20 Q 20 15, 40 25 T 80 20 L 80 40 L 0 40 Z"
        fill_opacity = "0.05"
        
    return f'''
        <svg viewBox="0 0 80 40" class="w-full h-full absolute bottom-0 left-0" preserveAspectRatio="none">
            <path d="{path}" fill="{color}" fill-opacity="{fill_opacity}" stroke="{color}" stroke-width="2" stroke-opacity="0.3" vector-effect="non-scaling-stroke" />
        </svg>
    '''

def format_currency(valor: float) -> str:
    return f'R${valor:,.2f}'.replace(",", "v").replace(".", ",").replace("v", ".")

# Renderização da página principal
def dashboard_page():
    
    # Carregamento e processamento dos dados
    carteira = get_carteira_mock()
    historico = get_historico_mock()
    
    total_investido = sum(a.custo_total for a in carteira)
    saldo_atual = sum(a.saldo_total for a in carteira)
    lucro_total = saldo_atual - total_investido
    total_proventos = sum(a.proventos_acumulados for a in carteira)
    
    rentabilidade_geral = (lucro_total / total_investido * 100) if total_investido > 0 else 0
    yield_on_cost = (total_proventos / total_investido * 100) if total_investido > 0 else 0

    # Definição de estilos condicionais (Cores e Indicadores)
    cor_lucro = '#10B981' if rentabilidade_geral >= 0 else '#EF4444'
    classe_cor_lucro = 'text-[#10B981]' if rentabilidade_geral >= 0 else 'text-red-500'
    seta_lucro = '▲' if rentabilidade_geral >= 0 else '▼'
    sparkline_type = 'up' if rentabilidade_geral >= 0 else 'down'

    with frame("Dashboard"):
        
        # Grid de KPIs
        # Exibe os 4 indicadores principais no topo da tela com largura total
        with ui.grid(columns=4).classes('w-full gap-6 mb-8'):
            
            # Card 1: Lucro/Prejuízo
            with ui.card().classes('relative overflow-hidden bg-[#15161A] shadow-lg p-5 rounded-xl flex-row items-center gap-4 py-8'):
                ui.html(get_sparkline_svg(color=cor_lucro, type=sparkline_type), sanitize=False).classes('absolute bottom-0 left-0 w-full h-16 pointer-events-none z-0')
                with ui.element('div').classes('z-10 w-14 h-14 bg-[#2A2B2F] rounded-xl flex items-center justify-center flex-shrink-0'):
                    ui.icon('account_balance_wallet').classes('text-2xl text-[#10B981]')
                with ui.element('div').classes('z-10 flex-1 flex justify-center'):
                    with ui.column().classes('items-end gap-1'):
                        ui.label('Lucro/Prejuízo').classes('text-gray-400 text-[13px] tracking-wide self-start')
                        ui.label(format_currency(lucro_total)).classes('text-xl text-white leading-none mt-1 self-end font-semibold')
                        with ui.row().classes('items-center gap-1 mt-1 self-end'):
                            rent_lucro_fmt = f"{rentabilidade_geral:.2f}".replace(".", ",")
                            ui.label(f'{seta_lucro}{rent_lucro_fmt}%').classes(f'{classe_cor_lucro} text-xs font-bold')

            # Card 2: Proventos
            with ui.card().classes('relative overflow-hidden bg-[#15161A] shadow-lg p-5 rounded-xl flex-row items-center gap-4 py-8'):
                ui.html(get_sparkline_svg(color='#10B981', type='up'), sanitize=False).classes('absolute bottom-0 left-0 w-full h-16 pointer-events-none z-0 opacity-50')
                with ui.element('div').classes('z-10 w-14 h-14 bg-[#2A2B2F] rounded-xl flex items-center justify-center flex-shrink-0'):
                    ui.icon('savings').classes('text-2xl text-[#10B981]')
                with ui.element('div').classes('z-10 flex-1 flex justify-center'):
                    with ui.column().classes('items-end gap-1'):
                        ui.label('Proventos').classes('text-gray-400 text-[13px] tracking-wide self-start')
                        ui.label(format_currency(total_proventos)).classes('text-xl text-white leading-none mt-1 self-end font-semibold')
                        with ui.row().classes('items-center gap-1 mt-1 self-end'):
                            yield_fmt = f"{yield_on_cost:.2f}".replace(".", ",")
                            ui.label(f'+{yield_fmt}% (DY)').classes('text-[#10B981] text-xs font-bold')

            # Card 3: Investido
            with ui.card().classes('relative overflow-hidden bg-[#15161A] shadow-lg p-5 rounded-xl flex-row items-center gap-4 py-8'):
                ui.html(get_sparkline_svg(color='#60A5FA', type='neutral'), sanitize=False).classes('absolute bottom-0 left-0 w-full h-16 pointer-events-none z-0 opacity-40')
                with ui.element('div').classes('z-10 w-14 h-14 bg-[#2A2B2F] rounded-xl flex items-center justify-center flex-shrink-0'):
                    ui.icon('credit_card').classes('text-2xl text-[#10B981]')
                with ui.element('div').classes('z-10 flex-1 flex justify-center'):
                    with ui.column().classes('items-end gap-1'):
                        ui.label('Investido').classes('text-gray-400 text-[13px] tracking-wide self-start')
                        ui.label(format_currency(total_investido)).classes('text-xl text-white leading-none mt-1 self-end font-semibold')
                        ui.label('Custo de Aquisição').classes('text-gray-600 text-[10px] font-medium self-end')

            # Card 4: Patrimônio
            with ui.card().classes('relative overflow-hidden bg-[#15161A] shadow-lg p-5 rounded-xl flex-row items-center gap-4 py-8'):
                ui.html(get_sparkline_svg(color='#10B981', type='up'), sanitize=False).classes('absolute bottom-0 left-0 w-full h-16 pointer-events-none z-0 opacity-60')
                with ui.element('div').classes('z-10 w-14 h-14 bg-[#2A2B2F] rounded-xl flex items-center justify-center flex-shrink-0'):
                    ui.icon('monetization_on').classes('text-2xl text-[#10B981]')
                with ui.element('div').classes('z-10 flex-1 flex justify-center'):
                    with ui.column().classes('items-end gap-1'):
                        ui.label('Patrimônio').classes('text-gray-400 text-[13px] tracking-wide self-start')
                        ui.label(format_currency(saldo_atual)).classes('text-xl text-white leading-none mt-1 self-end font-semibold')
                        ui.label('Valor de Mercado').classes('text-gray-600 text-[10px] font-medium self-end')

        # Área de Conteúdo Principal
        # Grid assimétrico de 8 colunas para permitir layouts flexíveis (ex: Gráfico 62.5% + Lista)
        with ui.grid(columns=8).classes('w-full gap-6'):
            
            # Gráfico de Evolução Patrimonial
            # Ocupa 5 colunas (aprox. 62% da largura)
            with ui.card().classes('col-span-5 bg-[#15161A] p-6 rounded-xl shadow-lg border border-[#2A2B2F]'):
                
                # Cabeçalho do Card
                # Título à esquerda e Controles (Legenda + Filtro) à direita
                with ui.row().classes('w-full items-center justify-between mb-6'):
                    
                    with ui.column().classes('gap-0'):
                        ui.label('Evolução Patrimonial').classes('text-lg font-semibold text-white tracking-tight')
                        ui.label('Comparativo com Benchmarks').classes('text-xs text-gray-400')
                    
                    # Container de Controles
                    with ui.row().classes('items-center gap-6'):
                        
                        # Legenda Personalizada (HTML)
                        # Renderizada fora do canvas para melhor controle de layout
                        with ui.row().classes('items-center gap-4'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('circle').classes('text-[10px] text-[#10B981]')
                                ui.label('Carteira').classes('text-xs text-gray-400 font-medium')
                            
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('circle').classes('text-[10px] text-[#FBBF24]')
                                ui.label('CDI').classes('text-xs text-gray-400 font-medium')

                            with ui.row().classes('items-center gap-2'):
                                ui.icon('circle').classes('text-[10px] text-[#6B7280]')
                                ui.label('IPCA').classes('text-xs text-gray-400 font-medium')

                        # Seletor de Período
                        opcoes_tempo = ['1 mês', '6 meses', '1 ano', '5 anos', '10 anos', 'Tempo máximo']
                        ui.select(options=opcoes_tempo, value='1 ano') \
                            .classes('w-32 text-xs') \
                            .props('outlined dense dark options-dense behavior="menu" label="Período"')

                # Componente de Gráfico (ECharts)
                ui.echart({
                    'backgroundColor': 'transparent',
                    'grid': {'top': 20, 'bottom': 30, 'left': 50, 'right': 20, 'containLabel': True},
                    'tooltip': {
                        'trigger': 'axis',
                        'backgroundColor': '#1F1A1A',
                        'borderColor': '#374151',
                        'textStyle': {'color': '#fff'},
                        'valueFormatter': '(val) => "R$ " + val.toLocaleString("pt-BR", {minimumFractionDigits: 2})'
                    },
                    'legend': {'show': False}, # Legenda nativa desativada em favor da customizada
                    'xAxis': {
                        'type': 'category',
                        'data': historico['meses'],
                        'boundaryGap': False,
                        'axisLine': {'lineStyle': {'color': '#374151'}},
                        'axisLabel': {'color': '#9CA3AF'}
                    },
                    'yAxis': {
                        'type': 'value',
                        'splitLine': {'lineStyle': {'color': '#2A2B2F', 'type': 'dashed'}},
                        'axisLabel': {'color': '#9CA3AF'}
                    },
                    'series': [
                        {
                            'name': 'Minha Carteira',
                            'type': 'line',
                            'smooth': True,
                            'showSymbol': False,
                            'data': historico['carteira'],
                            'itemStyle': {'color': '#10B981'},
                            'lineStyle': {'width': 3, 'shadowColor': 'rgba(16, 185, 129, 0.5)', 'shadowBlur': 10},
                            'areaStyle': {
                                'color': {
                                    'type': 'linear',
                                    'x': 0, 'y': 0, 'x2': 0, 'y2': 1,
                                    'colorStops': [
                                        {'offset': 0, 'color': 'rgba(16, 185, 129, 0.3)'}, 
                                        {'offset': 1, 'color': 'rgba(16, 185, 129, 0)'}
                                    ]
                                }
                            }
                        },
                        {
                            'name': 'CDI',
                            'type': 'line',
                            'smooth': True,
                            'showSymbol': False,
                            'data': historico['cdi'],
                            'itemStyle': {'color': '#FBBF24'},
                            'lineStyle': {'width': 2, 'type': 'dashed'}
                        },
                        {
                            'name': 'IPCA',
                            'type': 'line',
                            'smooth': True,
                            'showSymbol': False,
                            'data': historico['ipca'],
                            'itemStyle': {'color': '#6B7280'},
                            'lineStyle': {'width': 2, 'type': 'dotted'}
                        }
                    ]
                }).classes('w-full h-[350px]')
            
            # Espaço Lateral (Placeholder)
            # Reservado para lista de ativos ou notícias futuras (37.5% da largura)
            with ui.column().classes('col-span-3 gap-6'):
                pass