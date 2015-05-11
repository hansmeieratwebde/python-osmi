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






#list of tuples for each software, containing the software name, initial release, and main programming languages used
software_list = [("Firefox", 2002,  "C++"),
                 ("Eclipse", 2004, "Java" ),
                 ("Pitivi", 2004, "Python"),
                 ("Netbeans", 1996, "Java"),
                 ("Chrome", 2008, "C++"),
                 ("Filezilla", 2001, "C++"),
                 ("Bazaar", 2005, "Python"),
                 ("Git", 2005, "C"),
                 ("Linux Kernel", 1991, "C"),
                 ("GCC", 1987, "C"),
                 ("Frostwire", 2004, "Java")]

class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Treeview Filter Demo")
        self.set_border_width(10)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, int, str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for prog_language in ["Java", "C", "C++", "Python", "None"]:
            button = Gtk.Button(prog_language)
            self.buttons.append(button)
            button.connect("clicked", self.on_selection_button_clicked)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()


win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

test_data = {'entry_name': 'Sven', 'entry_comment': 'Hallo Welt', 'entry_time': '12:20', 'entry_email': 'scen@dfg.de',
             'entry_date': '150505'}
update_test = {'entry_name': 'Plönx', 'entry_date': '030303', 'entry_id': '1'}
my_crud_ops = crud_ops()
#my_crud_ops.create_entry(test_data)
my_crud_ops.read_table()
print (my_crud_ops.read_entry(3))
my_crud_ops.update_entry(update_test)
my_crud_ops.read_table()