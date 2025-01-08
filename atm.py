import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

transactions = []
minimum_balance = 500
window = None
pin_window = None

users = [
    {"name": "Arya", "pin": "1234", "balance": 1000.00},
    {"name": "Veeresh", "pin": "5678", "balance": 1500.00},
    {"name": "Dhanush", "pin": "9101", "balance": 800.00},
    {"name": "Microsoft", "pin": "1213", "balance": 2000.00},
    {"name": "Google", "pin": "1415", "balance": 1200.00}
]
def check_balance():
    show_info_message(f"Your Account Balance is: {balance}")
def open_withdraw_window():
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw")
    withdraw_window.configure(bg="#F0F0F0")
    withdraw_window.geometry("300x150")

    withdraw_label = tk.Label(withdraw_window, text="Enter Withdrawal Amount:\nOnly 100, 200, 500 notes dispensable", font=("Helvetica", 14), bg="#F0F0F0")
    withdraw_label.pack(pady=10)

    withdraw_entry = tk.Entry(withdraw_window, font=("Helvetica", 14))
    withdraw_entry.pack(pady=5)

    withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=lambda: withdraw(withdraw_entry.get(), withdraw_window), bg="#FF5733", fg="white", padx=10, pady=5, font=("Helvetica", 14, "bold"))
    withdraw_button.pack(pady=5)
def open_deposit_window():
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit")
    deposit_window.configure(bg="#F0F0F0")
    deposit_window.geometry("300x150")

    deposit_label = tk.Label(deposit_window, text="Enter Deposit Amount:\nAdd only 100, 200, 500 denominations", font=("Helvetica", 14), bg="#F0F0F0")
    deposit_label.pack(pady=10)

    deposit_entry = tk.Entry(deposit_window, font=("Helvetica", 14))
    deposit_entry.pack(pady=5)

    deposit_button = tk.Button(deposit_window, text="Deposit", command=lambda: deposit(deposit_entry.get(), deposit_window), bg="#33A1FF", fg="white", padx=10, pady=5, font=("Helvetica", 14, "bold"))
    deposit_button.pack(pady=5)
def show_error_message(message):
    error_window = tk.Toplevel()
    error_window.title("Error")
    error_window.configure(bg="#F0F0F0")

    error_label = tk.Label(error_window, text=message, font=("Helvetica", 16), bg="#F0F0F0")
    error_label.pack(padx=20, pady=10)

    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy, bg="#FF5733", fg="white",
                          font=("Helvetica", 14, "bold"))
    ok_button.pack(pady=10)
def show_info_message(message):
    info_window = tk.Toplevel()
    info_window.title("Success")
    info_window.configure(bg="#F0F0F0")

    info_label = tk.Label(info_window, text=message, font=("Helvetica", 16), bg="#F0F0F0")
    info_label.pack(padx=20, pady=10)

    ok_button = tk.Button(info_window, text="OK", command=info_window.destroy, bg="#FF5733", fg="white",
                          font=("Helvetica", 14, "bold"))
    ok_button.pack(pady=10)
def withdraw(amount, window):
    global balance
    try:
        withdraw_amount = float(amount)
        if withdraw_amount <= 0:
            show_error_message("Please enter a valid withdrawal amount.")
        elif balance - withdraw_amount < minimum_balance:
            show_error_message(f"Withdrawal failed! Minimum balance must be maintained. "f"\nYour current balance is {balance}.")
        else:
            balance -= withdraw_amount
            transactions.append(f"Withdrawal: -{withdraw_amount}")
            show_info_message(f"Withdrawal successful!\nRemaining amount in your account is: {balance}")
            window.destroy()  # Close the withdrawal window after successful withdrawal
    except ValueError:
        show_error_message("Please enter a valid withdrawal amount.")
def deposit(amount, window):
    global balance
    try:
        deposit_amount = float(amount)
        if deposit_amount <= 0:
            show_error_message("Please enter a valid deposit amount.")
        else:
            balance += deposit_amount
            transactions.append(f"Deposit: +{deposit_amount}")
            show_info_message(f"Deposit successful!\nTotal amount is: {balance}")
            window.destroy()  # Close the deposit window after successful deposit
    except ValueError:
        show_error_message("Please enter a valid deposit amount.")
