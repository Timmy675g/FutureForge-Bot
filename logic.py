import sqlite3

DATABASE = "futureforge.db"


def get_connection():
    return sqlite3.connect(DATABASE)


class CareerLogic:

    def analyze_user(self, message): # Extract keywords from the user message. For Example: 'I like coding and AI' so the keywords will be ['coding', 'ai']
        message = message.lower()

        STOP_WORDS = {
            "i", "me", "my",
            "like", "love", "enjoy",
            "and", "or", "the", "a", "an",
            "to", "of", "is", "am"
        }

        keywords = [
            word
            for word in message.replace(",", "").split()
            if word not in STOP_WORDS
        ]

        return keywords


    def search_database(self, keywords):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                title,
                category,
                description,
                salary_min,
                salary_max
            FROM careers
        """)

        careers = []

        for career in cursor.fetchall():

            career_id = career[0]

            # Load skills
            cursor.execute(
                """
                SELECT skill
                FROM career_skills
                WHERE career_id = ?
                """,
                (career_id,)
            )
            skills = [row[0].lower() for row in cursor.fetchall()]

            # Load interests
            cursor.execute(
                """
                SELECT interest
                FROM career_interests
                WHERE career_id = ?
                """,
                (career_id,)
            )
            interests = [row[0].lower() for row in cursor.fetchall()]

            score = 0

            for keyword in keywords:

                if keyword in skills:
                    score += 20

                if keyword in interests:
                    score += 10

            if score > 0:
                careers.append({
                    "id": career_id,
                    "title": career[1],
                    "category": career[2],
                    "description": career[3],
                    "salary_min": career[4],
                    "salary_max": career[5],
                    "score": score
                })

        conn.close()

        return careers

    def rank_results(self, careers): # It will Sort careers from highest score so like Software Engineer with 30% will be on top and if a Data Scientist has 20% it will be below it.

        careers.sort(
            key=lambda career: career["score"],
            reverse=True
        )

        return careers


    def create_recommendation(self, careers): # Return the top three recommendations.

        return careers[:3]