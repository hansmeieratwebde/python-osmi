__author__ = 'S Hinse'
from gi.repository import Gtk
import sqlite3

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "HelloGTK")
        self.button = Gtk.Button (label = "Click Here")
        self.add(self.button)

connection = sqlite3.connect("lagerverwaltung.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS lager (
    fachnummer INTEGER, seriennummer INTEGER, komponente TEXT,
    lieferant TEXT, reserviert INTEGER
)""")


win = MyWindow()
win.connect ("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

