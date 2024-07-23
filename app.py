from flask import Flask, render_template, request, redirect, url_for
import folium
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'fishing_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS catches (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        fish TEXT,
                        latitude REAL,
                        longitude REAL
                      )''')
    conn.commit()
    conn.close()

init_db()

# Lista de peces permitidos
FISH_TYPES = ["Lucio", "Carpa", "Perca Sol", "Black Bass", "Barbo"]

@app.route('/')
def index():
    return render_template('index.html', fish_types=FISH_TYPES)

@app.route('/add_catch', methods=['POST'])
def add_catch():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fish = request.form['fish']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO catches (date, fish, latitude, longitude) VALUES (?, ?, ?, ?)",
                   (date, fish, latitude, longitude))
    conn.commit()
    conn.close()
    
    return redirect(url_for('map'))

@app.route('/map')
def map():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catches")
    catches = cursor.fetchall()
    conn.close()
    
    # Crear el mapa
    embalse_map = folium.Map(location=[40.1500, -6.1000], zoom_start=13)
    
    for catch in catches:
        folium.Marker(
            location=[catch[3], catch[4]],
            popup=f"{catch[1]} - {catch[2]}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(embalse_map)
    
    # Guardar el mapa en un archivo HTML
    embalse_map.save('templates/map.html')
    
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True)
