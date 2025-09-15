from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from financiamento_routes import router as financiamento_router
from stellar_routes import router as stellar_router
from database import engine, Base
import uvicorn

# Criar as tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Inicializar aplicação FastAPI
app = FastAPI(
    title="FiLL Backend - Sistema de Financiamento Veicular",
    description="""
    ## API para Sistema de Financiamento Veicular com Integração Stellar
    
    Esta API permite gerenciar financiamentos veiculares com integração à rede Stellar para:
    
    * **Criar e gerenciar financiamentos** - CRUD completo para financiamentos
    * **Integração Stellar** - Aprovação e execução de pagamentos na blockchain
    * **Contratos inteligentes** - Simulação de smart contracts para financiamentos
    
    ### Fluxo de Financiamento:
    1. **Criar financiamento** - `POST /api/financiamento`
    2. **Aprovar na Stellar** - `POST /api/stellar/aprovar_financiamento/{id}`
    3. **Executar pagamento** - `POST /api/stellar/executar_pagamento`
    
    ### Tecnologias:
    - **FastAPI** - Framework web moderno e rápido
    - **SQLite** - Banco de dados embutido
    - **Stellar SDK** - Integração com blockchain Stellar
    - **Pydantic** - Validação de dados
    """,
    version="1.0.0",
    contact={
        "name": "FiLL Backend Team",
        "email": "contato@fill.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(financiamento_router)
app.include_router(stellar_router)

@app.get("/")
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "message": "Bem-vindo à API FiLL Backend - Sistema de Financiamento Veicular",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "financiamentos": "/api/financiamento",
            "stellar": "/api/stellar"
        }
    }

@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde da API
    """
    return {
        "status": "healthy",
        "message": "API funcionando corretamente"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
