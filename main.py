from flask import Flask

UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print('registring demo')
from blueprints.demo import bp as demo_bp
app.register_blueprint(demo_bp)

if (__name__ == "__main__"):
    app.run()