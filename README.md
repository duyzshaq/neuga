# Neuga AI Chatbot

![Neuga AI Badge](https://img.shields.io/badge/Neuga-indigo?style=for-the-badge&logo=openai)
![Python Badge](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask Badge](https://img.shields.io/badge/Framework-Flask-green?style=for-the-badge&logo=flask)
![MySQL Badge](https://img.shields.io/badge/Database-MySQL-orange?style=for-the-badge&logo=mysql)

Neuga AI is a next-generation, context-aware chatbot application capable of real-time web interaction. Powered by the DeepSeek LLM and enhanced with live internet search capabilities, Neuga AI bridges the gap between static knowledge and real-time events.

The application features a stunning, modern "Glassmorphism" user interface with immersive animations, designed to provide a premium user experience.

## ✨ Features

- **🧠 Advanced AI Intelligence**: Powered by DeepSeek API (OpenAI compatible) for high-quality, nuanced conversations.
- **🌐 Real-Time Web Search**: Integrated with DuckDuckGo to fetch the latest information (e.g., news, weather, current presidents) on the fly.
- **🗣️ Adaptive Language Engine**: Automatically detects and responds in the user's preferred language without manual configuration.
- **🔒 Secure Authentication**: Robust user registration and login system protected by Flask-Login and password hashing.
- **🎨 Modern Glassmorphism UI**: A visually striking interface featuring frosted glass panels, animated background globes, and responsive layout.
- **📝 Rich Markdown Support**: Beautifully renders code blocks, lists, bold text, and more using `marked.js`.
- **⚡ Fast & Lightweight**: Built on Flask for optimal performance and easy deployment.

## 🛠️ Technology Stack

- **Backend**: Python, Flask, OpenAI SDK, DuckDuckGo Search, Flask-SQLAlchemy, Flask-Login
- **Database**: MySQL (Production) / SQLite (Development fallback)
- **Frontend**: HTML5, CSS3 (Variables, Animations), JavaScript (Vanilla)
- **Design**: Google Fonts (Outfit), FontAwesome, Custom Glassmorphism Theme

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python Package Manager)
- MySQL Server (Optional, for production database)
- A valid DeepSeek API Key

### Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone https://github.com/duyzshaq/neuga.git
    cd neuga
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    Copy `env.example` to `.env` and updated it with your credentials:
    ```bash
    cp env.example .env
    ```
    
    Update `.env` with your actual keys:
    ```bash
    DEEPSEEK_API_KEY=your_actual_api_key_here
    DATABASE_URL=mysql+pymysql://username:password@localhost/neuga_db
    SECRET_KEY=your_secure_random_key
    ```

4.  **Database Setup**:
    If using MySQL, create the database and table using the provided SQL file:
    ```bash
    mysql -u root -p neuga_db < database.sql
    ```
    *Note: The application will automatically attempt to create tables if they don't exist, but using `database.sql` ensures the correct schema.*

### Running the Application

1.  **Start the Flask Server**:
    ```bash
    python app.py
    ```

2.  **Access the Interface**:
    Open your browser and navigate to:
    `http://127.0.0.1:5000`

## 📖 Usage Guide

- **Registration**: Create a new account on the landing page to access the bot.
- **General Chat**: Ask general questions like "Write a python script to sort a list".
- **Real-Time Queries**: Ask about current events, e.g., "Who won the latest World Cup?" or "What is the stock price of Apple?".
- **Coding Help**: Paste code snippets or ask for debugging help; the bot will format code beautifully.

## 📂 Project Structure

```
neuga/
├── app.py              # Main application entry point & API/Auth logic
├── requirements.txt    # Python dependencies
├── .env                # API keys and secrets
├── database.sql        # SQL schema for manual setup
├── static/
│   ├── style.css       # Main stylesheet (Themes, Animations)
│   └── script.js       # Frontend interaction logic
├── templates/
│   ├── index.html      # Main Chat Interface (Protected)
│   ├── landing.html    # Landing / Welcome Page
│   ├── login.html      # Login Page
│   ├── register.html   # Registration Page
│   └── ...             # Other content pages (about, privacy, etc.)
└── README.md           # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
