from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Financiamento
from models import StellarResponse
from stellar_service import stellar_service
from datetime import datetime

router = APIRouter(prefix="/api/stellar", tags=["stellar"])

@router.post("/aprovar_financiamento/{financiamento_id}", response_model=StellarResponse)
async def aprovar_financiamento_stellar(financiamento_id: int, db: Session = Depends(get_db)):
    """
    Assina e submete uma transação para a rede Stellar, indicando a aprovação de um financiamento
    """
    # Buscar financiamento no banco
    financiamento = db.query(Financiamento).filter(Financiamento.id == financiamento_id).first()
    
    if not financiamento:
        raise HTTPException(
            status_code=404,
            detail=f"Financiamento com ID {financiamento_id} não encontrado"
        )
    
    if financiamento.status_financiamento != "pendente":
        raise HTTPException(
            status_code=400,
            detail=f"Financiamento já foi processado. Status atual: {financiamento.status_financiamento}"
        )
    
    try:
        # Chamar serviço Stellar para aprovar
        resultado = await stellar_service.aprovar_financiamento(
            financiamento_id=financiamento_id,
            valor=financiamento.valor_financiado
        )
        
        if resultado["success"]:
            # Atualizar financiamento no banco
            financiamento.status_financiamento = "aprovado"
            financiamento.aprovado_em = datetime.utcnow()
            financiamento.stellar_transaction_id = resultado["transaction_id"]
            
            db.commit()
            
            return StellarResponse(
                success=True,
                transaction_id=resultado["transaction_id"],
                message=resultado["message"]
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado["message"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao aprovar financiamento na rede Stellar: {str(e)}"
        )

@router.post("/executar_pagamento", response_model=StellarResponse)
async def executar_pagamento_stellar(
    financiamento_id: int,
    destinatario: str,
    db: Session = Depends(get_db)
):
    """
    Simula a execução de um pagamento na rede Stellar
    """
    # Buscar financiamento no banco
    financiamento = db.query(Financiamento).filter(Financiamento.id == financiamento_id).first()
    
    if not financiamento:
        raise HTTPException(
            status_code=404,
            detail=f"Financiamento com ID {financiamento_id} não encontrado"
        )
    
    if financiamento.status_financiamento != "aprovado":
        raise HTTPException(
            status_code=400,
            detail="Financiamento deve estar aprovado para executar pagamento"
        )
    
    try:
        # Chamar serviço Stellar para executar pagamento
        resultado = await stellar_service.executar_pagamento(
            financiamento_id=financiamento_id,
            valor=financiamento.valor_financiado,
            destinatario=destinatario
        )
        
        if resultado["success"]:
            # Atualizar status do financiamento
            financiamento.status_financiamento = "pago"
            
            db.commit()
            
            return StellarResponse(
                success=True,
                transaction_id=resultado["transaction_id"],
                message=resultado["message"]
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=resultado["message"]
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao executar pagamento na rede Stellar: {str(e)}"
        )

@router.get("/saldo/{conta}")
async def verificar_saldo_stellar(conta: str):
    """
    Verifica o saldo de uma conta na rede Stellar
    """
    try:
        resultado = await stellar_service.verificar_saldo(conta)
        return resultado
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar saldo: {str(e)}"
        )

@router.get("/status/{financiamento_id}")
async def verificar_status_stellar(financiamento_id: int, db: Session = Depends(get_db)):
    """
    Verifica o status de um financiamento na rede Stellar
    """
    financiamento = db.query(Financiamento).filter(Financiamento.id == financiamento_id).first()
    
    if not financiamento:
        raise HTTPException(
            status_code=404,
            detail=f"Financiamento com ID {financiamento_id} não encontrado"
        )
    
    return {
        "financiamento_id": financiamento_id,
        "status_financiamento": financiamento.status_financiamento,
        "stellar_transaction_id": financiamento.stellar_transaction_id,
        "aprovado_em": financiamento.aprovado_em
    }
