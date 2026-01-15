from nicegui import ui
from contextlib import contextmanager

@contextmanager
def frame(nav_title: str):
    # Definição da paleta de cores do tema
    ui.colors(primary='#EF4444', secondary='#10b981', accent='#8b5cf6', dark='#1F1A1A')

    # Importação da tipografia Poppins
    ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">')

    # Remove paddings padrões do framework e aplica a fonte globalmente no body
    ui.query('.nicegui-content').classes('!p-0 w-full h-screen overflow-hidden')
    ui.query('body').classes('bg-[#1F1A1A] overflow-hidden').style('font-family: "Poppins", sans-serif;')

    # Divide a tela em dois grandes blocos (Esquerda e Direita)
    with ui.row().classes('w-full h-screen no-wrap gap-0'):

        # Sidebar
        # Fundo (#141111) com largura travada em 280px
        with ui.column().classes('w-[280px] h-full bg-[#15161A] text-white p-0 gap-0'):
            
            # Logo da Aplicação
            with ui.row().classes('w-full h-24 items-center justify-start px-10'):
                ui.label('Logo').classes('text-3xl tracking-tighter text-white')

            # Lista de Menus de Navegação
            with ui.column().classes('w-full gap-10 px-10 mt-16'):
                
                # Dashboard (Estado Ativo)
                with ui.row().classes('w-full items-center gap-6 cursor-pointer group'):
                    ui.icon('dashboard').classes('text-2xl text-[#51567D]')
                    ui.label('Dashboard').classes('text-base text-[#51567D]')

                # Transações (Estado Inativo com Hover)
                with ui.row().classes('w-full items-center gap-6 cursor-pointer transition-colors group'):
                    ui.icon('account_balance_wallet').classes('text-2xl text-[#FFFFFF] group-hover:text-[#51567D] transition-colors')
                    ui.label('Transações').classes('text-base text-[#FFFFFF] group-hover:text-[#51567D] transition-colors')

        # Conteúdo Fluido
        # Ocupa todo o espaço restante da tela e contém o Header e o Corpo
        with ui.column().classes('flex-1 h-full bg-[#1F1A1A] p-0 gap-0'):

            # Barra Superior (Header)
            # Fundo para alinhar visualmente com a Sidebar
            with ui.row().classes('w-full h-24 bg-[#15161A] items-center justify-between px-10'):
                
                # Título da Página Atual
                ui.label(nav_title).classes('text-3xl font-semibold tracking-tight text-white')

                # Área de Ferramentas (Direita do Header)
                with ui.row().classes('items-center gap-6'):
                    
                    # Barra de Pesquisa
                    with ui.input(placeholder='Pesquisar...') \
                            .props('dark dense borderless input-class="text-gray-300"') \
                            .classes('w-64 bg-[#2A2B2F] rounded-lg pl-3 text-sm'):
                        
                        # Ícone de Lupa (Injetado no slot 'append' do input)
                        ui.icon('search').props('slot=append').classes('text-gray-400 text-xl cursor-pointer hover:text-white transition-colors mr-2 self-center')

                    # Ícone de Notificações com indicador (Badge)
                    with ui.element('div').classes('relative cursor-pointer ml-2'):
                        ui.icon('notifications').classes('text-xl text-gray-400 hover:text-white transition-colors')
                        ui.element('div').classes('absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full')
                    
                    # Avatar do Usuário
                    ui.avatar('NA', color='primary', text_color='white', square=True).classes('!rounded-xl shadow-lg cursor-pointer font-semibold')

            # Área de Conteúdo (Yield)
            # Fundo cinza (#1F1A1A) onde as páginas injetam seu conteúdo específico
            with ui.column().classes('w-full flex-1 bg-[#2A2B2F] p-10 overflow-y-auto'):
                yield