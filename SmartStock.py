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
        return data

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
        return data
        
## New functions should be made between here until.. ##

# Added by Lewis Jones Function to make the Dashboard View button work
def update_dashboard():
    """HCI Requirement: Dashboard View (Total Items, Low Stock, Total Value)"""
    try:
        total_qty = sum(int(item.quantity) for item in stocks)
        total_val = calculate_total_value()
        #Low Stock Warning (< 5 units)
        low_stock_count = len([item for item in stocks if int(item.quantity) < 5])
        
        # Provides visual feedback on system status
        status_label.config(text=f"Total Items: {total_qty} | Inventory Value: £{total_val:,.2f}", fg="black")
        smart_alerts.config(text=f"Smart Alerts ({low_stock_count})", fg="red" if low_stock_count > 0 else "black")
    except Exception:
        status_label.config(text="Dashboard Error: Check Data Types")

# Added by Lewis jones: Function to make the Smart Alerts button work
# Updated by Aaron Rielly: Smart Alerts now includes expiry warnings
def show_smart_alerts():
    """Functional Requirement 2: Displays details of low stock items + expiry alerts"""
    low_stock = [f"{item.name} (Qty: {item.quantity})" for item in stocks if int(item.quantity) < 5]

    expiring_items = []
    current_time = time.time()

    for item in stocks:
        if isinstance(item, PerishableProduct):
            try:
                expiry_time = time.mktime(time.strptime(item.expiry_date, "%d/%m/%y"))
                days_left = ((expiry_time - current_time) / (60 * 60 * 24) + 1)

                if 0 <= days_left <= 7:
                    expiring_items.append(f"{item.name} (Expires in {int(days_left)} days)")
            except:
                continue

    message = ""

    if low_stock:
        message += "Low Stock Items:\n" + "\n".join(low_stock) + "\n\n"

    if expiring_items:
        message += "Expiring Soon:\n" + "\n".join(expiring_items)

    if message:
        messagebox.showwarning("Smart Alerts", message)
    else:
        messagebox.showinfo("Smart Alerts", "All stock levels are healthy.")

# added by Ben
def load_items():
    try:
        with open ("save.json", "r") as file:
            saved_items = json.load(file)
            for item in saved_items:
                if item["type"] == "perishable":
                    
                    new_item = PerishableProduct(item["id"], item["name"], item["price"], item["quantity"], item["expiry_date"], item["storage_temp"])
                    stocks.append(new_item)
                else:
                    new_item = ElectronicProduct(item["id"], item["name"], item["price"], item["quantity"], item["warranty_period"], item["power_usage"])
                    stocks.append(new_item)
            for item in stocks:
                if isinstance(item, PerishableProduct):
                    inventory_list.insert(tk.END,f"{item.name} (ID: {item.id}), Price: £{item.price}, Quantity: {item.quantity}, Exp date: {item.expiry_date}, temperature: {item.storage_temp}")
                else:
                    inventory_list.insert(tk.END, f"{item.name} (ID: {item.id}), Price: £{item.price}, Quantity: {item.quantity}, warranty: {item.warranty_period}, Power usage: {item.power_usage}")
        #status_label.config(text="File loaded", fg="blue")
    except FileNotFoundError:
        status_label.config(text="No file found", fg="blue")
    except json.decoder.JSONDecodeError:
        messagebox.showwarning("Broken or empty save file!", "Skipping load process.")


#added by Ben
# Added by Lewis Jones edit Ben's Save button to ensure it writes to the file
def save():
    try:
            # Writes the current stocks list to the physical JSON file   
        dict_form = []
        for items in stocks:
            dict_item = items.dict_conv()
            dict_form.append(dict_item)
        with open("save.json","w") as file:
            json.dump(dict_form, file, indent=4)
        status_label.config(text="Inventory Saved to JSON", fg="blue")
    except Exception as e:
        messagebox.showerror("Save Error", str(e))

