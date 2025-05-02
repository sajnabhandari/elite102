# main function to start the banking app
from bank_account import BankAccount # import the BankAccount class
#main functions are stored in bank_account.py, to make things organized(?)
def main():
    # ask user for their id
    user_id = input("Welcome! Please enter your account user ID: ")
    # create BankAccount object and start CLI menu
    account = BankAccount(user_id)
    account.run_menu()

if __name__ == "__main__":
    main()
