"""Application factory for the Bloomberg AI Infrastructure Platform."""
from flask import Flask
from flask_cors import CORS
from config import config

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    app.config.from_object(config[config_name])

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.api.bloomberg_routes import bloomberg_bp
    from app.api.ai_routes import ai_bp
    from app.api.training_routes import training_bp
    from app.api.dashboard_routes import dashboard_bp

    app.register_blueprint(bloomberg_bp, url_prefix='/api/bloomberg')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(training_bp, url_prefix='/api/training')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # Main route
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
