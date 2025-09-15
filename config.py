import os
from typing import Optional

class Settings:
    # Configurações do banco de dados
    DATABASE_URL: str = "sqlite:///./financiamentos.db"
    
    # Configurações da API
    API_TITLE: str = "FiLL Backend - Sistema de Financiamento Veicular"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Configurações Stellar
    STELLAR_NETWORK: str = "testnet"  # ou "mainnet" para produção
    STELLAR_HORIZON_URL: str = "https://horizon-testnet.stellar.org"
    STELLAR_NETWORK_PASSPHRASE: str = "Test SDF Network ; September 2015"
    
    # Chaves Stellar (em produção, usar variáveis de ambiente)
    STELLAR_ISSUER_SECRET: Optional[str] = os.getenv("STELLAR_ISSUER_SECRET")
    STELLAR_FINANCIADOR_SECRET: Optional[str] = os.getenv("STELLAR_FINANCIADOR_SECRET")
    
    # Configurações de CORS
    CORS_ORIGINS: list = ["*"]  # Em produção, especificar domínios permitidos
    
    # Configurações de logging
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

settings = Settings()
