from stellar_sdk import Server, Keypair, Network, TransactionBuilder, Asset
from stellar_sdk.exceptions import NotFoundError, BadResponseError
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv('environment.env')

class StellarService:
    def __init__(self):
        # Configuração para rede de teste (testnet)
        self.server = Server(os.getenv("STELLAR_HORIZON_URL", "https://horizon-testnet.stellar.org"))
        self.network_passphrase = os.getenv("STELLAR_NETWORK_PASSPHRASE", Network.TESTNET_NETWORK_PASSPHRASE)
        
        # Chaves Stellar das variáveis de ambiente
        issuer_secret = os.getenv("STELLAR_ISSUER_SECRET")
        financiador_secret = os.getenv("STELLAR_FINANCIADOR_SECRET")
        
        if issuer_secret and financiador_secret:
            # Usar chaves reais da testnet
            self.issuer_keypair = Keypair.from_secret(issuer_secret)
            self.financiador_keypair = Keypair.from_secret(financiador_secret)
            print(f"✅ Conectado à testnet com chaves reais")
            print(f"   Issuer: {self.issuer_keypair.public_key}")
            print(f"   Financiador: {self.financiador_keypair.public_key}")
        else:
            # Fallback para chaves aleatórias (modo simulação)
            self.issuer_keypair = Keypair.random()
            self.financiador_keypair = Keypair.random()
            print("⚠️  Modo simulação - usando chaves aleatórias")
        
        # Asset personalizado para simular token de financiamento
        self.financing_asset = Asset("FILL", self.issuer_keypair.public_key)

    async def aprovar_financiamento(self, financiamento_id: int, valor: float) -> Dict[str, Any]:
        """
        Aprova um financiamento criando uma transação na rede Stellar
        """
        try:
            # Simular criação de contrato inteligente simples
            # Em um cenário real, isso seria um contrato Soroban
            contract_data = {
                "financiamento_id": financiamento_id,
                "valor": valor,
                "status": "aprovado",
                "timestamp": str(int(datetime.now().timestamp()))
            }
            
            # Conexão real com a rede Stellar ativada
            # Descomentado para usar testnet real
            
            # CONEXÃO REAL COM A REDE STELLAR TESTNET ATIVADA
            print(f"🌐 Conectando à testnet para financiamento {financiamento_id}...")
            
            # Criar transação de aprovação simples
            source_account = self.server.load_account(self.financiador_keypair.public_key)
            print(f"✅ Conta carregada: {self.financiador_keypair.public_key}")
            
            # Usar operação de pagamento simples para simular aprovação
            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase=self.network_passphrase,
                    base_fee=100
                )
                .add_text_memo(f"APROVACAO_FINANCIAMENTO_{financiamento_id}")
                .append_payment_op(
                    destination=self.financiador_keypair.public_key,
                    asset=Asset.native(),
                    amount="0.0000001"
                )
                .set_timeout(300)
                .build()
            )
            
            transaction.sign(self.financiador_keypair)
            print(f"✅ Transação assinada")
            
            # Submeter transação
            print(f"🚀 Submetendo transação à testnet...")
            response = self.server.submit_transaction(transaction)
            print(f"✅ Transação submetida com sucesso!")
            
            return {
                "success": True,
                "transaction_id": response["id"],
                "message": f"Financiamento {financiamento_id} aprovado com sucesso na rede Stellar TESTNET",
                "contract_data": contract_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Erro ao aprovar financiamento: {str(e)}"
            }

    async def executar_pagamento(self, financiamento_id: int, valor: float, destinatario: str) -> Dict[str, Any]:
        """
        Executa o pagamento transferindo tokens na rede Stellar
        """
        try:
            # CONEXÃO REAL COM A REDE STELLAR TESTNET ATIVADA
            print(f"🌐 Executando pagamento na testnet para financiamento {financiamento_id}...")
            
            # Carregar conta do financiador
            source_account = self.server.load_account(self.financiador_keypair.public_key)
            print(f"✅ Conta carregada: {self.financiador_keypair.public_key}")
            
            # Criar transação de pagamento com XLM nativo
            transaction = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase=self.network_passphrase,
                    base_fee=100
                )
                .add_text_memo(f"PAGAMENTO_FINANCIAMENTO_{financiamento_id}")
                .append_payment_op(
                    destination=destinatario,
                    asset=Asset.native(),
                    amount="0.0000001"
                )
                .set_timeout(300)
                .build()
            )
            
            transaction.sign(self.financiador_keypair)
            print(f"✅ Transação assinada")
            
            # Submeter transação
            print(f"🚀 Submetendo pagamento à testnet...")
            response = self.server.submit_transaction(transaction)
            print(f"✅ Pagamento submetido com sucesso!")
            
            return {
                "success": True,
                "transaction_id": response["id"],
                "message": f"Pagamento de 0.0000001 XLM executado com sucesso para {destinatario} na TESTNET",
                "valor": valor,
                "destinatario": destinatario
            }
            
        except Exception as e:
            return {
                "success": False,
                "transaction_id": None,
                "message": f"Erro ao executar pagamento: {str(e)}"
            }

    async def verificar_saldo(self, conta: str) -> Dict[str, Any]:
        """
        Verifica o saldo de uma conta na rede Stellar
        """
        try:
            # Para demonstração, simular verificação de saldo
            # Em produção, descomente o código abaixo para conectar à rede Stellar
            """
            account = self.server.accounts().account_id(conta).call()
            balances = []
            
            for balance in account["balances"]:
                if balance["asset_type"] == "native":
                    balances.append({
                        "asset": "XLM",
                        "balance": balance["balance"]
                    })
                else:
                    balances.append({
                        "asset": f"{balance['asset_code']}:{balance['asset_issuer']}",
                        "balance": balance["balance"]
                    })
            """
            
            # Simulação para demonstração
            balances = [
                {"asset": "XLM", "balance": "10000.0000000"},
                {"asset": "FILL", "balance": "50000.0000000"}
            ]
            
            return {
                "success": True,
                "account": conta,
                "balances": balances,
                "message": "Saldo verificado (SIMULADO)"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro ao verificar saldo: {str(e)}"
            }

# Instância global do serviço
stellar_service = StellarService()
