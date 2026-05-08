import mysql.connector

# Підключення до MySQL
conn = mysql.connector.connect(
    host="10.200.10.14",
    user="root",
    password="2808200",
    database="office_chaos_manager"
)
cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'OK'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT,
    status VARCHAR(50) DEFAULT 'Open',
    priority VARCHAR(50)
)
""")

# Вставка тестових даних
cursor.execute("INSERT IGNORE INTO users (username, password) VALUES ('admin', 'admin')")
cursor.execute("INSERT IGNORE INTO systems (name) VALUES ('Web Server')")
cursor.execute("INSERT IGNORE INTO systems (name) VALUES ('Database')")
cursor.execute("INSERT IGNORE INTO systems (name) VALUES ('API Service')")

# Додамо тестовий тікет для демонстрації графіка
cursor.execute("INSERT IGNORE INTO tickets (title, status, priority) VALUES ('Database connection timeout', 'Open', 'MEDIUM')")
cursor.execute("INSERT IGNORE INTO tickets (title, status, priority) VALUES ('Server crash detected', 'Open', 'HIGH')")
cursor.execute("INSERT IGNORE INTO tickets (title, status, priority) VALUES ('Slow API response', 'Open', 'MEDIUM')")
cursor.execute("INSERT IGNORE INTO tickets (title, status, priority) VALUES ('Minor UI bug', 'Open', 'LOW')")

conn.commit()
conn.close()

print("Database initialized!")