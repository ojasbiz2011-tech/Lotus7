import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chess_leaderboard.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, rating INTEGER)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scores', methods=['GET', 'POST'])
def handle_scores():
    conn = get_db_connection()
    
    if request.method == 'POST':
        data = request.json
        conn.execute('INSERT INTO scores (name, rating) VALUES (?, ?)', (data['name'], data['rating']))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'})
    
    # GET: Fetch top 10 scores
    scores = conn.execute('SELECT name, rating FROM scores ORDER BY rating DESC LIMIT 10').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in scores])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
