# Importing various libraries
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import time
import locale

locale.setlocale(locale.LC_ALL, '') # Setting up locale for currency

# Array assigns values to coins
COINVALUE = [
    ["5p", "10p", "20p", "50p", "£1", "£2"],
    [5, 10, 20, 50, 100, 200]
]

# Array assigns values to notes
NOTEVALUE = [
    ["£5", "£10", "£20"],
    [500, 1000, 2000]
]

# Array to cotain all data on drinks in the machine
DRINKS = [
    ["Pepsi", "Pepsi Max", "Coca Cola", "Coca Cola ZERO",
     "Fanta Orange", "Fanta Cherry", "7up", "Sprite",
     "DrPepper", "Vimto", "Smart Water", "Lipton Peach",
     "Monster Energy", "Monster Ultra Rosá", "Red Bull", "Lucozade"], # Drink name
    [200, 180, 200, 180,
     200, 200, 160, 160,
     220, 180, 120, 150,
     300, 300, 280, 320], # Drink price
    ["A1", "A2", "A3", "A4",
     "B1", "B2", "B3", "B4",
     "C1", "C2", "C3", "C4",
     "D1", "D2", "D3", "D4"], # Drink Code
    [10, 10, 10, 10,
     10, 10, 10, 10,
     10, 10, 1, 10,
     10, 10, 10, 10], # Drink Stock
    ["pepsi", "pepsimax", "cocacola", "cocacolazero",
     "fantaorange", "fantacherry", "7up", "sprite",
     "drpepper", "vimto", "smartwater", "liptonpeach",
     "monsterenergy", "monsterultrarosa", "redbull", "lucozade"] # Drink image file name
]

# User wallets
COINWALLET = [5, 3, 10, 2, 4, 2] # Coin quanitity
NOTEWALLET = [4, 7, 2] # Note quanitity
card_balance = 00 # User card balance
valid_pin = "4321" # User card pin

CHANGE = [20, 30, 20, 10, 40, 20, 10, 10, 5] # Amount of change
KEYS = ["A", "1", "2", "B", "3", "4", "C", "5", "6", "D", "7", "8", "E", "9" ,"0"] # Keys for generating the keypad

# Variables used to set up the machine
user_input = ""
machine_balance = 0
processing_payment = False
loyalty_text = False
loyalty_scanned = False

# Staff code to access machine admin panel
staff_code = "ABC123"

root = tk.Tk()  # Creates window
payment_label_text = tk.StringVar(root, "")

