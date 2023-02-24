from flask import Flask
from selenium import webdriver
from flask import url_for
from .selenium import crawl
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    from . import models
    from .models import Data
    app.config.from_object(config)
    from .view import main_view
    app.register_blueprint(main_view.main)

    db.init_app(app)
    migrate.init_app(app, db)


    


    


    

    if __name__ == '__main__':
        db.create_all()
        app.run(host='0.0.0.0', port=80)


    return app

