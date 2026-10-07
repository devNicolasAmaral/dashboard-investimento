from nicegui import ui
from app.ui.pages.dashboard import dashboard_page
from app.core.config import settings

@ui.page('/')
def index():
    dashboard_page()

ui.run(
    title=settings.PROJECT_NAME,
    dark=True,
    language='pt-BR',
    favicon='📊',
    host='0.0.0.0',
    port=8080
)
