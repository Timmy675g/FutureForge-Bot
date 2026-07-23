import sqlite3

class Database:
    def __init__(self, db_name="futureforge.db"):
        print("Initializing database...")
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    # Browse Careers
    def get_all_careers(self):
        self.cursor.execute("""
            SELECT category, title
            FROM careers
            ORDER BY category, title
        """)
        return self.cursor.fetchall()

    # Career Details
    def get_career_by_name(self, title):
        self.cursor.execute("""
            SELECT *
            FROM careers
            WHERE LOWER(title)=LOWER(?)
        """, (title,))
        return self.cursor.fetchone()

    # Skills
    def get_skills(self, career_id):
        self.cursor.execute("""
            SELECT skill
            FROM career_skills
            WHERE career_id=?
            ORDER BY skill
        """, (career_id,))

        return [row[0] for row in self.cursor.fetchall()]

    # Interests
    def get_interests(self, career_id):
        self.cursor.execute("""
            SELECT interest
            FROM career_interests
            WHERE career_id=?
            ORDER BY interest
        """, (career_id,))

        return [row[0] for row in self.cursor.fetchall()]

    # Roadmap Lines
    def get_roadmap(self, career_id):
        self.cursor.execute("""
            SELECT step_order, step
            FROM career_roadmap
            WHERE career_id=?
            ORDER BY step_order
        """, (career_id,))

        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    print("Database initialized successfully!")
    db.close()