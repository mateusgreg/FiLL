import requests
import json

# URL base da API
BASE_URL = "http://localhost:8000"

def test_financiamento_flow():
    """Testa o fluxo completo de financiamento"""
    
    print("=== Testando Fluxo de Financiamento ===\n")
    
    # 1. Criar financiamento
    print("1. Criando financiamento...")
    financiamento_data = {
        "valor_veiculo": 50000.0,
        "valor_entrada": 10000.0,
        "valor_financiado": 40000.0,
        "taxa_juros": 2.5,
        "prazo_meses": 60
    }
    
    response = requests.post(f"{BASE_URL}/api/financiamento/", json=financiamento_data)
    if response.status_code == 201:
        financiamento = response.json()
        print(f"✅ Financiamento criado com ID: {financiamento['id']}")
        financiamento_id = financiamento['id']
    else:
        print(f"❌ Erro ao criar financiamento: {response.text}")
        return
    
    # 2. Verificar financiamento
    print(f"\n2. Verificando financiamento {financiamento_id}...")
    response = requests.get(f"{BASE_URL}/api/financiamento/{financiamento_id}")
    if response.status_code == 200:
        print("✅ Financiamento encontrado")
    else:
        print(f"❌ Erro ao buscar financiamento: {response.text}")
    
    # 3. Aprovar na Stellar
    print(f"\n3. Aprovando financiamento {financiamento_id} na Stellar...")
    response = requests.post(f"{BASE_URL}/api/stellar/aprovar_financiamento/{financiamento_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Financiamento aprovado: {result['message']}")
    else:
        print(f"❌ Erro ao aprovar: {response.text}")
    
    # 4. Executar pagamento
    print(f"\n4. Executando pagamento...")
    payment_data = {
        "financiamento_id": financiamento_id,
        "destinatario": "GCKFBEIYTKP4R4M4TZQK7X2Y3Z4X5X6X7X8X9X0X1X2X3X4X5X6X7X8X9X0"
    }
    response = requests.post(f"{BASE_URL}/api/stellar/executar_pagamento", json=payment_data)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Pagamento executado: {result['message']}")
    else:
        print(f"❌ Erro ao executar pagamento: {response.text}")
    
    # 5. Verificar status final
    print(f"\n5. Verificando status final...")
    response = requests.get(f"{BASE_URL}/api/financiamento/{financiamento_id}")
    if response.status_code == 200:
        financiamento = response.json()
        print(f"✅ Status final: {financiamento['status_financiamento']}")
        print(f"✅ Transaction ID: {financiamento['stellar_transaction_id']}")

if __name__ == "__main__":
    test_financiamento_flow()
