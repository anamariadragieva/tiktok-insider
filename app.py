from flask import Flask, render_template, request, jsonify
from apify_fetch import run_actor
import mysql.connector

app = Flask(__name__)
app.secret_key = "a8d9f7g6h5j4k3l2m1n0qwerty"

def insert_data_to_db(data, keyword):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vampire98",
        database="social_data"
    )
    cursor = conn.cursor()

    for item in data:
        try:
            video_id = item.get("id")
            authorMeta = item.get("authorMeta", {})
            username = authorMeta.get("name", "")
            description = item.get("text", "")
            views = item.get("playCount", 0)
            likes = item.get("diggCount", 0)
            comments = item.get("commentCount", 0)
            video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"

            cursor.execute("""
                INSERT INTO tiktoks (id, username, description, views, likes, comments, video_url, keyword)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    description=VALUES(description),
                    views=VALUES(views),
                    likes=VALUES(likes),
                    comments=VALUES(comments),
                    video_url=VALUES(video_url),
                    keyword=VALUES(keyword)
            """, (video_id, username, description, views, likes, comments, video_url, keyword))

        except Exception as e:
            print(f"Error inserting item {video_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/fetch_data')
def fetch_data():
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify([])

    try:
        data = run_actor(searchQueries=[keyword])
        insert_data_to_db(data, keyword)

        # Fetch most recent 20 entries for this keyword
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="vampire98",
            database="social_data"
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, description, views, likes, comments, video_url
            FROM tiktoks
            WHERE keyword = %s
            ORDER BY id DESC
            LIMIT 20
        """, (keyword,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(results)

    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify([]), 500

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
