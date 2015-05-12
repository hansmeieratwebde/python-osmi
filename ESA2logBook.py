# __author__ = 'S Hinse'
# -*- coding: utf-8 -*-

# Erstellen Sie ein Logbuch mit PyGTK, über das bestehende Log-Einträge gelesen und neue Log-Einträge geschrieben werden können.
# Die Daten sind persistent in einer relationalen Datenbank (sqlite) zu speichern.
#
# In der Aufgabe geht es mir darum, dass Sie
# - aus der DB lesen / in die DB schreiben
# - eine GUI mit Komponenten zur Eingabe und Darstellung von Informationen schaffen.
# Als Datenfelder sollten Sie mind. Name, Uhrzeit, Email und Kommentar haben.


from gi.repository import Gtk
import sqlite3


class crud_ops():
    def __init__(self):
        """creates db and table if necessary and returns db object"""

    __connection = sqlite3.connect('logbook.db')
    __connection.row_factory = sqlite3.Row
    __cursor = __connection.cursor()
    __cursor.execute("""CREATE TABLE IF NOT EXISTS my_log (
    id INTEGER PRIMARY KEY, entry_name TEXT, entry_date DATE, entry_time TIME,entry_email TEXT,
   entry_comment TEXT)""")

    def create_entry(self, entry_data):
        self.__cursor.execute(
            '''INSERT INTO my_log(entry_name,  entry_date, entry_time, entry_email, entry_comment) VALUES (:entry_name,  :entry_date, :entry_time, :entry_email, :entry_comment)''',
            entry_data)
        self.__connection.commit()

    def update_entry(self,  entry_data):
        self.__cursor.execute('''UPDATE my_log SET entry_name =:entry_name, entry_date = :entry_date, entry_time = :entry_time, entry_email= :entry_email, entry_comment = :entry_comment WHERE id=:entry_id''',entry_data)



    def read_entry(self, entry_id):
            self.__cursor.execute('''SELECT  * FROM my_log WHERE id = ?''', (entry_id,))
            return self.__cursor.fetchone()

    def drop_table(self):
        self.__cursor.execute('''DROP TABLE my_log''')

    def read_table(self):
        self.__cursor.execute('''SELECT * FROM my_log''')
        all_rows = self.__cursor.fetchall()

        for row in all_rows:
            # row[0] returns the first column in the query (name), row[1] returns email column.
            print('{0} : {1}, {2}'.format(row['id'], row['entry_date'], row['entry_name']))
            return all_rows







test_data = {'entry_name': 'Sven', 'entry_comment': 'Hallo Welt', 'entry_time': '12:20', 'entry_email': 'scen@dfg.de',
             'entry_date': '150505'}
update_test = {'entry_name': 'Plönx', 'entry_date': '030303', 'entry_id': '1'}
my_crud_ops = crud_ops()
#my_crud_ops.create_entry(test_data)
my_crud_ops.read_table()
print (my_crud_ops.read_entry(3))
my_crud_ops.update_entry(update_test)
my_crud_ops.read_table()