#!/usr/bin/env python3
"""
Exemplo de uso da API FiLL Backend
Demonstra o fluxo completo de financiamento veicular
"""

import requests
import json
import time

# Configuração
BASE_URL = "http://localhost:8000"

def print_separator(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_response(response, title):
    print(f"\n{title}:")
    print(f"Status: {response.status_code}")
    if response.status_code < 400:
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    else:
        print(f"Erro: {response.text}")

def main():
    print_separator("EXEMPLO DE USO - API FILL BACKEND")
    
    # Verificar se a API está funcionando
    print("\n1. Verificando saúde da API...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check")
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        print("   Execute: python main.py")
        return
    
    # 1. Criar financiamento
    print_separator("CRIANDO FINANCIAMENTO")
    
    financiamento_data = {
        "valor_veiculo": 75000.0,
        "valor_entrada": 15000.0,
        "valor_financiado": 60000.0,
        "taxa_juros": 2.8,
        "prazo_meses": 72
    }
    
    print(f"Dados do financiamento: {json.dumps(financiamento_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/api/financiamento/", json=financiamento_data)
    print_response(response, "Criação de Financiamento")
    
    if response.status_code != 201:
        print("❌ Falha ao criar financiamento. Encerrando exemplo.")
        return
    
    financiamento_id = response.json()["id"]
    print(f"✅ Financiamento criado com ID: {financiamento_id}")
    
    # 2. Verificar financiamento criado
    print_separator("VERIFICANDO FINANCIAMENTO")
    
    response = requests.get(f"{BASE_URL}/api/financiamento/{financiamento_id}")
    print_response(response, "Detalhes do Financiamento")
    
    # 3. Listar financiamentos por status
    print_separator("LISTANDO FINANCIAMENTOS PENDENTES")
    
    response = requests.get(f"{BASE_URL}/api/financiamento/status/pendente")
    print_response(response, "Financiamentos Pendentes")
    
    # 4. Aprovar financiamento na Stellar
    print_separator("APROVANDO FINANCIAMENTO NA STELLAR")
    
    print("⚠️  Nota: Esta operação simula a aprovação na rede Stellar (testnet)")
    print("   Em um ambiente real, isso criaria uma transação na blockchain")
    
    response = requests.post(f"{BASE_URL}/api/stellar/aprovar_financiamento/{financiamento_id}")
    print_response(response, "Aprovação na Stellar")
    
    if response.status_code == 200:
        print("✅ Financiamento aprovado na rede Stellar!")
        stellar_tx_id = response.json().get("transaction_id")
        if stellar_tx_id:
            print(f"   Transaction ID: {stellar_tx_id}")
    
    # 5. Verificar status após aprovação
    print_separator("STATUS APÓS APROVAÇÃO")
    
    response = requests.get(f"{BASE_URL}/api/financiamento/{financiamento_id}")
    print_response(response, "Status Atualizado")
    
    # 6. Executar pagamento
    print_separator("EXECUTANDO PAGAMENTO")
    
    # Endereço de exemplo para o destinatário (vendedor)
    destinatario = "GCKFBEIYTKP4R4M4TZQK7X2Y3Z4X5X6X7X8X9X0X1X2X3X4X5X6X7X8X9X0"
    
    payment_data = {
        "financiamento_id": financiamento_id,
        "destinatario": destinatario
    }
    
    print(f"Dados do pagamento: {json.dumps(payment_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/api/stellar/executar_pagamento", json=payment_data)
    print_response(response, "Execução do Pagamento")
    
    if response.status_code == 200:
        print("✅ Pagamento executado com sucesso!")
        payment_tx_id = response.json().get("transaction_id")
        if payment_tx_id:
            print(f"   Transaction ID: {payment_tx_id}")
    
    # 7. Status final
    print_separator("STATUS FINAL")
    
    response = requests.get(f"{BASE_URL}/api/financiamento/{financiamento_id}")
    print_response(response, "Status Final do Financiamento")
    
    # 8. Listar todos os financiamentos
    print_separator("TODOS OS FINANCIAMENTOS")
    
    response = requests.get(f"{BASE_URL}/api/financiamento/")
    print_response(response, "Lista Completa")
    
    print_separator("EXEMPLO CONCLUÍDO")
    print("✅ Fluxo de financiamento executado com sucesso!")
    print("\n📚 Para mais informações:")
    print(f"   - Documentação Swagger: {BASE_URL}/docs")
    print(f"   - Documentação ReDoc: {BASE_URL}/redoc")
    print(f"   - API Root: {BASE_URL}/")

if __name__ == "__main__":
    main()
