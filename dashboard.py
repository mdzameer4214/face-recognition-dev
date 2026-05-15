from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "database.db"

@app.route("/")
def index():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM attendance ORDER BY id DESC")
    attendance = cur.fetchall()

    cur.execute("SELECT * FROM movement_log ORDER BY id DESC")
    movements = cur.fetchall()

    cur.execute("SELECT * FROM unknown_log ORDER BY id DESC")
    unknowns = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        attendance=attendance,
        movements=movements,
        unknowns=unknowns,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)