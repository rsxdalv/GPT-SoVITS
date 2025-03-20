import os, json
from typing import List, Any, Optional ,Dict, Literal   
from pydantic import BaseModel, Field, model_validator
from ..Synthesizers.base import load_config

__version__ = "2.6.3"

common_config : dict = {}
# Read version from common config
try:
    with open('common_config.json', 'r') as f:
        common_config = json.load(f)
except:
    common_config = {
        "version": "0.1.0",
        "inbrowser":True,
        "is_share":False,
        "synthesizer": "gsv_fast",
        "server_name": "127.0.0.1",
        "server_port": 5000,
        "also_enable_api": False,
        "locale": "en_US",
        "max_text_length": 60,
    }
    os.makedirs(os.path.dirname("common_config.json"), exist_ok=True)
    with open('common_config.json', 'w') as f:
        json.dump(common_config, f, indent=4, ensure_ascii=False)

class CommonConfigManager:
    version: str = common_config.get("version", "0.1.0")
    synthesizer: str = common_config.get("synthesizer", "gsv_fast")
    server_name: str = common_config.get("server_name", "127.0.0.1")
    server_port: int = common_config.get("server_port", 5000)
    is_share: bool = common_config.get("is_share", False)
    inbrowser: bool = common_config.get("inbrowser", True)
    also_enable_api: bool = common_config.get("also_enable_api", False)
    locale: str = common_config.get("locale", "en_US")
    max_text_length: int = common_config.get("max_text_length", 60)

    def update(self, key:str, value:Any) -> None:
        if hasattr(self, key):
            setattr(self, key, value)
            common_config[key] = value
            with open("common_config.json", "w", encoding="utf-8") as f:
                json.dump(common_config, f, indent=4, ensure_ascii=False)

class Api_Config(BaseModel):   
    config_path:str = None
    tts_port: int = 5000
    tts_host: str = "0.0.0.0" 
    synthesizer: str = "gsv_fast"


    def __init__(self, config_path = None):
        super().__init__()
        
        self.config_path = config_path
        assert os.path.exists(self.config_path), f"配置文件不存在: {self.config_path}"
        if os.path.exists(self.config_path):
            all_config = load_config(self.config_path)
            config:dict = all_config.get("common", {})
            for key, value in config.items():
                setattr(self, key, value)
        
class App_Config(BaseModel):

    config_path:str = None
    locale: str = "auto"
    is_share: bool = False
    inbrowser: bool = True
    server_name: str = "0.0.0.0"
    server_port: int = -1 # -1 means auto select
    also_enable_api: bool = True
    synthesizer: str = "gsv_fast"
    max_text_length: int = -1

    @model_validator(mode='after')
    def check_locale(self):
        # Example: validating locale to be one of a set predefined values or patterns
        self.locale = self.locale.replace("-", "_")
        return self

    @staticmethod
    def check_port(port:int, server_name:str):
        url = f"http://{server_name}:{port}"
     
    
    def __init__(self, config_path = None):
        super().__init__()
        
        self.config_path = config_path
        assert os.path.exists(self.config_path), f"配置文件不存在: {self.config_path}"
        if os.path.exists(self.config_path):
            all_config = load_config(self.config_path)
            config = all_config.get("app_config", {})
            for key, value in config.items():
                setattr(self, key, value)

app_config = App_Config("common_config.json")
api_config = Api_Config("common_config.json")


