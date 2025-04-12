import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
print("API Key:", os.getenv("GOOGLE_API_KEY"))
app = Flask(__name__)
CORS(app)

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
model = genai.GenerativeModel('gemini-pro')

SYSTEM_PROMPT = """
You are a professional stock market analyst assistant. Provide accurate, concise information about:
- Stock prices and trends (when asked for specific symbols)
- Market indices (S&P 500, NASDAQ, etc.)
- Company financials and analysis
- Market news and insights
- Investment strategies (without giving direct advice)

Format responses with:
1. Clear headings for different sections
2. Bullet points for lists
3. Bold important numbers ($125.76, +2.5%)
4. Separate sections with line breaks

For stock prices:
- Provide the most recent available data
- Include change in price and percentage
- Add relevant metrics (P/E, market cap) when available

Current market context: {context}
"""

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    query = data.get("query", "").strip()
    context = data.get("context", "General market conditions")

    if not query:
        return jsonify({"response": "Please enter a valid query."})

    try:
        # Start chat with system prompt
        response = model.generate_content(
            SYSTEM_PROMPT.format(context=context) + f"\n\nUser question: {query}"
        )
        
        return jsonify({
            "status": "success",
            "response": response.text
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "response": f"Analysis error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)