#Add: added by Daniel Caveney
#radio buttons, all dictionary saves replaced by Ben McManus including the introduction of classes
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

    add_win.class_selection = tk.StringVar(value="perishable")
    def title_swap(expiry_or_warranty_func, temp_or_power_func):
        expiry_date_or_warranty.config(text = expiry_or_warranty_func)
        temp_or_power.config(text= temp_or_power_func)
        
    tk.Radiobutton(add_win, text="Perishable", value="perishable", variable=add_win.class_selection, command=lambda:title_swap("Expiry date:", "Temperature:")).grid(row=4, column=0)
    tk.Radiobutton(add_win, text="Electronic", value="electronic", variable= add_win.class_selection, command=lambda: title_swap("Warranty:","Power usage:")).grid(row=4, column=1)

    expiry_date_or_warranty = tk.Label(add_win, text="Expiry date:")
    expiry_date_or_warranty.grid(row=5, column=0)
    Expiry_or_warranty_input = tk.Entry(add_win)
    Expiry_or_warranty_input.grid(row=5, column=1)
    
    
    temp_or_power = tk.Label(add_win, text="Temperature:")
    temp_or_power.grid(row=6, column=0)
    temp_or_power_input = tk.Entry(add_win)
    temp_or_power_input.grid(row=6, column=1)

    def submit():
        id_val = stock_id.get().strip()
        name_val = stock_name.get().strip()
        price_val = stock_price.get().strip()
        qty_val = stock_qty.get().strip()
        Expiry_or_warranty_input_strip = Expiry_or_warranty_input.get().strip()
        temp_or_power_input_strip = temp_or_power_input.get().strip()

        # Added by Lewis Error handling to prevent empty submissions
        if not id_val or not name_val or not price_val or not qty_val or not Expiry_or_warranty_input_strip or not temp_or_power_input_strip:
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
        try:
            valid_time = time.strptime(Expiry_or_warranty_input_strip, "%d/%m/%y")
          
        except ValueError:
            messagebox.showwarning("Input Error!", "Expiry has to be in the format DD/MM/YY")
            return
        try:
            tp_or_pw = int(temp_or_power_input_strip)
        except ValueError:
            messagebox.showwarning("Input Error!", "Temperature or power usage must be an integer.")
            return

        #a variable that contains all the parts of the stock
        class_choice = add_win.class_selection.get()
        item_name = name_val
        if class_choice == "perishable":

            item_name = PerishableProduct(id_val, name_val, price_val, qty_val,time.strftime("%d/%m/%y",valid_time),tp_or_pw)
            # Updates Listbox
            inventory_list.insert(tk.END, f"{item_name.name} (ID: {item_name.id}), Price: £{item_name.price}, Quantity: {item_name.quantity}, Exp date: {item_name.expiry_date}, temperature: {item_name.storage_temp}")
        
        else:
            item_name= ElectronicProduct(id_val, name_val, price_val, qty_val,time.strftime("%d/%m/%y",valid_time),tp_or_pw)
            inventory_list.insert(tk.END, f"{item_name.name} (ID: {item_name.id}), Price: £{item_name.price}, Quantity: {item_name.quantity}, warranty: {item_name.warranty_period}, Power usage: {item_name.power_usage}")

        # Add new version to your list
        stocks.append(item_name)
        log_transaction("ADD", stocks[-1])
         
        # Update dashboard metrics
        update_dashboard()
        
        status_label.config(text=f"Added {item_name.name}", fg="green")
        add_win.destroy()

    tk.Button(add_win, text="Save Product", command=submit).grid(row=7, columnspan=2)

