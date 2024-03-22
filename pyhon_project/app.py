from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# PostgreSQL connection configuration
DB_HOST = 'db'
DB_NAME = 'admin'
DB_USER = 'jyoti'
DB_PASSWORD = 'admin'

# Function to establish PostgreSQL connection
def connect_db():
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

# Create 'entries' table if it doesn't exist
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Call create_table function when the application starts
create_table()

# Route to display form
@app.route('/')
def index():
    return render_template('form.html')

# Route to submit form data
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']

    # Insert form data into PostgreSQL database
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to fetch form data
@app.route('/entries')
def get_entries():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM entries")
    entries = cur.fetchall()
    conn.close()
    return render_template('entries.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

