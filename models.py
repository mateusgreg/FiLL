from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Modelo para criação de financiamento
class FinanciamentoCreate(BaseModel):
    valor_veiculo: float
    valor_entrada: float
    valor_financiado: float
    taxa_juros: float
    prazo_meses: int

# Modelo para atualização de status
class FinanciamentoUpdate(BaseModel):
    status_financiamento: str

# Modelo para resposta completa
class FinanciamentoResponse(BaseModel):
    id: int
    valor_veiculo: float
    valor_entrada: float
    valor_financiado: float
    taxa_juros: float
    prazo_meses: int
    status_financiamento: str
    data_criacao: datetime
    aprovado_em: Optional[datetime] = None
    stellar_transaction_id: Optional[str] = None

    class Config:
        from_attributes = True

# Modelo para operações Stellar
class StellarOperation(BaseModel):
    financiamento_id: int
    operation_type: str  # "aprovar" ou "executar_pagamento"

# Modelo para resposta de operações Stellar
class StellarResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    message: str
