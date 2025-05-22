from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vampire98",
        database="social_data"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tiktoks ORDER BY views DESC LIMIT 20")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
