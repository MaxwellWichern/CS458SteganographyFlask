from flask import Flask

app = Flask(__name__)

print('registring demo')
from blueprints.demo import bp as demo_bp
app.register_blueprint(demo_bp)

if (__name__ == "__main__"):
    app.run()