import sqlite3
from models import Band, Venue, Concert

def add_test_data(conn):
    cursor = conn.cursor()

    # Add Bands
    cursor.execute('INSERT INTO bands (name, hometown) VALUES (?, ?)', ("Wakadinali", "Nairobi"))
    cursor.execute('INSERT INTO bands (name, hometown) VALUES (?, ?)', ("Sauti Sol", "Nairobi"))
    cursor.execute('INSERT INTO bands (name, hometown) VALUES (?, ?)', ("Matata", "Kiambu"))
    cursor.execute('INSERT INTO bands (name, hometown) VALUES (?, ?)', ("Buruklyn Boyz", "Buruburu"))
    cursor.execute('INSERT INTO bands (name, hometown) VALUES (?, ?)', ("Wadagla", "Dagoreti"))

    # Add Venues
    cursor.execute('INSERT INTO venues (title, city) VALUES (?, ?)', ("Carnivore Grounds", "Nairobi"))
    cursor.execute('INSERT INTO venues (title, city) VALUES (?, ?)', ("Uhuru Gardens", "Nairobi"))
    cursor.execute('INSERT INTO venues (title, city) VALUES (?, ?)', ("Ngong Racecourse", "Nairobi"))
    cursor.execute('INSERT INTO venues (title, city) VALUES (?, ?)', ("Masai Lodge", "Nairobi"))

    # Add Concerts
    cursor.execute('SELECT id FROM bands WHERE name = ?', ("Wakadinali",))
    band_id = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM venues WHERE title = ?', ("Carnivore Grounds",))
    venue_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)', (band_id, venue_id, "2023-12-25"))

    cursor.execute('SELECT id FROM bands WHERE name = ?', ("Sauti Sol",))
    band_id = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM venues WHERE title = ?', ("Uhuru Gardens",))
    venue_id = cursor.fetchone()[0]
    cursor.execute('INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)', (band_id, venue_id, "2023-11-15"))

    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('concerts.db')
    add_test_data(conn)

    # Test example
    band = Band(1, "Wakadinali", "Nairobi", conn)
    venue = Venue(1, "Carnivore Grounds", "Nairobi", conn)
    concert = Concert(1, conn)

    print("Concert Hometown Show:", concert.hometown_show())
    print("Concert Introduction:", concert.introduction())
    print("Band Most Performances:", Band.most_performances(conn))
    print("Venue Concert on 2023-11-15:", venue.concert_on("2023-11-15"))
    print("Venue Most Frequent Band:", venue.most_frequent_band())

    conn.close()
