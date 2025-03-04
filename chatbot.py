import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_solution(code, error_message):
    """Generate a solution for the given code error."""
    prompt = f"""
    I have the following code that is throwing an error:
    ```
    {code}
    ```
    The error message is:
    "{error_message}"
    Please analyze and suggest a fix with an explanation.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert programmer and debugger."},
            {"role": "user", "content": prompt}
        ]
    )

    return response["choices"][0]["message"]["content"].strip()

@app.route("/")
def home():
    return "Welcome to the AI Debugging Chatbot!"

@app.route("/debug", methods=["POST"])
def debug():
    """API endpoint to receive code and error message and return a solution."""
    data = request.json
    code = data.get("code")
    error_message = data.get("error_message")

    if not code or not error_message:
        return jsonify({"error": "Both 'code' and 'error_message' are required!"}), 400

    solution = get_solution(code, error_message)
    return jsonify({"solution": solution})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Dynamically assign port
    app.run(host="0.0.0.0", port=port)
