# 🚀 Guia de Execução Rápida - FiLL Backend

## Execução em 3 Passos

### 1. Configuração Inicial
```bash
python setup.py
```

### 2. Executar a API
```bash
python main.py
```

### 3. Testar a API
```bash
python exemplo_uso.py
```

## 📋 Verificações Rápidas

### ✅ API Funcionando
- Acesse: http://localhost:8000
- Deve retornar: `{"message": "Bem-vindo à API FiLL Backend..."}`

### ✅ Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### ✅ Banco de Dados
- Arquivo: `financiamentos.db` (criado automaticamente)

## 🔧 Solução de Problemas

### Erro de Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro de Porta Ocupada
```bash
# Alterar porta no main.py ou matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Erro de Banco de Dados
```bash
# Deletar e recriar
rm financiamentos.db
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

## 📱 Testando com cURL

### Criar Financiamento
```bash
curl -X POST "http://localhost:8000/api/financiamento/" \
  -H "Content-Type: application/json" \
  -d '{
    "valor_veiculo": 50000.0,
    "valor_entrada": 10000.0,
    "valor_financiado": 40000.0,
    "taxa_juros": 2.5,
    "prazo_meses": 60
  }'
```

### Aprovar na Stellar
```bash
curl -X POST "http://localhost:8000/api/stellar/aprovar_financiamento/1"
```

### Executar Pagamento
```bash
curl -X POST "http://localhost:8000/api/stellar/executar_pagamento" \
  -H "Content-Type: application/json" \
  -d '{
    "financiamento_id": 1,
    "destinatario": "GCKFBEIYTKP4R4M4TZQK7X2Y3Z4X5X6X7X8X9X0X1X2X3X4X5X6X7X8X9X0"
  }'
```

## 🎯 Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Página inicial |
| GET | `/health` | Status da API |
| POST | `/api/financiamento/` | Criar financiamento |
| GET | `/api/financiamento/{id}` | Obter financiamento |
| PUT | `/api/financiamento/{id}` | Atualizar status |
| POST | `/api/stellar/aprovar_financiamento/{id}` | Aprovar na Stellar |
| POST | `/api/stellar/executar_pagamento` | Executar pagamento |

## 📊 Monitoramento

### Logs da Aplicação
- Os logs aparecem no terminal onde a API está rodando
- Nível de log: INFO (configurável em config.py)

### Status do Banco
- Arquivo SQLite: `financiamentos.db`
- Tabela: `financiamentos`
- Visualizar: Use um cliente SQLite ou SQLite Browser

## 🔄 Fluxo Completo

1. **POST** `/api/financiamento/` → Cria financiamento (status: pendente)
2. **POST** `/api/stellar/aprovar_financiamento/{id}` → Aprova na Stellar (status: aprovado)
3. **POST** `/api/stellar/executar_pagamento` → Executa pagamento (status: pago)

## 🆘 Suporte

- **Documentação completa**: README.md
- **Exemplo de uso**: exemplo_uso.py
- **Configuração**: config.py
- **Setup automático**: setup.py
