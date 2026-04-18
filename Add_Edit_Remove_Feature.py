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

def add_stock():
    add_win = tk.Toplevel(root)
    add_win.title("Add New Stock")

    
    #Creates input fields to input stock info
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
        id_val = stock_id.get().strip()
        name_val = stock_name.get().strip()
        price_val = stock_price.get().strip()
        qty_val = stock_qty.get().strip()

        
        if not id_val or not name_val or not price_val or not qty_val:
            messagebox.showwarning("Input Error!", "All fields need to be filled.")
            return

        try:
            price_val = float(price_val)
        except ValueError:
            messagebox.showwarning("Input Error!", "Price must be a float or integer.")
            return
        
        try:
            qty_val = int(qty_val)
        except ValueError:
            messagebox.showwarning("Input Error!", "Quantity must be an integer.")
            return
        
        #a variable that contains all the parts of the stock
        new_product = Product(id_val, name_val, price_val, qty_val)
        
        # Add new version to your list
        stocks.append(new_product.dict_conv())
        log_transaction("ADD", stocks[-1])
        
        # Updates Listbox
        inventory_list.insert(tk.END, f"{new_product.name} (ID: {new_product.id}), Price: £{new_product.price}, Quantity: {new_product.quantity}")
        
        status_label.config(text=f"Added {new_product.name}", fg="green")
        add_win.destroy()

    tk.Button(add_win, text="Save Product", command=submit).grid(row=4, columnspan=2)

#Edit: added by Daniel Caveney
def edit_stock():

    selected = inventory_list.curselection()

    if not selected:
        messagebox.showwarning("Error!", "Select a stock to edit")
        return
    
    index = selected[0]
    stock_info = stocks[index]

    edit_win = tk.Toplevel(root)
    edit_win.title("Edit Stock")

    #Similar layout to the add window (consistency)
    tk.Label(edit_win, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(edit_win)
    name_entry.insert(0, stock_info['name'])
    name_entry.grid(row=0, column=1)
    
    tk.Label(edit_win, text="Price:").grid(row=1, column=0)
    price_entry = tk.Entry(edit_win)
    price_entry.insert(0, stock_info['price'])
    price_entry.grid(row=1, column=1)

    tk.Label(edit_win, text="Quantity:").grid(row=2, column=0)
    qty_entry = tk.Entry(edit_win)
    qty_entry.insert(0, stock_info['quantity'])
    qty_entry.grid(row=2, column=1)

    def save_changes():
        #Updates the chosen item to what the user inputs
        name_val = name_entry.get().strip()
        price_val = price_entry.get().strip()
        qty_val = qty_entry.get().strip()

        if not name_val or not price_val or not qty_val:
            messagebox.showwarning("Input Error!", "All fields need to be filled.")
            return
        
        try:
            price_val = float(price_val)
        except ValueError:
            messagebox.showwarning("Input Error!", "Price must be a float or integer.")
            return
        
        try:
            qty_val = int(qty_val)
        except ValueError:
            messagebox.showwarning("Input Error!", "Quantity must be an integer.")
            return
        
        stocks[index]['name'] = name_val
        stocks[index]['price'] = price_val
        stocks[index]['quantity'] = qty_val

        #deletes the old values and inserts the new stock information
        inventory_list.delete(index)
        inventory_list.insert(index, 
        f"{stocks[index]['name']} (ID: {stocks[index]['id']}), Price: £{stocks[index]['price']}, Quantity: {stocks[index]['quantity']}")
        
        status_label.config(text="Product updated", fg="blue")
        edit_win.destroy()

    tk.Button(edit_win, text="Update", command=save_changes).grid(row=3, columnspan=2)

#Remove: added by Daniel Caveney
def remove_stock():

    selected = inventory_list.curselection()

    if not selected:
        messagebox.showwarning("Error!", "Select a stock to remove")
        return

    index = selected[0]

    if messagebox.askyesno("Confirm", "Remove Stock?"):
        removed_item = stocks[index]
        log_transaction("REMOVE", removed_item)
        stocks.pop(index)
        inventory_list.delete(index)

        status_label.config(text="Stock deleted from list", fg="green")
        root.after(3000, lambda: status_label.config(text=""))

# Transaction History: added by Esa
def log_transaction(action, product_data):
    try:
        with open("transaction_history.txt", "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(
                f"{timestamp} | {action} | "
                f"ID: {product_data['id']} | "
                f"Name: {product_data['name']} | "
                f"Price: {product_data['price']} | "
                f"Quantity: {product_data['quantity']}\n"
            )
    except:
        messagebox.showwarning("File Error!", "Could not write to transaction history file.")


def show_transaction_history():
    history_win = tk.Toplevel(root)
    history_win.title("Transaction History")
    history_win.geometry("600x400")

    text_box = tk.Text(history_win, wrap="word")
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    try:
        with open("transaction_history.txt", "r") as file:
            history_data = file.read()
            if history_data.strip() == "":
                text_box.insert("1.0", "No transaction history available.")
            else:
                text_box.insert("1.0", history_data)
    except FileNotFoundError:
        text_box.insert("1.0", "No transaction history file found yet.")
    except:
        text_box.insert("1.0", "Could not load transaction history.")

    text_box.config(state="disabled")


# Value Calculation: added by Esa Burtwistle
def calculate_total_value():
    total_value = 0

    for item in stocks:
        try:
            price = float(item["price"])
            quantity = int(item["quantity"])
            total_value += price * quantity
        except:
            continue

    return total_value


def show_total_value():
    total_value = calculate_total_value()
    messagebox.showinfo("Total Stock Value", f"Total stock value: £{total_value:.2f}")

## .. GUI design (LO3 HCI) ##
root = tk.Tk()
root.geometry("500x500")
root.title("Smart Stock")

btn_style = {"font": ("Arial", 12), "width": 12} #consistent button style: use **btn_style (Dan)

inventory_list = tk.Listbox(width=40, height=20)    #Someone
inventory_list.pack(side="left", anchor="n", padx=10, pady=10)

add_button = tk.Button(root, text="Add Stock", command=add_stock, **btn_style)  #Dan Caveney
add_button.pack(pady=5, padx=10)

edit_button = tk.Button(text="Edit Stock", command=edit_stock, **btn_style)    #Dan Caveney
edit_button.pack(pady=5, padx=10)

remove_button = tk.Button(root, text="Remove Stock", command=remove_stock, **btn_style)   #Dan Caveney
remove_button.pack(pady=5, padx=10)

smart_alerts = tk.Button(text=f"Smart Alerts")   #could have a little number next to it
# or something to act as a noticacation                 # Someone
smart_alerts.pack()

value_calculation_button = tk.Button(root, text="Value Calculation", command=show_total_value) # Esa
value_calculation_button.pack()

transaction_history_button = tk.Button(root, text="Transaction History", command=show_transaction_history) # Esa 
transaction_history_button.pack()

save_button = tk.Button(text="Save", command=save) # Ben
save_button.pack()

dashboard_button = tk.Button(text="Dashboard View") # Someone
dashboard_button.pack()

status_label = tk.Label(root, text="Ready") #Dan, added for the labels, allows users to 
                                            #know what they're doing
status_label.pack(pady=10)

root.mainloop()