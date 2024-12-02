import logging
import boto3
from botocore.exceptions import ClientError

class CloudWatchLogHandler(logging.Handler):
    """Handler customizado para envio de logs ao Amazon CloudWatch."""
    def __init__(self, log_group, log_stream, cloudwatch_logs):
        super().__init__()
        self.log_group = log_group
        self.log_stream = log_stream
        self.cloudwatch_logs = cloudwatch_logs

        try:
            # Cria o log group se não existir
            self.cloudwatch_logs.create_log_group(logGroupName=self.log_group)
        except self.cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
            pass

        try:
            # Cria o log stream se não existir
            self.cloudwatch_logs.create_log_stream(
                logGroupName=self.log_group,
                logStreamName=self.log_stream
            )
        except self.cloudwatch_logs.exceptions.ResourceAlreadyExistsException:
            pass

    def emit(self, record):
        try:
            msg = self.format(record)
            self.cloudwatch_logs.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[
                    {
                        'timestamp': int(record.created * 1000),
                        'message': msg
                    }
                ]
            )
        except Exception:
            self.handleError(record)

def setup_logger():
    """Configura logger com CloudWatch"""
    logger = logging.getLogger('legal_chatbot')
    logger.setLevel(logging.INFO)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    
    # CloudWatch Handler
    try:
        cloudwatch_logs = boto3.client('logs')
        cloudwatch_handler = CloudWatchLogHandler(
            log_group='/aws/chatbot/legal-documents',
            log_stream='chatbot_logs',
            cloudwatch_logs=cloudwatch_logs
        )
        cloudwatch_handler.setLevel(logging.INFO)
        logger.addHandler(cloudwatch_handler)
    except ClientError as e:
        print(f"Erro ao configurar CloudWatch: {e}")
    
    return logger

# Uso do logger
logger = setup_logger()
logger.info("Teste de log no CloudWatch")