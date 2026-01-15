from nicegui import ui

def kpi_card(titulo: str, valor: str, delta: str = None, icone: str = 'paid'):
    with ui.card().classes('w-full bg-[#1f2937] border border-gray-700 p-0 shadow-lg rounded-2xl'):
        with ui.column().classes('w-full p-5 gap-1'):
            
            # Título e Ícone
            with ui.row().classes('w-full justify-between items-start'):
                ui.label(titulo).classes('text-gray-400 text-xs font-bold uppercase tracking-wider')
                
                # Ícone
                with ui.element('div').classes('p-2 rounded-lg bg-gray-700/50'):
                    ui.icon(icone, color='white').classes('text-xl')

            # Valor Principal
            ui.label(valor).classes('text-3xl font-bold text-white mt-2')

            # Delta (Variação)
            if delta:
                cor = "text-emerald-400" if "+" in delta or "▲" in delta else "text-red-400"
                ui.label(delta).classes(f'text-xs font-semibold {cor} mt-1')