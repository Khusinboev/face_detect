import sqlite3

# Baza yaratish va ulanish
conn = sqlite3.connect('mydata.db')
cur = conn.cursor()

# Birinchi jadvalni yaratish
cur.execute('''CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY,
                name VARCHAR
            )''')

# Ikkinchi jadvalni yaratish va bog'lash
cur.execute('''CREATE TABLE IF NOT EXISTS faces_photos (
                id INTEGER PRIMARY KEY,
                person_id INTEGER,
                image BLOB,
                FOREIGN KEY (person_id) REFERENCES persons(id) ON DELETE CASCADE
            )''')

# Birinchi jadvalga ma'lumot kiritish
cur.execute("INSERT INTO persons (name) VALUES (?)", ('Xijinpin',))
person_id = cur.lastrowid

# Ikkinchi jadvalga rasmni kiritish
with open('face8.jpg', 'rb') as f:
    image_data = f.read()
cur.execute("INSERT INTO faces_photos (person_id, image) VALUES (?, ?)", (person_id, sqlite3.Binary(image_data)))

# O'zgartirishlarni saqlash va bog'lanishni bekor qilish
conn.commit()

# Ma'lumotlarni o'qish va rasmlarni o'qish
cur.execute("SELECT p.name, fp.image FROM persons p JOIN faces_photos fp ON p.id = fp.person_id")
rows = cur.fetchall()
for row in rows:
    print("Name:", row[0])
    with open("retrieved_image.jpg", "wb") as f:
        f.write(row[1])

# Bog'lanishni bekor qilish
cur.close()
conn.close()
