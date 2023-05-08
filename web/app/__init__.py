from flask import Flask
from flask_bootstrap import Bootstrap
from web.config import Config

...
def create_app(config_class=Config):
    app = Flask(__name__)
    Bootstrap(app)
    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app