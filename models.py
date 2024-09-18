import sqlite3

class Band:
    def __init__(self, id, name, hometown, conn):
        self.id = id
        self.name = name
        self.hometown = hometown
        self.conn = conn

    def concerts(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts WHERE band_id = ?
        ''', (self.id,))
        return cursor.fetchall()

    def venues(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT venues.* FROM venues
            JOIN concerts ON venues.id = concerts.venue_id
            WHERE concerts.band_id = ?
        ''', (self.id,))
        return cursor.fetchall()

    def play_in_venue(self, venue_title, date):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM venues WHERE title = ?', (venue_title,))
        venue = cursor.fetchone()
        if venue:
            venue_id = venue[0]
            cursor.execute('''
                INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)
            ''', (self.id, venue_id, date))
            self.conn.commit()
        else:
            raise ValueError(f"Venue '{venue_title}' does not exist.")

    def all_introductions(self):
        intros = []
        for concert in self.concerts():
            intro = Concert(concert[0], self.conn).introduction()
            intros.append(intro)
        return intros

    @staticmethod
    def most_performances(conn):
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, COUNT(concerts.id) as performance_count
            FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            GROUP BY bands.id
            ORDER BY performance_count DESC
            LIMIT 1
        ''')
        return cursor.fetchone()

class Venue:
    def __init__(self, id, title, city, conn):
        self.id = id
        self.title = title
        self.city = city
        self.conn = conn

    def concerts(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts WHERE venue_id = ?
        ''', (self.id,))
        return cursor.fetchall()

    def bands(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT DISTINCT bands.* FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            WHERE concerts.venue_id = ?
        ''', (self.id,))
        return cursor.fetchall()

    def concert_on(self, date):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts WHERE venue_id = ? AND date = ? LIMIT 1
        ''', (self.id, date))
        return cursor.fetchone()

    def most_frequent_band(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT bands.name, COUNT(concerts.id) as performance_count
            FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            WHERE concerts.venue_id = ?
            GROUP BY bands.id
            ORDER BY performance_count DESC
            LIMIT 1
        ''', (self.id,))
        return cursor.fetchone()

class Concert:
    def __init__(self, id, conn):
        self.id = id
        self.conn = conn

    def band(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            WHERE concerts.id = ?
        ''', (self.id,))
        band_data = cursor.fetchone()
        return Band(band_data[0], band_data[1], band_data[2], self.conn)

    def venue(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM venues
            JOIN concerts ON venues.id = concerts.venue_id
            WHERE concerts.id = ?
        ''', (self.id,))
        venue_data = cursor.fetchone()
        return Venue(venue_data[0], venue_data[1], venue_data[2], self.conn)

    def hometown_show(self):
        band = self.band()
        venue = self.venue()
        return band.hometown == venue.city

    def introduction(self):
        band = self.band()
        venue = self.venue()
        return f"Hello {venue.city}!!!!! We are {band.name} and we're from {band.hometown}"
