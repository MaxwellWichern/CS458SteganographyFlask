from flask import Flask
from flask_cors import CORS

UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from blueprints.demo import bp as demo_bp
app.register_blueprint(demo_bp)

from blueprints.textSteg import bp as textSteg_bp
app.register_blueprint(textSteg_bp)

if (__name__ == "__main__"):
    app.run()