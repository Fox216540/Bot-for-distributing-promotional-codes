import sqlite3


def text():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute("SELECT text FROM Promo").fetchall()[0][0]
    connection_obj.commit()
    connection_obj.close()
    return text


def users():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute("SELECT id FROM users").fetchall()
    connection_obj.commit()
    connection_obj.close()
    return text

def add_user(id):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    try:
        cursor_obj.execute("INSERT INTO users (id) VALUES(?)", (str(id),))
    except:
        pass
    connection_obj.commit()
    connection_obj.close()

def change(text):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(f'UPDATE Promo SET text = ?', (text,))
    connection_obj.commit()
    connection_obj.close()

def add_channel(channels):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM channels").fetchall()
    for channel in channels.split(' '):
        try:
            id = channel.split(":")[2]
            channele = ":".join(channel.split(":")[:2])
            cursor_obj.execute(f'INSERT INTO channels (channel, id) VALUES (?, ?)',(channele,id))
            connection_obj.commit()

        except:
            id = None
            channele = channel
            cursor_obj.execute("INSERT INTO channels (channel,id) VALUES(?,?)", (channele, id))
            connection_obj.commit()



    connection_obj.close()

def channels():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute("SELECT channel,id FROM channels").fetchall()
    connection_obj.commit()
    connection_obj.close()
    return text


