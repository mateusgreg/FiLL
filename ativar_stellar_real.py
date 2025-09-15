#!/usr/bin/env python3
"""
Script para ativar conexão real com a rede Stellar Testnet
"""

import os
import sys
from stellar_sdk import Server, Keypair
from stellar_sdk.exceptions import NotFoundError

def verificar_conexao_stellar():
    """Verifica se as chaves Stellar estão funcionando na testnet"""
    
    print("🔍 Verificando conexão com a rede Stellar Testnet...")
    
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv('environment.env')
    
    # Obter chaves
    issuer_secret = os.getenv("STELLAR_ISSUER_SECRET")
    financiador_secret = os.getenv("STELLAR_FINANCIADOR_SECRET")
    
    if not issuer_secret or not financiador_secret:
        print("❌ Chaves Stellar não encontradas no arquivo environment.env")
        return False
    
    try:
        # Criar keypairs
        issuer_keypair = Keypair.from_secret(issuer_secret)
        financiador_keypair = Keypair.from_secret(financiador_secret)
        
        print(f"✅ Chaves carregadas:")
        print(f"   Issuer: {issuer_keypair.public_key}")
        print(f"   Financiador: {financiador_keypair.public_key}")
        
        # Conectar ao servidor testnet
        server = Server("https://horizon-testnet.stellar.org")
        
        # Verificar se as contas existem
        try:
            issuer_account = server.load_account(issuer_keypair.public_key)
            print(f"✅ Conta Issuer ativa na testnet")
            print(f"   Saldo: {issuer_account.balances}")
        except NotFoundError:
            print(f"⚠️  Conta Issuer não encontrada - precisa de XLM para ativação")
            print(f"   Use o Friendbot: https://friendbot.stellar.org/?addr={issuer_keypair.public_key}")
        
        try:
            financiador_account = server.load_account(financiador_keypair.public_key)
            print(f"✅ Conta Financiador ativa na testnet")
            print(f"   Saldo: {financiador_account.balances}")
        except NotFoundError:
            print(f"⚠️  Conta Financiador não encontrada - precisa de XLM para ativação")
            print(f"   Use o Friendbot: https://friendbot.stellar.org/?addr={financiador_keypair.public_key}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar conexão: {e}")
        return False

def ativar_conexao_real():
    """Ativa a conexão real com a testnet no código"""
    
    print("\n🔧 Ativando conexão real com a testnet...")
    
    # Ler o arquivo stellar_service.py
    with open('stellar_service.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar se já está ativado
    if 'response = self.server.submit_transaction(transaction)' in content:
        print("✅ Conexão real já está ativada!")
        return True
    
    # Ativar conexão real
    content = content.replace(
        '# Para demonstração, simular transação sem conectar à rede real\n            # Em produção, descomente o código abaixo para conectar à rede Stellar\n            """',
        '# Conexão real com a rede Stellar ativada\n            # Descomentado para usar testnet real'
    )
    
    content = content.replace(
        '"""\n            \n            # Simulação para demonstração',
        '\n            # Código real ativado - conectando à testnet'
    )
    
    content = content.replace(
        'simulated_tx_id = hashlib.md5(f"financiamento_{financiamento_id}_{datetime.now()}".encode()).hexdigest()\n            \n            return {\n                "success": True,\n                "transaction_id": simulated_tx_id,\n                "message": f"Financiamento {financiamento_id} aprovado com sucesso na rede Stellar (SIMULADO)",\n                "contract_data": contract_data\n            }',
        'response = self.server.submit_transaction(transaction)\n            \n            return {\n                "success": True,\n                "transaction_id": response["id"],\n                "message": f"Financiamento {financiamento_id} aprovado com sucesso na rede Stellar",\n                "contract_data": contract_data\n            }'
    )
    
    # Salvar arquivo modificado
    with open('stellar_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Conexão real ativada no código!")
    return True

def main():
    print("🚀 ATIVAÇÃO DA CONEXÃO STELLAR REAL")
    print("=" * 50)
    
    # Verificar conexão
    if not verificar_conexao_stellar():
        print("\n❌ Falha na verificação. Verifique as chaves no environment.env")
        return
    
    # Ativar conexão real
    if ativar_conexao_real():
        print("\n🎉 CONEXÃO REAL ATIVADA COM SUCESSO!")
        print("\n📋 Próximos passos:")
        print("1. Instale a dependência: pip install python-dotenv")
        print("2. Execute: python main.py")
        print("3. Teste a API: python exemplo_uso.py")
        print("\n⚠️  ATENÇÃO: Agora as transações serão reais na testnet!")
    else:
        print("\n❌ Falha ao ativar conexão real")

if __name__ == "__main__":
    main()
