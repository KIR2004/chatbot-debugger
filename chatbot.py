import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Set your OpenAI API Key
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def get_solution(code, error_message):
    """Function to generate a solution for the given code error."""
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
        messages=[{"role": "system", "content": "You are an expert programmer and debugger."},
                  {"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    return response["choices"][0]["message"]["content"].strip()

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

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get the port dynamically
    app.run(host="0.0.0.0", port=port, debug=True)

