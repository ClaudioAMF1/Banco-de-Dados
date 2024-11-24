import logging
from datetime import datetime
import os

class Logger:
    def __init__(self):
        # Criar diretório de logs se não existir
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        # Configurar logging
        logging.basicConfig(
            filename=f'logs/sistema_{datetime.now().strftime("%Y%m%d")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SistemaAcademia')

    def info(self, message):
        self.logger.info(message)

    def error(self, message, exc_info=True):
        self.logger.error(message, exc_info=exc_info)

    def warning(self, message):
        self.logger.warning(message)

    def log_acesso(self, usuario, pagina):
        self.info(f"Acesso - Usuário: {usuario} - Página: {pagina}")

    def log_operacao(self, usuario, operacao, status):
        self.info(f"Operação - Usuário: {usuario} - Operação: {operacao} - Status: {status}")

    def log_erro(self, usuario, erro):
        self.error(f"Erro - Usuário: {usuario} - Erro: {str(erro)}")