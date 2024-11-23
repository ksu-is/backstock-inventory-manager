# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
from sqlite3 import Error
import datetime
import os
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Database configuration
path_root = os.path.dirname(os.path.abspath(__file__))
database_file_path = os.path.join(path_root, "backstock.db")

def create_connection():
    try:
        connection = sqlite3.connect(database_file_path)
        connection.row_factory = sqlite3.Row  # This enables column access by name
        return connection
    except Error as e:
        print(e)
        return None

def initialize_database():
    conn = create_connection()
    if conn:
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                quantity INTEGER DEFAULT 0,
                tags TEXT DEFAULT '',
                location TEXT DEFAULT '',
                barcode TEXT DEFAULT '',
                changemade TEXT DEFAULT ''
            )
            """
            conn.execute(sql)
            conn.commit()
        except Error as e:
            print("*** Database Initialization Error: ", e)
        finally:
            conn.close()

# Initialize the database on startup
initialize_database()

@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory ORDER BY name")
    items = cursor.fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        tags = request.form['tags']
        location = request.form['location']
        barcode = request.form['barcode']
        changemade = datetime.datetime.now().strftime("%Y/%m/%d")
        
        conn = create_connection()
        try:
            sql = "INSERT INTO inventory (name, quantity, tags, location, barcode, changemade) VALUES (?, ?, ?, ?, ?, ?)"
            conn.execute(sql, (name, quantity, tags, location, barcode, changemade))
            conn.commit()
            flash('Item added successfully!', 'success')
        except Error as e:
            flash(f'Error adding item: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    conn = create_connection()
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        tags = request.form['tags']
        location = request.form['location']
        barcode = request.form['barcode']
        changemade = datetime.datetime.now().strftime("%Y/%m/%d")
        
        try:
            sql = """UPDATE inventory 
                     SET name=?, quantity=?, tags=?, location=?, barcode=?, changemade=? 
                     WHERE id=?"""
            conn.execute(sql, (name, quantity, tags, location, barcode, changemade, id))
            conn.commit()
            flash('Item updated successfully!', 'success')
        except Error as e:
            flash(f'Error updating item: {str(e)}', 'error')
        finally:
            conn.close()
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE id=?", (id,))
    item = cursor.fetchone()
    conn.close()
    return render_template('edit_item.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    conn = create_connection()
    try:
        conn.execute("DELETE FROM inventory WHERE id=?", (id,))
        conn.commit()
        flash('Item deleted successfully!', 'success')
    except Error as e:
        flash(f'Error deleting item: {str(e)}', 'error')
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/export')
def export_csv():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        
        # Create a temporary CSV file
        csv_file_path = os.path.join(path_root, "backstock.csv")
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow([description[0] for description in cursor.description])
            # Write data
            writer.writerows(cursor.fetchall())
        
        return send_file(
            csv_file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='backstock.csv'
        )
    except Error as e:
        flash(f'Error exporting CSV: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
