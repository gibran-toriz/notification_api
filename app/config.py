import os
import hvac
import logging
import urllib3

# Suppress InsecureRequestWarning warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    VAULT_URL = os.getenv('VAULT_URL')
    VAULT_TOKEN = os.getenv('VAULT_TOKEN')
    SECRET_PATH = os.getenv('SECRET_PATH')
    SECRET_KEY = os.getenv('SECRET_KEY')

    @staticmethod
    def get_vault_secret(secret_path, secret_key):
        try:
            client = hvac.Client(url=Config.VAULT_URL, token=Config.VAULT_TOKEN, verify=False)
            # Fetch the secret using the correct method and path
            secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
            return secret['data']['data'][secret_key]
        except hvac.exceptions.InvalidPath as e:
            logger.error(f"Invalid path: {e}, on get {Config.VAULT_URL}/v1/secret/data/{secret_path}")
            raise
        except hvac.exceptions.VaultError as e:
            logger.error(f"Error connecting to Vault: {e}")
            raise
        except KeyError:
            logger.error(f"Secret key {secret_key} not found in path {secret_path}")
            raise

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    elif env == 'production':
        return ProductionConfig
    else:
        raise ValueError(f"Unknown FLASK_ENV: {env}")
