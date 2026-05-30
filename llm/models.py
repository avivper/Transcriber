import os
from google import genai 
from dotenv import load_dotenv

def list_gemini_models():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    try:
        client = genai.Client(api_key=api_key)

        for model in client.models.list():
            actions = ",".join(model.name)
            print(f"{model.name:<40} | {actions}")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    list_gemini_models()