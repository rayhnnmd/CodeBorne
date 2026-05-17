from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.achievements import achievements_bp
    from routes.profile import profile_bp
    from routes.leaderboard import leaderboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(achievements_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(leaderboard_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)