from nicegui import ui
from contextlib import contextmanager

@contextmanager
def frame(nav_title: str):
    """
    Define a estrutura padrão de todas as páginas (Menu, Fundo, etc).
    """

    ui.colors(primary='#3b82f6', secondary='#10b981', accent='#8b5cf6', dark='#1f2937')

    with ui.column().classes('w-full min-h-screen bg-[#141824] p-4 gap-4'):
        # Header
        with ui.row().classes('w-full justify-between items-center mb-6'):
            ui.label(nav_title).classes('text-2xl font-bold text-white tracking-wide')
            
            # Espaço para Menu
            with ui.row().classes('gap-2'):
                ui.icon('notifications', color='white').classes('opacity-60 cursor-pointer hover:opacity-100')
                ui.icon('account_circle', color='white').classes('opacity-60 cursor-pointer hover:opacity-100')
        
        # Conteúdo da Página
        yield