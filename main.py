from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

API_URL = "https://api.harmon.com.tr/ai/chat/openai/gpt-4o"
API_KEY = "hrmn_4tlfwcr4ljg5eknnbpgf2q"

@app.route('/')
def home():
    return '''
    <h1>Prompt Generator</h1>
    <form action="/generate" method="post">
        <label for="prompt">Enter your prompt:</label><br>
        <textarea id="prompt" name="prompt" rows="4" cols="50"></textarea><br>
        <button type="submit">Generate Response</button>
    </form>
    '''

@app.route('/generate', methods=['POST'])
def generate_response():
    prompt = request.form['prompt']
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "history": []
    }

    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json().get('response', 'No response generated')
        return render_template_string('''
        <h1>Generated Response</h1>
        <pre>{{ result }}</pre>
        <a href="/">Generate another response</a>
        ''', result=result)
    else:
        return jsonify({"error": "Failed to generate response"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=25560)
