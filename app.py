import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client with DeepSeek base URL
# API Key should be set in environment variables as DEEPSEEK_API_KEY
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def search_web(query):
    try:
        results = DDGS().text(query, max_results=3)
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Perform web search to get context
        search_results = search_web(user_message)
        context = "\n".join([f"- {r['title']}: {r['body']}" for r in search_results])

        system_prompt = f"""You are a helpful and knowledgeable AI assistant.
        
        Here is some real-time context from the web related to the user's request:
        {context}

        INSTRUCTIONS:
        1. Answer the user's question based on the provided context if relevant.
        2. ALWAYS reply in the SAME LANGUAGE as the user's message (e.g., if user speaks Indonesian, reply in Indonesian).
        3. If the context doesn't help, use your general knowledge but admit if you aren't sure about current specific events not in the context.
        4. Format your response using Markdown (bold, lists, code blocks, etc.) where appropriate.
        5. Response using recent events as of 2025.
        """

        # Create chat completion request
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            stream=False
        )

        bot_message = response.choices[0].message.content
        return jsonify({'response': bot_message})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
