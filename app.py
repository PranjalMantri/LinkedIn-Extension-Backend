from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask_cors import CORS  

load_dotenv()

app = Flask(__name__)
CORS(app)  

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def improve_text(input_text):
    try:
        prompt = f"""
        Take this LinkedIn post written in a formal and overly friendly tone with excessive emojis and unnecessary text, and rewrite it to sound direct and concise. Make it feel more straightforward and professional without sounding overly enthusiastic or personal.

        Guidelines:

        Remove excessive friendliness and cut down on any unnecessary details.
        Simplify language and remove any corporate buzzwords.
        Keep the message clear, make it less proffessional, while maintaining a warm, approachable tone without added enthusiasm.
        Original Text: {input_text}

        """

        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        print(f"Error processing with Gemini: {str(e)}")
        return "Error processing content"


@app.route('/improve', methods=['POST'])
def process_input():
    try:
        data = request.json
        input_text = data.get("input", "")
        
        if not input_text:
            return jsonify({"error": "No input text provided"}), 400
        
        processed_text = improve_text(input_text)
        
        return jsonify({
            "success": True,
            "processed_text": processed_text
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)