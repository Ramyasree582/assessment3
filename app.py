from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Create the database table if it doesn't exist
def init_db():
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            flavor TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Route: Welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')

# Route: Billing form
@app.route('/index')
def index():
    return render_template('index.html')

# Route: Generate Bill
@app.route('/generate', methods=['POST'])
def generate():
    customer_name = request.form['customer_name']
    flavor = request.form['flavor']
    quantity = int(request.form['quantity'])

    # Set price per scoop
    price_per_scoop = 50
    total_price = quantity * price_per_scoop

    # Insert into database
    conn = sqlite3.connect('bills.db')
    c = conn.cursor()
    c.execute('INSERT INTO bills (customer_name, flavor, quantity, total_price) VALUES (?, ?, ?, ?)',
              (customer_name, flavor, quantity, total_price))
    conn.commit()
    conn.close()

    return render_template('bill.html',
                           customer_name=customer_name,
                           flavor=flavor,
                           quantity=quantity,
                           total_price=total_price)

# Route: Thank You page
@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render requires this
    app.run(host='0.0.0.0', port=port)
