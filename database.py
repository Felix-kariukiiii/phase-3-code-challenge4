import sqlite3

def create_tables():
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS concerts')
    cursor.execute('DROP TABLE IF EXISTS bands')
    cursor.execute('DROP TABLE IF EXISTS venues')

    # Create bands table
    cursor.execute('''
        CREATE TABLE bands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hometown TEXT NOT NULL
        )
    ''')

    # Create venues table
    cursor.execute('''
        CREATE TABLE venues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')

    # Create concerts table
    cursor.execute('''
        CREATE TABLE concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            band_id INTEGER NOT NULL,
            venue_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (band_id) REFERENCES bands(id),
            FOREIGN KEY (venue_id) REFERENCES venues(id)
        )
    ''')

    conn.commit()
    conn.close()
