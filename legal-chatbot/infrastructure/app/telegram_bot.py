import telebot
from utils.logging import setup_logger
from rag_engine import RAGEngine

class TelegramLegalChatbot:
    def __init__(self, token: str, rag_engine: RAGEngine):
        self.bot = telebot.TeleBot(token)
        self.rag_engine = rag_engine
        self.logger = setup_logger()
        
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(
                message, 
                "Bem-vindo ao Zakbot! Como posso ajudar?"
            )
        @self.bot.message_handler(commands=['help'])
        def send_help(message):
            self.bot.reply_to(
                message,
                "Comandos disponíveis: /start, /help, /status")
        
        @self.bot.message_handler(func=lambda msg: True)
        def handle_message(message):
            try:
                pergunta = message.text
                resposta = self.rag_engine.query(pergunta)
                
                self.logger.info(f"Pergunta: {pergunta}")
                self.logger.info(f"Resposta: {resposta}")
                
                self.bot.reply_to(message, resposta)
            
            except Exception as e:
                self.logger.error(f"Erro: {e}")
                self.bot.reply_to(
                    message, 
                    "Desculpe, ocorreu um erro ao processar sua pergunta."
                )
    
    def start(self):
        self.bot.polling()
