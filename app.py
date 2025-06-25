from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.secrets import secrets_bp
from utils.db_init import initialize_db


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

initialize_db()

app.register_blueprint(auth_bp)
app.register_blueprint(secrets_bp)

if __name__ == '__main__':
    app.run(debug=True)