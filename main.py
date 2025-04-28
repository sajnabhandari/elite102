from bank_account import BankAccount //
def main():
    user_id = input("Welcome! Please enter your account user ID: ")
    account = BankAccount(user_id)
    account.run_menu()

if __name__ == "__main__":
    main()
