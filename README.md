# ChatBot Fiscal

O Chat Bot Fiscal é um projeto que utiliza tecnologias de processamento de linguagem natural (NLP) e infraestrutura em nuvem para fornecer respostas a perguntas jurídicas com base em documentos armazenados em um bucket S3. O chatbot é acessível via Telegram e utiliza um motor de Retrieval-Augmented Generation (RAG) para gerar respostas precisas e contextualizadas.

## Funcionalidades

- **Upload de Documentos**: Carrega documentos jurídicos de um diretório local para um bucket S3.
- **Processamento de Documentos**: Utiliza embeddings e modelos de linguagem da AWS Bedrock para indexar e consultar documentos.
- **Chatbot no Telegram**: Interface de usuário via Telegram para interagir com o chatbot.
- **Logs e Monitoramento**: Integração com Amazon CloudWatch para monitoramento e registro de logs.

## Estrutura do Projeto

- **Infraestrutura como Código (IaC)**: Utiliza Terraform para provisionar recursos na AWS, incluindo VPC, EC2, S3, e CloudWatch.
- **Backend**: Implementado em Python, utilizando bibliotecas como `boto3`, `langchain`, e `telebot`.
- **Frontend**: Interface de usuário via Telegram.

## Pré-requisitos

- **Conta AWS**: Necessário ter uma conta AWS com permissões para criar e gerenciar recursos.
- **Terraform**: Instalado e configurado na máquina local.
- **Python 3.8+**: Necessário para executar o código do chatbot.
- **Telegram Bot Token**: Token de acesso para o bot do Telegram.

## Configuração

### 1. Configuração do Terraform

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/legal-chatbot.git
   cd legal-chatbot
2. Inicialize o Terraform:
    ```bash
    terraform init
3. Aplique a configuração do Terraform para criar os recursos na AWS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
#
### 2. Configuração do Ambiente Python

1. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
2. Instale as dependências:
    ```bash
    pip install -r requirements.txt
#

### 3. Configuração do Telegram Bot

1. Crie um bot no Telegram utilizando o BotFather e obtenha o token de acesso.
2. Configure a variável de ambiente TELEGRAM_TOKEN no arquivo main.py ou exporte-a no terminal:
   ```bash
   export TELEGRAM_TOKEN="seu-token-aqui"

### Executando o Projeto

1. Execute o script principal:
  ```bash
  python main.py
```
2. Interaja com o bot no Telegram enviando mensagens para ele.
#

## Estrutura do Projeto

### Backend
- `s3_loader.py`: Carrega documentos do S3 e faz upload de documentos locais.
- `rag_engine.py`: Implementa o motor RAG para consultar documentos.
- `telegram_bot.py`: Implementa o bot do Telegram.
- `main.py`: Script principal para inicializar o chatbot.

### Infraestrutura
- `main.tf`: Configuração do Terraform para provisionar recursos na AWS.
- `variables.tf`: Define variáveis para o Terraform.
- `outputs.tf`: Define outputs para o Terraform.

### Logs
- `logging_setup.py`: Configuração de logs com CloudWatch.
