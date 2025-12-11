# Automação de Relatórios Zabbix com Pandas

Este projeto é uma ferramenta de automação que conecta à API do Zabbix, coleta informações sobre hosts (focando em bancos de dados) e gera relatórios gerenciais em Excel automaticamente.

## 🚀 Funcionalidades

- **Conexão via API:** Autenticação segura via token.
- **Filtros Inteligentes:** Seleciona apenas hosts do grupo "Databases" que estão desabilitados.
- **Processamento de Dados:** Utiliza `pandas` para estruturar e limpar os dados JSON brutos.
- **Exportação Excel:** Gera planilhas `.xlsx` com nomes versionados por data.

## 🛠️ Tecnologias Utilizadas

- Python 3.12.3
- Pandas (Manipulação de dados)
- Requests (Consumo de API HTTP)
- Zabbix API
- OpenPyXL (Engine para Excel)

## 📦 Como usar

1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt

## ⚙️ Configuração e Variáveis de Ambiente

Por questões de segurança, este projeto não armazena credenciais no código.
Para executá-lo, você deve configurar a seguinte variável de ambiente com o seu token de acesso:

**Variável Obrigatória:**
- `ZABBIX_TOKEN`: O token de autenticação gerado na interface do Zabbix.

### Como configurar (Exemplos):

**No Linux/Mac (Terminal):**
```bash
export ZABBIX_TOKEN="insira_seu_token_aqui_sem_aspas"
