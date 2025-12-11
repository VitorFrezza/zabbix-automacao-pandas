import requests
import json
import sys
import os
import pandas as pd 
from datetime import datetime

# --- CONFIGURAÇÕES ---
ZABBIX_URL = "http://localhost/zabbix/api_jsonrpc.php"

# SEGURANÇA (Token via Variável de Ambiente)
TOKEN = os.getenv('ZABBIX_TOKEN')
if not TOKEN:
    print("❌ ERRO: Variável ZABBIX_TOKEN não definida.")
    sys.exit(1)

HEADERS = {'Content-Type': 'application/json-rpc', 'Authorization': f'Bearer {TOKEN}'}

def enviar_pedido(metodo, parametros):
    payload = {"jsonrpc": "2.0", "method": metodo, "params": parametros, "id": 1}
    try:
        resposta = requests.post(ZABBIX_URL, data=json.dumps(payload), headers=HEADERS)
        return resposta.json().get('result')
    except Exception:
        sys.exit(1)

# --- AUTOMAÇÃO ---

print("🔐 Autenticando e buscando dados...")

# BUSCA DO GRUPO
grupos = enviar_pedido("hostgroup.get", {"output": "extend", "filter": {"name": ["Databases"]}})
if not grupos: sys.exit("Grupo não encontrado.")
id_grupo = grupos[0]['groupid']

# BUSCA DOS HOSTS (Filtro: BD- + Desabilitados)
filtro = {
    "output": ["name", "host", "status", "hostid"], # Trazendo mais campos
    "groupids": id_grupo,
    "search": {"name": "BD-"},
    "startSearch": True,
    "filter": {"status": "1"} # 1 = Desabilitado
}

hosts = enviar_pedido("host.get", filtro)

if not hosts:
    print("✅ Nenhum host desabilitado encontrado. O Excel não será gerado.")
    sys.exit()

# --- A MÁGICA DO EXCEL (PANDAS) ---

print(f"📊 Processando {len(hosts)} linhas para o Excel...")

# 1. Criamos uma lista limpa apenas com o que queremos no Excel
dados_para_excel = []

for h in hosts:
    # Adicionamos um dicionário para cada linha da planilha
    dados_para_excel.append({
        "ID do Zabbix": h['hostid'],
        "Nome do Servidor": h['name'],# Nome técnico
        "Status": "DESABILITADO",
        "Data da Coleta": datetime.now().strftime("%d/%m/%Y %H:%M")
    })

# 2. Transformamos essa lista num DataFrame (Tabela Inteligente)
df = pd.DataFrame(dados_para_excel)

# 3. Gerar o Nome do Arquivo com Data (para não sobrescrever)
data_hoje = datetime.now().strftime("%Y-%m-%d_%H-%M")
nome_arquivo = f"Relatorio_Inativos_{data_hoje}.xlsx"

# 4. Salvar em Excel (Sem o índice numérico 0,1,2 na esquerda)
df.to_excel(nome_arquivo, index=False)

print("-" * 50)
print(f"✅ SUCESSO! Arquivo gerado: {nome_arquivo}")
print(f"📂 Local: {os.getcwd()}/{nome_arquivo}")
print("-" * 50)