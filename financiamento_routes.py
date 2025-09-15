from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db, Financiamento
from models import FinanciamentoCreate, FinanciamentoUpdate, FinanciamentoResponse
from datetime import datetime
from typing import List

router = APIRouter(prefix="/api/financiamento", tags=["financiamentos"])

@router.post("/", response_model=FinanciamentoResponse, status_code=status.HTTP_201_CREATED)
async def criar_financiamento(financiamento: FinanciamentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo registro de financiamento no banco de dados
    """
    try:
        # Validar se o valor financiado é consistente
        if financiamento.valor_financiado != (financiamento.valor_veiculo - financiamento.valor_entrada):
            raise HTTPException(
                status_code=400,
                detail="Valor financiado deve ser igual ao valor do veículo menos a entrada"
            )
        
        # Criar novo financiamento
        db_financiamento = Financiamento(
            valor_veiculo=financiamento.valor_veiculo,
            valor_entrada=financiamento.valor_entrada,
            valor_financiado=financiamento.valor_financiado,
            taxa_juros=financiamento.taxa_juros,
            prazo_meses=financiamento.prazo_meses,
            status_financiamento="pendente"
        )
        
        db.add(db_financiamento)
        db.commit()
        db.refresh(db_financiamento)
        
        return db_financiamento
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar financiamento: {str(e)}")

@router.get("/{financiamento_id}", response_model=FinanciamentoResponse)
async def obter_financiamento(financiamento_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de um financiamento específico
    """
    financiamento = db.query(Financiamento).filter(Financiamento.id == financiamento_id).first()
    
    if not financiamento:
        raise HTTPException(
            status_code=404,
            detail=f"Financiamento com ID {financiamento_id} não encontrado"
        )
    
    return financiamento

@router.put("/{financiamento_id}", response_model=FinanciamentoResponse)
async def atualizar_financiamento(
    financiamento_id: int, 
    financiamento_update: FinanciamentoUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza o status de um financiamento
    """
    financiamento = db.query(Financiamento).filter(Financiamento.id == financiamento_id).first()
    
    if not financiamento:
        raise HTTPException(
            status_code=404,
            detail=f"Financiamento com ID {financiamento_id} não encontrado"
        )
    
    # Atualizar status
    financiamento.status_financiamento = financiamento_update.status_financiamento
    
    # Se aprovado, registrar data de aprovação
    if financiamento_update.status_financiamento == "aprovado":
        financiamento.aprovado_em = datetime.utcnow()
    
    db.commit()
    db.refresh(financiamento)
    
    return financiamento

@router.get("/status/{status}", response_model=List[FinanciamentoResponse])
async def listar_financiamentos_por_status(status: str, db: Session = Depends(get_db)):
    """
    Retorna todos os financiamentos com um determinado status
    """
    financiamentos = db.query(Financiamento).filter(
        Financiamento.status_financiamento == status
    ).all()
    
    return financiamentos

@router.get("/", response_model=List[FinanciamentoResponse])
async def listar_todos_financiamentos(db: Session = Depends(get_db)):
    """
    Retorna todos os financiamentos
    """
    financiamentos = db.query(Financiamento).all()
    return financiamentos
