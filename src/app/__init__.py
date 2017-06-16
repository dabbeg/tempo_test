from flask import Flask
from redis import Redis
from app.config import REDIS_HOST, REDIS_PORT

# Start flask and redis
app = Flask(__name__)
redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

# Register blueprints
from app.api.role import role as role_module
from app.api.membership import membership as membership_module

app.register_blueprint(role_module)
app.register_blueprint(membership_module)

# Initialize data
from app import db_helper
db_helper.init_db()
