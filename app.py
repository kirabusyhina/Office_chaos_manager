from turtle import title

from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)

app.secret_key = "secret123"


# вхід
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        if user:

            session["user"] = user["username"]

            return redirect("/")

    return render_template("login.html")


# вихід
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# дашборд
@app.route("/")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tickets")
    tickets = cursor.fetchall()

    cursor.execute("SELECT * FROM systems")
    systems = cursor.fetchall()

    return render_template(
        "dashboard.html",
        tickets=tickets,
        systems=systems,
        user=session["user"]
    )


def classify_ticket_priority(title):

    title_lower = title.lower()

    high_keywords = [
        "crash",
        "down",
        "error",
        "server",
        "database",
        "api",
        "outage",
        "failure"
    ]

    medium_keywords = [
        "slow",
        "lag",
        "delay",
        "timeout",
        "hang",
        "freeze",
        "performance"
    ]

    if any(keyword in title_lower for keyword in high_keywords):
        return "HIGH"

    if any(keyword in title_lower for keyword in medium_keywords):
        return "MEDIUM"

    return "LOW"


# створення тікета
@app.route("/create_ticket", methods=["POST"])
def create_ticket():

    title = request.form["title"]
    priority = classify_ticket_priority(title)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tickets (title, status, priority) VALUES (%s, %s, %s)",
        (title, "Open", priority)
    )

    conn.commit()

    return redirect("/")


#   симуляція інциденту
@app.route("/simulate")
def simulate():

    conn = get_connection()

    cursor = conn.cursor()

    # зміна статусу системи
    cursor.execute(
        "UPDATE systems SET status='DOWN' WHERE name='API Service'"
    )

    # створення тікета
    simulated_title = "API Service crashed 💥"
    cursor.execute(
        "INSERT INTO tickets (title, status, priority) VALUES (%s, %s, %s)",
        (simulated_title, "Open", classify_ticket_priority(simulated_title))
    )

    conn.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)