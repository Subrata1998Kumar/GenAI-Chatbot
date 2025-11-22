import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        self.__project_root = Path(__file__).parent.parent
        self.__load_environment_variables() # no return value
        self.__config = self.__load_config_ini()

    def __load_environment_variables(self):
        env_file = self.__project_root / '.env'
        if env_file.exists():
            load_dotenv(env_file)
        else:
            raise FileNotFoundError(f".env file not found at {env_file}")
    
    def __load_config_ini(self):
        config_file = self.__project_root / 'config.ini'
        config = configparser.ConfigParser()

        if config_file.exists():
            config.read(config_file)
            return config
        else:
            raise FileNotFoundError(f"config.ini file not found at {config_file}")

    def get_env_variable(self, source: str, key: str, section: str = None) -> str:
        if source == 'config':
            if section is None:
                raise ValueError("section is required when source='config'")
            return self.__config.get(section, key)
        elif source == 'env':
            return os.getenv(key)
        else:
            raise ValueError("source must be 'config' or 'env'")

if __name__ == "__main__":
    cm = ConfigManager()
    hug_key = cm.get_env_variable(source='env', key='HUG_KEY')
    sentence_embedding_model = cm.get_env_variable(source='config', key='SENTENCE_EMBEDDING_MODEL', section='VECTOR_DB')
    print("Hugging Face Key:", hug_key)
    print("Sentence Embedding Model:", sentence_embedding_model)      