from flask import Flask
from config import Config
from extensions import db, login_manager
from routes.application_routes import application_bp
from routes.auth_routes import auth_bp
from models.application import Application
from models.user import User

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(application_bp)
app.register_blueprint(auth_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, port=5001)