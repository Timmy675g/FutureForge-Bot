import requests

WORKER_URL = "WORKER_URL_HERE"

class AI:

    @staticmethod
    def analyze_profile(profile):
        response = requests.post(
            WORKER_URL,
            json={
                "profile": {
                    "name": profile.name,
                    "education": profile.education,
                    "subjects": profile.subjects,
                    "hobbies": profile.hobbies,
                    "skills": profile.skills,
                    "personality": profile.personality,
                    "goal": profile.goal,
                }
            },
            timeout=30
        )

        if not response.ok:
            print("Status:", response.status_code)
            print("Response:", response.text)
            response.raise_for_status()

        return response.json()["keywords"]