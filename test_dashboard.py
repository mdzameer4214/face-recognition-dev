from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "DASHBOARD IS WORKING"

if __name__ == "__main__":
    print("Starting dashboard...")
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
