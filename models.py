import sqlite3 as sql

def get_theme():
    con = sql.connect('data.db')
    cur = con.cursor()
    cur.execute('SELECT theme FROM website')
    data = cur.fetchall()
    con.close()
    return data[0][0]