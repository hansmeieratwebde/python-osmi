# -*- coding: utf-8 -*-
#  __author__ = 'Sven  Hinse'
#ESA 2, Gtk+3+ Logbook


# Erstellen Sie ein Logbuch mit PyGTK, über das bestehende Log-Einträge gelesen und neue Log-Einträge geschrieben werden können.
# Die Daten sind persistent in einer relationalen Datenbank (sqlite) zu speichern.
#
# In der Aufgabe geht es mir darum, dass Sie
# - aus der DB lesen / in die DB schreiben
# - eine GUI mit Komponenten zur Eingabe und Darstellung von Informationen schaffen.
# Als Datenfelder sollten Sie mind. Name, Uhrzeit, Email und Kommentar haben.


from gi.repository import Gtk, Pango

import sqlite3, sys, os


class MyWindow(Gtk.ApplicationWindow):



    def __init__(self, app, db):
        """

        :type db: crud_ops
        """
        self.db = db

        Gtk.Window.__init__(self, title="ESA 2 / Logbook Sven Hinse", application=app)
        self.set_default_size(600, 300)
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.init_treestore(db)
        self.grid.attach(self.view, 0, 0, 1, 1)

        # add buttons
        button_box = Gtk.Box(1)
        submit_changes_button = Gtk.Button("Änderungen speichern")
        submit_changes_button.connect("clicked", self.on_submit_changes_clicked)
        button_box.pack_start(submit_changes_button, True, True, 10)

        new_entry_button = Gtk.Button("Als neuen Eintrag speichern")
        new_entry_button.connect("clicked", self.on_new_entry_clicked)
        button_box.pack_start(new_entry_button, True, True, 10)

        delete_entry_button = Gtk.Button("Eintrag löschen")
        delete_entry_button.connect("clicked", self.on_delete_entry_clicked)
        button_box.pack_start(delete_entry_button, True, True, 10)

        self.grid.attach(button_box, 0, 8, 1, 1)



        # attach the grid to the window
        self.add(self.grid)


        #add input form
        self.edit_form = self.init__input_form()


    # Eventhandler

    def on_changed(self, selection):
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        # set contents of entry form to selection content
        if iter is not None:
            for i in range(len(self.edit_form)):
                self.edit_form[i].set_text(str(model[iter][i + 1]))
            return True


    def on_submit_changes_clicked(self, source):
        id = self.get_id_of_selection()
    #return if db is empty and no selection possible
        if id == -1:
            return

        # Get path pointing to selected row in list store, ListStore starts counting at 0, so we have to use "id-1"
        path = Gtk.TreePath(id - 1)
        treeiter = self.listmodel.get_iter(path)

        # read data from input fields and store them in a list object
        new_entry_data = []
        for i in range(len(self.edit_form)):
            entry = self.edit_form[i].get_text()
            new_entry_data.append(entry)
            #start at i+1, id is not changeable
            #update model of ListStore
            self.listmodel.set_value(treeiter, i + 1, entry)

        #write data to db
        self.db.update_entry(new_entry_data, id)


    def on_new_entry_clicked(self, source):
        new_entry_data = []
        for i in range(len(self.edit_form)):
            entry = self.edit_form[i].get_text()
            new_entry_data.append(entry)
        self.db.create_entry(new_entry_data)
        self.update_model()
        self.clear_edit_form()




    def on_delete_entry_clicked(self, source):
        id = self.get_id_of_selection()
        self.db.delete_entry(id)
        self.update_model()
        self.clear_edit_form()





    #init functions
    def init_treestore(self, db):
        """
        inits the list and adds it to the main window

        :param db:
        """
        self.listmodel = Gtk.ListStore(int, str, str, str, str)
        #read data from db
        self.update_model()
        #create view
        self.view = Gtk.TreeView(model=self.listmodel)
        # get the column names
        columns = db.get_column_names()
        for i in range(len(columns)):

            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
                cell.props.weight = Pango.Weight.BOLD
            # the column is created and the column name is inserted
            col = Gtk.TreeViewColumn(columns[i], cell, text=i)
            # and it is appended to the treeview
            self.view.append_column(col)


            # when a row is selected, it emits a signal
        self.view.get_selection().connect("changed", self.on_changed)

    def init__input_form(self):
        """
        creates the form for editing entries
        entry elements are packed in aGtk.Box and added to the grid
        returns list with entry form objects

        :return: list
        """
        form_container = []

        columns = self.db.get_column_names()

        #start at second column, id column is not editable
        for i in range(1, len(columns)):
            box = Gtk.Box(spacing=6)
            box.set_homogeneous(True)
            #set column names as label text
            label = Gtk.Label(columns[i])
            box.pack_start(label, True, True, 0)
            form_container.append(Gtk.Entry())
            box.pack_start(form_container[i - 1], True, True, 0)
            self.grid.attach(box, 0, 2 + i, 1, 1)
        return form_container





    #helper functions

    def update_model(self):
        #clears the model and rereads data from db

        self.listmodel.clear()

        db_content = self.db.read_table()
        for row in db_content:
            self.listmodel.append(row)

    def get_id_of_selection(self):
        """
        returns id of selected row, -1 if no row is available
        :rtype : int

        """
        selection = self.view.get_selection()
        (model, iter) = selection.get_selected()
        if iter is not None:
            # get entry_id
            id = int(model[iter][0])
            return id
        return -1

    def clear_edit_form(self):
        for i in range(len(self.edit_form)):
            self.edit_form[i].set_text("")

class crud_ops():
    def __init__(self):
        """creates db and table if necessary and returns db object"""

    __connection = sqlite3.connect('logbook.db')

    __cursor = __connection.cursor()
    __cursor.execute("""CREATE TABLE IF NOT EXISTS my_log (
    id INTEGER PRIMARY KEY, entry_name TEXT,  entry_time TIME,entry_email TEXT,
   entry_comment TEXT)""")

    def create_entry(self, entry_data):
        self.__cursor.execute(
            '''INSERT INTO my_log(entry_name,  entry_time, entry_email, entry_comment) VALUES (?,?,?,?)''',
            entry_data)
        self.__connection.commit()

    def update_entry(self, entry_data, id):
        entry_data.append(id)
        self.__cursor.execute(
            '''UPDATE my_log SET entry_name =?,  entry_time = ?, entry_email= ?,entry_comment = ? WHERE id=?''',
            entry_data)
        self.__connection.commit()


    def read_entry(self, entry_id):
        self.__cursor.execute('''SELECT  * FROM my_log WHERE id = ?''', (entry_id,))
        return self.__cursor.fetchone()

    def delete_entry (self, entry_id):
        self.__cursor.execute('''DELETE  from my_log WHERE id = ?''', (entry_id,))
        self.__connection.commit()


    def drop_table(self):
        self.__cursor.execute('''DROP TABLE my_log''')

    def read_table(self):
        self.__cursor.execute('''SELECT * FROM my_log''')
        all_rows = self.__cursor.fetchall()


        return all_rows

    def get_column_names(self):
        """
        returns a list with all column names


        :return: list
        """
        cursor = self.__connection.execute('''SELECT * FROM my_log''')
        names = [description[0] for description in cursor.description]
        return names





class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        # create db object and pass it to view
        db = crud_ops()
        win = MyWindow(self, db)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)