#!/usr/bin/env python3
"""
Script de configuração inicial para o projeto FiLL Backend
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_step(step, description):
    print(f"\n{'='*50}")
    print(f"PASSO {step}: {description}")
    print(f"{'='*50}")

def run_command(command, description):
    print(f"\nExecutando: {description}")
    print(f"Comando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso!")
        if result.stdout:
            print(f"Saída: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro!")
        print(f"Erro: {e.stderr}")
        return False

def check_python_version():
    print_step(1, "VERIFICANDO VERSÃO DO PYTHON")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detectado.")
        print("   Requerido: Python 3.8 ou superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK!")
    return True

def install_dependencies():
    print_step(2, "INSTALANDO DEPENDÊNCIAS")
    
    if not os.path.exists("requirements.txt"):
        print("❌ Arquivo requirements.txt não encontrado!")
        return False
    
    return run_command("pip install -r requirements.txt", "Instalação de dependências")

def create_database():
    print_step(3, "CRIANDO BANCO DE DADOS")
    
    try:
        # Importar e criar as tabelas
        from database import Base, engine
        Base.metadata.create_all(bind=engine)
        print("✅ Banco de dados SQLite criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def test_imports():
    print_step(4, "TESTANDO IMPORTAÇÕES")
    
    modules = [
        "fastapi",
        "uvicorn",
        "stellar_sdk",
        "pydantic",
        "sqlalchemy"
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK!")
        except ImportError as e:
            print(f"❌ {module} - Erro: {e}")
            all_ok = False
    
    return all_ok

def create_directories():
    print_step(5, "CRIANDO DIRETÓRIOS NECESSÁRIOS")
    
    directories = ["logs", "data"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Diretório {directory}/ criado")

def show_next_steps():
    print_step(6, "PRÓXIMOS PASSOS")
    
    print("""
🚀 Configuração concluída! Próximos passos:

1. Executar a aplicação:
   python main.py

2. Acessar a documentação:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Testar a API:
   python exemplo_uso.py

4. Para desenvolvimento:
   - Configure as chaves Stellar em config.py
   - Ajuste as configurações conforme necessário

📚 Documentação completa no README.md
""")

def main():
    print("🔧 CONFIGURAÇÃO INICIAL - FILL BACKEND")
    print("Sistema de Financiamento Veicular com Integração Stellar")
    
    # Verificações e configurações
    steps = [
        check_python_version,
        install_dependencies,
        create_database,
        test_imports,
        create_directories
    ]
    
    all_success = True
    for step in steps:
        if not step():
            all_success = False
            break
    
    if all_success:
        show_next_steps()
        print("\n✅ Configuração concluída com sucesso!")
    else:
        print("\n❌ Configuração falhou. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
