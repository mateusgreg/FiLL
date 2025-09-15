from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./financiamentos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo da tabela financiamentos
class Financiamento(Base):
    __tablename__ = "financiamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    valor_veiculo = Column(Float, nullable=False)
    valor_entrada = Column(Float, nullable=False)
    valor_financiado = Column(Float, nullable=False)
    taxa_juros = Column(Float, nullable=False)
    prazo_meses = Column(Integer, nullable=False)
    status_financiamento = Column(String(50), default="pendente")
    data_criacao = Column(DateTime, default=datetime.utcnow)
    aprovado_em = Column(DateTime, nullable=True)
    stellar_transaction_id = Column(String(255), nullable=True)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
