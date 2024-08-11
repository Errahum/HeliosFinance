import logging
import os

# Configuration des chemins de log
log_dir = 'logs'
info_log_file_path = os.path.join(log_dir, 'application_info.log')
error_log_file_path = os.path.join(log_dir, 'application_error.log')

# Créez le répertoire des logs s'il n'existe pas
os.makedirs(log_dir, exist_ok=True)

# Configuration des handlers
info_handler = logging.FileHandler(info_log_file_path)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

error_handler = logging.FileHandler(error_log_file_path)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Permet de capturer tous les niveaux de log
logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(logging.StreamHandler())  # Pour afficher les logs dans la console

# Utilisation de handlers différents pour les niveaux info et erreur
logger.info_handler = info_handler
logger.error_handler = error_handler
