import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from openai import OpenAI
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///neuga.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize OpenAI client
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

# Routes
@app.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('chat_interface'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat_interface'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
            
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('chat_interface'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/chat')
@login_required
def chat_interface():
    return render_template('index.html', user=current_user)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
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

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create tables if they don't exist
    app.run(debug=True, port=5000)