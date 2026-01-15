from nicegui import ui
from app.ui.pages.dashboard import dashboard_page
from app.core.config import settings

# Rota Principal
@ui.page('/')
def index():
    dashboard_page()

# Inicialização
# native=False garante que rode no navegador. 
ui.run(
    title=settings.PROJECT_NAME,
    dark=True,
    language='pt-BR',
    favicon='📊',
    port=8080
)