#Edit: added by Daniel Caveney
#radio buttons, all dictionary saves replaced by Ben McManus including the introduction of classes
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
    name_entry.insert(0, stock_info.name)
    name_entry.grid(row=0, column=1)
    
    tk.Label(edit_win, text="Price:").grid(row=1, column=0)
    price_entry = tk.Entry(edit_win)
    price_entry.insert(0, stock_info.price)
    price_entry.grid(row=1, column=1)

    tk.Label(edit_win, text="Quantity:").grid(row=2, column=0)
    qty_entry = tk.Entry(edit_win)
    qty_entry.insert(0, stock_info.quantity)
    qty_entry.grid(row=2, column=1)

    if isinstance(stock_info, PerishableProduct):
        tk.Label(edit_win, text="Expiry Date:").grid(row=3, column=0)
        expiry_entry = tk.Entry(edit_win)
        expiry_entry.insert(0, stock_info.expiry_date)
        expiry_entry.grid(row=3, column=1)

        tk.Label(edit_win, text="Storage Temperature:").grid(row=4, column=0)
        temp_entry = tk.Entry(edit_win)
        temp_entry.insert(0, stock_info.storage_temp)
        temp_entry.grid(row=4, column=1)
    else:
        tk.Label(edit_win, text="Warranty end:").grid(row=3, column=0)
        warranty_entry = tk.Entry(edit_win)
        warranty_entry.insert(0, stock_info.warranty_period)
        warranty_entry.grid(row=3, column=1)

        tk.Label(edit_win, text="Power Usage:").grid(row=4, column=0)
        power_entry = tk.Entry(edit_win)
        power_entry.insert(0, stock_info.power_usage)
        power_entry.grid(row=4, column=1)

    def save_changes():
        #Updates the chosen item to what the user inputs
        name_val = name_entry.get().strip()
        price_val = price_entry.get().strip()
        qty_val = qty_entry.get().strip()
        try:
            expiry_date =expiry_entry.get().strip()
            temperature = temp_entry.get().strip()
            
            try:
                valid_time = time.strptime(expiry_date, "%d/%m/%y")
            
            except ValueError:
                messagebox.showwarning("Input Error!", "Expiry has to be in the format DD/MM/YY")
                return
            try:
                tp_or_pw = int(temperature)
            except ValueError:
                messagebox.showwarning("Input Error!", "Temperature or power usage must be an integer.")
                return     
        except NameError:
            warranty_date = warranty_entry.get().strip()
            power_usage = power_entry.get().strip()

            try:
                valid_time = time.strptime(warranty_date, "%d/%m/%y")
            
            except ValueError:
                messagebox.showwarning("Input Error!", "Expiry has to be in the format DD/MM/YY")
                return
            try:
                tp_or_pw = int(power_usage)
            except ValueError:
                messagebox.showwarning("Input Error!", "Temperature or power usage must be an integer.")
                return

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
        
        stocks[index].name = name_val
        stocks[index].price = price_val
        stocks[index].quantity = qty_val
        if isinstance(stock_info, PerishableProduct):
            stocks[index].expiry_date = time.strftime("%d/%m/%y",valid_time)
            stocks[index].storage_temp = tp_or_pw
        else:
            stocks[index].warranty_period = time.strftime("%d/%m/%y",valid_time)
            stocks[index].power_usage = tp_or_pw

        #deletes the old values and inserts the new stock information
        inventory_list.delete(index)
        if isinstance(stock_info,PerishableProduct):
            inventory_list.insert(index, 
            f"{stocks[index].name} (ID: {stocks[index].id}), Price: £{stocks[index].price}, Quantity: {stocks[index].quantity} Exp date: {stocks[index].expiry_date}, temperature: {stocks[index].storage_temp}")
        else:
             inventory_list.insert(index, 
            f"{stocks[index].name} (ID: {stocks[index].id}), Price: £{stocks[index].price}, Quantity: {stocks[index].quantity} warranty: {stocks[index].warranty_period}, Power usage: {stocks[index].power_usage}")
        
        log_transaction("EDIT", stocks[index])
        
        # Update dashboard
        update_dashboard()
        
        status_label.config(text="Product updated", fg="blue")
        edit_win.destroy()

    tk.Button(edit_win, text="Update", command=save_changes).grid(row=5, columnspan=2)

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

        # Update dashboard
        update_dashboard()

        status_label.config(text="Stock deleted from list", fg="green")
        root.after(3000, lambda: status_label.config(text=""))

