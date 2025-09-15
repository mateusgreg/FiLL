# Exemplo de configuração para o projeto FiLL Backend
# Copie este arquivo para config.py e ajuste as configurações conforme necessário

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
    # Para desenvolvimento, você pode gerar chaves em: https://laboratory.stellar.org/
    STELLAR_ISSUER_SECRET: Optional[str] = os.getenv("STELLAR_ISSUER_SECRET", "SBPQVZPUE2PR2F75DJM7VW2N52X2C3QYHBCQBRQH3DA3Z6T2H3Y4X5X6")
    STELLAR_FINANCIADOR_SECRET: Optional[str] = os.getenv("STELLAR_FINANCIADOR_SECRET", "SBPQVZPUE2PR2F75DJM7VW2N52X2C3QYHBCQBRQH3DA3Z6T2H3Y4X5X7")
    
    # Configurações de CORS
    CORS_ORIGINS: list = ["*"]  # Em produção, especificar domínios permitidos
    
    # Configurações de logging
    LOG_LEVEL: str = "info"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Instruções para configuração:
"""
1. Para usar em desenvolvimento:
   - Mantenha as configurações padrão
   - As chaves Stellar são apenas para demonstração

2. Para usar em produção:
   - Configure as variáveis de ambiente
   - Use chaves Stellar reais
   - Configure CORS adequadamente
   - Use banco de dados PostgreSQL/MySQL
   - Configure rede Stellar mainnet

3. Variáveis de ambiente recomendadas:
   export STELLAR_ISSUER_SECRET="sua_chave_secreta_aqui"
   export STELLAR_FINANCIADOR_SECRET="sua_chave_secreta_aqui"
   export DATABASE_URL="postgresql://user:password@localhost/fill_db"
   export CORS_ORIGINS="https://seu-dominio.com,https://app.seu-dominio.com"
"""
