from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from MedicalQueryGenerator import MedicalQueryGenerator
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample user data
users = {"test@example.com": {"name": "Test User", "password": "password123"}}

# Database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vivek@2023",
    database="healthcare"
)

@app.route('/get_data')
def get_data():
    cursor = db_connection.cursor()
    query = "SELECT * FROM healthcare"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