# Transaction History: added by Esa
def log_transaction(action, product_data):
    try:
        with open("transaction_history.txt", "a") as file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            file.write(
                f"{timestamp} | {action} | "
                f"ID: {product_data.id} | "
                f"Name: {product_data.name} | "
                f"Price: {product_data.price} | "
                f"Quantity: {product_data.quantity}\n"
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
            price = float(item.price)
            quantity = int(item.quantity)
            total_value += price * quantity
        except:
            continue

    return total_value


def show_total_value():
    if not stocks:
        messagebox.showinfo("Total Stock Value", "No stock available.")
        return

    total_value = calculate_total_value()
    messagebox.showinfo("Total Stock Value", f"Total stock value: £{total_value:.2f}") # edited by esa, added for empty stock handling


# Added by Aaron Rielly: Dashboard Summary for the items with analytics + colour coding
def show_dashboard_summary():
    """HCI Requirement: Advanced Dashboard Summary (Visual + Analytics)"""
    try:
        if not stocks:
            messagebox.showinfo("Dashboard", "No inventory data available.")
            return

        total_qty = sum(int(item.quantity) for item in stocks)
        total_val = calculate_total_value()
        low_stock_items = [item for item in stocks if int(item.quantity) < 5]

        total_products = len(stocks)
        low_stock_count = len(low_stock_items)

        # Avoid division by zero
        low_stock_percent = (low_stock_count / total_products * 100) if total_products > 0 else 0

        # Determine system health colour + message
        if low_stock_count == 0:
            health_text = "Stock Levels Ok"
            health_color = "green"
        else:
            health_text = "Critical: Low Stock, replace immediately"
            health_color = "red"

        # Create dashboard window
        dash_win = tk.Toplevel(root)
        dash_win.title("Inventory Dashboard")
        dash_win.geometry("400x300")

        # Header
        tk.Label(dash_win, text="--- Inventory Dashboard ---", 
                 font=("Arial", 13, "bold")).pack(pady=10)

        # System Health
        tk.Label(dash_win, text=health_text, fg=health_color, 
                 font=("Arial", 13, "bold")).pack(pady=5)

        # Core Metrics
        tk.Label(dash_win, text=f"Total Products: {total_products}", font=("Arial", 11)).pack(pady=3)
        tk.Label(dash_win, text=f"Total Quantity: {total_qty}", font=("Arial", 11)).pack(pady=3)
        tk.Label(dash_win, text=f"Inventory Value: £{total_val:.2f}", font=("Arial", 11)).pack(pady=3)

        # Low Stock Analytics
        tk.Label(dash_win, text=f"Low Stock Items: {low_stock_count}", 
                 fg="red" if low_stock_count else "black",
                 font=("Arial", 11, "bold")).pack(pady=5)

        tk.Label(dash_win, text=f"Low Stock Percentage: {low_stock_percent:.1f}%", 
                 font=("Arial", 11)).pack(pady=3)

        # Divider
        tk.Label(dash_win, text="-----------------------------").pack(pady=5)

        # Low stock item list
        if low_stock_items:
            tk.Label(dash_win, text="Items needing restock:", 
                     font=("Arial", 11, "bold")).pack()

            for item in low_stock_items:
                tk.Label(dash_win, 
                         text=f"{item.name} (Qty: {item.quantity})", 
                         fg="red").pack()
        else:
            tk.Label(dash_win, text="All stock levels are healthy.", 
                     fg="green").pack()

    except Exception:
        messagebox.showerror("Dashboard Error", "Could not generate dashboard summary.")


# Added by Aaron Rielly: Detect items expiring within 7 days on startup
def check_expiry_alerts():
    """Functional Requirement: Detect perishable items expiring within 7 days"""
    try:
        expiring_items = []
        current_time = time.time()

        for item in stocks:
            if isinstance(item, PerishableProduct):
                try:
                    expiry_time = time.mktime(time.strptime(item.expiry_date, "%d/%m/%y"))
                    days_left = ((expiry_time - current_time) / (60 * 60 * 24)+1)

                    if 0 <= days_left <= 7:
                        expiring_items.append(f"{item.name} (Expires in {int(days_left)} days)")
                except:
                    continue

        # Show report on startup
        if expiring_items:
            messagebox.showwarning(
                "Expiry Alert Report",
                "Items expiring within 7 days:\n\n" + "\n".join(expiring_items)
            )

    except Exception:
        messagebox.showerror("Expiry Error", "Could not check expiry dates.")


## .. GUI design (LO3 HCI) ##
root = tk.Tk()
root.geometry("800x500") # Adjusted height for the dashboard elements
root.title("Smart Stock")

btn_style = {"font": ("Arial", 12), "width": 15} #consistent button style: use **btn_style (Dan)

# Added by Lewis Visual Dashboard Header
dashboard_header = tk.Label(root, text="--- SYSTEM DASHBOARD ---", font=("Arial", 12, "bold"))
dashboard_header.pack(side="top", pady=5)

inventory_list = tk.Listbox(width=80, height=20)    #Someone
inventory_list.pack(side="left", anchor="n", padx=10, pady=10)

add_button = tk.Button(root, text="Add Stock", command=add_stock, **btn_style)  #Dan Caveney
add_button.pack(pady=5, padx=10)

edit_button = tk.Button(text="Edit Stock", command=edit_stock, **btn_style)    #Dan Caveney
edit_button.pack(pady=5, padx=10)

remove_button = tk.Button(root, text="Remove Stock", command=remove_stock, **btn_style)   #Dan Caveney
remove_button.pack(pady=5, padx=10)

# Updated by Lewis Linked button to functional logic
smart_alerts = tk.Button(text=f"Smart Alerts", command=show_smart_alerts, **btn_style)   #could have a little number next to it
# or something to act as a noticacation                 # Someone
smart_alerts.pack(pady=5)

value_calculation_button = tk.Button(root, text="Value Calculation", command=show_total_value, **btn_style) # Esa
value_calculation_button.pack(pady=5)

transaction_history_button = tk.Button(root, text="Transaction History", command=show_transaction_history, **btn_style) # Esa 
transaction_history_button.pack(pady=5)

save_button = tk.Button(text="Save", command=save, **btn_style) # Ben
save_button.pack(pady=5)


# Updated by Lewis Linked button to Dashboard Refresh logic
dashboard_button = tk.Button(text="Dashboard View", command=show_dashboard_summary, **btn_style) #Added by Aaron, Links Dashboard Button to dashboard summary code.
dashboard_button.pack(pady=5)

status_label = tk.Label(root, text="Ready") #Dan, added for the labels, allows users to 
                                            #know what they're doing
status_label.pack(pady=10)

# Initialize stats on startup
load_items()
update_dashboard()
check_expiry_alerts() # <-- Added by Aaron to initalise the expiry checks
root.mainloop()
