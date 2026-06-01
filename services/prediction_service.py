import requests
from config import Config


API_KEY = Config.OPENROUTER_API_KEY


def generate_health_prediction(

    glucose,
    haemoglobin,
    cholesterol

):

    try:

        prompt = f"""
        Patient Blood Report:

        Glucose: {glucose}
        Haemoglobin: {haemoglobin}
        Cholesterol: {cholesterol}

        IMPORTANT:
        Respond ONLY in 3 short bullet points.
        Maximum 50 words total.
        """

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization": f"Bearer {API_KEY}",

                "Content-Type": "application/json"
            },

            json={

                "model": "openai/gpt-3.5-turbo",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                "temperature": 0.2,

                "max_tokens": 80
            },

            timeout=30
        )

        result = response.json()

        print(result)

        if "choices" in result:

            ai_response = result[
                "choices"
            ][0]["message"]["content"]

            return ai_response.strip()

        elif "error" in result:

            return result["error"]["message"]

        else:

            return "Unable to generate AI prediction."

    except Exception as e:

        return f"API Error: {str(e)}"
