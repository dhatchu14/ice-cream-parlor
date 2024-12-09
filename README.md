Ice Cream Parlor Application
This is a Python-based web application for a fictional ice cream parlor cafe. It uses Flask for the backend, SQLite for database management, and HTML/CSS/JavaScript for the frontend. The application allows users to browse seasonal flavors, manage an ingredient inventory, handle customer flavor suggestions and allergy concerns, and maintain a shopping cart.

Features
Core Functionalities:
Seasonal Flavor Offerings: Browse through available seasonal flavors.
Ingredient Inventory: Manage ingredients used in the ice cream flavors.
Customer Suggestions: Accept new flavor suggestions from customers.
Allergy Concerns: Add allergens to a list for better customer awareness.
Shopping Cart: Maintain a cart of favorite products, with total price calculation.
Search and Filter: Search and filter the list of available flavors.
Additional Features:
User-friendly and minimalist interface.
Persistent data storage using SQLite.
Requirements
Software Dependencies:
Python (3.8 or above)
Flask (install via pip install flask)
SQLite (pre-installed with Python)
Optional: SQLite CLI for direct database access.
Frontend:
HTML, CSS (minimalist design), and JavaScript.
Installation
Clone the Repository:
git clone <repository_url>
cd ice_cream_parlor
Install Dependencies: Install Flask if not already installed:


pip install flask
Initialize the Database: Run the Python script to initialize the SQLite database:


python ice_cream_parlor.py
This creates the database ice_cream_parlor.db with the necessary tables.

Run the Application: Start the Flask development server:


python ice_cream_parlor.py
The application will be accessible at http://127.0.0.1:5000.

Database Schema
Tables:
flavors:

id: Integer (Primary Key)
name: Text
description: Text
price: Real
ingredients:

id: Integer (Primary Key)
name: Text
quantity: Integer
allergens:

id: Integer (Primary Key)
name: Text
suggestions:

id: Integer (Primary Key)
flavor_name: Text
cart:

id: Integer (Primary Key)
flavor_name: Text
price: Real
Usage Instructions
Adding Seasonal Flavors:
Go to the database using SQLite CLI:

sqlite3 ice_cream_parlor.db
Insert a new flavor:
sql
Copy code
INSERT INTO flavors (name, description, price) VALUES ('Mint Chocolate Chip', 'Refreshing mint with chocolate chips.', 4.50);
Viewing Data:
To view data stored in the database:

Open SQLite CLI:

sqlite3 ice_cream_parlor.db
Use SQL commands, for example:
sql
Copy code
SELECT * FROM flavors;
SELECT * FROM cart;
Managing Inventory:
Navigate to the ingredient management section in the app to add or edit ingredients.

Files and Structure
plaintext
Copy code
ice_cream_parlor/
├── static/
│   ├── css/
│   │   └── styles.css       # CSS for frontend
│   └── js/
│       └── script.js        # JavaScript for frontend logic
├── templates/
│   └── index.html           # HTML file for the main page
├── ice_cream_parlor.py      # Main Python application
├── ice_cream_parlor.db      # SQLite database (generated at runtime)
└── README.md                # Documentation
Troubleshooting
Database Errors:

Ensure ice_cream_parlor.db exists in the project directory.
Re-run initialize_db() if the database is missing or corrupted.
CSS/JavaScript Not Loading:

Ensure the static folder is structured properly.
Check the paths in the <link> and <script> tags in index.html.
Port Conflict:

If port 5000 is in use, specify a different port:

flask run --port=5001
Template Not Found:

Ensure the templates folder is in the same directory as ice_cream_parlor.py.
License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute.

