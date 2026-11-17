import sqlite3

class ValidationError(Exception):
    pass

class WatchlistValidator:
    @staticmethod
    def validate(title_raw, type_raw, genre_raw, status_raw, rating_raw):
        title = title_raw.strip()
        
        if not title:
            raise ValidationError("Title cannot be empty!")
        if type_raw in ["", "Select Type..."]:
            raise ValidationError("Please select a valid Type.")
        if genre_raw in ["", "Select Genre..."]:
            raise ValidationError("Please select a valid Genre.")
        if status_raw in ["", "Select Status..."]:
            raise ValidationError("Please select a valid Watch Status.")
            
        
        if status_raw == "Watched":
            if rating_raw in ["", "Select Rating...", "No Rating"]:
                raise ValidationError("Please select a valid Rating for watched content.")
        
        elif status_raw == "Plan to Watch":
            rating_raw = "No Rating"
            
        return title, type_raw, genre_raw, status_raw, rating_raw


class DatabaseHelper:
    def __init__(self, db_name="watchlist.db"):
        self.db_name = db_name
        self._init_db()#sınıf çağırıldığında veritabani kur

    def get_connection(self):#her veritabani icin baglanti ac
        return sqlite3.connect(self.db_name)

    def _init_db(self):#islem bitince baglantinin otomatik kapanmasini sagladik guvenlik icin
        with self.get_connection() as conn:
            cursor = conn.cursor()
            #movies adinda bir tablomuz yoksa bastan olustur
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    media_type TEXT DEFAULT 'Movie',
                    genre TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            ''')

            #tabloda rating sütunu yoksa eski verileri silmeden sütun ekle
            cursor.execute("PRAGMA table_info(movies)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'rating' not in columns:
                cursor.execute("ALTER TABLE movies ADD COLUMN rating TEXT DEFAULT 'No Rating'")

    #yeni film ekleme sorgusu
    def insert_entry(self, title, media_type, genre, status, rating):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movies (title, media_type, genre, status, rating) VALUES (?, ?, ?, ?, ?)", 
                           (title, media_type, genre, status, rating))

    #butun kayitlari tablo icin cekme
    def get_all_entries(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, media_type, genre, status, rating FROM movies")
            return cursor.fetchall()

    
    def get_entries_by_status(self, status):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, media_type, genre, status, rating FROM movies WHERE status=?", (status,))
            return cursor.fetchall()

    
    def update_entry(self, entry_id, title, media_type, genre, status, rating):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE movies SET title=?, media_type=?, genre=?, status=?, rating=? WHERE id=?", 
                           (title, media_type, genre, status, rating, entry_id))

    #bir kaydi ID sine gore silme
    def delete_entry(self, entry_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM movies WHERE id=?", (entry_id,))

    #grafikler icin her genre den kac tane oldugunu gruplayarak sayma
    def get_statistics(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT genre, COUNT(*) FROM movies GROUP BY genre")
            return cursor.fetchall()