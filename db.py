import sqlite3

class Database:
    def __init__(self, db_name="futureforge.db"):
        print("Initializing database...")
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS careers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                education TEXT,
                salary_range TEXT,
                remote_friendly INTEGER DEFAULT 0,
                difficulty INTEGER,
                image_url TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                career_id INTEGER NOT NULL,
                skill TEXT NOT NULL,
                FOREIGN KEY (career_id) REFERENCES careers(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_interests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                career_id INTEGER NOT NULL,
                interest TEXT NOT NULL,
                FOREIGN KEY (career_id) REFERENCES careers(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS career_roadmap (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                career_id INTEGER NOT NULL,
                step_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                FOREIGN KEY (career_id) REFERENCES careers(id)
            )
        """)

        self.conn.commit()
        
if __name__ == "__main__":
    db = Database()
    print("Database created successfully!")
    db.close()