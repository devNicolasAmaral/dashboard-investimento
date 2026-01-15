from sqlmodel import create_engine, Session
from app.core.config import settings

# Cria a conexão
# echo=True faz o log mostrar o SQL real no terminal
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    """Dependência para injetar a sessão do banco nas rotas/funções."""
    with Session(engine) as session:
        yield session