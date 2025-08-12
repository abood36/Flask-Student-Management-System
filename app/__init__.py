import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager, csrf
from .auth import auth as auth_bp
from .students import students as students_bp

def create_app(config_class=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class or Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(students_bp, url_prefix="")

    # simple index route
    @app.route("/")
    def index():
        return app.send_static_file("index.html") if os.path.exists(app.static_folder + "/index.html") else ("", 204)

    # CLI helper to create admin
    @app.cli.command("create-admin")
    def create_admin():
        """Create initial admin user from CLI"""
        from .models import User
        import getpass
        username = input("Admin username: ").strip()
        if not username:
            print("username required")
            return
        pw = getpass.getpass("Admin password: ")
        if not pw:
            print("password required")
            return
        # create user
        from .extensions import db as _db
        if User.query.filter_by(username=username).first():
            print("user already exists")
            return
        user = User.create_admin(username, pw)
        _db.session.add(user)
        _db.session.commit()
        print("Admin user created.")

    return app
