from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from transformers import pipeline
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from flask_session import Session
import json

# Initialize Flask app
app = Flask(__name__)

# Configure session management with Flask-Session
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data on the server side
Session(app)

# MySQL Database Configuration
DATABASE_URI = "mysql+pymysql://username:password@localhost/healthcare_db"
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

# Initialize the transformer model for NLP processing
nlp_model = pipeline("text2text-generation", model="google/flan-t5-large")

# Dummy user data (for demonstration purposes)
users = {"test@example.com": {"name": "Test User", "password": "password123"}}

@app.route('/')
def home():
    # Redirect to login if not authenticated
    if 'user' not in session:
        return redirect(url_for('login_signup'))
    return redirect(url_for('main'))

@app.route('/login_signup', methods=['GET', 'POST'])
def login_signup():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if data.get("type") == "login":
            # Check if user exists and password matches
            if email in users and users[email]["password"] == password:
                session['user'] = users[email]["name"]  # Log in user
                return jsonify({"success": True})
            return jsonify({"success": False, "error": "Invalid credentials"})
        
        elif data.get("type") == "signup":
            name = data.get("name")
            # Add user if they don't exist
            if email not in users:
                users[email] = {"name": name, "password": password}
                session['user'] = name  # Log in new user
                return jsonify({"success": True})
            return jsonify({"success": False, "error": "User already exists"})
    return render_template('login_signup.html')

@app.route('/main')
def main():
    # Check if user is authenticated
    if 'user' in session:
        return render_template('main.html', user=session['user'])
    return redirect(url_for('login_signup'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_signup'))

# Define a route for querying
@app.route('/query', methods=['POST'])
def query():
    try:
        if 'user' not in session:
            return jsonify({"error": "Not authenticated"}), 401

        # Get the natural language query from the request
        user_query = request.json.get("query")
        
        # Use the NLP model to generate SQL
        sql_query_text = nlp_model(f"Convert this to SQL: {user_query}")[0]["generated_text"]
        
        # Create database session
        db_session = SessionLocal()
        
        # Execute query
        result = db_session.execute(text(sql_query_text)).fetchall()
        
        # Convert results to list of dictionaries
        records = []
        for row in result:
            records.append({
                "patient_id": row[0],
                "age": row[1],
                "gender": row[2],
                "symptom": row[3],
                "diagnosis": row[4],
                "treatment": row[5],
                "outcome": row[6],
                "lab_report": row[7]
            })
        
        db_session.close()
        return jsonify(records)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == '_main_':
    app.run(debug=True)