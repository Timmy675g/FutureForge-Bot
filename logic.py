import sqlite3
from ai import AI

DATABASE = "futureforge.db"

def get_connection():
    return sqlite3.connect(DATABASE)

class CareerLogic:

    def extract_keywords(self, message): # Extract keywords from the user message. For Example: 'I like coding and AI' so the keywords will be ['coding', 'ai']
         return AI.extract_keywords(message)


    def search_database(self, keywords):
        
        keywords = [k.lower().strip() for k in keywords]

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
            title = career[1].lower()
            description = (career[3] or "").lower()

            score = 0
            matches = []
            description_words = description.split()

            for keyword in keywords:
                if keyword == title:
                    score += 40
                    matches.append(keyword)

                elif keyword in title:
                    score += 30
                    matches.append(keyword)

                if keyword in skills:
                    score += 20
                    matches.append(keyword)

                if keyword in interests:
                    score += 10
                    matches.append(keyword)

                if keyword in description_words:
                    score += 5
                    matches.append(keyword)
                
            if score > 0:
                careers.append({
                    "id": career_id,
                    "title": career[1],
                    "category": career[2],
                    "description": career[3],
                    "salary_min": career[4],
                    "salary_max": career[5],
                    "score": score,
                    "matches": list(set(matches))
                })

        conn.close()

        return careers

    def rank_results(self, careers): # It will Sort careers from highest score so like Software Engineer with 30% will be on top and if a Data Scientist has 20% it will be below it.

        careers.sort(
        key=lambda career: career["score"],
        reverse=True
    )

        if not careers:
            return []

        if careers[0]["score"] < 40:
            return []

        highest = careers[0]["score"]

        for career in careers:
            career["match"] = round(
                career["score"] / highest * 100
            )

        return careers

    def create_recommendation(self, careers): # Return the top three recommendations.

        return careers[:3]