def reset_pin():
    global window

    def submit_current_pin():
        current_pin = current_pin_entry.get()
        for user in users:
            if current_pin == user["pin"]:
                reset_window = tk.Toplevel()
                reset_window.title("Reset PIN")

                def submit_new_pin():
                    new_pin = new_pin_entry.get()
                    if new_pin.isdigit() and len(new_pin) == 4:
                        # Update the correct PIN for the user in the users list
                        user["pin"] = new_pin
                        messagebox.showinfo("PIN Reset", "Your PIN has been reset successfully.")
                        reset_window.destroy()
                        window.destroy()
                        create_pin_window()
                    else:
                        show_error_message("Please enter a valid 4-digit PIN.")

                new_pin_label = tk.Label(reset_window, text="Enter new 4-digit PIN:", font=("Arial", 20))
                new_pin_label.pack()

                new_pin_entry = tk.Entry(reset_window, show="*", width=20, font=("Arial", 20))
                new_pin_entry.pack()

                submit_button = tk.Button(reset_window, text="Submit", command=submit_new_pin, font=("Arial", 20))
                submit_button.pack()

                # Break out of the loop since the correct user is found
                break
        else:
            # If the loop completes without finding a matching user, show error message
            show_error_message("Incorrect current PIN. Please try again.")

    reset_window = tk.Toplevel()
    reset_window.title("Reset PIN")

    current_pin_label = tk.Label(reset_window, text="Enter your current 4-digit PIN:", font=("Arial", 20))
    current_pin_label.pack()

    current_pin_entry = tk.Entry(reset_window, show="*", width=20, font=("Arial", 20))
    current_pin_entry.pack()

    submit_button = tk.Button(reset_window, text="Submit", command=submit_current_pin, font=("Arial", 20))
    submit_button.pack()

    reset_window.mainloop()
def view_and_plot_transactions():
    if transactions:
        transaction_history = "\n".join(transactions)
        show_info_message(f"Transaction History:\n\n{transaction_history}")

        withdrawals = []
        deposits = []
        for transaction in transactions:
            transaction_type, amount_str = transaction.split(": ")

            amount = float(amount_str.strip().split()[0][1:])
            print(transaction_type, amount_str, amount)
            if transaction_type.strip() == "Withdrawal":
                withdrawals.append(amount)
            elif transaction_type.strip() == "Deposit":
                deposits.append(amount)

        print("Withdrawals:", withdrawals)
        print("Deposits:", deposits)

        x_withdrawals = range(1, len(withdrawals) + 1)
        x_deposits = range(1, len(deposits) + 1)

        print("x_withdrawals:", x_withdrawals)
        print("x_deposits:", x_deposits)

        plt.figure(figsize=(8, 6))
        plt.plot(x_withdrawals, withdrawals, marker='o', linestyle='-', color='r', label='Withdrawals')
        plt.plot(x_deposits, deposits, marker='o', linestyle='-', color='g', label='Deposits')
        plt.title('Transaction History')
        plt.xlabel('Transaction Number')
        plt.ylabel('Amount')
        plt.legend()
        plt.tight_layout()
        plt.show()

    else:
        show_info_message("No transactions yet.")
def quit_program():
    window.destroy()
