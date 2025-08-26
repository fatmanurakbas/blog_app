from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()  # CSRF koruması (formlar için önerilir)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    # Blueprint'leri buraya ekle
    from app.routes import main
    app.register_blueprint(main)
   
    
    return app



