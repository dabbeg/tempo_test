from flask import Flask
from redis import Redis

# Start flask and redis
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

# Register blueprints
from app.api.role import role as role_module
from app.api.membership import membership as membership_module

app.register_blueprint(role_module)
app.register_blueprint(membership_module)
