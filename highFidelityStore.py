from tkinter import ttk
from tkinter import *
import sqlite3

class Product:
    dbName = "Products.db"

    def __init__(self, window):   #Constructor
        self.wind = window
        self.wind.title("High Fidelity Records")

        #Create a Frame Container
        frame = LabelFrame(self.wind, text = "Register Product")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)  #Position of frame
        #Name input
        Label(frame, text = "Name: ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)
        #Price input
        Label(frame, text = "Price: ").grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        #Button to add products
        ttk.Button(frame, text = "Save Product", command = self.add_products).grid(row = 3,
        columnspan = 2, sticky = W + E) #With command can specify funcionality
        #Output messages
        self.message = Label(text = "", fg = 'green')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        #Create Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading("#0", text = "Name", anchor = CENTER)
        self.tree.heading("#1", text = "Price", anchor = CENTER)
        #Buttons delete and edit
        ttk.Button(text = "Delete", command = self.delete_products).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = "Edit", command = self.edit_products).grid(row = 5, column = 1, sticky = W + E)
        #Fill the row
        self.get_products()

    def run_query(self, query, parameters = ()): #Execute query FROM DATABASE
        with sqlite3.connect(self.dbName) as connection:
            cursor = connection.cursor()
            result = cursor.execute(query, parameters)
            connection.commit()
        return result

    def get_products(self):
        records = self.tree.get_children()  #Obtain every data in table tree
        for element in records:
            self.tree.delete(element)   #Clean table
        #Quering data
        query = "SELECT * FROM product ORDER BY name DESC"
        db_rows = self.run_query(query)
        #Fill data
        for row in db_rows:  #Inserts in table
             self.tree.insert("", 0, text = row[1], values = row[2])
            #print(row)

    def validation(self):   #name and price
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_products(self):
        if(self.validation()):
            print(self.name.get())
            print(self.price.get())
            query = "INSERT INTO product VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get()) #Obtain price and name
            self.run_query(query, parameters)
            self.message["text"] = "Product {} added Successfully".format(self.name.get())
            #Cleans inputs
            self.name.delete(0, END)
            self.price.delete(0, END)
            print("Data saved")
        else:
            self.message["text"] = "Name and Price are required"
            print("tu eres weon")
        self.get_products

    def delete_products(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as error:
            self.message["text"] = "Please select a register"
            return
        self.message["text"] = ""
        name = self.tree.item(self.tree.selection())["text"]
        query = "DELETE FROM product WHERE name = ?"
        self.run_query(query, (name, ))
        self.message["text"] = "Register {} deleted".format(name)
        self.get_products()

    def edit_products(self):
        self.message["text"] = ""
        try:
            self.tree.item(self.tree.selection())["text"][0]
        except IndexError as error:
            self.message["text"] = "Please select a register"
            return
        #name and price selected
        name = self.tree.item(self.tree.selection())["text"]
        oldPrice = self.tree.item(self.tree.selection())["values"][0]
        self.edit_wind = Toplevel() #creates a window
        self.edit_wind.title = "Edit window"
        #Old name
        Label(self.edit_wind, text = "Old name: ").grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name),
        state = "readonly").grid(row = 0, column = 2)
        #New name
        Label(self.edit_wind, text = "New name: ").grid(row = 1, column = 1)
        newName = Entry(self.edit_wind)
        newName.grid(row = 1, column = 2)
        #Old price
        Label(self.edit_wind, text = "Old price: ").grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = oldPrice),
        state = "readonly").grid(row = 2, column = 2)
        #New price
        Label(self.edit_wind, text = "New price: ").grid(row = 3, column = 1)
        newPrice = Entry(self.edit_wind)
        newPrice.grid(row = 3, column = 2)

        Button(self.edit_wind, text = "Update", command = lambda: self.edit_registers(
        newName.get(), name, newPrice.get(), oldPrice)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_registers(self, newName, oldName, newPrice, oldPrice):
        query = "UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?"
        parameters = (newName, newPrice, oldName, oldPrice)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message["text"] = "Register {} updated".format(oldName)
        self.get_products()


if __name__ == '__main__':  #Execute main function
    window = Tk()
    application = Product(window)
    window.mainloop()   #Execute window

print("hola")
