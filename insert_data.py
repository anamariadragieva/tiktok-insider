import json
import mysql.connector


with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


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
        authorMeta = item.get("authorMeta")
        username = authorMeta.get("name")
        print(username)
        description = item.get("text", "")
        views = item.get("playCount")
        likes = item.get("diggCount")
        comments = item.get("commentCount")
        video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"

        cursor.execute("""
            INSERT INTO tiktoks (id, username, description, views, likes, comments, video_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                username = VALUES(username),
                description = VALUES(description),
                views = VALUES(views),
                likes = VALUES(likes),
                comments = VALUES(comments),
                video_url = VALUES(video_url)
        """, (video_id, username, description, views, likes, comments, video_url))
    



    
    except Exception as e:
        print(f"Error inserting item {video_id}: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ Data inserted into MySQL.")


