import sqlite3
from flask import g, request

# this function will creating the database of messages. It first check whether there is a database called message_db in the g attribute of the app. If not, then connect to that database then check whether a table called messages exists in message_db, and create it if not.
def get_message_db():
    # write some helpful comments here
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = """
            CREATE TABLE IF NOT EXISTS message_table(
            id INTEGER, 
            handle TEXT, 
            message TEXT
            )
            """
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
    return g.message_db


# this function could inserting a user message into the database of messages.
def insert_message(request):
    name = request.form["name"]
    message = request.form["message"]

    # open a connection to messages.db
    connection_obj = get_message_db()
    cursor_obj = connection_obj.cursor()


    id_cmd = "SELECT COUNT(*) FROM message_table"
    cursor_obj.execute(id_cmd)
    id = cursor_obj.fetchone()[0] + 1

    insert_cmd = """
        INSERT INTO message_table
        (id, handle, message)
        VALUES
        (?, ?, ?)
        """
    data = (id, name, message)
    cursor_obj.execute(insert_cmd, data)

    connection_obj.commit() # save changes
    connection_obj.close() # close connection


# this function will return a collection of n random messages from the message_db
# n argument is request.form["number"] which is a html script in string form
def random_messages(n):
    # open a connection to messages.db
    connection_obj = get_message_db()
    cursor_obj = connection_obj.cursor()

    length_cmd = "SELECT COUNT(*) FROM message_table"
    cursor_obj.execute(length_cmd)
    num_len = cursor_obj.fetchone()[0]
    
    out = ""

    if (int(n) > num_len):
        out = ("The number " + n + " you input is exceed the maximun number of messages(" + 
            str(num_len) +
            "), I can only show below messages:<br><br>")
        n = str(num_len)

    cmd = "SELECT * FROM message_table ORDER BY RANDOM() LIMIT " + n

    for row in cursor_obj.execute(cmd): # row is a tuple
        out = out + row[2] + "<br>" + "- " + row[1] + "<br><br>"

    connection_obj.close() # close connection

    return out # a html script in string form