from flask import Flask, render_template, request, redirect, url_for, jsonify
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv('DATABASE_URL')

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS catches (
            id SERIAL PRIMARY KEY,
            date DATE,
            fish VARCHAR(50),
            latitude REAL,
            longitude REAL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Inicializar la base de datos al inicio de la aplicación
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_capture', methods=['POST'])
def add_capture():
    date = request.form['date']
    fish = request.form['fish']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO catches (date, fish, latitude, longitude) VALUES (%s, %s, %s, %s)
    ''', (date, fish, latitude, longitude))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/get_captures')
def get_captures():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT date, fish, latitude, longitude FROM catches')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    captures = []
    for row in rows:
        captures.append({
            'date': row[0].isoformat(),
            'fish': row[1],
            'latitude': row[2],
            'longitude': row[3]
        })

    return jsonify(captures=captures)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
