import tkinter as tk
import time
import json
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



## .. Here ##
root = tk.Tk()
root.geometry("500x500")
root.title("Smart Stock")


inventory_list = tk.Listbox(width=30, height=20)    #Someone
inventory_list.pack(side="left", anchor="n", padx=10, pady=10)

add_button = tk.Button(text="Add")  #Someone
add_button.pack()

edit_button = tk.Button(text="Edit")    #Someone
edit_button.pack()

remove_button = tk.Button(text="Remove")    #Someone
remove_button.pack()

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


root.mainloop()