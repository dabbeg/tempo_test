from app import app
from app.config import FLASK_HOST, FLASK_PORT, DEBUG

app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)
