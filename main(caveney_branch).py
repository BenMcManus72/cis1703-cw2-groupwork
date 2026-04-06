#SmartStock inventory program

#importing tkinter for the GUI and JSON for saving the inventory stock
import tkinter as tk
from tkinter import messagebox
import time
import json

#SuperClass product, contains all necessary variables in a dictionary 
# to be retrieved for the inventory tasks.
class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
    def dict_conv(self):
        return{
            "type": "product",
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
        }

#subclasses- inherits the variables from the product class and contain 
# their own unique variables in seperate dictionaries
class PerishableProduct(Product):
    def __init__(self, id, name, price, quantity, expiry_date, storage_temp):
        super().__init__(id, name, price, quantity)
        self.expiry_date = expiry_date
        self.storage_temp = storage_temp
    def dict_conv(self):
        data = super().dict_conv()
        data.update({
            "type": "perishable",
            "expiry_date": self.expiry_date,
            "storage_temp":self.storage_temp
        })

class ElectronicProduct(Product):
    def __init__(self, id, name, price, quantity, warranty_period, power_usage):
        super().__init__(id, name, price, quantity)
        self.warranty_period = warranty_period
        self.power_usage = power_usage
    def dict_conv(self):
        data = super().dict_conv()
        data.update({
            "type": "electronic",
            "warranty_period": self.warranty_period,
            "power_usage": self.power_usage
        })
## New functions should be made between here until.. ##

def save():
    try:
        with open("save.json","r") as file:
            data = json.load(file)


    except:
        pass

#Add: added by Daniel Caveney
stocks = []

def open_add_window():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Product")
    
    # Create input fields
    tk.Label(add_win, text="ID:").grid(row=0, column=0)
    stock_id = tk.Entry(add_win)
    stock_id.grid(row=0, column=1)

    tk.Label(add_win, text="Name:").grid(row=1, column=0)
    stock_name = tk.Entry(add_win)
    stock_name.grid(row=1, column=1)

    tk.Label(add_win, text="Price:").grid(row=2, column=0)
    stock_price = tk.Entry(add_win)
    stock_price.grid(row=2, column=1)

    tk.Label(add_win, text="Quantity:").grid(row=3, column=0)
    stock_qty = tk.Entry(add_win)
    stock_qty.grid(row=3, column=1)

    def submit():
        #a variable that contains all the parts of the stock
        new_product = Product(stock_id.get(), stock_name.get(), stock_price.get(), stock_qty.get())
        
        # Add new version to your list
        stocks.append(new_product.dict_conv())
        
        # Updates Listbox
        inventory_list.insert(tk.END, f"{new_product.name} (ID: {new_product.id}), Price: £{new_product.price}, Quantity: {new_product.quantity}")
        
        status_label.config(text=f"Added {new_product.name}", fg="green")
        add_win.destroy()

    tk.Button(add_win, text="Save Product", command=submit).grid(row=4, columnspan=2)


    
#Remove: added by Daniel Caveney
def remove_stock():

    selected = inventory_list.curselection()

    if not selected:
        status_label.config(text="No stock selected")
        return

    index = selected[0]
    task = inventory_list.get(index)

    if messagebox.askyesno("Confirm", "Remove Stock?"):
        inventory_list.delete(selected[0])
        status_label.config(text="Stock deleted from list", fg="green")
        root.after(3000, lambda: status_label.config(text=""))

    inventory_list.delete(index)

    stocks.remove(task)

    status_label.config(text=f"{len(stocks)} total stock")


## .. GUI design (LO3 HCI) ##
root = tk.Tk()
root.geometry("500x500")
root.title("Smart Stock")

btn_style = {"font": ("Arial", 12), "width": 12} #consistent button style: use **btn_style (Dan)

inventory_list = tk.Listbox(width=40, height=20)    #Someone
inventory_list.pack(side="left", anchor="n", padx=10, pady=10)

add_button = tk.Button(root, text="Add Stock", command=open_add_window, **btn_style)  #Dan Caveney
add_button.pack(pady=5, padx=10)

edit_button = tk.Button(text="Edit", **btn_style)    #Someone
edit_button.pack(pady=5, padx=10)

remove_button = tk.Button(root, text="Remove Stock", command=remove_stock, **btn_style)   #Dan Caveney
remove_button.pack(pady=5, padx=10)

smart_alerts = tk.Button(text=f"Smart Alerts")   #could have a little number next to it
# or something to act as a noticacation                 # Someone
smart_alerts.pack()

value_calculation_button = tk.Button(text="Value Calculation") # Someone
value_calculation_button.pack()

transaction_history_button = tk.Button(text="Transaction History") # Someone
transaction_history_button.pack()

save_button = tk.Button(text="Save", command=save) # Ben
save_button.pack()

dashboard_button = tk.Button(text="Dashboard View") # Someone
dashboard_button.pack()

status_label = tk.Label(root, text="Ready") #Dan, added for the labels, allows users to 
                                            #know what they're doing
status_label.pack(pady=10)

root.mainloop()