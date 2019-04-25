import os

class Config:
    pass

class ProdConfig(config):
    pass

class DevConfig(config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
    
}