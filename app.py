from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vergehen')
def vergehen():
    return render_template('vergehen.html')

@app.route('/uebersicht')
def uebersicht():
    return render_template('uebersicht.html')

if __name__ == '__main__':
    app.run(debug=True)

# Datenbankverbindung herstellen
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Datenbank initialisieren (einmalig ausführen)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS spieler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            total_fines REAL DEFAULT 0
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bussen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spieler_id INTEGER,
            vergehen TEXT NOT NULL,
            betrag REAL NOT NULL,
            datum TEXT NOT NULL,
            FOREIGN KEY (spieler_id) REFERENCES spieler(id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialisiere die Datenbank (entferne diesen Aufruf nach der ersten Ausführung)
#init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    spieler = conn.execute('SELECT * FROM spieler').fetchall()
    conn.close()
    return render_template('index.html', spieler=spieler)

@app.route('/home/nils/Documents/VSCode/templates/vergehen.html', methods=('GET', 'POST'))
def vergehen():
    conn = get_db_connection()
    spieler = conn.execute('SELECT * FROM spieler').fetchall()
    
    if request.method == 'POST':
        spieler_id = request.form['spieler']
        vergehen = request.form['vergehen']
        betrag = float(request.form['betrag'])
        datum = request.form['datum']

        conn.execute('INSERT INTO bussen (spieler_id, vergehen, betrag, datum) VALUES (?, ?, ?, ?)',
                     (spieler_id, vergehen, betrag, datum))
        conn.execute('UPDATE spieler SET total_fines = total_fines + ? WHERE id = ?', (betrag, spieler_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('vergehen.html', spieler=spieler)

@app.route('/home/nils/Documents/VSCode/templates/uebersicht.html')
def übersicht():
    conn = get_db_connection()
    bussen = conn.execute('''
        SELECT s.name, b.vergehen, b.betrag, b.datum
        FROM bussen b
        JOIN spieler s ON b.spieler_id = s.id
    ''').fetchall()
    conn.close()
    return render_template('uebersicht.html', bussen=bussen)

if __name__ == '__main__':
    app.run(debug=True)
