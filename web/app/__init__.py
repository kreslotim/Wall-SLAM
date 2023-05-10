from flask import Flask
from flask_bootstrap import Bootstrap


from flask import Flask

def create_app():
    app = Flask(__name__)
    Bootstrap(app)


    # load configuration from config.py
    #app.config.from_object('config.Config')

    # register blueprints
    from . import routes
    app.register_blueprint(routes.main)



    return app
