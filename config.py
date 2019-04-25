import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://gichimu:trio.com@localhost/pitch_app'

class ProdConfig(config):
    pass

class DevConfig(config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
    
}