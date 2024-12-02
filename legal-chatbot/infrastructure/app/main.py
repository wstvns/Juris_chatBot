import sys
import os

# Adicionar o diretório src ao PYTHONPATH dinamicamente
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from s3_loader import S3DocumentLoader
from rag_engine import RAGEngine
from telegram_bot import TelegramLegalChatbot

def main():
    # Configurações
    BUCKET_NAME = 'legal-chatbot-documentos-91n2fcra' 
    TELEGRAM_TOKEN = "7794143543:AAGsrhwgU-xKkGWwCjMLk6D6JIwPMDEL7OQ"  # meu token hardcodado
    LOCAL_DATASET_PATH = './dataset/documentos_juridicos'

    # verificad se o token do telegram foi configurado
    if not TELEGRAM_TOKEN:
        raise ValueError("A variável de ambiente TELEGRAM_BOT_TOKEN não foi configurada!")

    # Carregamento de Documentos
    s3_loader = S3DocumentLoader(BUCKET_NAME)
    print(f"Carregando documentos do diretório {LOCAL_DATASET_PATH} para o bucket S3 '{BUCKET_NAME}'...")
    s3_loader.upload_documents(LOCAL_DATASET_PATH)
    print("Documentos carregados com sucesso!")

    # Motor RAG
    print("Inicializando o motor RAG...")
    rag_engine = RAGEngine(s3_loader, BUCKET_NAME)
    print("Motor RAG inicializado com sucesso!")

    # Bot do Telegram
    print("Iniciando o chatbot no Telegram...")
    telegram_bot = TelegramLegalChatbot(TELEGRAM_TOKEN, rag_engine)
    telegram_bot.start()

if __name__ == '__main__':
    main()