# Opened by entering staff code. Creates a window that allows staff to manage the machine
def admin_panel():
    global processing_payment
    def admin_close():  # Closes the admin panel and allows user to use the machine again
        global processing_payment
        processing_payment = False
        admin_window.destroy()

    def staff_menu():  # Method to create staff menu
        staff_menu = Frame(admin_window, height=300, width=270, padx=10, pady=10)
        staff_menu.pack()
        tk.Label(staff_menu, text="Please select an option", font=("Arial", 15)).pack(pady=10)
        Button(staff_menu, text="Check Drink Stock", command=lambda: [check_stock(), staff_menu.destroy()]).pack(pady=5)
        Button(staff_menu, text="Restock Drinks", command=lambda: [restock(), staff_menu.destroy()]).pack(pady=5)
        Button(staff_menu, text="Check Change", command=lambda: [check_change(), staff_menu.destroy()]).pack(pady=5)
        Button(staff_menu, text="Add Change", command=lambda: [add_change(), staff_menu.destroy()]).pack(pady=5)
        Button(staff_menu, text="Remove Non-Sellable Items", command=lambda: remove_non_sellable_items()).pack(pady=5)
        Button(staff_menu, text="Exit", command=admin_close).pack(pady=5)

    def check_stock():  # Check stock of drinks in the machine
        check_stock_frame = Frame(admin_window)
        check_stock_frame.pack()
        check_stock_labels = []
        row_count = 0
        column_count = 0
        for x in range(len(DRINKS[0])):
            check_stock_labels.append(Label(check_stock_frame, text=DRINKS[0][x] + "'s remaining:" + str(DRINKS[3][x]), font=("Arial", 9), width=30, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            column_count += 1
            if column_count == 4:
                column_count = 0
                row_count += 1
        Button(check_stock_frame, text="Back", command=lambda: [staff_menu(), check_stock_frame.destroy()]).grid(row=9, column=0, columnspan=4, sticky="nesw")

    def restock():  # Staff window to restock drinks
        restock_frame = Frame(admin_window)
        restock_frame.pack()
        restock_frame_buttons = []
        restock_frame_labels = []
        row_count = 1
        column_count = 0
        for x in range(len(DRINKS[0])):  # Loop to create all buttons and labels
            row_count -= 1
            restock_frame_labels.append(Label(restock_frame, text=DRINKS[0][x] + "'s remaining: " + str(DRINKS[3][x]), font=("Arial", 9), width=30, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            row_count += 1
            restock_frame_buttons.append(Button(restock_frame, text="Restock", font=("Arial", 9), command=lambda x=x: [restock_drink(x), restock_frame.destroy()]).grid(row=row_count, column=column_count, padx=5, pady=5))
            column_count += 1
            if column_count == 4:
                column_count = 0
                row_count += 2
        Button(restock_frame, text="Back", command=lambda: [staff_menu(), restock_frame.destroy()]).grid(row=9, column=0, columnspan=4, sticky="nesw")

    def restock_drink(value):  # Method to restock selected rink
        def restocking(drink): # Used to verify drink can be restocked
            global drinks_display_frame
            global DRINKS
            try:
                restock_num = int(restock_entry.get())  # Retrieves data from entry box and converts to int
                if restock_num < 0:
                    messagebox.showerror("Input error", "Please input a valid value.")
                elif (restock_num + DRINKS[3][drink]) > 10:
                    messagebox.showerror("Capacity Exceeded", "Capacity Exceeded. Max capacity: 10")
                else:
                    DRINKS[3][drink] += restock_num
                    if (DRINKS[3][drink] - restock_num) == 0:
                        drinks_display_frame.destroy()
                        drinks_display()
                    messagebox.showinfo("Restocked!",str(restock_num) + " " + DRINKS[0][drink] + "('s) have been added to the machine.")
                    restock_drink_frame.destroy()
                    staff_menu()
            except:
                messagebox.showerror("Input error", "Please input a valid value.")

        restock_drink_frame = Frame(admin_window)
        restock_drink_frame.pack()
        tk.Label(restock_drink_frame, text="How many " + DRINKS[0][value] + "'s would you like to add?", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)
        restock_entry = tk.Entry(restock_drink_frame)
        restock_entry.grid(row=1, column=0, pady=5)
        tk.Button(restock_drink_frame, justify=RIGHT, text="Restock", command=lambda: restocking(value)).grid(row=1, column=1, pady=5)
        Button(restock_drink_frame, text="Back", command=lambda: [restock(), restock_drink_frame.destroy()], width=15).grid(row=2, column=0, columnspan=2, pady=10)

    def check_change():
        check_change_frame = Frame(admin_window)
        check_change_frame.pack()
        check_change_labels = []
        row_count = 0
        column_count = 0
        for x in range(len(CHANGE)):
            if x < 6:
                check_change_labels.append(Label(check_change_frame, text=COINVALUE[0][x] + "'s remaining: " + str(CHANGE[x]), font=("Arial", 9), width=17, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            else:
                check_change_labels.append(Label(check_change_frame, text=NOTEVALUE[0][x-6] + "'s remaining: " + str(CHANGE[x]), font=("Arial", 9), width=17, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            column_count += 1
            if column_count == 3:
                column_count = 0
                row_count += 1
        Button(check_change_frame, text="Back", command=lambda: [staff_menu(), check_change_frame.destroy()]).grid(row=9, column=0, columnspan=4, sticky="nesw")

    def add_change():  # Staff window to restock drinks
        add_change_frame = Frame(admin_window)
        add_change_frame.pack()
        add_change_frame_buttons = []
        add_change_frame_labels = []
        row_count = 1
        column_count = 0
        for x in range(len(CHANGE)):  # Loop to create all buttons and labels
            row_count -= 1
            if x < 6:
                add_change_frame_labels.append(Label(add_change_frame, text=COINVALUE[0][x] + "'s remaining: " + str(CHANGE[x]), font=("Arial", 9), width=30, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            else:
                add_change_frame_labels.append(Label(add_change_frame, text=NOTEVALUE[0][x-6] + "'s remaining: " + str(CHANGE[x]), font=("Arial", 9), width=30, borderwidth=2, relief="sunken").grid(row=row_count, column=column_count, padx=5))
            row_count += 1
            add_change_frame_buttons.append(Button(add_change_frame, text="Restock", font=("Arial", 9), command=lambda x=x: [restock_change(x), add_change_frame.destroy()]).grid(row=row_count, column=column_count, padx=5, pady=5))
            column_count += 1
            if column_count == 3:
                column_count = 0
                row_count += 2
        Button(add_change_frame, text="Back", command=lambda: [staff_menu(), add_change_frame.destroy()]).grid(row=9, column=0, columnspan=4, sticky="nesw")

    def restock_change(value):
        def restocking(change):  # Used to verify drink can be restocked
            global CHANGE
            try:
                restock_num = int(restock_entry.get())  # Retrieves data from entry box and converts to int
                if restock_num < 0:
                    messagebox.showerror("Input error", "Please input a valid value.")
                elif (restock_num + CHANGE[change]) > 100:
                    messagebox.showerror("Capacity Exceeded", "Capacity Exceeded. Max capacity: 100")
                else:
                    CHANGE[change] += restock_num
                    if change < 6:
                        messagebox.showinfo("Restocked!", str(restock_num) + " " + COINVALUE[0][change] + " coins have been added to the machine.")
                    else:
                        messagebox.showinfo("Restocked!", str(restock_num) + " " + NOTEVALUE[0][change-6] + " notes have been added to the machine.")
                    restock_change_frame.destroy()
                    staff_menu()
            except:
                messagebox.showerror("Input error", "Please input a valid value.")

        restock_change_frame = Frame(admin_window)
        restock_change_frame.pack()
        if value < 6:
            tk.Label(restock_change_frame, text="How many " + COINVALUE[0][value] + " coins would you like to add?", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)
        else:
            tk.Label(restock_change_frame, text="How many " + NOTEVALUE[0][value-6] + " notes would you like to add?", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)

        restock_entry = tk.Entry(restock_change_frame)
        restock_entry.grid(row=1, column=0, pady=5)
        tk.Button(restock_change_frame, justify=RIGHT, text="Restock", command=lambda: restocking(value)).grid(row=1, column=1,  pady=5)
        Button(restock_change_frame, text="Back", command=lambda: [add_change(), restock_change_frame.destroy()], width=15).grid(row=2, column=0, columnspan=2, pady=10)


    def remove_non_sellable_items():  # Removes non-sellable items from the vending machine - For future implementation
        messagebox.showinfo("Items Removed", "Non-sellable-items have been removed.")

    processing_payment = True
    admin_window = tk.Toplevel(main_frame)
    admin_window.title("Admin Panel")
    admin_window.resizable(width=False, height=False)
    admin_window.protocol("WM_DELETE_WINDOW", admin_close)
    staff_menu()

# Creates and manages the drinks display frame
def drinks_display():
    global drinks_display_frame
    global drinks_display_frame_icons
    drinks_display_frame = Frame(main_frame, background="black", height=600, width=500, borderwidth=1)
    drinks_display_frame.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
    drinks_display_frame_icon_frames = []
    drinks_display_frame_labels = []
    drinks_display_images = []
    drinks_display_frame_icons = []
    row_count = 1
    column_count = 0
    for x in range(len(DRINKS[0])):  # Loop to create all frames, images and labels
        row_count -= 1
        frame = Frame(drinks_display_frame, height=144, width=94)
        frame.grid(row=row_count, column=column_count)

        drinks_display_frame_icon_frames.append(frame)
        drinks_display_images.append(ImageTk.PhotoImage(Image.open("Assets/" + DRINKS[4][x] + ".png").resize((40, 120))))
        drinks_display_frame_icons.append(tk.Label(drinks_display_frame_icon_frames[x], image=drinks_display_images[x]))
        drinks_display_frame_icons[x].photo = drinks_display_images[x]
        drinks_display_frame_icons[x].pack(padx=25, pady=10)
        if DRINKS[3][x] < 1:
            drinks_display_frame_icons[x].config(image="", height=59, width=38, font=("arial", 1))

        row_count += 1
        drinks_display_frame_labels.append(Label(drinks_display_frame, text=DRINKS[2][x], font=("Arial", 12)).grid(row=row_count, column=column_count))
        column_count += 1
        if column_count > 3:
            column_count = 0
            row_count += 2

# Creates and manages the screen display frame
def screen_display():
    global screen_display_frame
    global payment_label_text
    global user_input_label_text
    global system_label_text
    global processing_payment
    processing_payment = False
    screen_display_frame = Frame(main_frame)
    screen_display_frame.grid(row=0, column=1)
    system_label_text = tk.StringVar(screen_display_frame, "Please Select a Drink")
    system_label = tk.Label(screen_display_frame, textvariable=system_label_text, width=20, height=2, font=("Arial", 12), bg="Light Grey", borderwidth=1, relief="sunken")
    system_label.grid(row=0, sticky="WE")
    user_input_label_text = tk.StringVar(screen_display_frame, user_input)
    user_input_label = tk.Label(screen_display_frame, textvariable=user_input_label_text, height=2, font=("Arial", 12), bg="Light Grey", borderwidth=1, relief="sunken")
    user_input_label.grid(row=1, sticky="WE")
    machine_balance_label = tk.Label(screen_display_frame, textvariable=payment_label_text, font=("Arial", 12), height=2, bg="Light Grey", borderwidth=1, relief="sunken")
    machine_balance_label.grid(row=2, sticky="WE")
    machine_balance_label.config(text="Inserted: " + str(locale.currency(machine_balance/100)))

# Creates and manages the payment input frame
def payment_input():
    payment_input_frame = Frame(main_frame)
    payment_input_frame.grid(row=1, column=1)
    Button(payment_input_frame, text="Coin Input", command=coin_wallet).grid(row=0, column=0, sticky="nswe")
    Button(payment_input_frame, text="Note Input", command=note_wallet).grid(row=1, column=0, sticky="nswe")
    Button(payment_input_frame, text="Insert Card", command=insert_card).grid(row=0, column=1, sticky="nswe")
    Button(payment_input_frame, text="Present Card", command=present_card).grid(row=1, column=1, sticky="nswe")
    Button(payment_input_frame, text="Loyalty\ncard", command=loyalty_discount).grid(row=2, column=0, columnspan=2, sticky="nswe")

# Creates and manages the keypad frame
def keypad():
    global keypad_frame
    keypad_frame = Frame(main_frame, borderwidth=1, relief="sunken")
    keypad_frame.grid(row=2, column=1, padx=15, sticky="W")
    keycount = 5
    row_count = 0
    column_count = 0
    keypad_buttons = []
    for x in KEYS:  # Loop to create buttons on the keypad
        keypad_buttons.append(Button(keypad_frame, text=x, width=2, font=("Arial", 12), command=lambda x=x: keypad_input(x)).grid(row=row_count, column=column_count, sticky="NSWE"))
        column_count += 1
        if column_count == 3:
            column_count = 0
            row_count += 1
    Button(keypad_frame, text="Clear", font=("Arial", 12,), width=9, command=lambda: keypad_input("CLEAR")).grid(row=6, column=0, columnspan=3)
    Button(keypad_frame, text="Dispense", font=("Arial", 12,), width=8, height=3, command=destroy_wallet_dispense).grid(row=1, rowspan=7, column=4, pady=5, padx=5, sticky="s")

# Updates the screen display after button press
def keypad_input(value):
    global user_input
    global screen_display_frame
    global drink_selected
    global system_label_text
    global user_input_label
    if processing_payment == False:  # Check if machine is processing a payment/Disables input if true
        if value == "CLEAR":
            user_input = ""
        elif len(user_input) != 6:
            user_input += value
        user_input_label_text.set(user_input)
        for x in range(len(DRINKS[2])):  # Loop to check if the user input matches any drinks
            if user_input == DRINKS[2][x]:
                if DRINKS[3][x] < 1:
                    system_label_text.set(DRINKS[0][x] + ": Out of Stock.")
                    drink_selected = ["", False]
                    break
                else:
                    system_label_text.set(DRINKS[0][x] + ": " + locale.currency(DRINKS[1][x] / 100))
                    drink_selected = [x, True]
                    process_payment(1)
                    break
            elif user_input == staff_code:  # Opens admin panel if staff code is entered
                admin_panel()
                user_input_label_text.set("")
                user_input = ""
                break
            else:
                system_label_text.set("Please Select a Drink")
                drink_selected = ["", False]

# Output hatch to retrieve drink and end transaction
def output_hatch(has_drink):
    def take_drink():
        global processing_payment
        global payment_label_text
        processing_payment = False
        output_button.config(text="")
        payment_label_text.set("")
        screen_display()
    output_hatch_frame = Frame(main_frame)
    output_hatch_frame.grid(row=3, column=1)
    output_button = Button(output_hatch_frame, width=25, height=1, borderwidth=3, relief="sunken")
    output_button.pack()
    if has_drink:
        output_button.config(text="Drink Available", command=take_drink)

# Changes drink values to loyalty discounted values
def loyalty_discount():
    global DRINKS
    global loyalty_scanned
    global processing_payment
    global system_label_text
    if not loyalty_scanned and not processing_payment:
        for x in range(len(DRINKS[1])):
            DRINKS[1][x] *= 0.9
        loyalty_scanned = True
        system_label_text.set("Loyalty Discount Applied")
        processing_payment = True
        root.update_idletasks()
        root.after(2000, lambda: [change_processing_payment(), keypad_input("")])

# Manages inserted card window
def insert_card():
    global stored_input
    global card_payment_window
    global drink_selected
    global card_balance
    try:  # Trys to destroy duplicate card windows
        card_payment_window.destroy()
    except:
        pass
    def pin_button_press(value):  # Method to check pin inputted
        global stored_input
        global processing_payment
        if not processing_payment:
            processing_payment = True
            if len(stored_input) < 4 and value != "CANCEL" and value != "OK":
                stored_input += str(value)
                card_screen_text.set(card_screen_text.get() + "*")
                change_processing_payment()
            elif value == "OK":
                if stored_input == valid_pin and card_balance > DRINKS[1][drink_selected[0]]:
                    card_screen_text.set("Processing...")
                    root.update_idletasks()
                    card_screen.after(1000, lambda: card_screen_text.set("Card Accepted"))
                    root.update_idletasks()
                    card_screen.after(2000, lambda: [card_payment_window.destroy(), process_payment(0)])
                elif stored_input == valid_pin and card_balance < DRINKS[1][drink_selected[0]]:
                    card_screen_text.set("Processing...")
                    card_screen.after(1000, lambda: card_screen_text.set("Insufficient Funds."))
                    root.update_idletasks()
                    card_screen.after(2000, lambda: [card_payment_window.destroy(), change_processing_payment()])
                else:
                    card_screen_text.set("Invalid PIN: Please try again.")
                    card_screen.after(1500, lambda: [card_screen_text.set("Please enter your pin: "), change_processing_payment()])
                    stored_input = ""
            elif value == "CANCEL":
                if card_screen_text.get() != "Please enter your pin: ":
                    card_screen_text.set(card_screen_text.get()[:-1])
                    stored_input = stored_input[:-1]
                change_processing_payment()
            else:
                change_processing_payment()
        processing = False
    if drink_selected[1] and not processing_payment:  # Checks if system is processing a payment
        card_payment_window = tk.Toplevel(main_frame)
        card_payment_window.title("Card Payment")
        card_payment_window.resizable(width=False, height=False)
        card_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "OK", "0", "CANCEL"]
        row_count = 1
        column_count = 1
        stored_input = ""
        for x in range(len(card_buttons)):  # Creates keys
            Button(card_payment_window, text=card_buttons[x], font=("Arial", 12), width=8, height=2, command=lambda x=x: pin_button_press(card_buttons[x])).grid(row=row_count, column=column_count)
            column_count += 1
            if column_count == 4:
                column_count = 1
                row_count += 1
        card_screen_text = tk.StringVar(main_frame, "Please enter your pin: ")
        card_screen = tk.Label(card_payment_window, textvariable=card_screen_text, anchor="w", width=26, font=("Arial", 12), bg="Light Grey",borderwidth=1, relief="sunken", padx=5, pady=5)
        card_screen.grid(row=0, column=0, columnspan=5)

# Method for contactless card payment
def present_card():
    global payment_label_text
    global processing_payment
    if drink_selected[1] and not processing_payment:  # Checks if system is processing a payment
        if card_balance > DRINKS[1][drink_selected[0]]:
            processing_payment = True
            payment_label_text.set("Processing...")
            root.update_idletasks()
            root.after(1000, lambda: payment_label_text.set("Card Accepted"))
            root.update_idletasks()
            root.after(2000, lambda: [process_payment(0)])
        else:
            processing_payment = True
            old_text = payment_label_text.get()
            payment_label_text.set("Processing...")
            root.after(1000, lambda: payment_label_text.set("Insufficient Funds."))
            root.update_idletasks()
            root.after(2500, lambda: payment_label_text.set(old_text), change_processing_payment())

# Creates coin window and allows user to insert coins into the machine
def coin_wallet():
    global coin_wallet_window
    global payment_label_text
    try:  # Trys to delete duplicate coin wallets
        coin_wallet_window.destroy()
    except:
        pass
    def insert_coin(value):  # Method to calculate machine and wallet balances after inserting coins
        global machine_balance
        if COINWALLET[value] > 0:
            machine_balance += COINVALUE[1][value]
            COINWALLET[value] -= 1
            coin_count[value].set(COINVALUE[0][value] + "'s: " + str(COINWALLET[value]))
            process_payment(1)
        else:
            messagebox.showwarning("Cash Unavailable", "You do not have any " + COINVALUE[0][value] + "'s left.")
        payment_label_text.set("Inserted: " + str(locale.currency(machine_balance/100)))
    if not processing_payment:  # Checks if machine is processing a payment
        coin_wallet_window = tk.Toplevel(main_frame)
        coin_wallet_window.title("Coins")
        coin_wallet_window.resizable(width=False, height=False)
        coin_count = []
        coin_wallet_labels = []
        coin_wallet_buttons = []
        row_count = 0
        column_count = 0
        for x in range(len(COINVALUE[0])):
            coin_count.append(tk.StringVar(coin_wallet_window, COINVALUE[0][x] + "'s: " + str(COINWALLET[x])))
            coin_wallet_labels.append(tk.Label(coin_wallet_window, textvariable=coin_count[x], font=("Arial", 12), borderwidth=1, relief="solid", padx=5, pady=5).grid(row=row_count, column=column_count, sticky="NSWE"))
            coin_wallet_buttons.append(Button(coin_wallet_window, text="Insert: " + COINVALUE[0][x], font=("Arial", 12), command=lambda x=x: insert_coin(x)).grid(row=row_count + 1, column=column_count, sticky="NSWE"))
            column_count += 1
            if column_count == 3:
                column_count = 0
                row_count += 2

# Creates note window and allows user to insert notes into the machine
def note_wallet():
    global note_wallet_window
    try:  # Trys to delete duplicate note wallets
        note_wallet_window.destroy()
    except:
        pass
    def insert_note(value):  # Method to calculate machine and wallet balances after inserting notes
        global machine_balance
        if NOTEWALLET[value] > 0:
            machine_balance += NOTEVALUE[1][value]
            NOTEWALLET[value] -= 1
            note_count[value].set(NOTEVALUE[0][value] + "'s: " + str(NOTEWALLET[value]))
            process_payment(1)
        else:
            messagebox.showwarning("Cash Unavailable", "You do not have any " + NOTEVALUE[0][value] + " notes left.")
        payment_label_text.set("Inserted: " + str(locale.currency(machine_balance/100)))

    if not processing_payment:  # Checks if machine is processing a payment
        note_wallet_window = tk.Toplevel(main_frame)
        note_wallet_window.title("Notes")
        note_wallet_window.resizable(width=False, height=False)
        note_count = []
        note_wallet_labels = []
        note_wallet_buttons = []
        for x in range(len(NOTEVALUE[0])):
            note_count.append(tk.StringVar(note_wallet_window, NOTEVALUE[0][x] + "'s: " + str(NOTEWALLET[x])))
            note_wallet_labels.append(tk.Label(note_wallet_window, textvariable=note_count[x], font=("Arial", 12), borderwidth=1, relief="solid", padx=5, pady=5).grid(row=0, column=x, sticky="NSWE"))
            note_wallet_buttons.append(Button(note_wallet_window, text="Insert: " + NOTEVALUE[0][x], font=("Arial", 12), command=lambda x=x: insert_note(x)).grid(row=1 + 1, column=x, sticky="NSWE"))

# Function to destroy coin wallet windows if open and dispense any change
def destroy_wallet_dispense():
    global coin_wallet_window
    global note_wallet_window
    if not processing_payment:
        try:
            coin_wallet_window.destroy()
            note_wallet_window.destroy()
        except:
            pass
        finally:
            dispense_change(False)

# Dispense change using coins in the machine and attribute coins back to the user
def dispense_change(paying):
    global machine_balance
    global screen_display_frame
    global payment_label_text
    global processing_payment
    processing_payment = True
    dispensed = False
    i = len(CHANGE) - 1
    while machine_balance > 0:
        if CHANGE[i] > 0 and i > 5 and (machine_balance - NOTEVALUE[1][(i-6)]) >= 0:
            machine_balance -= round(NOTEVALUE[1][(i-6)], 2)
            CHANGE[i] -= 1
            NOTEWALLET[i-6] += 1
            dispensed = True
        elif CHANGE[i] > 0 and i < 6 and (machine_balance - COINVALUE[1][i]) >= 0:
            machine_balance -= round(COINVALUE[1][i], 2)
            CHANGE[i] -= 1
            COINWALLET[i] += 1
            dispensed = True
        else:
            i -= 1
    if dispensed and not paying:
        payment_label_text.set("Dispensing change...")
        root.after(1500, lambda: [payment_label_text.set(""), change_processing_payment()])
        root.update_idletasks()
    elif not paying:
        change_processing_payment()

# Manages payments and display during payment
def process_payment(value):
    global drink_selected
    global payment_label_text
    global card_balance
    global machine_balance
    global coin_wallet_window
    global note_wallet_window
    global card_payment_window
    global keypad_frame
    global processing_payment
    global drinks_display_frame_icons
    def reset_windows(value):  # Method to reset any windows and values used in payment
        try:
            coin_wallet_window.destroy()
        except:
            pass
        try:
            card_payment_window.destroy()
        except:
            pass
        try:
            note_wallet_window.destroy()
        except:
            pass
        global user_input
        global loyalty_scanned
        global DRINKS
        user_input = ""
        DRINKS[1] = [200, 180, 200, 180,
                    200, 200, 160, 160,
                    220, 180, 120, 150,
                    300, 300, 280, 320]
        DRINKS[3][value[0]] -= 1
        if DRINKS[3][value[0]] < 1:
            drinks_display_frame_icons[value[0]].config(image="", height=59, width=38, font=("arial", 1))
        loyalty_scanned = False
        root.after(2000, lambda: [payment_label_text.set("Thanks for your purchase\nHave a great day!"), output_hatch(True)])
    try:  # Trys to see if the user can pay
        if DRINKS[3][drink_selected[0]] > 0 and value == 0:
            processing_payment = True
            root.after(1000, payment_label_text.set("Payment Authorised\nDispensing Drink."))
            root.update_idletasks()
            card_balance -= DRINKS[1][drink_selected[0]]
            if machine_balance > 0:
                root.after(2000, lambda: [dispense_change(True), reset_windows(drink_selected)])
            else:
                root.after(1000, lambda: reset_windows(drink_selected))
        elif DRINKS[3][drink_selected[0]] > 0 and value == 1 and machine_balance >= DRINKS[1][drink_selected[0]]:
            processing_payment = True
            machine_balance -= DRINKS[1][drink_selected[0]]
            root.after(1, lambda: payment_label_text.set("Payment Authorised\nDispensing Drink."))
            root.update_idletasks()
            root.after(2000, lambda: [dispense_change(True), reset_windows(drink_selected)])
    except:
        pass

# Method used to allow unlock machine buttons
def change_processing_payment():
    global processing_payment
    processing_payment = False

# Main menu tkinter elements.
root.title("Vending Machine")
root.resizable(width=False, height=False)
# Main frame for all other frames to attach to
main_frame = Frame(root, pady=5)
main_frame.pack()
drinks_display()
screen_display()
keypad()
output_hatch(False)
payment_input()
root.mainloop()
