import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Initialize database
def initialize_db():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        seasonal INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_id INTEGER NOT NULL,
        ingredient TEXT NOT NULL,
        FOREIGN KEY (flavor_id) REFERENCES flavors(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        suggestion TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        allergen TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (flavor_id) REFERENCES flavors(id)
    )
    """)

    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS unique_cart_item ON cart (flavor_id);
    """)

    connection.commit()
    connection.close()

# Flask routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/flavors", methods=["GET", "POST"])
def flavors():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    try:
        if request.method == "POST":
            data = request.json
            name = data.get("name")
            price = data.get("price")
            stock = data.get("stock")
            seasonal = data.get("seasonal", 0)

            cursor.execute("""
            INSERT INTO flavors (name, price, stock, seasonal)
            VALUES (?, ?, ?, ?)
            """, (name, price, stock, seasonal))
            connection.commit()

            return jsonify({"message": "Flavor added successfully!"})

        cursor.execute("SELECT * FROM flavors")
        flavors = cursor.fetchall()
        return jsonify(flavors)
    finally:
        connection.close()

@app.route("/cart", methods=["GET", "POST", "DELETE"])
def cart():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    try:
        if request.method == "POST":
            data = request.json
            flavor_id = data.get("flavor_id")
            quantity = data.get("quantity")

            cursor.execute("""
            INSERT INTO cart (flavor_id, quantity)
            VALUES (?, ?)
            ON CONFLICT(flavor_id) DO UPDATE SET quantity = quantity + ?
            """, (flavor_id, quantity, quantity))
            connection.commit()

            return jsonify({"message": "Added to cart!"})

        elif request.method == "DELETE":
            cart_id = request.json.get("cart_id")
            cursor.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
            connection.commit()

            return jsonify({"message": "Item removed from cart!"})

        cursor.execute("""
        SELECT cart.id, flavors.name, cart.quantity
        FROM cart
        JOIN flavors ON cart.flavor_id = flavors.id
        """)
        items = cursor.fetchall()

        return jsonify(items)
    finally:
        connection.close()

@app.route("/allergens", methods=["GET", "POST"])
def allergens():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    try:
        if request.method == "POST":
            allergen = request.json.get("allergen")

            cursor.execute("""
            INSERT OR IGNORE INTO allergens (allergen)
            VALUES (?)
            """, (allergen,))
            connection.commit()

            return jsonify({"message": "Allergen added!"})

        cursor.execute("SELECT * FROM allergens")
        allergens = cursor.fetchall()
        return jsonify(allergens)
    finally:
        connection.close()

@app.route("/suggestions", methods=["POST"])
def suggestions():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    try:
        suggestion = request.json.get("suggestion")
        cursor.execute("""
        INSERT INTO suggestions (suggestion)
        VALUES (?)
        """, (suggestion,))
        connection.commit()
        return jsonify({"message": "Suggestion received!"})
    finally:
        connection.close()

@app.route("/search", methods=["GET"])
def search():
    term = request.args.get("term", "").lower()
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT * FROM flavors
        WHERE LOWER(name) LIKE ?
        """, (f"%{term}%",))
        results = cursor.fetchall()
        return jsonify(results)
    finally:
        connection.close()

# Initialize the database
initialize_db()

if __name__ == "__main__":
    app.run(debug=True)
