from flask import Flask, render_template, request, redirect
import MySQLdb

app = Flask(__name__)

# Database configuration
db = MySQLdb.connect(
    host="your-cloud-sql-private-ip",  # Replace with your Cloud SQL instance's private IP
    user="your-username",              # Replace with your Cloud SQL username
    passwd="your-password",            # Replace with your Cloud SQL password
    db="flaskdb"                       # Replace with your database name
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the 'contacts' table if it doesn't exist
def create_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        message TEXT
    )
    """)
    db.commit()

# Initialize the database
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        db.commit()
        
        return redirect('/')
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
