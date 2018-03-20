import glob
import sqlite3 as lite



messages_con = lite.connect('birds.db')

def add_message(db_name, msg):
    """
    Add discord message to database
    :param db_name: database to augment
    :param msg: message to add
    """
    con = sql_setup.get_con(db_name)
    with con:
        cur = con.cursor()
        cur.execute("INSERT INTO " + db_name + " VALUES(?, ?, ?, ?)",
                    ('NONE', 'NONE', 'NONE', msg))

for file in glob.glob("Birds/**/*.*", recursive=True):
    add_message('birds.db', file)

    print(file)

    imagedict = {
             'White Crowned Sparrow' : ('Birds/Sparrow/White Crowned Sparrow/*.*,'description','color'),
             'House Finch' : ('','description2','color2')
             }
