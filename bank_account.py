import sqlite3
class BankAccount:
    def __init__(self, user_id):
        self.user_id = user_id #stores user_id
        self.conn = sqlite3.connect('bank.db') #connects to the database
        self.cursor = self.conn.cursor() #creates cursor to run SQL commands
        self.create_tables() #if does not exist, creates the tables
        self.create_account_if_not_exists() 

    def create_tables(self): #accounts table that stores each user's balance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                user_id TEXT PRIMARY KEY,
                balance REAL DEFAULT 0.0
            )
        ''')
        #transactions table that stores each transaction (deposit/withdraw))
        self.cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                amount REAL,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit() #save changes

    def create_account_if_not_exists(self): #acc not found, create it w/ balance of 0.0
        self.cursor.execute(
            'INSERT OR IGNORE INTO accounts (user_id, balance) VALUES (?, ?)',
            (self.user_id, 0.0)
        )
        self.conn.commit()
#rounds to 2 decimals; if whole, adds ‘.00’
    def _format_amount(self, value):
        """Round to 2 decimals; if whole, add ‘.00’."""
        rounded = round(value, 2)
        if isinstance(rounded, float) and rounded.is_integer():
            return str(int(rounded)) + ".00"
        else:
            return str(rounded)

    def check_balance(self):
        self.cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = ?',
            (self.user_id,)
        )
        row = self.cursor.fetchone()
        if row:
            bal_str = self._format_amount(row[0])
            print("Your balance is: $" + bal_str)
        else:
            print("Account not found.")
#deposit amount must be positive
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.cursor.execute(
            'UPDATE accounts SET balance = balance + ? WHERE user_id = ?',
            (amount, self.user_id)
        )
        self.cursor.execute(
            'INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)',
            (self.user_id, amount, 'deposit')
        )
        self.conn.commit()
        amt_str = self._format_amount(amount)
        print("Deposited $" + amt_str + " successfully.")
#cannot withdraw more than balance nor negative amount
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdraw amount must be positive.")
            return
        balance = self.get_balance()
        if balance is not None and balance >= amount:
            self.cursor.execute(
                'UPDATE accounts SET balance = balance - ? WHERE user_id = ?',
                (amount, self.user_id)
            )
            self.cursor.execute(
                'INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)',
                (self.user_id, amount, 'withdraw')
            )
            self.conn.commit()
            amt_str = self._format_amount(amount)
            print("Withdrew $" + amt_str + " successfully.")
        else:
            print("Insufficient funds.")
#returns balance of user
    def get_balance(self):
        self.cursor.execute(
            'SELECT balance FROM accounts WHERE user_id = ?',
            (self.user_id,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()
#menu function
    def run_menu(self):
        while True:
            print("\nPlease choose an option:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("0. Exit")

            choice = input("Enter option number: ")

            if choice == "0":
                print("Goodbye!")
                self.close()
                break
            elif choice == "1":
                self.check_balance()
            elif choice == "2":
                try:
                    amt = float(input("Enter deposit amount: "))
                    self.deposit(amt)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == "3":
                try:
                    amt = float(input("Enter withdraw amount: "))
                    self.withdraw(amt)
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Invalid option. Try again.")