def welcome_window(user_name):
    global window,balance
    for user in users:
        if user["name"] == user_name:
            balance = user["balance"]
            break
    window = tk.Tk()
    window.title("ATM")
    window.configure(bg="#F0F0F0")  # Set background color
    window.geometry("500x600")  # Set window size

    # Add background image
    background_image = tk.PhotoImage(file="atm.png")
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    welcome_label = tk.Label(window, text=f"Welcome to SJCE ATM, {user_name}!", font=("Helvetica", 24, "bold"), pady=40, bg="#a0dec0")
    welcome_label.pack(side="top")  # Place label at the top

    select_label = tk.Label(window, text="Select a Transaction", font=("Helvetica", 20, "bold"), pady=10, bg="#b3ffec", fg="black")
    select_label.pack(side="top")  # Place label below welcome label with a gap

    # Check Balance and Withdraw Buttons
    btn_frame_1 = tk.Frame(window, bg="#2AAA8A")
    btn_frame_1.pack(side="top", pady=(60, 20))

    balance_btn = tk.Button(btn_frame_1, text="Check Balance", command=check_balance, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    balance_btn.pack(side=tk.LEFT, padx=(10, 20))

    withdraw_btn = tk.Button(btn_frame_1, text="Withdraw", command=open_withdraw_window, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    withdraw_btn.pack(side=tk.LEFT, padx=(20, 10))

    # Deposit and Reset PIN Buttons
    btn_frame_2 = tk.Frame(window, bg="#2AAA8A")
    btn_frame_2.pack(side="top", pady=20)

    deposit_btn = tk.Button(btn_frame_2, text="Deposit", command=open_deposit_window, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    deposit_btn.pack(side=tk.LEFT, padx=(10, 20))

    reset_pin_btn = tk.Button(btn_frame_2, text="Reset PIN", command=reset_pin, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    reset_pin_btn.pack(side=tk.LEFT, padx=(20, 10))

    # View Transactions and Quit Buttons
    btn_frame_3 = tk.Frame(window, bg="#2AAA8A")
    btn_frame_3.pack(side="top", pady=20)

    transactions_btn = tk.Button(btn_frame_3, text="View Transactions", command=view_and_plot_transactions, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    transactions_btn.pack(side=tk.LEFT, padx=(10, 20))

    quit_btn = tk.Button(btn_frame_3, text="Quit", command=quit_program, bg="#336699", fg="white", padx=20, pady=10, font=("Helvetica", 16, "bold"), width=15)
    quit_btn.pack(side=tk.LEFT, padx=(20, 10))

    window.mainloop()
def create_pin_window():
    def on_button_click(number):
        current_pin = pin_entry.get()
        pin_entry.delete(0, tk.END)
        pin_entry.insert(tk.END, current_pin + str(number))

    def backspace():
        current_pin = pin_entry.get()
        new_pin = current_pin[:-1]
        pin_entry.delete(0, tk.END)
        pin_entry.insert(tk.END, new_pin)

    def clear_entry():
        pin_entry.delete(0, tk.END)

    def authenticate_pin():
        entered_pin = pin_entry.get()
        if entered_pin == "":
            messagebox.showerror("Error", "Please enter a PIN.")
        else:
            authenticated = False
            user_name = None
            for user in users:
                if entered_pin == user["pin"]:
                    authenticated = True
                    user_name = user['name']
                    messagebox.showinfo("Success", f"Welcome, {user['name']}!")
                    pin_window.destroy()
                    welcome_window(user_name)
                    break
            if not authenticated:
                messagebox.showerror("Error", "Incorrect PIN. Please try again.")
        return user_name

    pin_window = tk.Tk()
    pin_window.title("ATM Login")
    pin_window.configure(bg="#F0F0F0")  # Set background color

    welcome_label = tk.Label(pin_window, text="ATM System", font=("Helvetica", 22, "bold"), pady=10,
                             bg="#F0F0F0")
    welcome_label.pack()
    pin_window.geometry("1200x600")  # Set window position

    background_image = tk.PhotoImage(file="atm.png")  # Replace "your-image-file.png" with the path to your image
    label = tk.Label(pin_window, image=background_image)
    label.pack()

    pin_label = tk.Label(pin_window, text="Enter Your PIN", font=("Helvetica", 24), bg="#F0F0F0")
    pin_label.place(relx=0.5, rely=0.2, anchor="center")

    pin_entry = tk.Entry(pin_window, show="*", font=("Helvetica", 24))
    pin_entry.place(relx=0.5, rely=0.3, anchor="center")

    button_positions = [
        (0.43, 0.5), (0.5, 0.5), (0.57, 0.5),
        (0.43, 0.6), (0.5, 0.6), (0.57, 0.6),
        (0.43, 0.7), (0.5, 0.7), (0.57, 0.7),
    ]

    for i in range(1, 10):
        button = tk.Button(pin_window, text=str(i), command=lambda num=i: on_button_click(num), bg="grey", fg="black",
                           padx=20, pady=10, font=("Helvetica", 18, "bold"))
        button.place(relx=button_positions[i - 1][0], rely=button_positions[i - 1][1], anchor="center")

    zero_button = tk.Button(pin_window, text="0", command=lambda: on_button_click(0), bg="grey", fg="black", padx=20,
                            pady=10, font=("Helvetica", 18, "bold"))
    zero_button.place(relx=0.5, rely=0.8, anchor="center")

    backspace_button = tk.Button(pin_window, text="←", command=backspace, bg="lightgrey", fg="black", padx=16, pady=10,
                                 font=("Helvetica", 18, "bold"))
    backspace_button.place(relx=0.57, rely=0.8, anchor="center")

    clear_button = tk.Button(pin_window, text="Clear", command=clear_entry, bg="#ff5c33", fg="black", padx=20, pady=10,
                             font=("Helvetica", 14, "bold"))
    clear_button.place(relx=0.65, rely=0.5, anchor="center")

    cancel_button = tk.Button(pin_window, text="Cancel", command=pin_window.destroy, bg="#ff5c33", fg="black", padx=13,
                              pady=10, font=("Helvetica", 14, "bold"))
    cancel_button.place(relx=0.65, rely=0.6, anchor="center")

    enter_btn = tk.Button(pin_window, text="Enter", command=authenticate_pin, bg="#4CAF50", fg="white", padx=20,
                          pady=10, font=("Helvetica", 14, "bold"))
    enter_btn.place(relx=0.65, rely=0.7, anchor="center")

    pin_window.mainloop()

create_pin_window()