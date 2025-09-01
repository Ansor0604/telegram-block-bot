from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# --- Database funksiyasi ---
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/greet", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        name = request.form["name"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return redirect("/users")
    return render_template("form.html")

@app.route("/users")
def users():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    all_users = c.fetchall()
    conn.close()
    return render_template("users.html", users=all_users)

if __name__ == "__main__":
    init_db()  # Dastur ishga tushganda DB yaratiladi
    app.run(debug=True)
