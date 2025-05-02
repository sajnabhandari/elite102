from bank_account import BankAccount

# this is a test acc 
account = BankAccount("test_user")
# testing the deposit function
account.deposit(50)
if account.get_balance() == 50:
    print("Depositing done!")

# testing the withdraw
account.withdraw(20)
if account.get_balance() == 30:
    print("Withdrawing done!")
print("Tests finished!")
