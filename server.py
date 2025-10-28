from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os, json, re

app = Flask(__name__)
CORS(app)

# Configure Gemini API key
genai.configure(api_key="AIzaSyANXqIyIyOsuzJ3G59NMIYtoRZiooZyyUQ")

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        prompt = f"""
        You are an e-commerce assistant. 
        Respond ONLY in valid JSON format (array). 
        Each object should contain:
        - title
        - price
        - store
        Do NOT include extra text or markdown.

        Example:
        [
          {{"title": "iPhone 15 Pro", "price": "$999", "store": "Apple"}},
          {{"title": "Samsung Galaxy S24", "price": "$849", "store": "Amazon"}}
        ]

        Now return a list of popular {query} products.
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        print("Raw Gemini Response:", text)

        # Extract JSON array if present
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            data = []

        return jsonify({"results": data})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
