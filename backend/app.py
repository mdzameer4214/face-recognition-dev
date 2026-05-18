from flask import Flask
from backend.api.routes import api_bp

app = Flask(__name__)

app.register_blueprint(api_bp)

@app.route("/")
def home():
    return {
        "message": "Enterprise Face Recognition API Running"
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )