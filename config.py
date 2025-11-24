"""Application configuration management."""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Bloomberg API Configuration
    BLOOMBERG_HOST = os.environ.get('BLOOMBERG_HOST', 'localhost')
    BLOOMBERG_PORT = int(os.environ.get('BLOOMBERG_PORT', 8194))
    BLOOMBERG_TIMEOUT = int(os.environ.get('BLOOMBERG_TIMEOUT', 30000))

    # AI Agent Configuration
    AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

    # Application settings
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
