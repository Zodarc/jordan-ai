from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file to get the API key
load_dotenv()

app = Flask(__name__)

# Set up OpenRouter client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"  # This is OpenRouter's base URL
)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    blog = ""
    language = "English"
    error = None
    languages = ["English", "Swahili", "Spanish", "French", "Portuguese", "German", "Chinese", "Korean"]

    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        language = request.form.get("language", "English")

        if not prompt:
            error = "Please enter a blog topic."
        else:
            try:
                response = client.chat.completions.create(
                    model="mistralai/mistral-7b-instruct",  # OpenRouter model
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a blog writer creating content in {language}."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                blog = response.choices[0].message.content.strip()
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template("index.html", blog=blog, prompt=prompt, language=language, error=error, languages=languages)

if __name__ == "__main__":
    app.run(debug=True)
