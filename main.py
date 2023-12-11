from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Required for CORS access
# Imports blueprint for app routes
from blueprints.textSteg import bp as textSteg_bp
app.register_blueprint(textSteg_bp)

if (__name__ == "__main__"):
    app.run()