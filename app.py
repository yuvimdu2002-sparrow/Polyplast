from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Create database
conn = sqlite3.connect("contact.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    company TEXT, 
    message TEXT
)
""")

conn.commit()
conn.close()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Form Submit
@app.route("/contact", methods=["POST"])
def contact():

    # Retrieve frontend data
    name = request.form["name"]
    email = request.form["email"]
    company = request.form["company"]
    message = request.form["message"]

    # Store in SQL
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contacts(name, email, company, message)
    VALUES(?, ?, ?, ?)
    """, (name, email, message, company))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})


# Retrieve SQL data
@app.route("/messages")
def messages():

    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")

    data = cursor.fetchall()

    conn.close()

    return str(data)


if __name__ == "__main__":
    app.run(debug=True)
