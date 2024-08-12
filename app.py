import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            date_of_joining TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/add', methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        date_of_joining = request.form['date_of_joining']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO faculty (name, department, email, phone, address, date_of_joining)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, department, email, phone, address, date_of_joining))
        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add_edit_faculty.html', action="Add")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_faculty(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        date_of_joining = request.form['date_of_joining']

        cursor.execute('''
            UPDATE faculty
            SET name = ?, department = ?, email = ?, phone = ?, address = ?, date_of_joining = ?
            WHERE id = ?
        ''', (name, department, email, phone, address, date_of_joining, id))
        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute('SELECT * FROM faculty WHERE id = ?', (id,))
    data = cursor.fetchone()
    conn.close()
    return render_template('add_edit_faculty.html', data=data, action="Edit")

@app.route('/delete/<int:id>')
def delete_faculty(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM faculty WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/view/<int:id>')
def view_faculty(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM faculty WHERE id = ?', (id,))
    data = cursor.fetchone()
    conn.close()
    return render_template('faculty_detail.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE name LIKE ? OR department LIKE ?", ('%'+query+'%', '%'+query+'%'))
        data = cursor.fetchall()
        conn.close()
        return render_template('index.html', data=data)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
